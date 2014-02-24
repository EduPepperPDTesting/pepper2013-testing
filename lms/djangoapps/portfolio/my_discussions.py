from courseware.courses import get_course_with_access
import comment_client as cc
from mitxmako.shortcuts import render_to_response
from django_comment_client.utils import (merge_dict, extract, strip_none, get_courseware_context)
import django_comment_client.utils as utils
from django.contrib.auth.models import User
import xml.sax.saxutils as saxutils
from django.http import Http404
import json
from django_comment_client.permissions import cached_has_permission
from courseware.access import has_access
escapedict = {'"': '&quot;'}
def user_discussions_profile(request, course_id, portfolio_user):
    course = get_course_with_access(portfolio_user, course_id, 'load_forum')
    try:
        profiled_user = cc.User(id=portfolio_user.id, course_id=course_id)

        query_params = {
            'page': 1,
            'per_page': 100,   # more than threads_per_page to show more activities
        }

        threads, page, num_pages = profiled_user.active_threads(query_params)
        thread_output = []
        for thread in threads:
            courseware_context = get_courseware_context(thread, course)
            if courseware_context:
                thread.update(courseware_context)
            
            if len(thread.get('tags'))>0:
                if thread.get('tags')[0]!='portfolio' and str(thread.get('courseware_url')).find('__am')<0:
                    thread_output.append(thread)
        query_params['page'] = page
        query_params['num_pages'] = num_pages
        user_info = cc.User.from_django_user(portfolio_user).to_dict()

        annotated_content_info = utils.get_metadata_for_threads(course_id, thread_output, portfolio_user, user_info)

        if request.is_ajax():
            return utils.JsonResponse({
                'discussion_data': map(utils.safe_content, thread_output),
                'page': query_params['page'],
                'num_pages': query_params['num_pages'],
                'annotated_content_info': saxutils.escape(json.dumps(annotated_content_info), escapedict),
            })
        else:
            context = {
                'course': course,
                'curr_user':portfolio_user,
                'user': request.user,
                'django_user': User.objects.get(id=portfolio_user.id),
                'profiled_user': profiled_user.to_dict(),
                'threads': saxutils.escape(json.dumps(thread_output), escapedict),
                'threads_num': len(thread_output),
                'user_info': saxutils.escape(json.dumps(user_info), escapedict),
                'annotated_content_info': saxutils.escape(json.dumps(annotated_content_info), escapedict),
                'portfolio_user':portfolio_user,
                'portfolio_user_id':portfolio_user.id,
                'roles': saxutils.escape(json.dumps(utils.get_role_ids(course_id)), escapedict),
                'flag_moderator': cached_has_permission(portfolio_user, 'openclose_thread', course.id) or has_access(portfolio_user, course, 'staff'),
            }
            
            return context
    except:
        raise Http404


    