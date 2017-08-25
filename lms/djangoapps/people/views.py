from django.http import Http404
from mitxmako.shortcuts import render_to_response
import datetime
from django.db import connection
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from student.models import CourseEnrollment, get_user_by_id, People
from django.contrib.auth.models import User
from student.feeding import dashboard_feeding_store
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

from people_in_es import gen_people_search_query, search_people, add_user_people_of, del_user_people_of

import re
from student.models import User
from xmodule.remindstore import myactivitystore, myactivitystaticstore

# import logging
# log = logging.getLogger("tracking")

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
    message = {'success': True}

    try:
        people = User.objects.get(id=request.POST.get('people_id'))
        add_user_people_of(people, request.user.id)

        user1 = User.objects.get(id=request.user.id)
        user1_id = user1.id
        user1_username = user1.username
        user2_id = people.id
        ma_db = myactivitystore()
        store = dashboard_feeding_store()
        if is_people(people, request.user.id) and is_people(request.user, request.POST.get('people_id')):
            my_activity = {"GroupType": "People", "EventType": "Both_Added_Network", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": user2_id,
                           "URLValues": {"username": people.username},
                           "TokenValues": {"user_id1": user2_id},
                           "LogoValues": {}}
            ma_db.insert_item(my_activity)
            
            content = get_my_activity_info(my_activity, "Both_Added_Network")
            store.create(type="post", user_id=long(request.user.id), content=content,receivers=[long(request.POST.get('people_id'))],date=datetime.datetime.utcnow(),is_people_add=1)
        else:
            my_activity = {"GroupType": "People", "EventType": "Add_Me_Network", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": user2_id,
                           "URLValues": {"username": user1_username},
                           "TokenValues": {"user_id1": user1_id, "user_id2": user2_id},
                           "LogoValues": {}}
            ma_db.insert_item(my_activity)

            content = get_my_activity_info(my_activity, "Add_Me_Network")
            store.create(type="post", user_id=request.user.id, content=content,receivers=[long(request.POST.get('people_id'))],date=datetime.datetime.utcnow(),is_people_add=1) 
    except Exception as e:
        message = {'success': False, 'error': "%s" % e}
        
    return HttpResponse(json.dumps(message))

def del_people(request):
    message={'success':True}
    try:
        del_user_people_of(User.objects.get(id=request.POST.get('people_id')),request.user.id)
    except Exception as e:
        message={'success':False, 'error': "%s" % e}
    return HttpResponse(json.dumps(message))

def get_pager(total,size,page,jumps):
    import math
    
    page_count=int(math.ceil(float(total)/float(size)))

    if page_count<1:page_count=1

    r={'total':total,'size':size,'page':page,'jumps':[],'pages':page_count}

    half=math.ceil(jumps/2)

    f=page-half
    t=f+jumps-1

    a=f-1
    b=page_count-t

    if b>0:b=0
    if a>0:a=0

    m=math.ceil(b-a)

    if m<>0:
        f=f+m
        t=t+m

    if f<1:f=1
    if t>page_count:t=page_count

    for i in range(int(f),int(t+1)):
        if i==page:
            r['jumps'].append("c")
        else:
            r['jumps'].append(i)

    return r

