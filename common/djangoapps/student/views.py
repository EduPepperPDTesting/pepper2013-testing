"""
Student Views
"""
from __future__ import division
import datetime
import json
import logging
import random
import re
import urllib
import uuid
import time

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset_confirm
from django.core.cache import cache
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import validate_email, validate_slug, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from django.utils.http import cookie_date
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from courseware.model_data import FieldDataCache
from courseware.masquerade import setup_masquerade
from ratelimitbackend.exceptions import RateLimitException
from mitxmako.shortcuts import render_to_response, render_to_string
from student.models import (Registration, UserProfile, TestCenterUser, TestCenterUserForm,
                            TestCenterRegistration, TestCenterRegistrationForm,
                            PendingNameChange, PendingEmailChange,
                            CourseEnrollment, unique_id_for_user,
                            get_testcenter_registration, CourseEnrollmentAllowed)
from student.forms import PasswordResetFormNoActive
from certificates.models import CertificateStatuses, certificate_status_for_student
from xmodule.course_module import CourseDescriptor
from xmodule.modulestore.exceptions import ItemNotFoundError
from xmodule.modulestore.django import modulestore
from collections import namedtuple
from courseware.courses import get_courses, sort_by_announcement
from courseware.access import has_access
from external_auth.models import ExternalAuthMap
from bulk_email.models import Optout
import track.views
from statsd import statsd
from pytz import UTC
from PIL import Image
from StringIO import StringIO
from courseware.module_render import get_module
from student.models import CmsLoginInfo
from mongo_user_store import MongoUserStore
from courseware.views import course_filter
import requests
from django import db
from student.models import District, School, State
from django.db import models
from mail import send_html_mail
from courseware.courses import get_course_by_id
from study_time.models import record_time_store
from administration.models import site_setting_store

#@begin:add pd_time to total_time
#@date:2016-06-06
from django.db.models import Sum
from administration.models import PepRegStudent
#@end

#@begin:change to current year course time and total_time
#@date:2016-06-21
from reporting.models import reporting_store
#@end

from administration.models import UserLoginInfo
from datetime import timedelta

#@begin:Add for Dashboard Posts
#@date:2016-12-29
from student.models import (DashboardPosts, DashboardPostsImages, DashboardComments, DashboardLikes)
#@end

log = logging.getLogger("mitx.student")
AUDIT_LOG = logging.getLogger("audit")

Article = namedtuple('Article', 'title url author image deck publication publish_date')

def csrf_token(context):
    """A csrf token that can be included in a form."""
    csrf_token = context.get('csrf_token', '')
    if csrf_token == 'NOTPROVIDED':
        return ''
    return (u'<div style="display:none"><input type="hidden"'
            ' name="csrfmiddlewaretoken" value="%s" /></div>' % (csrf_token))

# NOTE: This view is not linked to directly--it is called from
# branding/views.py:index(), which is cached for anonymous users.
# This means that it should always return the same thing for anon
# users. (in particular, no switching based on query params allowed)
def index(request, extra_context={}, user=None):
    """
    Render the edX main page.

    extra_context is used to allow immediate display of certain modal windows, eg signup,
    as used by external_auth.
    """

    # The course selection work is done in courseware.courses.
    domain = settings.MITX_FEATURES.get('FORCE_UNIVERSITY_DOMAIN')  # normally False
    # do explicit check, because domain=None is valid
    if domain is False:
        domain = request.META.get('HTTP_HOST')

    courses = get_courses(None, domain=domain)
    courses = sort_by_announcement(courses)
    context = {'courses': courses, 'index': True}
    context.update(extra_context)
    return render_to_response('index.html', context)

day_pattern = re.compile(r'\s\d+,\s')
multimonth_pattern = re.compile(r'\s?\-\s?\S+\s')

def _get_date_for_press(publish_date):
    # strip off extra months, and just use the first:
    date = re.sub(multimonth_pattern, ", ", publish_date)
    if re.search(day_pattern, date):
        date = datetime.datetime.strptime(date, "%B %d, %Y").replace(tzinfo=UTC)
    else:
        date = datetime.datetime.strptime(date, "%B, %Y").replace(tzinfo=UTC)
    return date

def press(request):
    json_articles = cache.get("student_press_json_articles")
    if json_articles is None:
        if hasattr(settings, 'RSS_URL'):
            content = urllib.urlopen(settings.PRESS_URL).read()
            json_articles = json.loads(content)
        else:
            content = open(settings.PROJECT_ROOT / "templates" / "press.json").read()
            json_articles = json.loads(content)
        cache.set("student_press_json_articles", json_articles)
    articles = [Article(**article) for article in json_articles]
    articles.sort(key=lambda item: _get_date_for_press(item.publish_date), reverse=True)
    return render_to_response('static_templates/press.html', {'articles': articles})

def process_survey_link(survey_link, user):
    """
    If {UNIQUE_ID} appears in the link, replace it with a unique id for the user.
    Currently, this is sha1(user.username).  Otherwise, return survey_link.
    """
    return survey_link.format(UNIQUE_ID=unique_id_for_user(user))

def cert_info(user, course):
    """
    Get the certificate info needed to render the dashboard section for the given
    student and course.  Returns a dictionary with keys:

    'status': one of 'generating', 'ready', 'notpassing', 'processing', 'restricted'
    'show_download_url': bool
    'download_url': url, only present if show_download_url is True
    'show_disabled_download_button': bool -- true if state is 'generating'
    'show_survey_button': bool
    'survey_url': url, only if show_survey_button is True
    'grade': if status is not 'processing'
    """
    if not course.has_ended():
        return {}

    return _cert_info(user, course, certificate_status_for_student(user, course.id))

def _cert_info(user, course, cert_status):
    """
    Implements the logic for cert_info -- split out for testing.
    """
    default_status = 'processing'

    default_info = {'status': default_status,
                    'show_disabled_download_button': False,
                    'show_download_url': False,
                    'show_survey_button': False}

    if cert_status is None:
        return default_info

    # simplify the status for the template using this lookup table
    template_state = {
        CertificateStatuses.generating: 'generating',
        CertificateStatuses.regenerating: 'generating',
        CertificateStatuses.downloadable: 'ready',
        CertificateStatuses.notpassing: 'notpassing',
        CertificateStatuses.restricted: 'restricted',
    }

    status = template_state.get(cert_status['status'], default_status)

    d = {'status': status,
         'show_download_url': status == 'ready',
         'show_disabled_download_button': status == 'generating', }

    if (status in ('generating', 'ready', 'notpassing', 'restricted') and
            course.end_of_course_survey_url is not None):
        d.update({
            'show_survey_button': True,
            'survey_url': process_survey_link(course.end_of_course_survey_url, user)})
    else:
        d['show_survey_button'] = False

    if status == 'ready':
        if 'download_url' not in cert_status:
            log.warning("User %s has a downloadable cert for %s, but no download url",
                        user.username, course.id)
            return default_info
        else:
            d['download_url'] = cert_status['download_url']

    if status in ('generating', 'ready', 'notpassing', 'restricted'):
        if 'grade' not in cert_status:
            # Note: as of 11/20/2012, we know there are students in this state-- cs169.1x,
            # who need to be regraded (we weren't tracking 'notpassing' at first).
            # We can add a log.warning here once we think it shouldn't happen.
            return default_info
        else:
            d['grade'] = cert_status['grade']

    return d

@ensure_csrf_cookie
def signin_user(request):
    """
    This view will display the non-modal login form
    """
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))

    email = request.GET.get('regcheck', None)
    if email:
        reg = registration_check(email)
        if reg['status'] == 'unregistered':
            next_page = request.GET.get('next', '')
            return redirect(reverse('register_user') + reg['key'] + '?next=' + next_page)
        elif not reg['status']:
            message = '''Your account has not been set up in our system. This means your district has not provided us
                         with the necessary information. Please contact your district or school's professional
                         development coordinator to have your account created in Pepper. You can also email
                         <a href="mailto:pcgpepper@pcgus.com">pcgpepper@pcgus.com</a> for assistance. You will receive a
                         response within two business days.'''
            error_context = {'window_title': 'Missing Account',
                             'error_title': 'Missing Account',
                             'error_message': message}
            return render_to_response('error.html', error_context)
    elif email is not None:
        message = '''Your email was not successfully sent by your PD system (TNL). This likely means that your email
                     needs to be added in that system. Please contact your school or district PD coordinator or Data
                     Administrator to fix your email in the source system for that information. Once that information is
                     fixed, within 24 hours you should be able to access the course.'''
        error_context = {'window_title': 'Missing Email',
                         'error_title': 'Missing Email',
                         'error_message': message}
        return render_to_response('error.html', error_context)

    context = {
        'course_id': request.GET.get('course_id'),
        'enrollment_action': request.GET.get('enrollment_action')
    }
    return render_to_response('login.html', context)

@ensure_csrf_cookie
def cms_login_info(request):
    """
    """
    csrf_token = csrf(request)['csrf_token']
    return render_to_response('cms_login_info.html', {
        'csrf': csrf_token,
        'forgot_password_link': "//{base}/#forgot-password-modal".format(base=settings.LMS_BASE),
    })

