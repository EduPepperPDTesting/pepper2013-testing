import time
import random
import os
import os.path
import logging
import urlparse
import functools

import comment_client as cc
import django_comment_client.utils as utils
import django_comment_client.settings as cc_settings


from django.core import exceptions
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators import csrf
from django.core.files.storage import get_storage_class
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from mitxmako.shortcuts import render_to_string
from courseware.courses import get_course_with_access, get_course_by_id
from course_groups.cohorts import get_cohort_id, is_commentable_cohorted

from django_comment_client.utils import JsonResponse, JsonError, extract, get_courseware_context

from django_comment_client.permissions import check_permissions_by_view, cached_has_permission
from django_comment_common.models import Role
from courseware.access import has_access
from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import capa.xqueue_interface as xqueue_interface
from django.conf import settings
from datetime import datetime
from pytz import UTC
from models import *
from xmodule.remindstore import myactivitystore

log = logging.getLogger(__name__)

s3_interface = {
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
            'secret_access_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
            'storage_bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        }

def permitted(fn):
    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        def fetch_content():
            if "thread_id" in kwargs:
                content = cc.Thread.find(kwargs["thread_id"]).to_dict()
            elif "comment_id" in kwargs:
                content = cc.Comment.find(kwargs["comment_id"]).to_dict()
            else:
                content = None
            return content
        if check_permissions_by_view(request.user, kwargs['course_id'], fetch_content(), request.view_name):
            return fn(request, *args, **kwargs)
        else:
            return JsonError("unauthorized", status=401)
    return wrapper


def ajax_content_response(request, course_id, content, template_name):
    context = {
        'course_id': course_id,
        'content': content,
    }
    html = render_to_string(template_name, context)
    user_info = cc.User.from_django_user(request.user).to_dict()
    annotated_content_info = utils.get_annotated_content_info(course_id, content, request.user, user_info)
    return JsonResponse({
        'html': html,
        'content': utils.safe_content(content),
        'annotated_content_info': annotated_content_info,
    })


@require_POST
@login_required
@permitted
def create_thread(request, course_id, commentable_id):
    """
    Given a course and commentble ID, create the thread
    """
    
    log.debug("Creating new thread in %r, id %r", course_id, commentable_id)
    course = get_course_with_access(request.user, course_id, 'load')
    post = request.POST

    if course.allow_anonymous:
        anonymous = post.get('anonymous', 'false').lower() == 'true'
    else:
        anonymous = False

    if course.allow_anonymous_to_peers:
        anonymous_to_peers = post.get('anonymous_to_peers', 'false').lower() == 'true'
    else:
        anonymous_to_peers = False

    thread = cc.Thread(**extract(post, ['body', 'title', 'tags', 'pd_plan_id']))
    thread.update_attributes(**{
        'anonymous': anonymous,
        'anonymous_to_peers': anonymous_to_peers,
        'commentable_id': commentable_id,
        'course_id': course_id,
        'user_id': request.user.id,
        'tags':'default',
    })
    
    print "============================="
    print extract(post, ['body', 'title', 'tags', 'pd_plan_id'])
    
    user = cc.User.from_django_user(request.user)

    #kevinchugh because the new requirement is that all groups will be determined
    #by the group id in the request this all goes away
    #not anymore, only for admins

    # Cohort the thread if the commentable is cohorted.
    if is_commentable_cohorted(course_id, commentable_id):
        user_group_id = get_cohort_id(user, course_id)

        # TODO (vshnayder): once we have more than just cohorts, we'll want to
        # change this to a single get_group_for_user_and_commentable function
        # that can do different things depending on the commentable_id
        if cached_has_permission(request.user, "see_all_cohorts", course_id):
            # admins can optionally choose what group to post as
            group_id = post.get('group_id', user_group_id)
        else:
            # regular users always post with their own id.
            group_id = user_group_id

        if group_id:
            thread.update_attributes(group_id=group_id)

    thread.save()

    ma_db = myactivitystore()
    my_activity = {"GroupType": "Courses", "EventType": "courses_creatediscussion", "ActivityDateTime": datetime.utcnow(), "UsrCre": request.user.id, 
    "URLValues": {"course_id": course_id, "commentable_id": thread.commentable_id, "SourceID": thread.id},    
    "TokenValues": {"SourceID": thread.id}, "LogoValues": {"course_id": course_id}}
    ma_db.insert_item(my_activity)

    courseware_context = get_courseware_context(thread, course)
    if courseware_context:
        if str(courseware_context.get('courseware_url')).find('__am')>0:
            thread.update_attributes(**{
                'tags':'aboutme',
            })
        thread.save()
    #patch for backward compatibility to comments service
    if not 'pinned' in thread.attributes:
        thread['pinned'] = False

    if post.get('auto_subscribe', 'false').lower() == 'true':
        user = cc.User.from_django_user(request.user)
        user.follow(thread)
    courseware_context = get_courseware_context(thread, course)
    data = thread.to_dict()
    if courseware_context:
        data.update(courseware_context)
    create_comment_auto(request, course_id, thread.id)
    if request.is_ajax():
        return ajax_content_response(request, course_id, data, 'discussion/ajax_create_thread.html')
    else:
        return JsonResponse(utils.safe_content(data))


@require_POST
@login_required
@permitted
def update_thread(request, course_id, thread_id):
    """
    Given a course id and thread id, update a existing thread, used for both static and ajax submissions
    """
    thread = cc.Thread.find(thread_id)
    thread.update_attributes(**extract(request.POST, ['body', 'title', 'tags']))
    thread.update_attributes(**{
        'tags':'default',
    })
   
    thread.save()
    course = get_course_with_access(request.user, course_id, 'load')
    courseware_context = get_courseware_context(thread, course)
    if courseware_context:
        if str(courseware_context.get('courseware_url')).find('__am')>0:
            thread.update_attributes(**{
                'tags':'aboutme',
            })
        thread.save()
    if request.is_ajax():
        return ajax_content_response(request, course_id, thread.to_dict(), 'discussion/ajax_update_thread.html')
    else:
        return JsonResponse(utils.safe_content(thread.to_dict()))


def _create_comment(request, course_id, thread_id=None, parent_id=None):
    """
    given a course_id, thread_id, and parent_id, create a comment,
    called from create_comment to do the actual creation
    """
    post = request.POST
    comment = cc.Comment(**extract(post, ['body']))

    course = get_course_with_access(request.user, course_id, 'load')
    if course.allow_anonymous:
        anonymous = post.get('anonymous', 'false').lower() == 'true'
    else:
        anonymous = False

    if course.allow_anonymous_to_peers:
        anonymous_to_peers = post.get('anonymous_to_peers', 'false').lower() == 'true'
    else:
        anonymous_to_peers = False

    comment.update_attributes(**{
        'anonymous': anonymous,
        'anonymous_to_peers': anonymous_to_peers,
        'user_id': request.user.id,
        'course_id': course_id,
        'thread_id': thread_id,
        'parent_id': parent_id,
    })
    comment.save()
   
    thread = cc.Thread.find(comment.thread_id)

    ma_db = myactivitystore()
    my_activity = {"GroupType": "Courses", "EventType": "courses_replydiscussion", "ActivityDateTime": datetime.utcnow(), "UsrCre": request.user.id,
    "URLValues": {"course_id": course_id, "commentable_id": thread.commentable_id, "SourceID": thread.id},    
    "TokenValues": {"SourceID": thread.id}, "LogoValues": {"course_id": course_id}}
    ma_db.insert_item(my_activity)   

    if post.get('auto_subscribe', 'false').lower() == 'true':
        user = cc.User.from_django_user(request.user)
        user.follow(comment.thread)
    if request.is_ajax():
        return ajax_content_response(request, course_id, comment.to_dict(), 'discussion/ajax_create_comment.html')
    else:
        return JsonResponse(utils.safe_content(comment.to_dict()))

@require_POST
def create_comment_auto(request, course_id, thread_id=None, parent_id=None):
    """
    given a course_id, thread_id, and parent_id, create a comment,
    called from create_comment to do the actual creation
    """
    #post = request.POST
    comment_data={"body":"Let's discuss!"}
    comment = cc.Comment(**extract(comment_data, ['body']))
    
    course = get_course_with_access(request.user, course_id, 'load')
    '''
    if course.allow_anonymous:
        anonymous = post.get('anonymous', 'false').lower() == 'true'
    else:
        anonymous = False

    if course.allow_anonymous_to_peers:
        anonymous_to_peers = post.get('anonymous_to_peers', 'false').lower() == 'true'
    else:
        anonymous_to_peers = False
    '''
    anonymous = False
    anonymous_to_peers = False
    comment.update_attributes(**{
        'anonymous': anonymous,
        'anonymous_to_peers': anonymous_to_peers,
        'user_id': request.user.id,
        'course_id': course_id,
        'thread_id': thread_id,
        'parent_id': parent_id,
    })
    comment.save()
    '''
    if post.get('auto_subscribe', 'false').lower() == 'true':
        user = cc.User.from_django_user(request.user)
        user.follow(comment.thread)
    '''
    user = cc.User.from_django_user(request.user)
    user.follow(comment.thread)

def create_comment_auto_load(request, course_id, thread_id=None, thread_user=None, parent_id=None):
    """
    given a course_id, thread_id, and parent_id, create a comment,
    called from create_comment to do the actual creation
    """
    comment_data={"body":"Let's discuss!"}
    comment = cc.Comment(**extract(comment_data, ['body']))
    
    course = get_course_with_access(thread_user, course_id, 'load')

    anonymous = False
    anonymous_to_peers = False
    comment.update_attributes(**{
        'anonymous': anonymous,
        'anonymous_to_peers': anonymous_to_peers,
        'user_id': thread_user.id,
        'course_id': course_id,
        'thread_id': thread_id,
        'parent_id': parent_id,
    })
    comment.save()
    user = cc.User.from_django_user(thread_user)
    user.follow(comment.thread)

@require_POST
@login_required
@permitted
def create_comment(request, course_id, thread_id):
    """
    given a course_id and thread_id, test for comment depth. if not too deep,
    call _create_comment to create the actual comment.
    """
    if cc_settings.MAX_COMMENT_DEPTH is not None:
        if cc_settings.MAX_COMMENT_DEPTH < 0:
            return JsonError("Comment level too deep")
    return _create_comment(request, course_id, thread_id=thread_id)


@require_POST
@login_required
@permitted
def delete_thread(request, course_id, thread_id):
    """
    given a course_id and thread_id, delete this thread
    this is ajax only
    """
    thread = cc.Thread.find(thread_id)
    thread.delete()
    return JsonResponse(utils.safe_content(thread.to_dict()))


@require_POST
@login_required
@permitted
def update_comment(request, course_id, comment_id):
    """
    given a course_id and comment_id, update the comment with payload attributes
    handles static and ajax submissions
    """
    comment = cc.Comment.find(comment_id)
    comment.update_attributes(**extract(request.POST, ['body']))
    comment.save()
    if request.is_ajax():
        return ajax_content_response(request, course_id, comment.to_dict(), 'discussion/ajax_update_comment.html')
    else:
        return JsonResponse(utils.safe_content(comment.to_dict()))


@require_POST
@login_required
@permitted
def endorse_comment(request, course_id, comment_id):
    """
    given a course_id and comment_id, toggle the endorsement of this comment,
    ajax only
    """
    comment = cc.Comment.find(comment_id)
    comment.endorsed = request.POST.get('endorsed', 'false').lower() == 'true'
    comment.save()
    return JsonResponse(utils.safe_content(comment.to_dict()))


@require_POST
@login_required
@permitted
def openclose_thread(request, course_id, thread_id):
    """
    given a course_id and thread_id, toggle the status of this thread
    ajax only
    """
    thread = cc.Thread.find(thread_id)
    thread.closed = request.POST.get('closed', 'false').lower() == 'true'
    thread.save()
    thread = thread.to_dict()
    return JsonResponse({
        'content': utils.safe_content(thread),
        'ability': utils.get_ability(course_id, thread, request.user),
    })


@require_POST
@login_required
def create_sub_comment(request, course_id, comment_id):
    """
    given a course_id and comment_id, create a response to a comment
    after checking the max depth allowed, if allowed
    """
    if cc_settings.MAX_COMMENT_DEPTH is not None:
        if cc_settings.MAX_COMMENT_DEPTH <= cc.Comment.find(comment_id).depth:
            return JsonError("Comment level too deep")
    return _create_comment(request, course_id, parent_id=comment_id)


@require_POST
@login_required
@permitted
def delete_comment(request, course_id, comment_id):
    """
    given a course_id and comment_id delete this comment
    ajax only
    """
    comment = cc.Comment.find(comment_id)
    comment.delete()
    return JsonResponse(utils.safe_content(comment.to_dict()))


@login_required
def admin_delete_comment(request, course_id, comment_id):
    """
    given a course_id and comment_id delete this comment
    ajax only
    """
    comment = cc.Comment.find(comment_id)
    comment.delete()
    return JsonResponse(utils.safe_content(comment.to_dict()))
    
@login_required
def admin_delete_discussion(request, course_id, discussion_id):
    course_location = course_id.split('/')
    location=Location('i4x://'+course_location[0]+'/'+course_location[1]+'/discussion/'+discussion_id)
    if modulestore().has_item(course_id,location)==True:
        modulestore().delete_item(location)
    return JsonResponse({})

@require_POST
@login_required
@permitted
def vote_for_comment(request, course_id, comment_id, value):
    """
    given a course_id and comment_id,
    """
    user = cc.User.from_django_user(request.user)
    comment = cc.Comment.find(comment_id)
    user.vote(comment, value)
    return JsonResponse(utils.safe_content(comment.to_dict()))


@require_POST
@login_required
@permitted
def undo_vote_for_comment(request, course_id, comment_id):
    """
    given a course id and comment id, remove vote
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    comment = cc.Comment.find(comment_id)
    user.unvote(comment)
    return JsonResponse(utils.safe_content(comment.to_dict()))


@require_POST
@login_required
@permitted
def vote_for_thread(request, course_id, thread_id, value):
    """
    given a course id and thread id vote for this thread
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    user.vote(thread, value)
    return JsonResponse(utils.safe_content(thread.to_dict()))


@require_POST
@login_required
@permitted
def flag_abuse_for_thread(request, course_id, thread_id):
    """
    given a course_id and thread_id flag this thread for abuse
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    thread.flagAbuse(user, thread)
    return JsonResponse(utils.safe_content(thread.to_dict()))


@require_POST
@login_required
@permitted
def un_flag_abuse_for_thread(request, course_id, thread_id):
    """
    given a course id and thread id, remove abuse flag for this thread
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    course = get_course_by_id(course_id)
    thread = cc.Thread.find(thread_id)
    removeAll = cached_has_permission(request.user, 'openclose_thread', course_id) or has_access(request.user, course, 'staff')
    thread.unFlagAbuse(user, thread, removeAll)
    return JsonResponse(utils.safe_content(thread.to_dict()))


@require_POST
@login_required
@permitted
def flag_abuse_for_comment(request, course_id, comment_id):
    """
    given a course and comment id, flag comment for abuse
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    comment = cc.Comment.find(comment_id)
    comment.flagAbuse(user, comment)
    return JsonResponse(utils.safe_content(comment.to_dict()))


@require_POST
@login_required
@permitted
def un_flag_abuse_for_comment(request, course_id, comment_id):
    """
    given a course_id and comment id, unflag comment for abuse
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    course = get_course_by_id(course_id)
    removeAll = cached_has_permission(request.user, 'openclose_thread', course_id) or has_access(request.user, course, 'staff')
    comment = cc.Comment.find(comment_id)
    comment.unFlagAbuse(user, comment, removeAll)
    return JsonResponse(utils.safe_content(comment.to_dict()))


@require_POST
@login_required
@permitted
def undo_vote_for_thread(request, course_id, thread_id):
    """
    given a course id and thread id, remove users vote for thread
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    user.unvote(thread)
    return JsonResponse(utils.safe_content(thread.to_dict()))


@require_POST
@login_required
@permitted
def pin_thread(request, course_id, thread_id):
    """
    given a course id and thread id, pin this thread
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    thread.pin(user, thread_id)
    return JsonResponse(utils.safe_content(thread.to_dict()))


def un_pin_thread(request, course_id, thread_id):
    """
    given a course id and thread id, remove pin from this thread
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    thread.un_pin(user, thread_id)
    return JsonResponse(utils.safe_content(thread.to_dict()))


@require_POST
@login_required
@permitted
def follow_thread(request, course_id, thread_id):
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    user.follow(thread)

    ma_db = myactivitystore()
    my_activity = {"GroupType": "Courses", "EventType": "courses_followdiscussion", "ActivityDateTime": datetime.utcnow(), "UsrCre": request.user.id, 
    "URLValues": {"course_id": course_id, "commentable_id": thread.commentable_id, "SourceID": thread.id},    
    "TokenValues": {"SourceID": thread.id, "course_id": course_id}, "LogoValues": {"course_id": course_id}}
    ma_db.insert_item(my_activity)

    return JsonResponse({})


@require_POST
@login_required
@permitted
def follow_commentable(request, course_id, commentable_id):
    """
    given a course_id and commentable id, follow this commentable
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    commentable = cc.Commentable.find(commentable_id)
    user.follow(commentable)
    return JsonResponse({})


@require_POST
@login_required
@permitted
def follow_user(request, course_id, followed_user_id):
    user = cc.User.from_django_user(request.user)
    followed_user = cc.User.find(followed_user_id)
    user.follow(followed_user)
    return JsonResponse({})


@require_POST
@login_required
@permitted
def unfollow_thread(request, course_id, thread_id):
    """
    given a course id and thread id, stop following this thread
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    thread = cc.Thread.find(thread_id)
    user.unfollow(thread)
    return JsonResponse({})


@require_POST
@login_required
@permitted
def unfollow_commentable(request, course_id, commentable_id):
    """
    given a course id and commentable id stop following commentable
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    commentable = cc.Commentable.find(commentable_id)
    user.unfollow(commentable)
    return JsonResponse({})


@require_POST
@login_required
@permitted
def unfollow_user(request, course_id, followed_user_id):
    """
    given a course id and user id, stop following this user
    ajax only
    """
    user = cc.User.from_django_user(request.user)
    followed_user = cc.User.find(followed_user_id)
    user.unfollow(followed_user)
    return JsonResponse({})


@require_POST
@login_required
@permitted
def update_moderator_status(request, course_id, user_id):
    """
    given a course id and user id, check if the user has moderator
    and send back a user profile
    """
    is_moderator = request.POST.get('is_moderator', '').lower()
    if is_moderator not in ["true", "false"]:
        return JsonError("Must provide is_moderator as boolean value")
    is_moderator = is_moderator == "true"
    user = User.objects.get(id=user_id)
    role = Role.objects.get(course_id=course_id, name="Moderator")
    if is_moderator:
        user.roles.add(role)
    else:
        user.roles.remove(role)
    if request.is_ajax():
        course = get_course_with_access(request.user, course_id, 'load')
        discussion_user = cc.User(id=user_id, course_id=course_id)
        context = {
            'course': course,
            'course_id': course_id,
            'user': request.user,
            'django_user': user,
            'profiled_user': discussion_user.to_dict(),
        }
        return JsonResponse({
            'html': render_to_string('discussion/ajax_user_profile.html', context)
        })
    else:
        return JsonResponse({})


@require_GET
def search_similar_threads(request, course_id, commentable_id):
    """
    given a course id and commentable id, run query given in text get param
    of request
    """
    text = request.GET.get('text', None)
    if text:
        query_params = {
            'text': text,
            'commentable_id': commentable_id,
        }
        threads = cc.search_similar_threads(course_id, recursive=False, query_params=query_params)
    else:
        theads = []
    context = {'threads': map(utils.extend_content, threads)}
    return JsonResponse({
        'html': render_to_string('discussion/_similar_posts.html', context)
    })


@require_GET
def tags_autocomplete(request, course_id):
    value = request.GET.get('q', None)
    results = []
    if value:
        results = cc.tags_autocomplete(value)
    return JsonResponse(results)

'''
@require_POST
@login_required
@csrf.csrf_exempt
def upload(request, course_id):  # ajax upload file to a question or answer
    """view that handles file upload via Ajax
    """

    # check upload permission
    result = ''
    error = ''
    new_file_name = ''
    try:
        # TODO authorization
        #may raise exceptions.PermissionDenied
        #if request.user.is_anonymous():
        #    msg = _('Sorry, anonymous users cannot upload files')
        #    raise exceptions.PermissionDenied(msg)

        #request.user.assert_can_upload_file()

        # check file type
        f = request.FILES['file-upload']
        file_extension = os.path.splitext(f.name)[1].lower()
        if not file_extension in cc_settings.ALLOWED_UPLOAD_FILE_TYPES:
            file_types = "', '".join(cc_settings.ALLOWED_UPLOAD_FILE_TYPES)
            msg = _("allowed file types are '%(file_types)s'") % \
                {'file_types': file_types}
            raise exceptions.PermissionDenied(msg)

        # generate new file name
        new_file_name = str(time.time()).replace('.', str(random.randint(0, 100000))) + file_extension

        file_storage = get_storage_class()()
        # use default storage to store file
        file_storage.save(new_file_name, f)
        # check file size
        # byte
        size = file_storage.size(new_file_name)
        if size > cc_settings.MAX_UPLOAD_FILE_SIZE:
            file_storage.delete(new_file_name)
            msg = _("maximum upload file size is %(file_size)sK") % \
                {'file_size': cc_settings.MAX_UPLOAD_FILE_SIZE}
            raise exceptions.PermissionDenied(msg)

    except exceptions.PermissionDenied, err:
        error = unicode(err)
    except Exception, err:
        print err
        logging.critical(unicode(err))
        error = _('Error uploading file. Please contact the site administrator. Thank you.')

    if error == '':
        result = 'Good'
        file_url = file_storage.url(new_file_name)
        parsed_url = urlparse.urlparse(file_url)
        file_url = urlparse.urlunparse(
            urlparse.ParseResult(
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                '', '', ''
            )
        )
    else:
        result = ''
        file_url = ''

    return JsonResponse({
        'result': {
            'msg': result,
            'error': error,
            'file_url': file_url,
        }
    })
'''
@require_POST
@login_required
@csrf.csrf_exempt
def upload(request, course_id):  # ajax upload file to a question or answer
    """view that handles file upload via Ajax
    """
    result = 'Good'
    error = ''
    try:
        fd = request.FILES['file-upload']
        index=fd.name.rfind(".")
        extensions_name=fd.name[index+1:] 
        main_name=fd.name[0:index] 
        #fname = fd.name.split(".")
        file_key = main_name +"_"+datetime.now(UTC).strftime(
            xqueue_interface.dateformat
        )+"."+extensions_name

        fd.seek(0)
        s3_public_url = upload_to_s3(
            fd, file_key, s3_interface
        )
    except Exception:
        result = ''
        error = unicode(err)
    return utils.JsonResponse({
        'result': {
            'msg': result,
            'error': error,
            'file_url': s3_public_url,
        }
    })
def upload_to_s3(file_to_upload, keyname, s3_interface):

    conn = S3Connection(s3_interface['access_key'], s3_interface['secret_access_key'])
    bucketname = str(s3_interface['storage_bucket_name'])
    bucket = conn.create_bucket(bucketname.lower())

    k = Key(bucket)
    k.key = 'openended/'+keyname
    k.set_metadata('filename', file_to_upload.name)
    k.set_contents_from_file(file_to_upload)

    k.set_acl("public-read")
    public_url = k.generate_url(60 * 60 * 24 * 1825) # URL timeout in seconds.

    return public_url

#@begin:add get and set discussion rating
#@date:2016-06-29
@require_POST
@login_required
#@permitted
def set_rating(request, course_id, thread_id):
    userid = str(request.user.id)
    post_param = extract(request.POST, ['rating', 'option_type'])

    discussion_rating = discussion_rating_store()
    discussion_rating.set_rating(thread_id, userid, post_param['rating'])
  
    thread = cc.Thread.find(thread_id)

    ma_db = myactivitystore()
    my_activity = {"GroupType": "Courses", "EventType": "courses_ratediscussion", "ActivityDateTime": datetime.utcnow(), "UsrCre": request.user.id, 
    "URLValues": {"course_id": course_id, "commentable_id": thread.commentable_id, "SourceID": thread.id},
    "TokenValues": {"SourceID": thread.id, "course_id": course_id}, "LogoValues": {"course_id": course_id}}
    ma_db.insert_item(my_activity)

    return JsonResponse({})

@require_POST
@login_required
#@permitted
def get_rating(request, course_id, thread_id):
    userid = str(request.user.id)
    ratingDict = extract(request.POST, ['option_type']) #dict
    ratingDict['rating'] = '0'
    ratingDict['avg_rating'] = '0'
    ratingDict['avg_rating_count'] = '0'

    discussion_rating = discussion_rating_store()

    if ratingDict['option_type'] == 'get_rating':
        try:
            rating = discussion_rating.get_rating(thread_id, userid)['rating']
            if(rating):
                ratingDict['rating'] = rating
        except Exception as e:
            pass    
    elif ratingDict['option_type'] == 'get_avg_rating':
        try:
            avg_rating = discussion_rating.get_avg_rating(thread_id, userid)
            avg_rating_count = avg_rating.count()
            if(avg_rating_count > 0):
                rating_temp = 0
                for value in avg_rating:
                    log.debug(float(value['rating']))
                    rating_temp = rating_temp + float(value['rating'])
                ratingDict['avg_rating'] = str(rating_temp/avg_rating_count)
                ratingDict['avg_rating_count'] = avg_rating_count
        except Exception as e:
            pass  
    return JsonResponse(ratingDict)
#@end
