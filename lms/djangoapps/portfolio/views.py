from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)
from mitxmako.shortcuts import render_to_response
from django.conf import settings
from courseware.module_render import toc_for_course, get_module_for_descriptor
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django_future.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_control
from portfolio_utils import get_module_combinedopenended, get_chaper_for_course
from my_discussions import get_module_discussions
from django.contrib.auth.models import User
from about_me import create_discussion_about_me
def get_portfolio_user(request,user_id=None):
    if request.user.id == user_id or user_id==None:
        if request.GET.get('pf_id') != None:
            return User.objects.get(id=request.GET.get('pf_id'))
        else:
            return request.user
    else:
        return User.objects.get(id=user_id)

def about_me(request,course_id, user_id=None):
    portfolio_user = get_portfolio_user(request, user_id)
    course = get_course_with_access(portfolio_user, course_id, 'load')
    content = create_discussion_about_me(request, course, portfolio_user)
    return render_to_response('portfolio/about_me.html', {'course':course,'content':content,'portfolio_user_id':portfolio_user.id,'portfolio_user':portfolio_user})

@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def journal_and_reflections(request,course_id, user_id, chapter_id=''):
    portfolio_user = get_portfolio_user(request,user_id)
    course = get_course_with_access(portfolio_user, course_id, 'load')
    content=[]
    chapters = get_chaper_for_course(request,course,chapter_id,portfolio_user)
    if chapter_id != '':
        content = get_module_combinedopenended(request,course,chapter_id,portfolio_user)
    return render_to_response('portfolio/journal_and_reflections.html', {'course':course, 'csrf': csrf(request)['csrf_token'],
        'content':content,'portfolio_user_id':portfolio_user.id,'portfolio_user':portfolio_user,'chapters':chapters,'chapter_id':chapter_id,'xqa_server': settings.MITX_FEATURES.get('USE_XQA_SERVER', 'http://xqa:server@content-qa.mitx.mit.edu/xqa')})

def uploads(request,course_id):
    course = get_course_with_access(request.user, course_id, 'load')
    content = get_module_combinedopenended(request,course,course_id,"True")
    return render_to_response('portfolio/uploads.html', {'course':course, 'csrf': csrf(request)['csrf_token'],
        'content':content,'xqa_server': settings.MITX_FEATURES.get('USE_XQA_SERVER', 'http://xqa:server@content-qa.mitx.mit.edu/xqa')})

def my_discussions(request,course_id,user_id):
    portfolio_user = get_portfolio_user(request,user_id)
    course = get_course_with_access(portfolio_user, course_id, 'load')
    content=[]
    content = get_module_discussions(request,course,portfolio_user)
    return render_to_response('portfolio/my_discussions.html', {'course':course,'content':content,'portfolio_user_id':portfolio_user.id})