@ensure_csrf_cookie
def register_user(request, activation_key=None):
    """
    This view will display the non-modal registration form
    """

    if not activation_key:
        return HttpResponse("Invalid Activation Key.")

    regs = Registration.objects.filter(activation_key=activation_key)

    if not regs:
        return render_to_response("registration/invalid_activation_key.html", {})
    else:
        reg = regs[0]

    profile = UserProfile.objects.get(user_id=reg.user_id)

    if request.user.is_authenticated() and profile.user == request.user:
        return redirect(reverse('dashboard'))

    if profile.subscription_status == 'Registered':
        return HttpResponse("User already registered.")

    # if not profile.cohort_id:
    #    return HttpResponse("Invalid cohort.")

    context = {
        'profile': profile,
        'activation_key': activation_key,
        'course_id': request.GET.get('course_id'),
        'enrollment_action': request.GET.get('enrollment_action')
    }
    # if extra_context is not None:
    #     context.update(extra_context)

    return render_to_response('register.html', context)


def registration_check(email):
    try:
        user = User.objects.get(email=email)
        if user.is_active == 0:
            reg = Registration.objects.get(user_id=user.id)
            return_value = {'status': 'unregistered', 'key': reg.activation_key}
        else:
            raise Exception('User is already active.')
    except User.DoesNotExist:
        return_value = {'status': False}
    except Exception as e:
        return_value = {'status': 'registered', 'error': '{e}'.format(e=e)}
    return return_value


# copy from lms/djangoapps/courseware/module_render.py
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


class StudentModule(models.Model):
    """
    Keeps student state for a particular module in a particular course.
    """
    class Meta:
        db_table = 'courseware_studentmodule'
        # unique_together = (('student', 'module_state_key', 'course_id'),)

    module_type = models.CharField(max_length=32, default='problem', db_index=True)
    module_state_key = models.CharField(max_length=255, db_index=True, db_column='module_id')
    # student = models.ForeignKey(User, db_index=True)
    student_id = models.IntegerField(default=0)
    course_id = models.CharField(max_length=255, db_index=True)
    state = models.TextField(null=True, blank=True)
    grade = models.FloatField(null=True, blank=True, db_index=True)
    max_grade = models.FloatField(null=True, blank=True)
    done = models.CharField(max_length=8, default='na', db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)
    module_id = models.CharField(max_length=255, db_index=True)

def course_completed(request, user, course):
    field_data_cache = FieldDataCache([course], course.id, user)
    course_instance = get_module(user, request, course.location, field_data_cache, course.id, grade_bucket_type='ajax')
    if course_instance.complete_course:
        return True

def course_from_id(course_id):
    """Return the CourseDescriptor corresponding to this course_id"""
    course_loc = CourseDescriptor.id_to_location(course_id)
    return modulestore().get_instance(course_id, course_loc)

@login_required
def more_courses_available(request):
    # allowed course_id list
    allowed = list(CourseEnrollmentAllowed.objects.filter(email=request.user.email, is_active=True).values_list('course_id', flat=True))

    # remove enrolled course_id
    for enrollment in CourseEnrollment.enrollments_for_user(request.user):
        if enrollment.course_id in allowed:
            allowed.remove(enrollment.course_id)

    # fetch courses
    courses = []
    for course_id in allowed:
        try:
            course = course_from_id(course_id)
            courses.append(course)
        except:
            pass

    # sort courses
    #@begin:change the type of display_subject to list 
    #@date:2016-05-31
    #courses.sort(cmp=lambda x, y: cmp(x.display_subject.lower(), y.display_subject.lower()))
    courses.sort(cmp=lambda x, y: cmp(x.display_subject[0].lower(), y.display_subject[0].lower()))
    more_subjects_courses = [[], [], [], [], []]
    #@end

    # 20160322 modify "Add new grade 'PreK-3'"
    # begin
    subject_index = [-1, -1, -1, -1, -1]
    currSubject = ["", "", "", "", ""]
    g_courses = [[], [], [], [], []]
    # end 

    for course in courses:
        course_filter(course, subject_index, currSubject, g_courses, '', more_subjects_courses)

    #@begin:add the course which subject more than 1 to g_courses 
    #@date:2016-05-31
    for i in range(0,len(more_subjects_courses)):
        if len(more_subjects_courses[i]) > 0:
            g_courses[i].append(more_subjects_courses[i])
    #@end

    for gc in g_courses:
        for sc in gc:
            sc.sort(key=lambda x: x.display_coursenumber)

    context = {'courses': g_courses}

    return render_to_response('more_courses_available.html', context)

@login_required
@ensure_csrf_cookie
def dashboard(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=request.user.id)

    # Build our courses list for the user, but ignore any courses that no longer
    # exist (because the course IDs have changed). Still, we don't delete those
    # enrollments, because it could have been a data push snafu.

    courses_complated = []
    courses_incomplated = []
    courses = []

    external_time = 0
    external_times = {}
    exists = 0

    total_course_times = {}

    # get none enrolled course count for current login user
    rts = record_time_store()
    if user_id != request.user.id:
        allowed = CourseEnrollmentAllowed.objects.filter(email=user.email, is_active=True).values_list('course_id', flat=True)
        # make sure the course exists
        for course_id in allowed:
            try:
                # course=course_from_id(course_id)
                exists = exists + 1
            except:
                pass

    for enrollment in CourseEnrollment.enrollments_for_user(user):
        try:
            c = course_from_id(enrollment.course_id)
            c.student_enrollment_date = enrollment.created

            if enrollment.course_id in allowed:
                exists = exists - 1

            # model_data_cache = FieldDataCache.cache_for_descriptor_descendents(c.id, user, c, depth=1)
            # chapter_count=len(model_data_cache.descriptors)
            # model_data_cache = FieldDataCache.cache_for_descriptor_descendents(c.id, user, c, depth=2)
            # count_history=0
            # c.is_completed=False
            # chapter_count=len(model_data_cache.descriptors)-chapter_count
            # for m in model_data_cache.descriptors:
            #     if m.ispublic:
            #         chapter_count=chapter_count+1
            #     if len(StudentModule.objects.filter(student_id=user.id,
            #                                         course_id=c.id,
            #                                         module_type='sequential',
            #                                         module_id=m.location)) > 0:
            #         count_history=count_history+1

            courses.append(c)

            # grade_precent=grade(user,request,c)['percent']
            # if count_history==chapter_count and grade_precent >= 0.85:
            #     courses_complated.append(c)
            # else:
            #     courses_incomplated.append(c)
            if user.is_superuser:
                external_times[c.id] = 0
            else:
                external_times[c.id] = rts.get_external_time(str(user.id), c.id)
                external_time += external_times[c.id]
                external_times[c.id] = study_time_format(external_times[c.id])
            field_data_cache = FieldDataCache([c], c.id, user)
            course_instance = get_module(user, request, c.location, field_data_cache, c.id, grade_bucket_type='ajax')

            if course_instance.complete_course:
                c.complete_date = course_instance.complete_date
                c.student_enrollment_date = course_instance.complete_date
                courses_complated.append(c)
            else:
                courses_incomplated.append(c)

        except ItemNotFoundError:
            log.error("User {0} enrolled in non-existent course {1}"
                      .format(user.username, enrollment.course_id))

    courses_complated = sorted(courses_complated, key=lambda x: x.complete_date, reverse=True)
    courses_incomplated = sorted(courses_incomplated, key=lambda x: x.student_enrollment_date, reverse=True)

    course_optouts = Optout.objects.filter(user=user).values_list('course_id', flat=True)
    message = ""
    if not user.is_active:
        message = render_to_string('registration/activate_account_notice.html', {'email': user.email})
    # Global staff can see what courses errored on their dashboard
    staff_access = False
    errored_courses = {}
    if has_access(user, 'global', 'staff'):
        # Show any courses that errored on load
        staff_access = True
        errored_courses = modulestore().get_errored_courses()

    show_courseware_links_for = frozenset(course.id for course in courses
                                          if has_access(user, course, 'load'))

    cert_statuses = {course.id: cert_info(user, course) for course in courses}
    exam_registrations = {course.id: exam_registration_info(request.user, course) for course in courses}
    if user.is_superuser:
        course_times = {course.id: 0 for course in courses}
        total_course_times = {course.id: 0 for course in courses}
    else:
        course_times = {course.id: study_time_format(rts.get_aggregate_course_time(str(user.id), course.id, 'courseware')) for course in courses}

        #@begin:change to current year course time and total_time
        #@date:2016-06-21
        rs = reporting_store()
        rs.set_collection('UserCourseView')
        for course in courses:
            results = rs.collection.find({"user_id":request.user.id,"course_id":course.id},{"_id":0,"total_time":1})
            total_time_user = 0
            for v in results:
                total_time_user = total_time_user + v['total_time']
           
            total_course_times[course.id] = study_time_format(total_time_user) 
        #@end

    # get info w.r.t ExternalAuthMap
    external_auth_map = None
    try:
        external_auth_map = ExternalAuthMap.objects.get(user=user)
    except ExternalAuthMap.DoesNotExist:
        pass

    #@begin:add pd_time to total_time
    #@date:2016-06-06
    id_of_user = ''
    if user_id:
        id_of_user = user_id
    else:
        id_of_user = request.user.id
    pd_time = 0;
    pd_time_tmp = PepRegStudent.objects.values('student_id').annotate(credit_sum=Sum('student_credit')).filter(student_id=id_of_user)
    if pd_time_tmp:
        pd_time = pd_time_tmp[0]['credit_sum'] * 3600
    #@end

    if user.is_superuser:

        course_time = 0
        discussion_time = 0
        portfolio_time = 0
        all_course_time = 0
        collaboration_time = 0
        adjustment_time_totle = 0
        total_time_in_pepper = 0
    else:
        course_time, discussion_time, portfolio_time = rts.get_stats_time(str(user.id))
        all_course_time = course_time + external_time
        collaboration_time = discussion_time + portfolio_time
        adjustment_time_totle = rts.get_adjustment_time(str(user.id), 'total', None)
        #@begin:add pd_time to total_time
        #@date:2016-06-06
        #total_time_in_pepper = all_course_time + collaboration_time + adjustment_time_totle
        total_time_in_pepper = all_course_time + collaboration_time + adjustment_time_totle + pd_time
        #@end

    #20160413 load alert_message
    #begin
    site_settings = site_setting_store()
    al_text = "__NONE__"
    try:
        al_text = site_settings.get_item('alert_text')['value']
    except Exception as e:
        pass
    if al_text == "__NONE__":
        al_text = ""

    al_enabled = "un_enabled"
    try:
        al_enabled = site_settings.get_item('alert_enabled')['value']
    except Exception as e:
        pass
    #end

    context = {
        'courses_complated': courses_complated,
        'courses_incomplated': courses_incomplated,
        'course_optouts': course_optouts,
        'message': message,
        'external_auth_map': external_auth_map,
        'staff_access': staff_access,
        'errored_courses': errored_courses,
        'show_courseware_links_for': show_courseware_links_for,
        'cert_statuses': cert_statuses,
        'exam_registrations': exam_registrations,
        'curr_user': user,
        'havent_enroll': exists,
        'all_course_time': study_time_format(all_course_time),
        'collaboration_time': study_time_format(collaboration_time),
        'total_time_in_pepper': study_time_format(total_time_in_pepper),
        'course_times': course_times,
        'external_times': external_times,
        'totle_adjustment_time': study_time_format(adjustment_time_totle, True),
        'alert_text':al_text,
        'alert_enabled':al_enabled,
        'total_course_times':total_course_times
    }

    return render_to_response('dashboard.html', context)

