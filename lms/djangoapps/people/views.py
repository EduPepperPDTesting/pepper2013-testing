from django.http import Http404
from mitxmako.shortcuts import render_to_response
from django.db import connection

from student.models import CourseEnrollment,get_user_by_id
from django.contrib.auth.models import User

from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404
from people.user import search_user, JuncheePaginator

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


def people(request):
    # people searching
    f=search_user(course_id=request.GET.get('course_id',''),
                         email=request.GET.get('email',''),
                         username=request.GET.get('username',''),
                         first_name=request.GET.get('first_name',''),
                         last_name=request.GET.get('last_name',''),
                         district_id=request.GET.get('district_id',''),
                         school_id=request.GET.get('school_id',''),
                         subject_area_id=request.GET.get('subject_area_id',''),
                         grade_level_id=request.GET.get('grade_level_id',''),
                         years_in_education_id=request.GET.get('years_in_education_id',''))
    
    pager=JuncheePaginator(f,5,6)
    profiles=valid_pager(pager,request.GET.get('page'))
    params=pager_params(request)

    return render_to_response('people/people.html', {
        'profiles':profiles,
        'pager':pager,
        'params':params,
        'people_search_debug':1})

def my_people(request):
    # from modle
    # people=CourseEnrollment.objects.filter(is_active=1, course_id =course_id)
    cursor = connection.cursor()
    context={'users':[]}

    sql = """
    select distinct user_id from student_courseenrollment
where course_id in (select course_id from student_courseenrollment
where is_active=1 and user_id='{user_id}')""".format(user_id=request.user.id)

    # add the result for each of the table_queries to the results object

    cursor.execute(sql)
    user_ids = dictfetchall(cursor)
    for row in user_ids:
        try:
            u,up=get_user_by_id(row[0])
            up.email=u.email
            context['users'].append(up)

        except Exception,e:
            pass

    # p = Paginator(context['users'], 10)
    # add the result for each of the table_queries to the results object
    # cursor.execute(sql)
    # user_ids = dictfetchall(cursor)
    # for row in user_ids:
    #     u,up=get_user_by_id(row[0])
    #     context['users'].append(up)
        
    return render_to_response('people/my_people.html', context)