@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def people(request,course_id=''):
    total=0
    profiles=[]
    
    # check course enrollment, when user visiting course people
    if course_id:
        registered = CourseEnrollment.is_enrolled(request.user, course_id)
        if not registered:
            return redirect(reverse('cabout', args=[course_id]))

    # check loging
    if not request.user.is_authenticated():
       return redirect(reverse('signin_user'))

    # fetch page size
    size=request.GET.get('size','')
    if size.isdigit() and int(size)>0:
        size=int(size)
    else:
        size=25

    # fetch page
    page=request.GET.get('page','')
    if page.isdigit() and int(page)>0:
        page=int(page)
    else:
        page=1

    # template context    
    context={}

    # fetch course_id, default current course id
    search_course_id=request.GET.get('course_id')
    if search_course_id is None:
        search_course_id=course_id
        
    # searching
    if request.GET.get('searching'):
        cond=gen_people_search_query(
            sort={'last_login':'desc'},
            start=(page -1) * size,
            size=size,
            must_not={'_id':request.user.id,'is_superuser':1,'is_staff':1},
            must={
                'is_active':1,
                'course':search_course_id,
                'email_lower':request.GET.get('email','').lower(),
                'username_lower':request.GET.get('username','').lower(),
                'first_name_lower':request.GET.get('first_name','').lower(),
                'last_name_lower':request.GET.get('last_name','').lower(),
                'state_id':request.GET.get('state_id',''),
                'district_id':request.GET.get('district_id',''),
                'school_id':request.GET.get('school_id',''),
                'major_subject_area_id':request.GET.get('subject_area_id',''),
                'grade_level_id':request.GET.get('grade_level_id',''),
                'years_in_education_id':request.GET.get('years_in_education_id',''),
                'percent_lunch':request.GET.get('percent_lunch',''),
                'percent_iep':request.GET.get('percent_iep',''),
                'percent_eng_learner':request.GET.get('percent_eng_learner','')})

        # import logging
        # log = logging.getLogger("tracking")
        # log.debug("++++++++++")
        # log.debug(cond)
        # log.debug("++++++++++")

        profiles,total=search_people(cond)

        # gether pager params
        params=pager_params(request)

        context={
            'params':params,
            'people_search_debug':1}
    
    courses=list()
    courses=get_courses(request.user, request.META.get('HTTP_HOST'))

    # courses=sorted(courses, key=lambda course: course.number.lower())
    courses=sorted(courses, key=lambda course: course.display_name.lower())

    context['courses']=courses
    course=None
    if course_id:
        course=get_course_with_access(request.user, course_id, 'load')

    # import logging
    # log = logging.getLogger("tracking")
    # log.debug("search:%s " % get_pager(total,size,page,5))

    context['pager']=get_pager(total,size,page,5)
    context['course']=course
    context['course_id'] = course_id
    context['search_course_id'] = search_course_id
    context['profiles']=profiles

    return render_to_response('people/people.html', context)

@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def my_people(request,course_id=''):
    # check course enrollment, when user visiting course people
    if course_id:
        registered = CourseEnrollment.is_enrolled(request.user, course_id)
        if not registered:
            return redirect(reverse('cabout', args=[course_id]))

    # check loging
    if not request.user.is_authenticated():
       return redirect(reverse('signin_user'))

    # fetch page size
    size=request.GET.get('size','')
    if size.isdigit() and int(size)>0:
        size=int(size)
    else:
        size=25

    # fetch page
    page=request.GET.get('page','')
    if page.isdigit() and int(page)>0:
        page=int(page)
    else:
        page=1

    # template context    
    context={}

    # fetch course_id, default current course id
    search_course_id=request.GET.get('course_id')
    if search_course_id is None:
        search_course_id=course_id

    # searching
    cond=gen_people_search_query(
        sort={'last_login':'desc'},
        start=(page -1) * size,
        size=size,
        must_not={'_id':request.user.id,'is_superuser':1,'is_staff':1},
        must={
            'people_of':request.user.id,
            'is_active':1,
            'course':search_course_id,
            'email_lower':request.GET.get('email','').lower(),
            'username_lower':request.GET.get('username','').lower(),
            'first_name_lower':request.GET.get('first_name','').lower(),
            'last_name_lower':request.GET.get('last_name','').lower(),
            'state_id':request.GET.get('state_id',''),            
            'district_id':request.GET.get('district_id',''),
            'school_id':request.GET.get('school_id',''),
            'major_subject_area_id':request.GET.get('subject_area_id',''),
            'grade_level_id':request.GET.get('grade_level_id',''),
            'years_in_education_id':request.GET.get('years_in_education_id',''),
            'percent_lunch':request.GET.get('percent_lunch',''),
            'percent_iep':request.GET.get('percent_iep',''),
            'percent_eng_learner':request.GET.get('percent_eng_learner','')
            })

    profiles,total=search_people(cond)

    # gether pager params
    params=pager_params(request)

    context={
        'params':params,
        'people_search_debug':1}
    
    courses=list()
    courses=get_courses(request.user, request.META.get('HTTP_HOST'))
    
    courses=sorted(courses, key=lambda course: course.display_name.lower())
    
    context['courses']=courses
    course=None
    if course_id:
        course=get_course_with_access(request.user, course_id, 'load')

    context['pager']=get_pager(total,size,page,5)
    context['course']=course
    context['course_id'] = course_id
    context['search_course_id'] = search_course_id
    context['profiles']=profiles

    return render_to_response('people/my_people.html', context)