def try_change_enrollment(request):
    """
    This method calls change_enrollment if the necessary POST
    parameters are present, but does not return anything. It
    simply logs the result or exception. This is usually
    called after a registration or login, as secondary action.
    It should not interrupt a successful registration or login.
    """
    if 'enrollment_action' in request.POST:
        try:
            enrollment_response = change_enrollment(request)
            # There isn't really a way to display the results to the user, so we just log it
            # We expect the enrollment to be a success, and will show up on the dashboard anyway
            log.info(
                "Attempted to automatically enroll after login. Response code: {0}; response body: {1}".format(
                    enrollment_response.status_code,
                    enrollment_response.content
                )
            )
        except Exception, e:
            log.exception("Exception automatically enrolling after login: {0}".format(str(e)))

def change_enrollment(request):
    """
    Modify the enrollment status for the logged-in user.

    The request parameter must be a POST request (other methods return 405)
    that specifies course_id and enrollment_action parameters. If course_id or
    enrollment_action is not specified, if course_id is not valid, if
    enrollment_action is something other than "enroll" or "unenroll", if
    enrollment_action is "enroll" and enrollment is closed for the course, or
    if enrollment_action is "unenroll" and the user is not enrolled in the
    course, a 400 error will be returned. If the user is not logged in, 403
    will be returned; it is important that only this case return 403 so the
    front end can redirect the user to a registration or login page when this
    happens. This function should only be called from an AJAX request or
    as a post-login/registration helper, so the error messages in the responses
    should never actually be user-visible.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    user = request.user
    if not user.is_authenticated():
        return HttpResponseForbidden()

    action = request.POST.get("enrollment_action")
    course_id = request.POST.get("course_id")
    if course_id is None:
        return HttpResponseBadRequest(_("Course id not specified"))

    if action == "enroll":
        # Make sure the course exists
        # We don't do this check on unenroll, or a bad course id can't be unenrolled from
        try:
            course = course_from_id(course_id)
        except ItemNotFoundError:
            log.warning("User {0} tried to enroll in non-existent course {1}"
                        .format(user.username, course_id))
            return HttpResponseBadRequest(_("Course id is invalid"))

        if not has_access(user, course, 'enroll'):
            return HttpResponseBadRequest(_("Enrollment is closed"))

        org, course_num, run = course_id.split("/")
        statsd.increment("common.student.enrollment",
                         tags=["org:{0}".format(org),
                               "course:{0}".format(course_num),
                               "run:{0}".format(run)])

        CourseEnrollment.enroll(user, course.id)

        return HttpResponse()

    elif action == "unenroll":
        try:
            CourseEnrollment.unenroll(user, course_id)

            org, course_num, run = course_id.split("/")
            statsd.increment("common.student.unenrollment",
                             tags=["org:{0}".format(org),
                                   "course:{0}".format(course_num),
                                   "run:{0}".format(run)])

            return HttpResponse()
        except CourseEnrollment.DoesNotExist:
            return HttpResponseBadRequest(_("You are not enrolled in this course"))
    else:
        return HttpResponseBadRequest(_("Enrollment action is invalid"))

@ensure_csrf_cookie
def accounts_login(request, error=""):
    if settings.MITX_FEATURES.get('AUTH_USE_CAS'):
        return redirect(reverse('cas-login'))
    return render_to_response('login.html', {'error': error})


# Need different levels of logging
@ensure_csrf_cookie
def login_user(request, error=""):
    """AJAX request to log in the user."""
    if 'email' not in request.POST or 'password' not in request.POST:
        return HttpResponse(json.dumps({'success': False,
                                        'value': _('There was an error receiving your login information. Please email us.')}),
                            content_type="application/json")  # TODO: User error message

    email = request.POST['email']
    password = request.POST['password']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        AUDIT_LOG.warning(u"Login failed - Unknown user email: {0}".format(email))
        user = None

    # if the user doesn't exist, we want to set the username to an invalid
    # username so that authentication is guaranteed to fail and we can take
    # advantage of the ratelimited backend
    username = user.username if user else ""
    try:
        user = authenticate(username=username, password=password, request=request)

        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', 'not get')
        login_info = CmsLoginInfo(ip_address=ip_address, user_name=username, log_type_login=True, login_or_logout_time=datetime.datetime.utcnow())
        login_info.save()
    # this occurs when there are too many attempts from the same IP address
    except RateLimitException:
        return HttpResponse(json.dumps({'success': False,
                                        'value': _('Too many failed login attempts. Try again later.')}),
                            content_type="application/json")
    if user is None:
        # if we didn't find this username earlier, the account for this email
        # doesn't exist, and doesn't have a corresponding password
        if username != "":
            AUDIT_LOG.warning(u"Login failed - password for {0} is invalid".format(email))
        return HttpResponse(json.dumps({'success': False,
                                        'value': _('Email or password is incorrect.')}),
                            content_type="application/json")

    if user is not None and user.is_active:
        try:
            # We do not log here, because we have a handler registered
            # to perform logging on successful logins.
            login(request, user)
            if request.POST.get('remember') == 'true':
                request.session.set_expiry(604800)
                log.debug("Setting user session to never expire")
            else:
                request.session.set_expiry(0)
        except Exception as e:
            AUDIT_LOG.critical("Login failed - Could not create session. Is memcached running?")
            log.critical("Login failed - Could not create session. Is memcached running?")
            log.exception(e)
            raise

        try_change_enrollment(request)

        statsd.increment("common.student.successful_login")
        response = HttpResponse(json.dumps({'success': True}), content_type="application/json")

        # set the login cookie for the edx marketing site
        # we want this cookie to be accessed via javascript
        # so httponly is set to None

        if request.session.get_expire_at_browser_close():
            max_age = None
            expires = None
        else:
            max_age = request.session.get_expiry_age()
            expires_time = time.time() + max_age
            expires = cookie_date(expires_time)

        response.set_cookie(settings.EDXMKTG_COOKIE_NAME,
                            'true', max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path='/',
                            secure=None,
                            httponly=None)

        #@begin:record user login time
        #@date:2016-08-22
        utctime_str = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        utctime_30m_str = (datetime.datetime.utcnow() + timedelta(seconds=30*60)).strftime('%Y-%m-%d %H:%M:%S')

        user_log_info = UserLoginInfo.objects.filter(user_id=user.id)
        if user_log_info:
            user_log_info[0].login_time = utctime_str
            user_log_info[0].logout_time = utctime_30m_str
            user_log_info[0].temp_time = utctime_str

            user_log_info[0].last_session = 60 * 30
            user_log_info[0].total_session = user_log_info[0].total_session + 60 * 30

            user_log_info[0].login_times = user_log_info[0].login_times + 1
            user_log_info[0].logout_press = 0

            user_log_info[0].save()
        else:
            user_log_info = UserLoginInfo(user_id=user.id,login_time=utctime_str,logout_time=utctime_30m_str,last_session=1800,total_session=1800,temp_time=utctime_str)
            user_log_info.save();
        #@end

        return response

    AUDIT_LOG.warning(u"Login failed - Account not active for user {0}, resending activation".format(username))

    # reactivation_email_for_user(user)
    not_activated_msg = _(
        "You do not have an active Pepper account. Please click <a href='{0}'>here</a> to contact Pepper Support.".format(reverse('contact_us')))
    return HttpResponse(json.dumps({'success': False,
                                    'value': not_activated_msg}),
                        content_type="application/json")

@ensure_csrf_cookie
def logout_user(request):
    """
    HTTP request to log out the user. Redirects to marketing page.
    Deletes both the CSRF and sessionid cookies so the marketing
    site can determine the logged in state of the user
    """
    # We do not log here, because we have a handler registered
    # to perform logging on successful logouts.

    #@begin:record user logout time
    #@date:2016-08-22
    user_id = request.user.id
    utctime = datetime.datetime.utcnow()
    utctime_str = utctime.strftime('%Y-%m-%d %H:%M:%S')

    user_log_info = UserLoginInfo.objects.filter(user_id=user_id)
    if user_log_info:
        user_log_info[0].logout_time = utctime_str
        db_login_time = datetime.datetime.strptime(user_log_info[0].login_time, '%Y-%m-%d %H:%M:%S')
        last_session = datetime.datetime.strptime(utctime_str, '%Y-%m-%d %H:%M:%S') - db_login_time
        user_log_info[0].last_session = last_session.seconds

        time_diff = utctime - datetime.datetime.strptime(user_log_info[0].temp_time, '%Y-%m-%d %H:%M:%S')
        time_diff_seconds = time_diff.seconds
        user_log_info[0].total_session = user_log_info[0].total_session + time_diff_seconds - 1800
        user_log_info[0].logout_press = 1
        user_log_info[0].save()       
    #@end

    logout(request)
    if settings.MITX_FEATURES.get('AUTH_USE_CAS'):
        target = reverse('cas-logout')
    else:
        target = '/'
    username = request.user.username if request.user else ""
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', 'not get')
    login_info = CmsLoginInfo(ip_address=ip_address, user_name=username, log_type_login=False, login_or_logout_time=datetime.datetime.utcnow())
    login_info.save()
    response = redirect(target)
    response.delete_cookie(settings.EDXMKTG_COOKIE_NAME,
                           path='/',
                           domain=settings.SESSION_COOKIE_DOMAIN)
    return response

@login_required
@ensure_csrf_cookie
def change_setting(request):
    """JSON call to change a profile setting: Right now, location"""
    # TODO (vshnayder): location is no longer used
    up = UserProfile.objects.get(user=request.user)  # request.user.profile_cache
    if 'location' in request.POST:
        up.location = request.POST['location']
    up.save()

    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location, }))

def _do_create_account(post_vars):
    """
    Given cleaned post variables, create the User and UserProfile objects, as well as the
    registration for this user.

    Returns a tuple (User, UserProfile, Registration).

    Note: this function is also used for creating test users.
    """
    user = User(username=post_vars['username'],
                email=post_vars['email'],
                is_active=False)
    user.set_password(post_vars['password'])
    registration = Registration()
    # TODO: Rearrange so that if part of the process fails, the whole process fails.
    # Right now, we can have e.g. no registration e-mail sent out and a zombie account
    try:
        user.save()
    except IntegrityError:
        js = {'success': False}
        # Figure out the cause of the integrity error
        if len(User.objects.filter(username=post_vars['username'])) > 0:
            js['value'] = _("An account with the Public Username '{username}' already exists.").format(username=post_vars['username'])
            js['field'] = 'username'
            return HttpResponse(json.dumps(js))

        if len(User.objects.filter(email=post_vars['email'])) > 0:
            js['value'] = _("An account with the Email '{email}' already exists.").format(email=post_vars['email'])
            js['field'] = 'email'
            return HttpResponse(json.dumps(js))

        raise

    registration.register(user)

    profile = UserProfile(user=user)
    # profile.name = post_vars['name']
    profile.user.first_name = post_vars['first_name']
    profile.user.last_name = post_vars['last_name']
    profile.major_subject_area_id = post_vars['major_subject_area_id']
    profile.grade_level_id = post_vars['grade_level_id']
    profile.district_id = post_vars['district_id']
    profile.school_id = post_vars['school_id']
    profile.years_in_education_id = post_vars['years_in_education_id']
    profile.level_of_education = post_vars.get('level_of_education')
    profile.gender = post_vars.get('gender')
    profile.mailing_address = post_vars.get('mailing_address')
    profile.goals = post_vars.get('goals')

    try:
        profile.year_of_birth = int(post_vars['year_of_birth'])
    except (ValueError, KeyError):
        # If they give us garbage, just ignore it instead
        # of asking them to put an integer.
        profile.year_of_birth = None
    try:
        profile.user.save()
        profile.save()
    except Exception:
        log.exception("UserProfile creation failed for user {id}.".format(id=user.id))
    return (user, profile, registration)

@ensure_csrf_cookie
def create_account(request, post_override=None):
    """
    JSON call to create new edX account.
    Used by form in signup_modal.html, which is included into navigation.html
    """
    js = {'success': False}

    post_vars = post_override if post_override else request.POST

    # if doing signup for an external authorization, then get email, password, name from the eamap
    # don't use the ones from the form, since the user could have hacked those
    # unless originally we didn't get a valid email or name from the external auth
    DoExternalAuth = 'ExternalAuthMap' in request.session
    if DoExternalAuth:
        eamap = request.session['ExternalAuthMap']
        try:
            validate_email(eamap.external_email)
            email = eamap.external_email
        except ValidationError:
            email = post_vars.get('email', '')

        if eamap.external_name.strip() == '':
            name = post_vars.get('first_name', '') + post_vars.get('last_name', '')
        else:
            name = eamap.external_name

        password = eamap.internal_password
        post_vars = dict(post_vars.items())
        post_vars.update(dict(email=email, name=name, password=password))
        log.debug(u'In create_account with external_auth: user = %s, email=%s', name, email)

    # Confirm we have a properly formed request
    for a in ['username', 'email', 'password', 'first_name', 'last_name']:
        if a not in post_vars:
            js['value'] = _("Error (401 {field}). E-mail us.").format(field=a)
            js['field'] = a
            return HttpResponse(json.dumps(js))

    # Can't have terms of service for certain SHIB users, like at Stanford
    tos_not_required = settings.MITX_FEATURES.get("AUTH_USE_SHIB") \
        and settings.MITX_FEATURES.get('SHIB_DISABLE_TOS') \
        and DoExternalAuth and ("shib" in eamap.external_domain)

    if not tos_not_required:
        if post_vars.get('terms_of_service', 'false') != u'true':
            js['value'] = _("You must accept the terms of service.").format(field=a)
            js['field'] = 'terms_of_service'
            return HttpResponse(json.dumps(js))

    # Confirm appropriate fields are there.
    # TODO: Check e-mail format is correct.
    # TODO: Confirm e-mail is not from a generic domain (mailinator, etc.)? Not sure if
    # this is a good idea
    # TODO: Check password is sane
    required_post_vars = ['username', 'email', 'first_name', 'last_name', 'password', 'terms_of_service']     # 'honor_code'
    if tos_not_required:
        required_post_vars = ['username', 'email', 'first_name', 'last_name', 'password']  # 'honor_code'

    for a in required_post_vars:
        if len(post_vars[a]) < 2:
            error_str = {'username': 'Username must be minimum of two characters long.',
                         'email': 'A properly formatted e-mail is required.',
                         'first_name': 'Your first name must be a minimum of two characters long.',
                         'last_name': 'Your last name must be a minimum of two characters long.',
                         'password': 'A valid password is required.',
                         'terms_of_service': 'Accepting Terms of Service is required.',
                         'honor_code': 'Agreeing to the Honor Code is required.',
                         }
            js['value'] = error_str[a]
            js['field'] = a
            return HttpResponse(json.dumps(js))

    if post_vars.get('username') == post_vars.get('password'):
        js['value'] = 'Password and Public Username cannot be the same.'
        js['field'] = 'password'
        return HttpResponse(json.dumps(js))

    required_post_vars_dropdown = ['major_subject_area_id', 'grade_level_id', 'district_id',
                                   'school_id', 'years_in_education_id',
                                   'percent_lunch', 'percent_iep', 'percent_eng_learner'
                                   ]

    for a in required_post_vars_dropdown:
        if len(post_vars[a]) < 1:
            error_str = {
                'major_subject_area_id': 'Major Subject Area is required',
                'grade_level_id': 'Grade Level-Check is required',
                'district_id': 'District is required',
                'school_id': 'School is required',
                'years_in_education_id': 'Number of Years in Education is required',
                'percent_lunch': 'Free/Reduced Lunch is required',
                'percent_iep': 'IEPs is required',
                'percent_eng_learner': 'English Learners is required'
            }
            js['value'] = error_str[a]
            js['field'] = a
            return HttpResponse(json.dumps(js))
    try:
        validate_email(post_vars['email'])
    except ValidationError:
        js['value'] = _("Valid e-mail is required.").format(field=a)
        js['field'] = 'email'
        return HttpResponse(json.dumps(js))

    try:
        validate_slug(post_vars['username'])
    except ValidationError:
        js['value'] = _("Username should only consist of A-Z and 0-9, with no spaces.").format(field=a)
        js['field'] = 'username'
        return HttpResponse(json.dumps(js))

    if post_vars.get('activation_key'):
        return activate_imported_account(post_vars, request.FILES.get("photo"))

    # Ok, looks like everything is legit.  Create the account.
    ret = _do_create_account(post_vars)
    if isinstance(ret, HttpResponse):  # if there was an error then return that
        return ret
    (user, profile, registration) = ret
    d = {'first_name': post_vars['first_name'],
         'last_name': post_vars['last_name'],
         'key': registration.activation_key,
         }

    # composes activation email
    subject = render_to_string('emails/activation_email_subject.txt', d)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('emails/activation_email.txt', d)

    # dont send email if we are doing load testing or random user generation for some reason
    if not (settings.MITX_FEATURES.get('AUTOMATIC_AUTH_FOR_TESTING')):
        try:
            if settings.MITX_FEATURES.get('REROUTE_ACTIVATION_EMAIL'):
                dest_addr = settings.MITX_FEATURES['REROUTE_ACTIVATION_EMAIL']
                message = ("Activation for %s (%s): %s\n" % (user, user.email, profile.name) +
                           '-' * 80 + '\n\n' + message)
                # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [dest_addr], fail_silently=False)
            else:
                _res = user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        except:
            log.warning('Unable to send activation email to user', exc_info=True)
            js['value'] = _('Could not send activation e-mail.')
            return HttpResponse(json.dumps(js))

    # Immediately after a user creates an account, we log them in. They are only
    # logged in until they close the browser. They can't log in again until they click
    # the activation link from the email.
    login_user = authenticate(username=post_vars['username'], password=post_vars['password'])
    login(request, login_user)
    request.session.set_expiry(0)

    # TODO: there is no error checking here to see that the user actually logged in successfully,
    # and is not yet an active user.
    if login_user is not None:
        AUDIT_LOG.info(u"Login success on new account creation - {0}".format(login_user.username))

    if DoExternalAuth:
        eamap.user = login_user
        eamap.dtsignup = datetime.datetime.now(UTC)
        eamap.save()
        AUDIT_LOG.info("User registered with external_auth %s", post_vars['username'])
        AUDIT_LOG.info('Updated ExternalAuthMap for %s to be %s', post_vars['username'], eamap)

        if settings.MITX_FEATURES.get('BYPASS_ACTIVATION_EMAIL_FOR_EXTAUTH'):
            log.info('bypassing activation email')
            login_user.is_active = True
            login_user.save()
            AUDIT_LOG.info(u"Login activated on extauth account - {0} ({1})".format(login_user.username, login_user.email))

    try_change_enrollment(request)

    statsd.increment("common.student.account_created")

    js = {'success': True}
    HttpResponse(json.dumps(js), mimetype="application/json")

    response = HttpResponse(json.dumps({'success': True}))

    # set the login cookie for the edx marketing site
    # we want this cookie to be accessed via javascript
    # so httponly is set to None

    if request.session.get_expire_at_browser_close():
        max_age = None
        expires = None
    else:
        max_age = request.session.get_expiry_age()
        expires_time = time.time() + max_age
        expires = cookie_date(expires_time)

    response.set_cookie(settings.EDXMKTG_COOKIE_NAME,
                        'true', max_age=max_age,
                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        path='/',
                        secure=None,
                        httponly=None)
    return response

def exam_registration_info(user, course):
    """ Returns a Registration object if the user is currently registered for a current
    exam of the course.  Returns None if the user is not registered, or if there is no
    current exam for the course.
    """
    exam_info = course.current_test_center_exam
    if exam_info is None:
        return None

    exam_code = exam_info.exam_series_code
    registrations = get_testcenter_registration(user, course.id, exam_code)
    if registrations:
        registration = registrations[0]
    else:
        registration = None
    return registration

@login_required
@ensure_csrf_cookie
def begin_exam_registration(request, course_id):
    """ Handles request to register the user for the current
    test center exam of the specified course.  Called by form
    in dashboard.html.
    """
    user = request.user

    try:
        course = course_from_id(course_id)
    except ItemNotFoundError:
        log.error("User {0} enrolled in non-existent course {1}".format(user.username, course_id))
        raise Http404

    # get the exam to be registered for:
    # (For now, we just assume there is one at most.)
    # if there is no exam now (because someone bookmarked this stupid page),
    # then return a 404:
    exam_info = course.current_test_center_exam
    if exam_info is None:
        raise Http404

    # determine if the user is registered for this course:
    registration = exam_registration_info(user, course)

    # we want to populate the registration page with the relevant information,
    # if it already exists.  Create an empty object otherwise.
    try:
        testcenteruser = TestCenterUser.objects.get(user=user)
    except TestCenterUser.DoesNotExist:
        testcenteruser = TestCenterUser()
        testcenteruser.user = user

    context = {'course': course,
               'user': user,
               'testcenteruser': testcenteruser,
               'registration': registration,
               'exam_info': exam_info,
               }

    return render_to_response('test_center_register.html', context)

@ensure_csrf_cookie
def create_exam_registration(request, post_override=None):
    """
    JSON call to create a test center exam registration.
    Called by form in test_center_register.html
    """
    post_vars = post_override if post_override else request.POST

    # first determine if we need to create a new TestCenterUser, or if we are making any update
    # to an existing TestCenterUser.
    username = post_vars['username']
    user = User.objects.get(username=username)
    course_id = post_vars['course_id']
    course = course_from_id(course_id)  # assume it will be found....

    # make sure that any demographic data values received from the page have been stripped.
    # Whitespace is not an acceptable response for any of these values
    demographic_data = {}
    for fieldname in TestCenterUser.user_provided_fields():
        if fieldname in post_vars:
            demographic_data[fieldname] = (post_vars[fieldname]).strip()
    try:
        testcenter_user = TestCenterUser.objects.get(user=user)
        needs_updating = testcenter_user.needs_update(demographic_data)
        log.info("User {0} enrolled in course {1} {2}updating demographic info for exam registration"
                 .format(user.username, course_id, "" if needs_updating else "not "))
    except TestCenterUser.DoesNotExist:
        # do additional initialization here:
        testcenter_user = TestCenterUser.create(user)
        needs_updating = True
        log.info("User {0} enrolled in course {1} creating demographic info for exam registration".format(user.username, course_id))

    # perform validation:
    if needs_updating:
        # first perform validation on the user information
        # using a Django Form.
        form = TestCenterUserForm(instance=testcenter_user, data=demographic_data)
        if form.is_valid():
            form.update_and_save()
        else:
            response_data = {'success': False}
            # return a list of errors...
            response_data['field_errors'] = form.errors
            response_data['non_field_errors'] = form.non_field_errors()
            return HttpResponse(json.dumps(response_data), mimetype="application/json")

    # create and save the registration:
    needs_saving = False
    exam = course.current_test_center_exam
    exam_code = exam.exam_series_code
    registrations = get_testcenter_registration(user, course_id, exam_code)
    if registrations:
        registration = registrations[0]
        # NOTE: we do not bother to check here to see if the registration has changed,
        # because at the moment there is no way for a user to change anything about their
        # registration.  They only provide an optional accommodation request once, and
        # cannot make changes to it thereafter.
        # It is possible that the exam_info content has been changed, such as the
        # scheduled exam dates, but those kinds of changes should not be handled through
        # this registration screen.

    else:
        accommodation_request = post_vars.get('accommodation_request', '')
        registration = TestCenterRegistration.create(testcenter_user, exam, accommodation_request)
        needs_saving = True
        log.info("User {0} enrolled in course {1} creating new exam registration".format(user.username, course_id))

    if needs_saving:
        # do validation of registration.  (Mainly whether an accommodation request is too long.)
        form = TestCenterRegistrationForm(instance=registration, data=post_vars)
        if form.is_valid():
            form.update_and_save()
        else:
            response_data = {'success': False}
            # return a list of errors...
            response_data['field_errors'] = form.errors
            response_data['non_field_errors'] = form.non_field_errors()
            return HttpResponse(json.dumps(response_data), mimetype="application/json")

    # only do the following if there is accommodation text to send,
    # and a destination to which to send it.
    # TODO: still need to create the accommodation email templates
#    if 'accommodation_request' in post_vars and 'TESTCENTER_ACCOMMODATION_REQUEST_EMAIL' in settings:
#        d = {'accommodation_request': post_vars['accommodation_request'] }
#
#        # composes accommodation email
#        subject = render_to_string('emails/accommodation_email_subject.txt', d)
#        # Email subject *must not* contain newlines
#        subject = ''.join(subject.splitlines())
#        message = render_to_string('emails/accommodation_email.txt', d)
#
#        try:
#            dest_addr = settings['TESTCENTER_ACCOMMODATION_REQUEST_EMAIL']
#            from_addr = user.email
#            send_mail(subject, message, from_addr, [dest_addr], fail_silently=False)
#        except:
#            log.exception(sys.exc_info())
#            response_data = {'success': False}
#            response_data['non_field_errors'] =  [ 'Could not send accommodation e-mail.', ]
#            return HttpResponse(json.dumps(response_data), mimetype="application/json")

    js = {'success': True}
    return HttpResponse(json.dumps(js), mimetype="application/json")

def auto_auth(request):
    """
    Automatically logs the user in with a generated random credentials
    This view is only accessible when
    settings.MITX_SETTINGS['AUTOMATIC_AUTH_FOR_TESTING'] is true.
    """

    def get_dummy_post_data(username, password, email, name):
        """
        Return a dictionary suitable for passing to post_vars of _do_create_account or post_override
        of create_account, with specified values.
        """
        return {'username': username,
                'email': email,
                'password': password,
                'name': name,
                'honor_code': u'true',
                'terms_of_service': u'true', }

    # generate random user credentials from a small name space (determined by settings)
    name_base = 'USER_'
    pass_base = 'PASS_'

    max_users = settings.MITX_FEATURES.get('MAX_AUTO_AUTH_USERS', 200)
    number = random.randint(1, max_users)

    # Get the params from the request to override default user attributes if specified
    qdict = request.GET

    # Use the params from the request, otherwise use these defaults
    username = qdict.get('username', name_base + str(number))
    password = qdict.get('password', pass_base + str(number))
    email = qdict.get('email', '%s_dummy_test@mitx.mit.edu' % username)
    name = qdict.get('name', '%s Test' % username)

    # if they already are a user, log in
    try:
        user = User.objects.get(username=username)
        user = authenticate(username=username, password=password, request=request)
        login(request, user)

    # else create and activate account info
    except ObjectDoesNotExist:
        post_override = get_dummy_post_data(username, password, email, name)
        create_account(request, post_override=post_override)
        request.user.is_active = True
        request.user.save()

    # return empty success
    return HttpResponse('')

@ensure_csrf_cookie
def activate_account(request, key):
    """When link in activation e-mail is clicked"""
    r = Registration.objects.filter(activation_key=key)
    if len(r) == 1:
        user_logged_in = request.user.is_authenticated()
        already_active = True
        if not r[0].user.is_active:
            r[0].activate()
            already_active = False

        # Enroll student in any pending courses he/she may have if auto_enroll flag is set
        student = User.objects.filter(id=r[0].user_id)
        if student:
            ceas = CourseEnrollmentAllowed.objects.filter(email=student[0].email)
            for cea in ceas:
                if cea.auto_enroll:
                    CourseEnrollment.enroll(student[0], cea.course_id)

        resp = render_to_response(
            "registration/activation_complete.html",
            {
                'user_logged_in': user_logged_in,
                'already_active': already_active
            }
        )
        return resp
    if len(r) == 0:
        return render_to_response(
            "registration/activation_invalid.html",
            {'csrf': csrf(request)['csrf_token']}
        )
    return HttpResponse(_("Unknown error. Please e-mail us to let us know how it happened."))

@ensure_csrf_cookie
def password_reset(request):
    """ Attempts to send a password reset e-mail. """
    if request.method != "POST":
        raise Http404

    form = PasswordResetFormNoActive(request.POST)
    if form.is_valid():

        profile = UserProfile.objects.get(user__email=request.POST.get('email'))

        if profile.subscription_status != 'Registered':
            return HttpResponse(json.dumps({'success': False,
                                'error': _("You do not have an active Pepper account. Please click <a href='{0}'>here</a> to contact Pepper Support."
                                           .format(reverse('contact_us')))}))

        form.save(use_https=request.is_secure(),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  request=request,
                  domain_override=request.get_host())

        # registration=Registration.objects.get(user_id=profile.user_id)
        # registration.activate()

        return HttpResponse(json.dumps({'success': True,
                                        'value': render_to_string('registration/password_reset_done.html', {})}))
    else:
        return HttpResponse(json.dumps({'success': False,
                                        'error': _('Invalid e-mail or user')}))

def password_reset_confirm_wrapper(
    request,
    uidb36=None,
    token=None,
):
    """ A wrapper around django.contrib.auth.views.password_reset_confirm.
        Needed because we want to set the user as active at this step.
    """
    # cribbed from django.contrib.auth.views.password_reset_confirm
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)

        if not user.is_active:
            return render_to_response("inactivate_reset_pwd.html", {})

        user.is_active = True
        user.save()
    except (ValueError, User.DoesNotExist):
        pass
    # we also want to pass settings.PLATFORM_NAME in as extra_context

    extra_context = {"platform_name": settings.PLATFORM_NAME}
    return password_reset_confirm(
        request, uidb36=uidb36, token=token, extra_context=extra_context
    )

def reactivation_email_for_user(user):
    try:
        reg = Registration.objects.get(user=user)
    except Registration.DoesNotExist:
        return HttpResponse(json.dumps({'success': False,
                                        'error': _('No inactive user with this e-mail exists')}))

    d = {'name': "%s %s" % (user.first_name, user.last_name),
         'key': reg.activation_key,
         'district': user.profile.district.name
         }

    subject = render_to_string('emails/activation_email_subject.txt', d)
    subject = ''.join(subject.splitlines())
    message = render_to_string('emails/activation_email.txt', d)

    try:
        _res = user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
    except:
        log.warning('Unable to send reactivation email', exc_info=True)
        return HttpResponse(json.dumps({'success': False, 'error': _('Unable to send reactivation email')}))

    return HttpResponse(json.dumps({'success': True}))

@ensure_csrf_cookie
def change_email_request(request):
    """ AJAX call from the profile page. User wants a new e-mail.
    """
    # Make sure it checks for existing e-mail conflicts
    if not request.user.is_authenticated:
        raise Http404

    user = request.user
    new_email = request.POST['new_email']
    try:
        validate_email(new_email)
    except ValidationError:
        return HttpResponse(json.dumps({'success': False,
                                        'error': _('Valid e-mail address required.')}))

    if User.objects.filter(email=new_email).count() != 0:
        # CRITICAL TODO: Handle case sensitivity for e-mails
        return HttpResponse(json.dumps({'success': False,
                                        'error': _('An account with this e-mail already exists.')}))

    pec_list = PendingEmailChange.objects.filter(user=request.user)
    if len(pec_list) == 0:
        pec = PendingEmailChange()
        pec.user = user
    else:
        pec = pec_list[0]

    pec.new_email = request.POST['new_email']
    pec.activation_key = uuid.uuid4().hex
    pec.save()

    if pec.new_email == user.email:
        pec.delete()
        return HttpResponse(json.dumps({'success': False,
                                        'error': _('Old email is the same as the new email.')}))

    d = {'key': pec.activation_key,
         'old_email': user.email,
         'new_email': pec.new_email}

    subject = render_to_string('emails/email_change_subject.txt', d)
    subject = ''.join(subject.splitlines())
    message = render_to_string('emails/email_change.txt', d)

    _res = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [pec.new_email])

    return HttpResponse(json.dumps({'success': True}))

@ensure_csrf_cookie
@transaction.commit_manually
def confirm_email_change(request, key):
    """ User requested a new e-mail. This is called when the activation
    link is clicked. We confirm with the old e-mail, and update
    """
    try:
        try:
            pec = PendingEmailChange.objects.get(activation_key=key)
        except PendingEmailChange.DoesNotExist:
            transaction.rollback()
            return render_to_response("invalid_email_key.html", {})

        user = pec.user
        address_context = {
            'old_email': user.email,
            'new_email': pec.new_email
        }

        if len(User.objects.filter(email=pec.new_email)) != 0:
            transaction.rollback()
            return render_to_response("email_exists.html", {})

        subject = render_to_string('emails/email_change_subject.txt', address_context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('emails/confirm_email_change.txt', address_context)
        up = UserProfile.objects.get(user=user)
        meta = up.get_meta()
        if 'old_emails' not in meta:
            meta['old_emails'] = []
        meta['old_emails'].append([user.email, datetime.datetime.now(UTC).isoformat()])
        up.set_meta(meta)
        up.save()
        # Send it to the old email...
        try:
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        except Exception:
            transaction.rollback()
            log.warning('Unable to send confirmation email to old address', exc_info=True)
            return render_to_response("email_change_failed.html", {'email': user.email})

        user.email = pec.new_email
        user.save()
        pec.delete()
        # And send it to the new email...
        try:
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        except Exception:
            transaction.rollback()
            log.warning('Unable to send confirmation email to new address', exc_info=True)
            return render_to_response("email_change_failed.html", {'email': pec.new_email})

        transaction.commit()
        return render_to_response("email_change_successful.html", address_context)
    except Exception:
        # If we get an unexpected exception, be sure to rollback the transaction
        transaction.rollback()
        raise


@ensure_csrf_cookie
def change_skype_name(request):
    user = UserProfile.objects.get(user_id=request.user.id)
    user.skype_username = request.POST['username']
    user.save()
    return HttpResponse(json.dumps({'success?': True}))

@ensure_csrf_cookie
def change_name_request(request):
    """ Log a request for a new name. """
    if not request.user.is_authenticated:
        raise Http404

    try:
        pnc = PendingNameChange.objects.get(user=request.user)
    except PendingNameChange.DoesNotExist:
        pnc = PendingNameChange()
    pnc.user = request.user
    pnc.new_first_name = request.POST['new_first_name']
    pnc.new_last_name = request.POST['new_last_name']
    pnc.rationale = request.POST['rationale']
    if len(pnc.new_first_name) < 2:
        return HttpResponse(json.dumps({'success': False, 'error': _('First Name required')}))
    if len(pnc.new_last_name) < 2:
        return HttpResponse(json.dumps({'success': False, 'error': _('Last Name required')}))

    pnc.new_name = "%s %s" % (request.POST['new_first_name'], request.POST['new_last_name'])
    pnc.save()

    # The following automatically accepts name change requests. Remove this to
    # go back to the old system where it gets queued up for admin approval.
    accept_name_change_by_id(pnc.id)

    return HttpResponse(json.dumps({'success': True}))

@ensure_csrf_cookie
def pending_name_changes(request):
    """ Web page which allows staff to approve or reject name changes. """
    if not request.user.is_staff:
        raise Http404

    changes = list(PendingNameChange.objects.all())
    js = {'students': [{'new_name': c.new_name,
                        'rationale': c.rationale,
                        'old_name': UserProfile.objects.get(user=c.user).name,
                        'email': c.user.email,
                        'uid': c.user.id,
                        'cid': c.id} for c in changes]}
    return render_to_response('name_changes.html', js)

@ensure_csrf_cookie
def reject_name_change(request):
    """ JSON: Name change process. Course staff clicks 'reject' on a given name change """
    if not request.user.is_staff:
        raise Http404

    try:
        pnc = PendingNameChange.objects.get(id=int(request.POST['id']))
    except PendingNameChange.DoesNotExist:
        return HttpResponse(json.dumps({'success': False, 'error': _('Invalid ID')}))

    pnc.delete()
    return HttpResponse(json.dumps({'success': True}))

def accept_name_change_by_id(id):
    try:
        pnc = PendingNameChange.objects.get(id=id)
    except PendingNameChange.DoesNotExist:
        return HttpResponse(json.dumps({'success': False, 'error': _('Invalid ID')}))

    u = pnc.user
    up = UserProfile.objects.get(user=u)

    # Save old name
    meta = up.get_meta()
    if 'old_names' not in meta:
        meta['old_names'] = []
    meta['old_names'].append([up.name, pnc.rationale, datetime.datetime.now(UTC).isoformat()])
    up.set_meta(meta)

    up.name = pnc.new_name
    u.first_name = pnc.new_first_name
    u.last_name = pnc.new_last_name
    u.save()
    up.save()
    pnc.delete()

    return HttpResponse(json.dumps({'success': True}))

@ensure_csrf_cookie
def accept_name_change(request):
    """ JSON: Name change process. Course staff clicks 'accept' on a given name change

    We used this during the prototype but now we simply record name changes instead
    of manually approving them. Still keeping this around in case we want to go
    back to this approval method.
    """
    if not request.user.is_staff:
        raise Http404

    return accept_name_change_by_id(int(request.POST['id']))

@require_POST
@login_required
@ensure_csrf_cookie
def change_email_settings(request):
    """Modify logged-in user's setting for receiving emails from a course."""
    user = request.user

    course_id = request.POST.get("course_id")
    receive_emails = request.POST.get("receive_emails")
    if receive_emails:
        optout_object = Optout.objects.filter(user=user, course_id=course_id)
        if optout_object:
            optout_object.delete()
        log.info(u"User {0} ({1}) opted in to receive emails from course {2}".format(user.username, user.email, course_id))
        track.views.server_track(request, "change-email-settings", {"receive_emails": "yes", "course": course_id}, page='dashboard')
    else:
        Optout.objects.get_or_create(user=user, course_id=course_id)
        log.info(u"User {0} ({1}) opted out of receiving emails from course {2}".format(user.username, user.email, course_id))
        track.views.server_track(request, "change-email-settings", {"receive_emails": "no", "course": course_id}, page='dashboard')

    return HttpResponse(json.dumps({'success': True}))

