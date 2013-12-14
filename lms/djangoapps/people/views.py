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

def people(request,course_id=None):
    if not request.user.is_authenticated():
       return redirect(reverse('signin_user')) 
    prepage=request.GET.get('prepage','')

    if prepage.isdigit() and int(prepage)>0:
        prepage=int(prepage)
    else:
        prepage=5
        
    context={}

    course=None

    if not course_id:
        course_id=request.GET.get('course_id','')
    else:
        course=get_course_with_access(request.user, course_id, 'load')


        
    if request.GET.get('searching',''):
        f=search_user(me=request.user,
                      course_id=course_id,
                      email=request.GET.get('email',''),
                      username=request.GET.get('username',''),
                      first_name=request.GET.get('first_name',''),
                      last_name=request.GET.get('last_name',''),
                      district_id=request.GET.get('district_id',''),
                      school_id=request.GET.get('school_id',''),
                      subject_area_id=request.GET.get('subject_area_id',''),
                      grade_level_id=request.GET.get('grade_level_id',''),
                      years_in_education_id=request.GET.get('years_in_education_id',''))

        pager=JuncheePaginator(f,prepage,6)
        profiles=valid_pager(pager,request.GET.get('page'))

        params=pager_params(request)
        context={
            'profiles':profiles,
            'pager':pager,
            'params':params,
            'people_search_debug':1}
    
    courses=list()

    if not course:
        from student.views import course_from_id
        for e in CourseEnrollment.enrollments_for_user(request.user):
            try:
                c=course_from_id(e.course_id)
                courses.append(c)
            except:
                pass
        context['courses']=courses
    
    context['prepage']=prepage
    context['course']=course
    context['course_id'] = course_id


    return render_to_response('people/people.html', context)

def my_people(request,course_id=None):
    if not request.user.is_authenticated():
       return redirect(reverse('signin_user')) 
    prepage=request.GET.get('prepage','')

    course=None
    if not course_id:
        course_id=request.GET.get('course_id','')
    else:
        course=get_course_with_access(request.user, course_id, 'load')    
    
    if prepage.isdigit() and int(prepage)>0:
        prepage=int(prepage)
    else:
        prepage=5
    
    cursor = connection.cursor()
    context={'users':[]}

    people=People.objects.filter(user_id=request.user.id)

    if request.GET.get('username',''):
        people=people.filter(people__username = request.GET.get('username',''))
    if request.GET.get('first_name',''):
        people=people.filter(people__profile__first_name = request.GET.get('first_name',''))
    if request.GET.get('last_name',''):
        people=people.filter(people__profile__last_name = request.GET.get('last_name',''))        
    if course_id:
        people=people.filter(people__courseenrollment__course_id = course_id)
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

    pager=JuncheePaginator(people,prepage,6)
    people=valid_pager(pager,request.GET.get('page'))
    params=pager_params(request)
    courses=list()

    context={
        'prepage':prepage,
        'course':course,
        'people':people,
        'pager':pager,
        'params':params,
        'people_search_debug':1}

    if not course:
        from student.views import course_from_id
        for e in CourseEnrollment.enrollments_for_user(request.user):
            try:
                c=course_from_id(e.course_id)
                courses.append(c)
            except:
                pass
        context['courses']=courses

    return render_to_response('people/my_people.html', context)
