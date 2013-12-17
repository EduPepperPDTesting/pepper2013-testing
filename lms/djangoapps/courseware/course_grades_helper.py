from courseware.model_data import FieldDataCache,DjangoKeyValueStore
from xblock.fields import Scope
from django.conf import settings
from xmodule import graders
from xmodule.graders import Score
from xmodule.modulestore.exceptions import ItemNotFoundError, InvalidLocationError
from xmodule.modulestore.django import modulestore
from xmodule.course_module import CourseDescriptor
from courseware.access import has_access
from django.core.urlresolvers import reverse
from courseware.masquerade import setup_masquerade
from xblock.runtime import DbModel
from lms.xblock.field_data import lms_field_data
from xblock.runtime import KeyValueStore
from statsd import statsd
from xmodule.x_module import ModuleSystem
from mitxmako.shortcuts import render_to_string
import static_replace
from student.models import unique_id_for_user
from django.core.cache import cache
from util.sandboxing import can_execute_unsafe_code
from psychometrics.psychoanalyze import make_psychometrics_data_update_handler
from xmodule.error_module import ErrorDescriptor, NonStaffErrorDescriptor
from xmodule.errortracker import exc_info_to_str
from xmodule_modifiers import replace_course_urls, replace_jump_to_id_urls, replace_static_urls, add_histogram, wrap_xmodule, save_module  # pylint: disable=F0401
from capa.xqueue_interface import XQueueInterface
from requests.auth import HTTPBasicAuth
from functools import partial
if settings.XQUEUE_INTERFACE.get('basic_auth') is not None:
    requests_auth = HTTPBasicAuth(*settings.XQUEUE_INTERFACE['basic_auth'])
else:
    requests_auth = None

xqueue_interface = XQueueInterface(
    settings.XQUEUE_INTERFACE['url'],
    settings.XQUEUE_INTERFACE['django_auth'],
    requests_auth,
)

#@begin:
#@data:
def make_track_function(request):
    '''
    Make a tracking function that logs what happened.
    For use in ModuleSystem.
    '''
    import track.views

    def function(event_type, event):
        return track.views.server_track(request, event_type, event, page='x_module')
    return function

def get_xqueue_callback_url_prefix(request):
    """
    Calculates default prefix based on request, but allows override via settings

    This is separated from get_module_for_descriptor so that it can be called
    by the LMS before submitting background tasks to run.  The xqueue callbacks
    should go back to the LMS, not to the worker.
    """
    prefix = '{proto}://{host}'.format(
        proto=request.META.get('HTTP_X_FORWARDED_PROTO', 'https' if request.is_secure() else 'http'),
        host=request.get_host()
    )
    return settings.XQUEUE_INTERFACE.get('callback_url', prefix)

def get_score_bucket(grade, max_grade):
    """
    Function to split arbitrary score ranges into 3 buckets.
    Used with statsd tracking.
    """
    score_bucket = "incorrect"
    if(grade > 0 and grade < max_grade):
        score_bucket = "partial"
    elif(grade == max_grade):
        score_bucket = "correct"

    return score_bucket