def download_certificate(request):
    return render_to_response("download_certificate.html", {})

def latest_news(request):
    return render_to_response("latest_news.html", {})

def change_school_request(request):
    up = UserProfile.objects.get(user=request.user)
    if 'school_id' in request.POST:
        up.school_id = request.POST['school_id']
    up.save()
    return HttpResponse(json.dumps({'success': True, 'school_id': up.school_id,
                                    'location': up.location}))

def change_grade_level_request(request):
    up = UserProfile.objects.get(user=request.user)
    if 'grade_level_id' in request.POST:
        up.grade_level_id = request.POST['grade_level_id']
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location}))

def change_major_subject_area_request(request):
    up = UserProfile.objects.get(user=request.user)
    if 'major_subject_area_id' in request.POST:
        up.major_subject_area_id = request.POST['major_subject_area_id']
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location}))

def change_years_in_education_request(request):
    up = UserProfile.objects.get(user=request.user)
    if 'years_in_education_id' in request.POST:
        up.years_in_education_id = request.POST['years_in_education_id']
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location}))

def change_bio_request(request):
    up = UserProfile.objects.get(user=request.user)
    if 'bio' in request.POST:
        up.bio = request.POST['bio']
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location, }))

def change_percent_lunch(request):
    up = UserProfile.objects.get(user=request.user)
    up.percent_lunch = request.POST.get("percent_lunch")
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location, }))