def is_people(user,owner_id):
    owner_id = str(owner_id)
    people_of = []
    if user.profile.people_of:
        people_of = user.profile.people_of.split(',')

    if owner_id not in people_of:
        return False
    else:
        return True

def get_my_activity_info(my_activity, etype):
    static_info = myactivitystaticstore().get_item_by_etype(etype)
    data = my_activity
    for data_s in static_info:
        data['URL'] = data_s['URL']
        data['Logo'] = data_s['Logo']
        data['DisplayInfo'] = data_s['DisplayInfo']
        break

    ma_dict = {}

    # URL
    ma_dict["URL"] = re.sub("{([\w ]*)}", lambda x: str(data["URLValues"].get(x.group(1))), data["URL"])

    ma_dict["DisplayInfo"] = get_displayInfo(data).replace('href=#', 'href=' + ma_dict["URL"])

    return ma_dict["DisplayInfo"]

def get_displayInfo(data):
    displayInfo_values = {}
    info_list = re.findall("{([\w |,.()'_/]*)}", data["DisplayInfo"])
    dt = {}
    for d in info_list:
        t1 = d.split(',')
        value = ''
        if t1[0] == 'mysql':
            dt = {}
            t21 = t1[1].split('|')
            t22 = t1[2].split('|')
            dt['db'] = t1[0]
            dt['models'] = t21[0]
            dt['models2'] = t21[1]
            dt['getby'] = t22[0]
            dt['key'] = data['TokenValues'][t22[1]]
            dt['key_name'] = t1[3]
            try:
                value = data['LogoValues'][dt['key_name']]
            except:
                list_key = str(dt['key']).split(',')
                _symbol = '='
                if len(list_key) > 1:
                    dt['key'] = []
                    _symbol = '__in='
                    for d in list_key:
                        dt['key'].append(int(d))
                str_get = dt['models'] + '.objects.filter(' + dt['getby'] + _symbol + str(dt['key']) + ')'
                e1 = eval(str_get)
                value = ""
                e2_list = []
                for d in e1:
                    if len(e1) == 1:
                        value = eval("d." + dt['models2'])
                    else:
                        e2 = eval("d." + dt['models2'])
                        e2_list.append(e2)
                        value = ", ".join(e2_list)
        elif t1[0] == 'mongo':
            dt = {}
            dt['db'] = t1[0]
            dt['models'] = re.sub("/([\w _]*)/", lambda x: str(data['TokenValues'].get(x.group(1))), t1[1])
            dt['models'] = dt['models'].replace('|',',')
            dt['key_name'] = t1[2]
            try:
                value = data['LogoValues'][dt['key_name']]
            except:
                try:
                    value = eval(dt['models'])
                except:
                    pass
        else:
            info = re.sub("{([\w ]*)}", lambda x: str(data["TokenValues"].get(x.group(1))), data["DisplayInfo"])
            return info
        displayInfo_values[dt['key_name']] = value
    info = replace_values(data["DisplayInfo"],displayInfo_values)
    return info

def replace_values(body, values):
    return re.sub("{[\w |,.()'_/]*,([\w ]*)}", lambda x: str(values.get(x.group(1))), body)