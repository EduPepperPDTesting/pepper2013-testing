from django.http import Http404
from mitxmako.shortcuts import render_to_response
from django.db import connection
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from student.models import CourseEnrollment,get_user_by_id,People
from django.contrib.auth.models import User

from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404
from people.user import search_user, JuncheePaginator

import json
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django_future.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_control

def dictfetchall(cursor):
    '''Returns a list of all rows from a cursor as a column: result dict.
    Borrowed from Django documentation'''
    desc = cursor.description
    table = []
    # table.append([col[0] for col in desc])
    
    # ensure response from db is a list, not a tuple (which is returned
    # by MySQL backed django instances)
    rows_from_cursor=cursor.fetchall()
    table = table + [list(row) for row in rows_from_cursor]
    return table

def SQL_query_to_list(cursor, query_string):
    cursor.execute(query_string)
    raw_result=dictfetchall(cursor)
    return raw_result

def course_index(request,course_id):
    course = get_course_with_access(request.user, course_id, 'load')
    return render_to_response('people/people.html', {'course':course})

def my_course_index(request,course_id):
    course = get_course_with_access(request.user, course_id, 'load')
    return render_to_response('people/my_people.html', {'course':course})

def valid_pager(paginator,page):
    try:
        page=int(page)
    except Exception:
        page=1
    if page<1: page=1
    if page>paginator.num_pages: page=paginator.num_pages
    data=paginator.page(page)
    return data

def pager_params(request):
    b=list()
    for (n,v) in request.GET.items():
        if n != 'page':
            b.append("%s=%s" % (n,v))
    return "&".join(b)

def add_people(request):
    message={'success':True}    
    try:
        p=People()
        p.user_id=request.user.id
        p.people_id=request.POST.get('people_id')
        p.save()
    except Exception as e:
        message={'success':False, 'error': "%s" % e}
    message['id']=p.id
        
    return HttpResponse(json.dumps(message))

def remove_people(request):
    message={'success':True}
    try:
        People.objects.filter(id=request.POST.get('id')).delete()
    except Exception as e:
        message={'success':False, 'error': "%s" % e}
    return HttpResponse(json.dumps(message))

@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def people(request,course_id=None):

    if not request.user.is_authenticated():
       return redirect(reverse('signin_user')) 
    prepage=request.GET.get('prepage','')

    if prepage.isdigit() and int(prepage)>0:
        prepage=int(prepage)
    else:
        prepage=25
        
    context={}
    
    search_course_id=request.GET.get('course_id')
    if search_course_id is None:
        search_course_id=course_id

    if request.GET.get('searching'):
        f=search_user(me=request.user,
            course_id=search_course_id,
            email=request.GET.get('email',''),
            username=request.GET.get('username',''),
            first_name=request.GET.get('first_name',''),
            last_name=request.GET.get('last_name',''),
            district_id=request.GET.get('district_id',''),
            school_id=request.GET.get('school_id',''),
            subject_area_id=request.GET.get('subject_area_id',''),
            grade_level_id=request.GET.get('grade_level_id',''),
            years_in_education_id=request.GET.get('years_in_education_id',''),
            percent_lunch=request.GET.get('percent_lunch',''),
            percent_iep=request.GET.get('percent_iep',''),
            percent_eng_learner=request.GET.get('percent_eng_learner',''))

        pager=JuncheePaginator(f,prepage,6)
        profiles=valid_pager(pager,request.GET.get('page'))

        params=pager_params(request)
        context={
            'profiles':profiles,
            'pager':pager,
            'params':params,
            'people_search_debug':1}
    
    courses=list()

    courses=get_courses(request.user, request.META.get('HTTP_HOST'))
    courses=sorted(courses, key=lambda course: course.number.lower())
    context['courses']=courses
    
    # === Courses of myself ===        
    # from student.views import course_from_id
    # for e in CourseEnrollment.enrollments_for_user(request.user):
    #     try:
    #         c=course_from_id(e.course_id)
    #         courses.append(c)
    #     except:
    #         pass
    # context['courses']=courses

    course=None
    if course_id:
        course=get_course_with_access(request.user, course_id, 'load')
        
    context['prepage']=prepage
    context['course']=course
    context['course_id'] = course_id
    context['search_course_id'] = search_course_id

    return render_to_response('people/people.html', context)