def change_percent_iep(request):
    up = UserProfile.objects.get(user=request.user)
    up.percent_iep = request.POST.get("percent_iep")
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location, }))

def change_percent_eng_learner(request):
    up = UserProfile.objects.get(user=request.user)
    up.percent_eng_learner = request.POST.get("percent_eng_learner")
    up.save()
    return HttpResponse(json.dumps({'success': True,
                                    'location': up.location, }))
# called by create_account()
def activate_imported_account(post_vars, photo):
    ret = {'success': False}
    try:
        registration = Registration.objects.get(activation_key=post_vars.get('activation_key', ''))
        user_id = registration.user_id

        profile = UserProfile.objects.get(user_id=user_id)
        profile.subscription_status = 'Registered'
        profile.user.first_name = post_vars.get('first_name', '')
        profile.user.last_name = post_vars.get('last_name', '')
        profile.school_id = post_vars.get('school_id', '')
        profile.grade_level_id = post_vars.get('grade_level_id', '')
        profile.major_subject_area_id = post_vars.get('major_subject_area_id', '')
        profile.years_in_education_id = post_vars.get('years_in_education_id', '')
        profile.percent_lunch = post_vars.get('percent_lunch', '')
        profile.percent_iep = post_vars.get('percent_iep', '')
        profile.percent_eng_learner = post_vars.get('percent_eng_learner', '')
        profile.bio = post_vars.get('bio', '')
        profile.activate_date = datetime.datetime.now(UTC)
        profile.save()

        ceas = CourseEnrollmentAllowed.objects.filter(email=profile.user.email)
        for cea in ceas:
            if cea.auto_enroll:
                CourseEnrollment.enroll(profile.user, cea.course_id)

        # CourseEnrollment.enroll(User.objects.get(id=user_id), 'PCG_Education/PEP101.1/S2016')

        d = {"first_name": profile.user.first_name, "last_name": profile.user.last_name, "district": profile.district.name}


        # composes activation email
        subject = render_to_string('emails/welcome_subject.txt', d)

        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('emails/welcome_body.txt', d)

        profile.user.username=post_vars.get('username','')
        profile.user.set_password(post_vars.get('password',''))

        try:
            profile.user.save()
            registration.activate()
        except Exception as e:
            if "for key 'username'" in "%s" % e:
                ret['value'] = "Username '%s' already exists" % profile.user.username
                ret['field'] = 'username'
            raise e

        upload_user_photo(profile.user.id, photo)

        # send_html_mail(subject, message, settings.SUPPORT_EMAIL,[profile.user.email])

        ret={'success': True}
    except Exception as e:
        # transaction.rollback()

        ret['success']=False
        ret['error']="%s" % e

    return HttpResponse(json.dumps(ret), content_type="application/json")

