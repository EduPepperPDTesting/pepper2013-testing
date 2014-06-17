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
from my_discussions import user_discussions_profile
from django.contrib.auth.models import User
from about_me import create_discussion_about_me
from django.core.paginator import Paginator, InvalidPage, EmptyPage
def get_portfolio_user(request,user_id=None):
    if request.user.id == user_id or user_id==None:
        if request.GET.get('pf_id') != None:
            return User.objects.get(id=request.GET.get('pf_id'))
        else:
            return request.user
    else:
        return User.objects.get(id=user_id)
        
@login_required
def about_me(request,course_id, user_id=None):
    portfolio_user = get_portfolio_user(request, user_id)
    course = get_course_with_access(portfolio_user, course_id, 'load')
    content = create_discussion_about_me(request, course, portfolio_user)
    return render_to_response('portfolio/about_me.html', {'curr_user':portfolio_user,'course':course,'content':content,'portfolio_user_id':portfolio_user.id,'portfolio_user':portfolio_user})

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
    paginator = Paginator(content, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        contacts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('portfolio/journal_and_reflections.html', {'curr_user':portfolio_user,'course':course, 'csrf': csrf(request)['csrf_token'],
        'content':contacts,'portfolio_user_id':portfolio_user.id,'portfolio_user':portfolio_user,'chapters':chapters,'chapter_id':chapter_id,'xqa_server': settings.MITX_FEATURES.get('USE_XQA_SERVER', 'http://xqa:server@content-qa.mitx.mit.edu/xqa')})

def uploads(request,course_id):
    course = get_course_with_access(request.user, course_id, 'load')
    content = get_module_combinedopenended(request,course,course_id,"True")
    return render_to_response('portfolio/uploads.html', {'course':course, 'csrf': csrf(request)['csrf_token'],
        'content':content,'xqa_server': settings.MITX_FEATURES.get('USE_XQA_SERVER', 'http://xqa:server@content-qa.mitx.mit.edu/xqa')})

@login_required
def my_discussions(request,course_id,user_id):
    portfolio_user = get_portfolio_user(request,user_id)
    course = get_course_with_access(portfolio_user, course_id, 'load')
    content=[]
    context = user_discussions_profile(request,course_id,portfolio_user)
    return render_to_response('portfolio/my_discussions.html', context)