@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def my_people(request,course_id=None):
    if not request.user.is_authenticated():
       return redirect(reverse('signin_user')) 
    prepage=request.GET.get('prepage','')

    if prepage.isdigit() and int(prepage)>0:
        prepage=int(prepage)
    else:
        prepage=25
    
    cursor = connection.cursor()
    context={'users':[]}

    people=People.objects.filter(user_id=request.user.id)
    
    search_course_id=request.GET.get('course_id')
    if search_course_id is None:
        search_course_id=course_id

    import re

    un=request.GET.get('username','')
    if un:
        if len(un)<3:
            people=people.filter(people__username = un)
        else:
            people=people.filter(people__username__istartswith = un)

    fn=request.GET.get('first_name','') 
    if fn:
        if len(fn)<3:
            people=people.filter(people__profile__first_name = fn)
        else:
            people=people.filter(people__profile__first_name__istartswith = fn)

    ln=request.GET.get('last_name','') 
    if ln:
        if len(ln)<3:
            people=people.filter(people__profile__last_name = ln)
        else:
            people=people.filter(people__profile__last_name__istartswith = ln)

    if search_course_id:
        people=people.filter(people__courseenrollment__course_id = search_course_id, people__courseenrollment__is_active = True)
    if request.GET.get('district_id',''):
        people=people.filter(people__profile__cohort__district_id = request.GET.get('district_id',''))
    if request.GET.get('school_id',''):
        people=people.filter(people__profile__school_id = request.GET.get('school_id',''))
    if request.GET.get('subject_area_id',''):
        people=people.filter(people__profile__major_subject_area_id = request.GET.get('subject_area_id',''))
    if request.GET.get('grade_level_id',''):
        people=people.filter(people__profile__grade_level_id__regex = "(^|,)%s(,|$)" % request.GET.get('grade_level_id',''))
    if request.GET.get('years_in_education_id',''):
        people=people.filter(people__profile__years_in_education_id = request.GET.get('years_in_education_id',''))
    if request.GET.get('percent_lunch',''):
        people=people.filter(people__profile__percent_lunch = request.GET.get('percent_lunch',''))
    if request.GET.get('percent_iep',''):
        people=people.filter(people__profile__percent_iep = request.GET.get('percent_iep',''))
    if request.GET.get('percent_eng_learner',''):
        people=people.filter(people__profile__percent_eng_learner = request.GET.get('percent_eng_learner',''))

    people=people.order_by('people__profile__last_name').order_by('people__profile__first_name')

    pager=JuncheePaginator(people,prepage,6)
    people=valid_pager(pager,request.GET.get('page'))
    params=pager_params(request)
    courses=list()

    from online_status.status import status_for_user
    for p in people:
        p.people.online=not (status_for_user(User.objects.get(id=p.people.id))) is None

    course=None
    if course_id:
        course=get_course_with_access(request.user, course_id, 'load')    

    context={
        'prepage':prepage,
        'course':course,
        'course_id':course_id,
        'people':people,
        'pager':pager,
        'params':params,
        'people_search_debug':1}

    courses=get_courses(request.user, request.META.get('HTTP_HOST'))
    courses=sorted(courses, key=lambda course: course.number.lower())
    context['courses']=courses
    context['search_course_id']=search_course_id

    # === Courses of myself ===
    # from student.views import course_from_id
    # for e in CourseEnrollment.enrollments_for_user(request.user):
    #     try:
    #         c=course_from_id(e.course_id)
    #         courses.append(c)
    #     except:
    #         pass
    # context['courses']=courses

    return render_to_response('people/my_people.html', context)