def activate_easyiep_account(request):
    vars=request.POST

    #** fetch user by activation_key
    registration=Registration.objects.get(activation_key=vars.get('activation_key',''))
    user_id=registration.user_id
    profile=UserProfile.objects.get(user_id=user_id)

    #** validate username
    try:
        validate_slug(vars['username'])
    except ValidationError:
        js = {'success': False}
        js['value'] = _("Username should only consist of A-Z and 0-9, with no spaces.")
        js['field'] = 'username'
        return HttpResponse(json.dumps(js), content_type="application/json")

    #** validate if user exists
    if User.objects.filter(username=vars['username']).exclude(email=profile.user.email).exists():
        js = {'success': False}
        js['value'] = _("An account with the Public Username '{username}' already exists.").format(username=vars['username'])
        js['field'] = 'username'
        return HttpResponse(json.dumps(js), content_type="application/json")

    #** validate fields
    required_post_vars_dropdown = [
        'first_name',
        'last_name',
        'state_id',
        'district_id',
        'school_id',
        'major_subject_area_id',
        'years_in_education_id',
        'percent_lunch', 'percent_iep', 'percent_eng_learner']
    
    for a in required_post_vars_dropdown:
        if len(vars[a]) < 1:
            error_str = {
                'first_name': 'Your first name must be a minimum of two characters long.',
                'last_name': 'Your last name must be a minimum of two characters long.',
                'state_id': 'State is required',
                'district_id': 'District is required',
                'school_id': 'School is required',
                'major_subject_area_id': 'Major Subject Area is required',
                # 'grade_level_id': 'Grade Level-Check is required',
                'years_in_education_id': 'Number of Years in Education is required',
                'percent_lunch': 'Free/Reduced Lunch is required',
                'percent_iep': 'IEPs is required',
                'percent_eng_learner': 'English Learners is required'
            }
            js = {'success': False}
            js['value'] = error_str[a]
            js['field'] = a
            return HttpResponse(json.dumps(js), content_type="application/json")

    #** validate terms_of_service
    tos_not_required = settings.MITX_FEATURES.get("AUTH_USE_SHIB") \
                       and settings.MITX_FEATURES.get('SHIB_DISABLE_TOS') \
                       and DoExternalAuth and ("shib" in eamap.external_domain)
    if not tos_not_required:
        if vars.get('terms_of_service', 'false') != u'true':
            js = {'success': False}
            js['value'] = _("You must accept the terms of service.")
            js['field'] = 'terms_of_service'
            return HttpResponse(json.dumps(js), content_type="application/json")

    try:
        #** update user
        profile.user.first_name = vars.get('first_name', '')
        profile.user.last_name = vars.get('last_name', '')
        profile.user.username = vars.get('username', '')
        profile.user.is_active = True
        profile.user.save()

        #** update profile
        profile.district_id = vars.get('district_id', '')
        profile.school_id = vars.get('school_id', '')
        profile.subscription_status = 'Registered'
        profile.major_subject_area_id = vars.get('major_subject_area_id', '')
        profile.years_in_education_id = vars.get('years_in_education_id', '')
        profile.grade_level_id = vars.get('grade_level_id', '')
        profile.percent_lunch = vars.get('percent_lunch', '')
        profile.percent_iep = vars.get('percent_iep', '')
        profile.percent_eng_learner = vars.get('percent_eng_learner', '')
        profile.bio = vars.get('bio', '')
        profile.activate_date = datetime.datetime.now(UTC)
        profile.save()

        #** upload photo
        photo=request.FILES.get("photo")
        upload_user_photo(profile.user.id, photo)
        js={'success': True}
    except Exception as e:
        transaction.rollback()
        js = {'success': False}
        js['error']="%s" % e

    #** log the user in
    profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, profile.user)

    return HttpResponse(json.dumps(js), content_type="application/json")