def get_module_for_descriptor_internal(user, descriptor, field_data_cache, course_id,
                                       track_function, xqueue_callback_url_prefix,
                                       position=None, wrap_xmodule_display=True, grade_bucket_type=None,
                                       static_asset_path=''):
    """
    Actually implement get_module, without requiring a request.

    See get_module() docstring for further details.
    """

    # Short circuit--if the user shouldn't have access, bail without doing any work
    if not has_access(user, descriptor, 'load', course_id):
        return None

    # Setup system context for module instance
    ajax_url = reverse(
        'modx_dispatch',
        kwargs=dict(
            course_id=course_id,
            location=descriptor.location.url(),
            dispatch=''
        ),
    )
    # Intended use is as {ajax_url}/{dispatch_command}, so get rid of the trailing slash.
    ajax_url = ajax_url.rstrip('/')

    def make_xqueue_callback(dispatch='score_update'):
        # Fully qualified callback URL for external queueing system
        relative_xqueue_callback_url = reverse(
            'xqueue_callback',
            kwargs=dict(
                course_id=course_id,
                userid=str(user.id),
                mod_id=descriptor.location.url(),
                dispatch=dispatch
            ),
        )
        return xqueue_callback_url_prefix + relative_xqueue_callback_url

    # Default queuename is course-specific and is derived from the course that
    #   contains the current module.
    # TODO: Queuename should be derived from 'course_settings.json' of each course
    xqueue_default_queuename = descriptor.location.org + '-' + descriptor.location.course

    xqueue = {
        'interface': xqueue_interface,
        'construct_callback': make_xqueue_callback,
        'default_queuename': xqueue_default_queuename.replace(' ', '_'),
        'waittime': settings.XQUEUE_WAITTIME_BETWEEN_REQUESTS
    }

    # This is a hacky way to pass settings to the combined open ended xmodule
    # It needs an S3 interface to upload images to S3
    # It needs the open ended grading interface in order to get peer grading to be done
    # this first checks to see if the descriptor is the correct one, and only sends settings if it is

    # Get descriptor metadata fields indicating needs for various settings
    needs_open_ended_interface = getattr(descriptor, "needs_open_ended_interface", False)
    needs_s3_interface = getattr(descriptor, "needs_s3_interface", False)

    # Initialize interfaces to None
    open_ended_grading_interface = None
    s3_interface = None

    # Create interfaces if needed
    if needs_open_ended_interface:
        open_ended_grading_interface = settings.OPEN_ENDED_GRADING_INTERFACE
        open_ended_grading_interface['mock_peer_grading'] = settings.MOCK_PEER_GRADING
        open_ended_grading_interface['mock_staff_grading'] = settings.MOCK_STAFF_GRADING
    if needs_s3_interface:
        s3_interface = {
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
            'secret_access_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
            'storage_bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        }

    def inner_get_module(descriptor):
        """
        Delegate to get_module_for_descriptor_internal() with all values except `descriptor` set.

        Because it does an access check, it may return None.
        """
        # TODO: fix this so that make_xqueue_callback uses the descriptor passed into
        # inner_get_module, not the parent's callback.  Add it as an argument....
        return get_module_for_descriptor_internal(user, descriptor, field_data_cache, course_id,
                                                  track_function, make_xqueue_callback,
                                                  position, wrap_xmodule_display, grade_bucket_type,
                                                  static_asset_path)

    def xblock_field_data(descriptor):
        student_data = DbModel(DjangoKeyValueStore(field_data_cache))
        return lms_field_data(descriptor._field_data, student_data)

    def publish(event):
        """A function that allows XModules to publish events. This only supports grade changes right now."""
        if event.get('event_name') != 'grade':
            return

        # Construct the key for the module
        key = KeyValueStore.Key(
            scope=Scope.user_state,
            student_id=user.id,
            block_scope_id=descriptor.location,
            field_name='grade'
        )

        student_module = field_data_cache.find_or_create(key)
        # Update the grades
        student_module.grade = event.get('value')
        student_module.max_grade = event.get('max_value')
        # Save all changes to the underlying KeyValueStore
        student_module.save()

        # Bin score into range and increment stats
        score_bucket = get_score_bucket(student_module.grade, student_module.max_grade)
        org, course_num, run = course_id.split("/")

        tags = [
            "org:{0}".format(org),
            "course:{0}".format(course_num),
            "run:{0}".format(run),
            "score_bucket:{0}".format(score_bucket)
        ]

        if grade_bucket_type is not None:
            tags.append('type:%s' % grade_bucket_type)

        statsd.increment("lms.courseware.question_answered", tags=tags)

    # TODO (cpennington): When modules are shared between courses, the static
    # prefix is going to have to be specific to the module, not the directory
    # that the xml was loaded from

    system = ModuleSystem(
        track_function=track_function,
        render_template=render_to_string,
        ajax_url=ajax_url,
        xqueue=xqueue,
        # TODO (cpennington): Figure out how to share info between systems
        filestore=descriptor.system.resources_fs,
        get_module=inner_get_module,
        user=user,
        # TODO (cpennington): This should be removed when all html from
        # a module is coming through get_html and is therefore covered
        # by the replace_static_urls code below
        replace_urls=partial(
            static_replace.replace_static_urls,
            data_directory=getattr(descriptor, 'data_dir', None),
            course_id=course_id,
            static_asset_path=static_asset_path or descriptor.static_asset_path,
        ),
        replace_course_urls=partial(
            static_replace.replace_course_urls,
            course_id=course_id
        ),
        replace_jump_to_id_urls=partial(
            static_replace.replace_jump_to_id_urls,
            course_id=course_id,
            jump_to_id_base_url=reverse('jump_to_id', kwargs={'course_id': course_id, 'module_id': ''})
        ),
        node_path=settings.NODE_PATH,
        xblock_field_data=xblock_field_data,
        publish=publish,
        anonymous_student_id=unique_id_for_user(user),
        course_id=course_id,
        open_ended_grading_interface=open_ended_grading_interface,
        s3_interface=s3_interface,
        cache=cache,
        can_execute_unsafe_code=(lambda: can_execute_unsafe_code(course_id)),
        # TODO: When we merge the descriptor and module systems, we can stop reaching into the mixologist (cpennington)
        mixins=descriptor.system.mixologist._mixins,
    )

    # pass position specified in URL to module through ModuleSystem
    system.set('position', position)
    system.set('DEBUG', settings.DEBUG)
    if settings.MITX_FEATURES.get('ENABLE_PSYCHOMETRICS'):
        system.set(
            'psychometrics_handler',  # set callback for updating PsychometricsData
            make_psychometrics_data_update_handler(course_id, user, descriptor.location.url())
        )

    try:
        module = descriptor.xmodule(system)
    except:
        log.exception("Error creating module from descriptor {0}".format(descriptor))

        # make an ErrorDescriptor -- assuming that the descriptor's system is ok
        if has_access(user, descriptor.location, 'staff', course_id):
            err_descriptor_class = ErrorDescriptor
        else:
            err_descriptor_class = NonStaffErrorDescriptor

        err_descriptor = err_descriptor_class.from_descriptor(
            descriptor,
            error_msg=exc_info_to_str(sys.exc_info())
        )

        # Make an error module
        return err_descriptor.xmodule(system)

    system.set('user_is_staff', has_access(user, descriptor.location, 'staff', course_id))
    _get_html = module.get_html

    if wrap_xmodule_display is True:
        _get_html = wrap_xmodule(module.get_html, module, 'xmodule_display.html')

    module.get_html = replace_static_urls(
        _get_html,
        getattr(descriptor, 'data_dir', None),
        course_id=course_id,
        static_asset_path=static_asset_path or descriptor.static_asset_path
    )

    # Allow URLs of the form '/course/' refer to the root of multicourse directory
    #   hierarchy of this course
    module.get_html = replace_course_urls(module.get_html, course_id)

    # this will rewrite intra-courseware links
    # that use the shorthand /jump_to_id/<id>. This is very helpful
    # for studio authored courses (compared to the /course/... format) since it is
    # is durable with respect to moves and the author doesn't need to
    # know the hierarchy
    # NOTE: module_id is empty string here. The 'module_id' will get assigned in the replacement
    # function, we just need to specify something to get the reverse() to work
    module.get_html = replace_jump_to_id_urls(
        module.get_html,
        course_id,
        reverse('jump_to_id', kwargs={'course_id': course_id, 'module_id': ''})
    )

    if settings.MITX_FEATURES.get('DISPLAY_HISTOGRAMS_TO_STAFF'):
        if has_access(user, module, 'staff', course_id):
            module.get_html = add_histogram(module.get_html, module, user)

    # force the module to save after rendering
    module.get_html = save_module(module.get_html, module)
    return module

def get_module_for_descriptor(user, request, descriptor, field_data_cache, course_id,
                          position=None, wrap_xmodule_display=True, grade_bucket_type=None,
                          static_asset_path=''):
    """
    Implements get_module, extracting out the request-specific functionality.

    See get_module() docstring for further details.
    """
    # allow course staff to masquerade as student
    if has_access(user, descriptor, 'staff', course_id):
        setup_masquerade(request, True)

    track_function = make_track_function(request)
    xqueue_callback_url_prefix = get_xqueue_callback_url_prefix(request)

    return get_module_for_descriptor_internal(user, descriptor, field_data_cache, course_id,
                                              track_function, xqueue_callback_url_prefix,
                                              position, wrap_xmodule_display, grade_bucket_type,
                                              static_asset_path)
#@end

#@begin:
#@data:
def get_course_by_id(course_id, depth=0):
    """
    Given a course id, return the corresponding course descriptor.

    If course_id is not valid, raises a 404.

    depth: The number of levels of children for the modulestore to cache. None means infinite depth
    """
    try:
        course_loc = CourseDescriptor.id_to_location(course_id)
        return modulestore().get_instance(course_id, course_loc, depth=depth)
    except (KeyError, ItemNotFoundError):
        raise Http404("Course not found.")
    except InvalidLocationError:
        raise Http404("Invalid location")

def get_course_with_access(user, course_id, action, depth=0):
    """
    Given a course_id, look up the corresponding course descriptor,
    check that the user has the access to perform the specified action
    on the course, and return the descriptor.

    Raises a 404 if the course_id is invalid, or the user doesn't have access.

    depth: The number of levels of children for the modulestore to cache. None means infinite depth
    """
    course = get_course_by_id(course_id, depth=depth)
    if not has_access(user, course, action):
        # Deliberately return a non-specific error message to avoid
        # leaking info about access control settings
        raise Http404("Course not found.")
    return course

def yield_dynamic_descriptor_descendents(descriptor, module_creator):
    """
    This returns all of the descendants of a descriptor. If the descriptor
    has dynamic children, the module will be created using module_creator
    and the children (as descriptors) of that module will be returned.
    """
    def get_dynamic_descriptor_children(descriptor):
        if descriptor.has_dynamic_children():
            module = module_creator(descriptor)
            if module is None:
                return []
            return module.get_child_descriptors()
        else:
            return descriptor.get_children()

    stack = [descriptor]

    while len(stack) > 0:
        next_descriptor = stack.pop()
        stack.extend(get_dynamic_descriptor_children(next_descriptor))
        yield next_descriptor

def get_score(course_id, user, problem_descriptor, module_creator, field_data_cache):
    """
    Return the score for a user on a problem, as a tuple (correct, total).
    e.g. (5,7) if you got 5 out of 7 points.

    If this problem doesn't have a score, or we couldn't load it, returns (None,
    None).

    user: a Student object
    problem_descriptor: an XModuleDescriptor
    module_creator: a function that takes a descriptor, and returns the corresponding XModule for this user.
           Can return None if user doesn't have access, or if something else went wrong.
    cache: A FieldDataCache
    """
    if not user.is_authenticated():
        return (None, None)

    # some problems have state that is updated independently of interaction
    # with the LMS, so they need to always be scored. (E.g. foldit.)
    if problem_descriptor.always_recalculate_grades:
        problem = module_creator(problem_descriptor)
        if problem is None:
            return (None, None)
        score = problem.get_score()
        if score is not None:
            return (score['score'], score['total'])
        else:
            return (None, None)

    if not problem_descriptor.has_score:
        # These are not problems, and do not have a score
        return (None, None)

    # Create a fake KeyValueStore key to pull out the StudentModule
    key = DjangoKeyValueStore.Key(
        Scope.user_state,
        user.id,
        problem_descriptor.location,
        None
    )

    student_module = field_data_cache.find(key)

    if student_module is not None and student_module.max_grade is not None:
        correct = student_module.grade if student_module.grade is not None else 0
        total = student_module.max_grade
    else:
        # If the problem was not in the cache, or hasn't been graded yet,
        # we need to instantiate the problem.
        # Otherwise, the max score (cached in student_module) won't be available
        problem = module_creator(problem_descriptor)
        if problem is None:
            return (None, None)

        correct = 0.0
        total = problem.max_score()

        # Problem may be an error module (if something in the problem builder failed)
        # In which case total might be None
        if total is None:
            return (None, None)

    # Now we re-weight the problem, if specified
    weight = problem_descriptor.weight
    if weight is not None:
        if total == 0:
            log.exception("Cannot reweight a problem with zero total points. Problem: " + str(student_module))
            return (correct, total)
        correct = correct * weight / total
        total = weight

    return (correct, total)

def grade_for_percentage(grade_cutoffs, percentage):
    """
    Returns a letter grade as defined in grading_policy (e.g. 'A' 'B' 'C' for 6.002x) or None.

    Arguments
    - grade_cutoffs is a dictionary mapping a grade to the lowest
        possible percentage to earn that grade.
    - percentage is the final percent across all problems in a course
    """

    letter_grade = None

    # Possible grades, sorted in descending order of score
    descending_grades = sorted(grade_cutoffs, key=lambda x: grade_cutoffs[x], reverse=True)
    for possible_grade in descending_grades:
        if percentage >= grade_cutoffs[possible_grade]:
            letter_grade = possible_grade
            break

    return letter_grade

def grade(student, request, course, field_data_cache=None, keep_raw_scores=False):
    """
    This grades a student as quickly as possible. It returns the
    output from the course grader, augmented with the final letter
    grade. The keys in the output are:

    course: a CourseDescriptor

    - grade : A final letter grade.
    - percent : The final percent for the class (rounded up).
    - section_breakdown : A breakdown of each section that makes
        up the grade. (For display)
    - grade_breakdown : A breakdown of the major components that
        make up the final grade. (For display)
    - keep_raw_scores : if True, then value for key 'raw_scores' contains scores for every graded module

    More information on the format is in the docstring for CourseGrader.
    """
    grading_context = course.grading_context
    raw_scores = []

    if field_data_cache is None:
        field_data_cache = FieldDataCache(grading_context['all_descriptors'], course.id, student)

    totaled_scores = {}
    # This next complicated loop is just to collect the totaled_scores, which is
    # passed to the grader
    for section_format, sections in grading_context['graded_sections'].iteritems():
        format_scores = []
        for section in sections:
            section_descriptor = section['section_descriptor']
            section_name = section_descriptor.display_name_with_default

            should_grade_section = False
            # If we haven't seen a single problem in the section, we don't have to grade it at all! We can assume 0%
            for moduledescriptor in section['xmoduledescriptors']:
                # some problems have state that is updated independently of interaction
                # with the LMS, so they need to always be scored. (E.g. foldit.)
                if moduledescriptor.always_recalculate_grades:
                    should_grade_section = True
                    break

                # Create a fake key to pull out a StudentModule object from the FieldDataCache

                key = DjangoKeyValueStore.Key(
                    Scope.user_state,
                    student.id,
                    moduledescriptor.location,
                    None
                )
                if field_data_cache.find(key):
                    should_grade_section = True
                    break

            if should_grade_section:
                scores = []

                def create_module(descriptor):
                    '''creates an XModule instance given a descriptor'''
                    # TODO: We need the request to pass into here. If we could forego that, our arguments
                    # would be simpler
                    return get_module_for_descriptor(student, request, descriptor, field_data_cache, course.id)

                for module_descriptor in yield_dynamic_descriptor_descendents(section_descriptor, create_module):

                    (correct, total) = get_score(course.id, student, module_descriptor, create_module, field_data_cache)
                    if correct is None and total is None:
                        continue

                    if settings.GENERATE_PROFILE_SCORES:    # for debugging!
                        if total > 1:
                            correct = random.randrange(max(total - 2, 1), total + 1)
                        else:
                            correct = total

                    graded = module_descriptor.graded
                    if not total > 0:
                        #We simply cannot grade a problem that is 12/0, because we might need it as a percentage
                        graded = False

                    scores.append(Score(correct, total, graded, module_descriptor.display_name_with_default))

                _, graded_total = graders.aggregate_scores(scores, section_name)
                if keep_raw_scores:
                    raw_scores += scores
            else:
                graded_total = Score(0.0, 1.0, True, section_name)

            #Add the graded total to totaled_scores
            if graded_total.possible > 0:
                format_scores.append(graded_total)
            else:
                log.exception("Unable to grade a section with a total possible score of zero. " +
                              str(section_descriptor.location))

        totaled_scores[section_format] = format_scores

    grade_summary = course.grader.grade(totaled_scores, generate_random_scores=settings.GENERATE_PROFILE_SCORES)

    # We round the grade here, to make sure that the grade is an whole percentage and
    # doesn't get displayed differently than it gets grades
    grade_summary['percent'] = round(grade_summary['percent'] * 100 + 0.05) / 100

    letter_grade = grade_for_percentage(course.grade_cutoffs, grade_summary['percent'])
    grade_summary['grade'] = letter_grade
    grade_summary['totaled_scores'] = totaled_scores    # make this available, eg for instructor download & debugging
    if keep_raw_scores:
        grade_summary['raw_scores'] = raw_scores        # way to get all RAW scores out to instructor
                                                        # so grader can be double-checked
    return grade_summary
#@end