#@begin:change photo by Dashboard
#@date:2013-11-24
# def uploadphoto(request):
#     if request.method == 'POST':
#         up = UserProfile.objects.get(user=request.user)
#         img_name = up.photo
#         file_img = request.FILES['photo']

#         if img_name:
#             targetFile = os.path.join('/home/tahoe/edx_all/uploads/photos/', img_name)
#             if os.path.isfile(targetFile):
#                 os.remove(targetFile)

#         if file_img:
#             time_int = int(time.time()*100)
#             random_int1 = random.randint(10000,100000000)
#             random_int2 = random.randint(10000,100000000)
#             zf1 = '%d' %time_int
#             zf2 = '%d' %random_int1
#             zf3 = '%d' %random_int2
#             filename = file_img.name
#             zf4 = filename.split('.')[-1]
#             img_name = zf1 + zf2 + zf3 + '.' + zf4
#             img = Image.open(file_img)
#             img.thumbnail((110,110),Image.ANTIALIAS)
#             img.save('/home/tahoe/edx_all/uploads/photos/'+img_name)

#         up.photo = img_name
#         up.save()
#     return redirect(reverse('dashboard'))
#@end

def upload_user_photo(user_id, file_img):
    options=settings.USERSTORE.get("OPTIONS")

    us=MongoUserStore(options.get("host"),
                      options.get("db"),
                      options.get("port"),
                      options.get('user'),
                      options.get('password'))

    # img_name = up.photo
    _id={"user_id":user_id,"type":"photo"}
    if file_img:
        # mime_type = mimetypes.guess_type(image_url)[0]

        img = Image.open(file_img)
        img.thumbnail((110,110),Image.ANTIALIAS)

        file=StringIO()
        img.save(file, 'JPEG')
        file.seek(0)

        us.save(_id,file.getvalue())

def upload_photo(request):
    upload_user_photo(request.user.id,request.FILES.get('photo'))

    return redirect(reverse('dashboard'))

def user_photo(request,user_id=None):
    if not user_id:
        user_id=request.user.id
    else:
        user_id=int(user_id)

    options=settings.USERSTORE.get("OPTIONS")
    us=MongoUserStore(options.get("host"),
                      options.get("db"),
                      options.get("port"),
                      options.get('user'),
                      options.get('password'))

    content=us.find_one(user_id,'photo')

    response = HttpResponse(content_type='image/JPEG')
    if content:
        response.write(content.get("data"))
    else:
        f=open(settings.PROJECT_ROOT.dirname().dirname() + '/edx-platform/lms/static/images/photos/photo_temp.png','rb')
        response.write(f.read())
        f.close()
    return response


def request_course_access_ajax(request):
    try:
        course=get_course_by_id(request.POST.get('course_id'))
        subject="Course Access Request From "+request.META['HTTP_HOST']
        message="""User: {first_name} {last_name}
District: {district_name}
School: {school_name}
Cohort: {cohort_code}
Email: {email}
Course: {course_number} {course_name}
Request Date: {date_time}""".format(first_name=request.user.first_name,
    last_name=request.user.last_name,
    cohort_code=request.user.profile.cohort.code if request.user.profile.cohort_id else '',
    district_name=request.user.profile.district.name,
    school_name=request.user.profile.school.name,
    email=request.user.email,
    course_number=course.display_coursenumber,
    course_name=course.display_name,
    date_time=datetime.datetime.now())
    
        send_html_mail(subject, message, settings.MAIL_REQUEST_COURSE_ACCESS_RECEIVER, [
            settings.MAIL_REQUEST_COURSE_ACCESS_RECEIVER,
            # "gingerj@education2000.com",
            # "acoffman@pcgus.com",
            # "mmullen@pcgus.com",
            # "jmclaughlin@pcgus.com"
            "pnayyer@gmail.com"
        ])
    except Exception as e:
        return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    return HttpResponse(json.dumps({'success': True}))


def study_time_format(t, is_sign=False):
    sign = ''
    if t < 0 and is_sign:
        sign = '-'
        t = abs(t)
    hour_unit = ' Hour, '
    minute_unit = ' Minute'
    hour = int(t / 60 / 60)
    minute = int(t / 60 % 60)
    if hour != 1:
        hour_unit = ' Hours, '
    if minute != 1:
        minute_unit = 'Minutes'
    if hour > 0:
        hour_full = str(hour) + hour_unit
    else:
        hour_full = ''
    return ('{0}{1} {2} {3}').format(sign, hour_full, minute, minute_unit)


def drop_states(request):
    data = State.objects.all()
    data = data.order_by("name")
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r))


def drop_districts(request):
    data = District.objects.all()
    
    state_id = request.GET.get('state_id', 0)
    if not state_id:
        state_id = 0
        
    data = data.filter(state_id=int(state_id))
    data = data.order_by("name")
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r))


def drop_schools(request):
    data = School.objects.all()

    district_id = request.GET.get('district_id', 0)
    if not district_id:
        district_id = 0
    
    data = data.filter(district_id=int(district_id))
    r = list()
    data = data.order_by("name")
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r))


@login_required
def get_pepper_stats(request):
    user = User.objects.get(id=request.POST.get('user_id'))
    courses = []

    external_time = 0
    external_times = {}
    orig_external_times = {}
    total_course_times = {}
    rts = record_time_store()

    for enrollment in CourseEnrollment.enrollments_for_user(user):
        try:
            c = course_from_id(enrollment.course_id)
            c.student_enrollment_date = enrollment.created

            courses.append(c)
            if user.is_superuser:
                orig_external_times[c.id] = 0
                external_time = 0
                external_times[c.id] = 0
            else:
                orig_external_times[c.id] = rts.get_external_time(str(user.id), c.id)
                external_time += orig_external_times[c.id]
                external_times[c.id] = study_time_format(orig_external_times[c.id])

        except ItemNotFoundError:
            log.error("User {0} enrolled in non-existent course {1}"
                      .format(user.username, enrollment.course_id))

    #@begin:add pd_time to total_time
    #@date:2016-06-06
    id_of_user = request.POST.get('user_id')
    pd_time = 0;
    pd_time_tmp = PepRegStudent.objects.values('student_id').annotate(credit_sum=Sum('student_credit')).filter(student_id=id_of_user)
    if pd_time_tmp:
        pd_time = pd_time_tmp[0]['credit_sum'] * 3600
    #@end

    if user.is_superuser:
        course_times = {course.id: 100 for course in courses}
        total_course_times = {course.id: 0 for course in courses}

        course_time = 0
        discussion_time = 0
        portfolio_time = 0
        all_course_time = 0
        collaboration_time = 0
        adjustment_time_totle = 0
        total_time_in_pepper = 0
        
    else:
        course_times = {course.id: study_time_format(rts.get_aggregate_course_time(str(user.id), course.id, 'courseware') + orig_external_times[course.id]) for course in courses}
        course_time, discussion_time, portfolio_time = rts.get_stats_time(str(user.id))
        all_course_time = course_time + external_time
        collaboration_time = discussion_time + portfolio_time
        adjustment_time_totle = rts.get_adjustment_time(str(user.id), 'total', None)
        #@begin:add pd_time to total_time
        #@date:2016-06-06
        #total_time_in_pepper = all_course_time + collaboration_time + adjustment_time_totle
        total_time_in_pepper = all_course_time + collaboration_time + adjustment_time_totle + pd_time
        #@end

        #@begin:change to current year course time and total_time
        #@date:2016-06-21
        rs = reporting_store()
        rs.set_collection('UserCourseView')
        for course in courses:
            results = rs.collection.find({"user_id":request.user.id,"course_id":course.id},{"_id":0,"total_time":1})
            total_time_user = 0
            for v in results:
                total_time_user = total_time_user + v['total_time']
           
            total_course_times[course.id] = study_time_format(total_time_user) 
        #@end

    context = {
        'all_course_time': study_time_format(all_course_time),
        'collaboration_time': study_time_format(collaboration_time),
        'total_time_in_pepper': study_time_format(total_time_in_pepper),
        'course_times': course_times,
        'external_times': external_times,
        'totle_adjustment_time': study_time_format(adjustment_time_totle, True),
        'total_course_times':total_course_times
    }
    return HttpResponse(json.dumps(context), content_type="application/json")