import logging
import urllib

from functools import partial

from django.conf import settings
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from mitxmako.shortcuts import render_to_response, render_to_string
from django_future.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_control
from markupsafe import escape

from courseware import grades
from courseware.access import has_access
from courseware.courses import (get_courses, get_course_with_access,get_course_by_id,
                                get_courses_by_university, sort_by_announcement, sort_by_custom)
import courseware.tabs as tabs
from courseware.masquerade import setup_masquerade
from courseware.model_data import FieldDataCache
from .module_render import toc_for_course, get_module_for_descriptor, get_module
from courseware.models import StudentModule, StudentModuleHistory
from course_modes.models import CourseMode

from django_comment_client.utils import get_discussion_title

from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State
from util.cache import cache, cache_if_anonymous
from xmodule.modulestore import Location
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import InvalidLocationError, ItemNotFoundError, NoPathToItem
from xmodule.modulestore.search import path_to_location
from xmodule.course_module import CourseDescriptor

import comment_client
import json
import pymongo
log = logging.getLogger("mitx.courseware")
template_imports = {'urllib': urllib}
#log = logging.getLogger("tracking") 

def user_groups(user):
    """
    TODO (vshnayder): This is not used. When we have a new plan for groups, adjust appropriately.
    """
    if not user.is_authenticated():
        return []

    # TODO: Rewrite in Django
    key = 'user_group_names_{user.id}'.format(user=user)
    cache_expiration = 60 * 60  # one hour

    # Kill caching on dev machines -- we switch groups a lot
    group_names = cache.get(key)
    if settings.DEBUG:
        group_names = None

    if group_names is None:
        group_names = [u.name for u in UserTestGroup.objects.filter(users=user)]
        cache.set(key, group_names, cache_expiration)

    return group_names


@ensure_csrf_cookie
@cache_if_anonymous
def courses(request):
    """
    Render "find courses" page.  The course selection work is done in courseware.courses.
    """
    courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    courses = sort_by_custom(courses)
    extitles = []
    exurl = []
    titles = ['Mathematics','English Language Arts', 'Science', 'Special Education' ,'Writing and Poetry', 'Leadership', 'English Language Learners', "Pepper's Online Workshops", "Visual & Perfoming Arts", 'Digital Citizenship', "Teacher ToolKit", "State Content Collections", "District Content Collections"]
    for tmp in courses:
        if tmp.create_toplevel_title:
            if (tmp.create_toplevel_title not in titles) and (tmp.create_toplevel_title not in extitles):
                extitles.append(tmp.create_toplevel_title)
                exurl.append(tmp.create_toplevel_title.strip().replace(' ','%20'))

    state_list, district_list, all_state, all_district = get_state_and_district_list(request, courses)
    #20160324 modify
    #begin
    state_key_list, district_key_list = get_state_and_district_list_users(request)
    #end
    collections = get_collection_num()
    return render_to_response("courseware/courses.html", {
                              "courses": courses,
                              "states": state_list,
                              "districts": district_list,
                              "states_keys": state_key_list,
                              "districts_keys": district_key_list,
                              "collections": collections,
                              "extitles":extitles,
                              "exurl":exurl,
                              "link": True})


def is_all(course, type):
    if type == 'collection':
        if 'All' in course.content_collections:
            return True
    elif type == 'state':
        if 'All' in course.display_state:
            return True
    elif type == 'district':
        if 'All' in course.display_district:
            return True
    return False


def get_all_state_and_district(courses):
    state = []
    district = []
    for course in courses:
        if is_all(course, 'state') is False:
            state.extend(course.display_state)

        if is_all(course, 'district') is False:
            district.extend(course.display_district)
    return state, district


def get_state_and_district_list(request, courses):
    state_temp = []
    state_list = []
    district_name = {}
    district_temp = []
    district_list = []
    all_state = []
    all_district = []

    if request.user.is_authenticated():
        for course in courses:

            if is_all(course, 'state') is False:
                all_state.extend(course.display_state)

            if is_all(course, 'district') is False:
                all_district.extend(course.display_district)

            if request.user.is_superuser is False:

                if request.user.profile.district.state.name in course.display_state:
                    state_temp.append(request.user.profile.district.state.name)

                if request.user.profile.district.code in course.display_district:
                    district = District.objects.filter(code=request.user.profile.district.code)[0]
                    district_temp.append(request.user.profile.district.code)
                    district_name[request.user.profile.district.code] = district.name
            else:
                if len(course.display_state) > 0 and is_all(course, 'state') is False:
                    state_temp.extend(course.display_state)

                if len(course.display_district) > 0 and is_all(course, 'district') is False:
                    districts = District.objects.filter(code__in=course.display_district)
                    district_temp.extend(course.display_district)
                    for district in districts:
                        district_name[district.code] = district.name

        all_state = list(set(all_state))
        all_district = list(set(all_district))
        state_list = sorted(set(state_temp), key=lambda x: x[0])
        district_temp = sorted(set(district_temp), key=lambda x: x[0])
        for dl in district_temp:
            district_list.append({'id': dl, 'name': district_name[dl]})

    return state_list, district_list, all_state, all_district

#20160324 add get state and district of normal user
#begin
def get_state_and_district_list_users(request):
    state_temp = []
    state_list = []
    district_name = {}
    district_id = []
    district_list = []

    if request.user.is_authenticated():
        if request.user.is_superuser is False:
            state_temp.append(request.user.profile.district.state.name)

            district = District.objects.filter(code=request.user.profile.district.code)[0]
            district_id.append(request.user.profile.district.code)
            district_name[request.user.profile.district.code] = district.name
        if state_temp:
            state_list = sorted(set(state_temp), key=lambda x: x[0])
        if district_id:
            district_id = sorted(set(district_id), key=lambda x: x[0])
            for dl in district_id:
                district_list.append({'id': dl, 'name': district_name[dl]})
        
    return state_list, district_list
#end

#20160324 add
#begin
def drop_districts(request):
    data=District.objects.all()
    state_id_byname = '-1'
    if request.GET.get('state_name'):
        if(request.GET.get('state_name') != '__NONE__'):
            state_id_byname = State.objects.get(name=request.GET.get('state_name')).id  
        data=data.filter(state_id=state_id_byname)
    data=data.order_by("name")
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name,"code":item.code})
    return HttpResponse(json.dumps(r))
#end

def is_state_district_show(user, course, is_member):
    if user.is_authenticated():
        if user.is_superuser:
            return True
        else:
            if course.state_district_only:
                state = user.profile.district.state.name
                district = user.profile.district.code
                if state in course.display_state or district in course.display_district:
                    return True

                if (is_all(course, 'state') and is_member['state']) or (is_all(course, 'district') and is_member['district']):
                    return True
            else:
                return True
    else:
        if len(course.display_state) == 0 and len(course.display_district) == 0:
            return True
    return False


def custom_collection_visibility(user, course, collection):
    if user.is_authenticated():
        if user.is_superuser:
            return True
        else:
            if course.custom_collection_only:
                # TODO: test whether the user is allowed to see this collection here. If they are allowed, return True.
                pass
            else:
                return True
    else:
        if len(course.content_collections) == 0:
            return True
    return False


# 20151203 add for dpicourses
# begin
@ensure_csrf_cookie
@cache_if_anonymous
def newgroup_courses(request):
    """
    Render "find courses" page.  The course selection work is done in courseware.courses.
    """
    courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    # courses = sort_by_announcement(courses)
    courses = sort_by_custom(courses)

    return render_to_response("courseware/dpicourses.html", {'courses': courses, 'link': True})
# end


def course_filter(course, subject_index, currSubject, g_courses, currGrades, more_subjects_courses):
    #@begin:change the type of display_subject to list 
    #@date:2016-05-31
    # 20151130 modify the courses shown in different course grade after press All button
    # begin
    if not course.close_course or course.close_course and course.keep_in_directory:
        if course.display_grades == 'K-5':
            if len(course.display_subject) > 1:
                more_subjects_courses[0].append(course)
            else:
                if course.display_subject != currSubject[0]:
                    currSubject[0] = course.display_subject
                    subject_index[0] += 1
                    g_courses[0].append([])
                g_courses[0][subject_index[0]].append(course)
        if (course.display_grades == '6-8' or course.display_grades == '6-12') and currGrades != '9-12':
            if len(course.display_subject) > 1:
                more_subjects_courses[1].append(course)
            else:
                if course.display_subject != currSubject[1]:
                    currSubject[1] = course.display_subject
                    subject_index[1] += 1
                    g_courses[1].append([])
                g_courses[1][subject_index[1]].append(course)
        if (course.display_grades == '9-12' or course.display_grades == '6-12') and currGrades != '6-8':
            if len(course.display_subject) > 1:
                more_subjects_courses[2].append(course)
            else:
                if course.display_subject != currSubject[2]:
                    currSubject[2] = course.display_subject
                    subject_index[2] += 1
                    g_courses[2].append([])
                g_courses[2][subject_index[2]].append(course)
        if course.display_grades == 'K-12':
            if len(course.display_subject) > 1:
                more_subjects_courses[3].append(course)
            else:
                if course.display_subject != currSubject[3]:
                    currSubject[3] = course.display_subject
                    subject_index[3] += 1
                    g_courses[3].append([])
                g_courses[3][subject_index[3]].append(course)
        # end

        # 20160322 add "Add new grade 'PreK-3'"
        # begin
        if course.display_grades == 'PreK-3':
            if len(course.display_subject) > 1:
                more_subjects_courses[4].append(course)
            else:
                if course.display_subject != currSubject[4]:
                    currSubject[4] = course.display_subject
                    subject_index[4] += 1
                    g_courses[4].append([])
                g_courses[4][subject_index[4]].append(course)
    #@end
    '''
    # 20151130 modify the courses shown in different course grade after press All button
    # begin
    if course.display_grades == 'K-5':
        if course.display_subject != currSubject[0]:
            currSubject[0] = course.display_subject
            subject_index[0] += 1
            g_courses[0].append([])
        g_courses[0][subject_index[0]].append(course)
    if (course.display_grades == '6-8' or course.display_grades == '6-12') and currGrades != '9-12':
        if course.display_subject != currSubject[1]:
            currSubject[1] = course.display_subject
            subject_index[1] += 1
            g_courses[1].append([])
        g_courses[1][subject_index[1]].append(course)
    if (course.display_grades == '9-12' or course.display_grades == '6-12') and currGrades != '6-8':
        if course.display_subject != currSubject[2]:
            currSubject[2] = course.display_subject
            subject_index[2] += 1
            g_courses[2].append([])
        g_courses[2][subject_index[2]].append(course)
    if course.display_grades == 'K-12':
        if course.display_subject != currSubject[3]:
            currSubject[3] = course.display_subject
            subject_index[3] += 1
            g_courses[3].append([])
        g_courses[3][subject_index[3]].append(course)
    # end

    # 20160322 add "Add new grade 'PreK-3'"
    # begin
    if course.display_grades == 'PreK-3':
        if course.display_subject != currSubject[4]:
            currSubject[4] = course.display_subject
            subject_index[4] += 1
            g_courses[4].append([])
        g_courses[4][subject_index[4]].append(course)
    # end
    '''

#@begin:Add dpicourse_filter just for dpicourses
#@date:2016-10-27
def dpicourse_filter(course, subject_index, currSubject, g_courses, currGrades):
    # 20151130 modify the courses shown in different course grade after press All button
    # begin
    if course.display_grades == 'K-5':
        if course.display_subject != currSubject[0]:
            currSubject[0] = course.display_subject
            subject_index[0] += 1
            g_courses[0].append([])
        g_courses[0][subject_index[0]].append(course)
    if (course.display_grades == '6-8' or course.display_grades == '6-12') and currGrades != '9-12':
        if course.display_subject != currSubject[1]:
            currSubject[1] = course.display_subject
            subject_index[1] += 1
            g_courses[1].append([])
        g_courses[1][subject_index[1]].append(course)
    if (course.display_grades == '9-12' or course.display_grades == '6-12') and currGrades != '6-8':
        if course.display_subject != currSubject[2]:
            currSubject[2] = course.display_subject
            subject_index[2] += 1
            g_courses[2].append([])
        g_courses[2][subject_index[2]].append(course)
    if course.display_grades == 'K-12':
        if course.display_subject != currSubject[3]:
            currSubject[3] = course.display_subject
            subject_index[3] += 1
            g_courses[3].append([])
        g_courses[3][subject_index[3]].append(course)
    # end

    # 20160322 add "Add new grade 'PreK-3'"
    # begin
    if course.display_grades == 'PreK-3':
        if course.display_subject != currSubject[4]:
            currSubject[4] = course.display_subject
            subject_index[4] += 1
            g_courses[4].append([])
        g_courses[4][subject_index[4]].append(course)
    # end
# end

@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def course_list(request):
    """
    Render "find courses" page.  The course selection work is done in courseware.courses.
    """
    subject_id = request.GET.get('subject_id', 'all')
    grade_id = request.GET.get('grade_id', 'all')
    author_id = request.GET.get('author_id', 'all')
    district = request.GET.get('district', '') #id
    state = request.GET.get('state', '') #name
    collection = request.GET.get('collection', '')
    credit = request.GET.get('credit', '')
    is_new = request.GET.get('is_new', '')
    district_id = request.GET.get('district', '') #search keyword get from client
    state_id = request.GET.get('state', '') #it's name,not id.search keyword get from client,not id
    origin_page = request.GET.get('origin', '')
    toplevel_title = request.GET.get('toplevel_title', '')

    all_courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    state_list, district_list, all_state, all_district = get_state_and_district_list(request, all_courses)
    state_key_list, district_key_list = get_state_and_district_list_users(request) #use for 'select option' 

    is_member = {'state': False, 'district': False}

    filterDic = {'_id.category': 'course'}
    if toplevel_title:
        filterDic['metadata.create_toplevel_title'] = toplevel_title
        
    if subject_id != 'all':
        filterDic['metadata.display_subject'] = subject_id

    if grade_id != 'all':
        if grade_id == '6-8' or grade_id == '9-12':
            filterDic['metadata.display_grades'] = {'$in': [grade_id, '6-12']}
        else:
            filterDic['metadata.display_grades'] = grade_id

    if author_id != 'all':
        filterDic['metadata.display_organization'] = author_id

    if origin_page == 'courses':
        if district_id != '' and district_id != '__NONE__':
            if district in all_district:
                is_member['district'] = True
                filterDic['metadata.display_district'] = {'$in': [district, 'All']}
            else:
                filterDic['metadata.display_district'] = district
        elif state_id != '' and state_id != '__NONE__':
            #state = State.objects.get(id=state_id).name
            if state in all_state:
                is_member['state'] = True
                filterDic['metadata.display_state'] = {'$in': [state, 'All']}
            else:
                filterDic['metadata.display_state'] = state
    else:
        if district != '':
            if district in all_district:
                is_member['district'] = True
                filterDic['metadata.display_district'] = {'$in': [district, 'All']}
            else:
                filterDic['metadata.display_district'] = district
        if state != '':
            if state in all_state:
                is_member['state'] = True
               
                filterDic['metadata.display_state'] = {'$in': [state, 'All']}
            else:
                filterDic['metadata.display_state'] = state

    if collection != '':
        filterDic['metadata.content_collections'] = {'$in': [collection, 'All']}

    if credit != '':
        filterDic['metadata.display_credit'] = True

    items = modulestore().collection.find(filterDic).sort("metadata.display_subject.0", pymongo.ASCENDING)
    courses = modulestore()._load_items(list(items), 0)
    # 20160322 modify "Add new grade 'PreK-3'"
    # begin
    subject_index = [-1, -1, -1, -1, -1]
    currSubject = ["", "", "", "", ""]
    g_courses = [[], [], [], [], []]
    # end 

    #@begin:change the type of display_subject to list 
    #@date:2016-05-31
    more_subjects_courses = [[], [], [], [], []]
    #@end

    for course in courses:
        if (is_new == '' or course.is_newish) and is_state_district_show(request.user, course, is_member) and \
                custom_collection_visibility(request.user, course, collection):
            #@begin:change the type of display_subject to list 
            #@date:2016-05-31
            #course_filter(course, subject_index, currSubject, g_courses, grade_id)
            course_filter(course, subject_index, currSubject, g_courses, grade_id, more_subjects_courses)
            #@end

    #@begin:add the course which subject more than 1 to g_courses 
    #@date:2016-05-31
    if subject_id == 'all':
        for i in range(0,len(more_subjects_courses)):
            if len(more_subjects_courses[i]) > 0:
                g_courses[i].append(more_subjects_courses[i])
    else:
        for i in range(0,len(more_subjects_courses)):
            if len(more_subjects_courses[i]) > 0:
                if len(g_courses[i]) > 0:
                    for n in range(0,len(more_subjects_courses[i])):
                        g_courses[i][0].append(more_subjects_courses[i][n])
    #@end
    

    for gc in g_courses:
        for sc in gc:
            sc.sort(key=lambda x: x.display_coursenumber)
    return render_to_response("courseware/courses.html", {
                              "courses": g_courses,
                              "states": state_list,
                              "districts": district_list,
                              "states_keys": state_key_list,
                              "districts_keys": district_key_list})


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def dpicourse_list(request):
    """
    Render "find courses" page.  The course selection work is done in courseware.courses.
    """
    subject_id = request.GET.get('subject_id', '')
    grade_id = request.GET.get('grade_id', '')
    author_id = request.GET.get('author_id', '')
    district = request.GET.get('district', '')
    state = request.GET.get('state', '')
    credit = request.GET.get('credit', '')
    is_new = request.GET.get('is_new', '')
    
    filterDic = {'_id.category': 'course'}
    if subject_id != 'all':
        filterDic['metadata.display_subject'] = subject_id

    if grade_id != 'all':
        if grade_id == '6-8' or grade_id == '9-12':
            filterDic['metadata.display_grades'] = {'$in': [grade_id, '6-12']}
        else:
            filterDic['metadata.display_grades'] = grade_id

    if author_id != 'all':
        filterDic['metadata.display_organization'] = author_id

    if district != '':
        filterDic['metadata.display_district'] = district

    if state != '':
        filterDic['metadata.display_state'] = state

    if credit != '':
        filterDic['metadata.display_credit'] = True

    items = modulestore().collection.find(filterDic).sort("metadata.display_subject", pymongo.ASCENDING)
    courses = modulestore()._load_items(list(items), 0)

    subject_index = [-1, -1, -1, -1, -1]
    currSubject = ["", "", "", "", ""]
    g_courses = [[], [], [], [], []]
    
    if is_new != '':
        for course in courses:
            if course.is_newish:
                dpicourse_filter(course, subject_index, currSubject, g_courses, grade_id)
    else:
        for course in courses:
            dpicourse_filter(course, subject_index, currSubject, g_courses, grade_id)
    for gc in g_courses:
        for sc in gc:
            sc.sort(key=lambda x: x.display_coursenumber)
    return render_to_response("courseware/dpicourses.html", {'courses': g_courses})


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def states(request):
    """
    Render "find states" page.
    """
    state = request.GET.get('state', '')
    filterDic = {'_id.category': 'course'}
    state_list = []
    if request.user.is_superuser is False:
        filterDic['metadata.display_state'] = state
    items = modulestore().collection.find(filterDic)
    courses = modulestore()._load_items(list(items), 0)
    state_temp = []
    for course in courses:
        if len(course.display_state) > 0 and is_all(course, 'state') is False:
            if request.user.is_superuser is False:
                state_temp.append(state)
            else:
                state_temp.extend(course.display_state)
    state_temp = sorted(set(state_temp), key=lambda x: x[0])
    for sl in state_temp:
        state_list.append({'id': sl, 'name': sl})
    return render_to_response("courseware/collections.html", {'page_title': 'State',
                                                              'collection_type': 'state',
                                                              'items': state_list})


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def districts(request):
    """
    Render "find districts" page.
    """
    district = request.GET.get('district', '')
    filterDic = {'_id.category': 'course'}

    district_name = {}
    district_temp = []
    district_list = []

    if request.user.is_superuser is False:
        filterDic['metadata.display_district'] = district
    items = modulestore().collection.find(filterDic)
    courses = modulestore()._load_items(list(items), 0)
    for course in courses:
        if len(course.display_district) > 0 and is_all(course, 'district') is False:
            if request.user.is_superuser is False:
                district = filterDic['metadata.display_district']
                districts = District.objects.filter(code=district)
                district_temp.append(district)
            else:
                districts = District.objects.filter(code__in=course.display_district)
                district_temp.extend(course.display_district)

            for district in districts:
                district_name[district.code] = district.name
    district_temp = sorted(set(district_temp), key=lambda x: x[0])
    for dl in district_temp:
        district_list.append({'id': dl, 'name': district_name[dl]})
    return render_to_response("courseware/collections.html", {'page_title': 'District',
                                                              'collection_type': 'district',
                                                              'items': district_list})


def get_collection_num():
    filterDic = {'_id.category': 'course', 'metadata.content_collections': {'$exists': True}}
    items = modulestore().collection.find(filterDic)
    return len(list(items))


def get_collection_course_num(user, collection):
    filterDic = {'_id.category': 'course'}
    if collection != '':
        filterDic['metadata.content_collections'] = {'$in': [collection, 'All']}
    items = modulestore().collection.find(filterDic).sort("metadata.display_subject", pymongo.ASCENDING)
    courses = modulestore()._load_items(list(items), 0)

    course_count = 0
    for course in courses:
        if custom_collection_visibility(user, course, collection):
            course_count += 1

    return course_count


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def collections(request):
    """
    Render "find collections" page.
    """
    collection = request.GET.get('collection', '')
    filterDic = {'_id.category': 'course'}

    collection_temp = []
    collection_list = []

    filterDic['metadata.content_collections'] = {'$exists': True}
    if collection != '':
        filterDic['metadata.content_collections'] = {'$in': [collection, 'All']}
    items = modulestore().collection.find(filterDic)
    courses = modulestore()._load_items(list(items), 0)

    superuser = request.user.is_superuser
    for course in courses:
        if len(course.content_collections) > 0:
            collection_temp = list(set(collection_temp) | set(course.content_collections))

    collection_temp = sorted(set(collection_temp), key=lambda x: x[0])
    for cl in collection_temp:
        collection_list.append({'id': cl, 'name': cl})
    return render_to_response("courseware/collections.html", {'page_title': 'Leadership',
                                                              'collection_type': 'collection',
                                                              'items': collection_list})


def render_accordion(request, course, chapter, section, field_data_cache):
    """
    Draws navigation bar. Takes current position in accordion as
    parameter.

    If chapter and section are '' or None, renders a default accordion.

    course, chapter, and section are the url_names.

    Returns the html string
    """

    # grab the table of contents
    user = User.objects.prefetch_related("groups").get(id=request.user.id)
    request.user = user  # keep just one instance of User
    toc = toc_for_course(user, request, course, chapter, section, field_data_cache)

    context = dict([('toc', toc),
                    ('course_id', course.id),
                    ('csrf', csrf(request)['csrf_token']),
                    ('show_timezone', course.show_timezone)] + template_imports.items())
    return render_to_string('courseware/accordion.html', context)


def get_current_child(xmodule):
    """
    Get the xmodule.position's display item of an xmodule that has a position and
    children.  If xmodule has no position or is out of bounds, return the first child.
    Returns None only if there are no children at all.
    """
    if not hasattr(xmodule, 'position'):
        return None

    if xmodule.position is None:
        pos = 0
    else:
        # position is 1-indexed.
        pos = xmodule.position - 1

    children = xmodule.get_display_items()
    if 0 <= pos < len(children):
        child = children[pos]
    elif len(children) > 0:
        # Something is wrong.  Default to first child
        child = children[0]
    else:
        child = None
    return child


def redirect_to_course_position(course_module):
    """
    Return a redirect to the user's current place in the course.

    If this is the user's first time, redirects to COURSE/CHAPTER/SECTION.
    If this isn't the users's first time, redirects to COURSE/CHAPTER,
    and the view will find the current section and display a message
    about reusing the stored position.

    If there is no current position in the course or chapter, then selects
    the first child.

    """
    urlargs = {'course_id': course_module.descriptor.id}
    chapter = get_current_child(course_module)
    if chapter is None:
        # oops.  Something bad has happened.
        raise Http404("No chapter found when loading current position in course")

    urlargs['chapter'] = chapter.url_name
    if course_module.position is not None:
        return redirect(reverse('courseware_chapter', kwargs=urlargs))

    # Relying on default of returning first child
    section = get_current_child(chapter)
    if section is None:
        raise Http404("No section found when loading current position in course")

    urlargs['section'] = section.url_name
    return redirect(reverse('courseware_section', kwargs=urlargs))


def save_child_position(seq_module, child_name):
    """
    child_name: url_name of the child
    """
    for position, c in enumerate(seq_module.get_display_items(), start=1):
        if c.url_name == child_name:
            # Only save if position changed
            if position != seq_module.position:
                seq_module.position = position
    # Save this new position to the underlying KeyValueStore
    seq_module.save()


def check_for_active_timelimit_module(request, course_id, course):
    """
    Looks for a timing module for the given user and course that is currently active.
    If found, returns a context dict with timer-related values to enable display of time remaining.
    """
    context = {}

    # TODO (cpennington): Once we can query the course structure, replace this with such a query
    timelimit_student_modules = StudentModule.objects.filter(student=request.user, course_id=course_id, module_type='timelimit')
    if timelimit_student_modules:
        for timelimit_student_module in timelimit_student_modules:
            # get the corresponding section_descriptor for the given StudentModel entry:
            module_state_key = timelimit_student_module.module_state_key
            timelimit_descriptor = modulestore().get_instance(course_id, Location(module_state_key))
            timelimit_module_cache = FieldDataCache.cache_for_descriptor_descendents(course.id, request.user,
                                                                                     timelimit_descriptor, depth=None)
            timelimit_module = get_module_for_descriptor(request.user, request, timelimit_descriptor,
                                                         timelimit_module_cache, course.id, position=None)
            if timelimit_module is not None and timelimit_module.category == 'timelimit' and \
                    timelimit_module.has_begun and not timelimit_module.has_ended:
                location = timelimit_module.location
                # determine where to go when the timer expires:
                if timelimit_descriptor.time_expired_redirect_url is None:
                    raise Http404("no time_expired_redirect_url specified at this location: {} ".format(timelimit_module.location))
                context['time_expired_redirect_url'] = timelimit_descriptor.time_expired_redirect_url
                # Fetch the remaining time relative to the end time as stored in the module when it was started.
                # This value should be in milliseconds.
                remaining_time = timelimit_module.get_remaining_time_in_ms()
                context['timer_expiration_duration'] = remaining_time
                context['suppress_toplevel_navigation'] = timelimit_descriptor.suppress_toplevel_navigation
                return_url = reverse('jump_to', kwargs={'course_id': course_id, 'location': location})
                context['timer_navigation_return_url'] = return_url
    return context


def update_timelimit_module(user, course_id, field_data_cache, timelimit_descriptor, timelimit_module):
    """
    Updates the state of the provided timing module, starting it if it hasn't begun.
    Returns dict with timer-related values to enable display of time remaining.
    Returns 'timer_expiration_duration' in dict if timer is still active, and not if timer has expired.
    """
    context = {}
    # determine where to go when the exam ends:
    if timelimit_descriptor.time_expired_redirect_url is None:
        raise Http404("No time_expired_redirect_url specified at this location: {} ".format(timelimit_module.location))
    context['time_expired_redirect_url'] = timelimit_descriptor.time_expired_redirect_url

    if not timelimit_module.has_ended:
        if not timelimit_module.has_begun:
            # user has not started the exam, so start it now.
            if timelimit_descriptor.duration is None:
                raise Http404("No duration specified at this location: {} ".format(timelimit_module.location))
            # The user may have an accommodation that has been granted to them.
            # This accommodation information should already be stored in the module's state.
            timelimit_module.begin(timelimit_descriptor.duration)

        # the exam has been started, either because the student is returning to the
        # exam page, or because they have just visited it.  Fetch the remaining time relative to the
        # end time as stored in the module when it was started.
        context['timer_expiration_duration'] = timelimit_module.get_remaining_time_in_ms()
        # also use the timed module to determine whether top-level navigation is visible:
        context['suppress_toplevel_navigation'] = timelimit_descriptor.suppress_toplevel_navigation
    return context


def chat_settings(course, user):
    """
    Returns a dict containing the settings required to connect to a
    Jabber chat server and room.
    """
    domain = getattr(settings, "JABBER_DOMAIN", None)
    if domain is None:
        log.warning('You must set JABBER_DOMAIN in the settings to '
                    'enable the chat widget')
        return None

    return {
        'domain': domain,

        # Jabber doesn't like slashes, so replace with dashes
        'room': "{ID}_class".format(ID=course.id.replace('/', '-')),

        'username': "{USER}@{DOMAIN}".format(
            USER=user.username, DOMAIN=domain
        ),

        # TODO: clearly this needs to be something other than the username
        #       should also be something that's not necessarily tied to a
        #       particular course
        'password': "{USER}@{DOMAIN}".format(
            USER=user.username, DOMAIN=domain
        ),
    }


@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index(request, course_id, chapter=None, section=None,
          position=None):
    """
    Displays courseware accordion and associated content.  If course, chapter,
    and section are all specified, renders the page, or returns an error if they
    are invalid.

    If section is not specified, displays the accordion opened to the right chapter.

    If neither chapter or section are specified, redirects to user's most recent
    chapter, or the first chapter if this is the user's first visit.

    Arguments:

     - request    : HTTP request
     - course_id  : course id (str: ORG/course/URL_NAME)
     - chapter    : chapter url_name (str)
     - section    : section url_name (str)
     - position   : position in module, eg of <sequential> module (str)

    Returns:

     - HTTPresponse
    """

    user = User.objects.prefetch_related("groups").get(id=request.user.id)
    request.user = user # keep just one instance of User
    course = get_course_with_access(user, course_id, 'load', depth=2)
    staff_access = has_access(user, course, 'staff')
    registered = registered_for_course(course, user)
    if not registered:
        # TODO (vshnayder): do course instructors need to be registered to see course?
        log.debug('User %s tried to view course %s but is not enrolled' % (user, course.location.url()))
        return redirect(reverse('cabout', args=[course.id]))

    masq = setup_masquerade(request, staff_access)

    try:
        field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
            course.id, user, course, depth=2)

        course_module = get_module_for_descriptor(user, request, course, field_data_cache, course.id)
        if course_module is None:
            log.warning('If you see this, something went wrong: if we got this'
                        ' far, should have gotten a course module for this user')
            return redirect(reverse('about_course', args=[course.id]))

        if chapter is None:
            return redirect_to_course_position(course_module)

        context = {
            'csrf': csrf(request)['csrf_token'],
            'accordion': render_accordion(request, course, chapter, section, field_data_cache),
            'COURSE_TITLE': course.display_name_with_default,
            'course': course,
            'init': '',
            'content': '',
            'staff_access': staff_access,
            'masquerade': masq,
            'xqa_server': settings.MITX_FEATURES.get('USE_XQA_SERVER', 'http://xqa:server@content-qa.mitx.mit.edu/xqa'),
#@begin:Inform the template that it is in homepage
#@date:2013-11-02        
            'is_index':'True'
#@end                        
            }

        # Only show the chat if it's enabled by the course and in the
        # settings.
        show_chat = course.show_chat and settings.MITX_FEATURES['ENABLE_CHAT']
        if show_chat:
            context['chat'] = chat_settings(course, user)
            # If we couldn't load the chat settings, then don't show
            # the widget in the courseware.
            if context['chat'] is None:
                show_chat = False

        context['show_chat'] = show_chat

        chapter_descriptor = course.get_child_by(lambda m: m.url_name == chapter)
        if chapter_descriptor is not None:
            save_child_position(course_module, chapter)
        else:
            raise Http404('No chapter descriptor found with name {}'.format(chapter))

        chapter_module = course_module.get_child_by(lambda m: m.url_name == chapter)
        if chapter_module is None:
            # User may be trying to access a chapter that isn't live yet
            if masq=='student':  # if staff is masquerading as student be kinder, don't 404
                log.debug('staff masq as student: no chapter %s' % chapter)
                return redirect(reverse('courseware', args=[course.id]))
            raise Http404

        if section is not None:
            section_descriptor = chapter_descriptor.get_child_by(lambda m: m.url_name == section)
            if section_descriptor is None:
                # Specifically asked-for section doesn't exist
                if masq=='student':  # if staff is masquerading as student be kinder, don't 404
                    log.debug('staff masq as student: no section %s' % section)
                    return redirect(reverse('courseware', args=[course.id]))
                raise Http404

            # cdodge: this looks silly, but let's refetch the section_descriptor with depth=None
            # which will prefetch the children more efficiently than doing a recursive load
            section_descriptor = modulestore().get_instance(course.id, section_descriptor.location, depth=None)

            # Load all descendants of the section, because we're going to display its
            # html, which in general will need all of its children
            section_field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
                course_id, user, section_descriptor, depth=None)
            section_module = get_module(request.user, request,
                                section_descriptor.location,
                                section_field_data_cache, course_id, position, depth=None)

            if section_module is None:
                # User may be trying to be clever and access something
                # they don't have access to.
                raise Http404

            # Save where we are in the chapter
            save_child_position(chapter_module, section)

            # check here if this section *is* a timed module.
            if section_module.category == 'timelimit':
                timer_context = update_timelimit_module(user, course_id, student_module_cache,
                                                        section_descriptor, section_module)
                if 'timer_expiration_duration' in timer_context:
                    context.update(timer_context)
                else:
                    # if there is no expiration defined, then we know the timer has expired:
                    return HttpResponseRedirect(timer_context['time_expired_redirect_url'])
            else:
                # check here if this page is within a course that has an active timed module running.  If so, then
                # add in the appropriate timer information to the rendering context:
                context.update(check_for_active_timelimit_module(request, course_id, course))

            context['content'] = section_module.runtime.render(section_module, None, 'student_view').content
        else:
            # section is none, so display a message
            prev_section = get_current_child(chapter_module)
            if prev_section is None:
                # Something went wrong -- perhaps this chapter has no sections visible to the user
                raise Http404
            prev_section_url = reverse('courseware_section', kwargs={'course_id': course_id,
                                                                     'chapter': chapter_descriptor.url_name,
                                                                     'section': prev_section.url_name})
            context['content'] = render_to_string('courseware/welcome-back.html',
                                                  {'course': course,
                                                   'chapter_module': chapter_module,
                                                   'prev_section': prev_section,
                                                   'prev_section_url': prev_section_url})

        result = render_to_response('courseware/courseware.html', context)
    except Exception as e:
        if isinstance(e, Http404):
            # let it propagate
            raise

        # In production, don't want to let a 500 out for any reason
        if settings.DEBUG:
            raise
        else:
            log.exception("Error in index view: user={user}, course={course},"
                          " chapter={chapter} section={section}"
                          "position={position}".format(
                              user=user,
                              course=course,
                              chapter=chapter,
                              section=section,
                              position=position
                              ))
            try:
                result = render_to_response('courseware/courseware-error.html',
                                            {'staff_access': staff_access,
                                            'course': course})
            except:
                # Let the exception propagate, relying on global config to at
                # at least return a nice error message
                log.exception("Error while rendering courseware-error page")
                raise

    return result


@ensure_csrf_cookie
def jump_to_id(request, course_id, module_id):
    """
    This entry point allows for a shorter version of a jump to where just the id of the element is
    passed in. This assumes that id is unique within the course_id namespace
    """

    course_location = CourseDescriptor.id_to_location(course_id)

    items = modulestore().get_items(
        ['i4x', course_location.org, course_location.course, None, module_id],
        course_id=course_id
    )

    if len(items) == 0:
        raise Http404("Could not find id = {0} in course_id = {1}. Referer = {2}".
                      format(module_id, course_id, request.META.get("HTTP_REFERER", "")))
    if len(items) > 1:
        log.warning("Multiple items found with id = {0} in course_id = {1}. Referer = {2}. Using first found {3}...".
                    format(module_id, course_id, request.META.get("HTTP_REFERER", ""), items[0].location.url()))

    return jump_to(request, course_id, items[0].location.url())


@ensure_csrf_cookie
def jump_to(request, course_id, location):
    """
    Show the page that contains a specific location.

    If the location is invalid or not in any class, return a 404.

    Otherwise, delegates to the index view to figure out whether this user
    has access, and what they should see.
    """
    # Complain if the location isn't valid
    try:
        location = Location(location)
    except InvalidLocationError:
        raise Http404("Invalid location")

    # Complain if there's not data for this location
    try:
        (course_id, chapter, section, position) = path_to_location(modulestore(), course_id, location)
    except ItemNotFoundError:
        raise Http404("No data at this location: {0}".format(location))
    except NoPathToItem:
        raise Http404("This location is not in any class: {0}".format(location))

    # choose the appropriate view (and provide the necessary args) based on the
    # args provided by the redirect.
    # Rely on index to do all error handling and access control.
    if chapter is None:
        return redirect('courseware', course_id=course_id)
    elif section is None:
        return redirect('courseware_chapter', course_id=course_id, chapter=chapter)
    elif position is None:
        return redirect('courseware_section', course_id=course_id, chapter=chapter, section=section)
    else:
        return redirect('courseware_position', course_id=course_id, chapter=chapter, section=section, position=position)


@ensure_csrf_cookie
def course_info(request, course_id):
    """
    Display the course's info.html, or 404 if there is no such course.

    Assumes the course_id is in a valid format.
    """
    course = get_course_with_access(request.user, course_id, 'load')
    staff_access = has_access(request.user, course, 'staff')
    masq = setup_masquerade(request, staff_access)    # allow staff to toggle masquerade on info page

    return render_to_response('courseware/info.html', {'request': request, 'course_id': course_id, 'cache': None,
            'course': course, 'staff_access': staff_access, 'masquerade': masq})


@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def static_tab(request, course_id, tab_slug, is_global=None):

    """
    Display the courses tab with the given name.

    Assumes the course_id is in a valid format.
    """

    registered = CourseEnrollment.is_enrolled(request.user, course_id)
    if not registered:
        return redirect(reverse('cabout', args=[course_id]))

    if is_global:
      course = get_course_by_id(course_id)
      if not request.user.is_authenticated():
          raise Http404("Page not found.")
    else:
      course = get_course_with_access(request.user, course_id, 'load')

    tab = tabs.get_static_tab_by_slug(course, tab_slug)
    if tab is None:
        raise Http404

    contents = tabs.get_static_tab_contents(
        request,
        course,
        tab
    )
    if contents is None:
        raise Http404
    if request.GET.get('pf_id') != None:
        curr_user = User.objects.get(id=int(request.GET.get('pf_id')))
    else:
        curr_user = None
    staff_access = has_access(request.user, course, 'staff')
    return render_to_response('courseware/static_tab.html',
                              {'course': course,
                               'curr_user':curr_user,
                               'tab': tab,
                               'tab_contents': contents,
                               'staff_access': staff_access,
                               'is_global':is_global})

# TODO arjun: remove when custom tabs in place, see courseware/syllabus.py


@ensure_csrf_cookie
def syllabus(request, course_id):
    """
    Display the course's syllabus.html, or 404 if there is no such course.

    Assumes the course_id is in a valid format.
    """
    course = get_course_with_access(request.user, course_id, 'load')
    staff_access = has_access(request.user, course, 'staff')

    return render_to_response('courseware/syllabus.html', {'course': course,
                                            'staff_access': staff_access, })


def registered_for_course(course, user):
    """
    Return True if user is registered for course, else False
    """
    if user is None:
        return False
    if user.is_authenticated():
        return CourseEnrollment.is_enrolled(user, course.id)
    else:
        return False


@ensure_csrf_cookie
@cache_if_anonymous
def course_about(request, course_id):
    if settings.MITX_FEATURES.get('ENABLE_MKTG_SITE', False):
        raise Http404

    course = get_course_with_access(request.user, course_id, 'see_exists')
    registered = registered_for_course(course, request.user)

    if has_access(request.user, course, 'load'):
        course_target = reverse('info', args=[course.id])
    else:
        course_target = reverse('about_course', args=[course.id])

    show_courseware_link = (has_access(request.user, course, 'load') or
                            settings.MITX_FEATURES.get('ENABLE_LMS_MIGRATION'))

    return render_to_response('courseware/course_about.html',
                              {'course': course,
                               'registered': registered,
                               'course_target': course_target,
                               'show_courseware_link': show_courseware_link})


@ensure_csrf_cookie
@cache_if_anonymous
#@begin:View of the course
#@date:2013-11-02        
def cabout(request, course_id):
    
    if settings.MITX_FEATURES.get('ENABLE_MKTG_SITE', False):
        raise Http404

    course = get_course_with_access(request.user, course_id, 'see_exists')
    registered = registered_for_course(course, request.user)

    if has_access(request.user, course, 'load'):
        course_target = reverse('info', args=[course.id])
    else:
        course_target = reverse('about_course', args=[course.id])

    show_courseware_link = (has_access(request.user, course, 'load') or
                            settings.MITX_FEATURES.get('ENABLE_LMS_MIGRATION'))

    return render_to_response('courseware/cabout.html',
                              {
                               'course': course,
                               'registered': registered,
                               'course_target': course_target,
                               'show_courseware_link': show_courseware_link})


#@end

@ensure_csrf_cookie
@cache_if_anonymous
def mktg_course_about(request, course_id):
    """
    This is the button that gets put into an iframe on the Drupal site
    """

    try:
        course = get_course_with_access(request.user, course_id, 'see_exists')
    except (ValueError, Http404) as e:
        # if a course does not exist yet, display a coming
        # soon button
        return render_to_response('courseware/mktg_coming_soon.html',
                                  {'course_id': course_id})

    registered = registered_for_course(course, request.user)

    if has_access(request.user, course, 'load'):
        course_target = reverse('info', args=[course.id])
    else:
        course_target = reverse('about_course', args=[course.id])

    allow_registration = has_access(request.user, course, 'enroll')

    show_courseware_link = (has_access(request.user, course, 'load') or
                            settings.MITX_FEATURES.get('ENABLE_LMS_MIGRATION'))
    course_modes = CourseMode.modes_for_course(course.id)

    return render_to_response('courseware/mktg_course_about.html',
                              {
                                  'course': course,
                                  'registered': registered,
                                  'allow_registration': allow_registration,
                                  'course_target': course_target,
                                  'show_courseware_link': show_courseware_link,
                                  'course_modes': course_modes,
                              })


def render_notifications(request, course, notifications):
    context = {
        'notifications': notifications,
        'get_discussion_title': partial(get_discussion_title, request=request, course=course),
        'course': course,
    }
    return render_to_string('courseware/notifications.html', context)


@login_required
def news(request, course_id):
    course = get_course_with_access(request.user, course_id, 'load')

    notifications = comment_client.get_notifications(request.user.id)

    context = {
        'course': course,
        'content': render_notifications(request, course, notifications),
    }

    return render_to_response('courseware/news.html', context)


@login_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def progress(request, course_id, student_id=None):
    """ User progress. We show the grade bar and every problem score.

    Course staff are allowed to see the progress of students in their class.
    """

    registered = CourseEnrollment.is_enrolled(request.user, course_id)
    if not registered:
        return redirect(reverse('cabout', args=[course_id]))

    course = get_course_with_access(request.user, course_id, 'load', depth=None)
    staff_access = has_access(request.user, course, 'staff')

    if student_id is None or student_id == request.user.id:
        # always allowed to see your own profile
        student = request.user
    else:
        # Requesting access to a different student's profile
        if not staff_access:
            raise Http404
        student = User.objects.get(id=int(student_id))

    # NOTE: To make sure impersonation by instructor works, use
    # student instead of request.user in the rest of the function.

    # The pre-fetching of groups is done to make auth checks not require an
    # additional DB lookup (this kills the Progress page in particular).
    student = User.objects.prefetch_related("groups").get(id=student.id)

    field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
        course_id, student, course, depth=None)

    courseware_summary = grades.progress_summary(student, request, course,
                                                 field_data_cache)
    grade_summary = grades.grade(student, request, course, field_data_cache)

    if courseware_summary is None:
        #This means the student didn't have access to the course (which the instructor requested)
        raise Http404

    context = {'course': course,
               'courseware_summary': courseware_summary,
               'grade_summary': grade_summary,
               'staff_access': staff_access,
               'student': student,
               }
    context.update()

    return render_to_response('courseware/progress.html', context)


@login_required
def submission_history(request, course_id, student_username, location):
    """Render an HTML fragment (meant for inclusion elsewhere) that renders a
    history of all state changes made by this user for this problem location.
    Right now this only works for problems because that's all
    StudentModuleHistory records.
    """
    course = get_course_with_access(request.user, course_id, 'load')
    staff_access = has_access(request.user, course, 'staff')

    # Permission Denied if they don't have staff access and are trying to see
    # somebody else's submission history.
    if (student_username != request.user.username) and (not staff_access):
        raise PermissionDenied

    try:
        student = User.objects.get(username=student_username)
        student_module = StudentModule.objects.get(course_id=course_id,
                                                   module_state_key=location,
                                                   student_id=student.id)
    except User.DoesNotExist:
        return HttpResponse(escape("User {0} does not exist.".format(student_username)))
    except StudentModule.DoesNotExist:
        return HttpResponse(escape("{0} has never accessed problem {1}".format(student_username, location)))

    history_entries = StudentModuleHistory.objects.filter(
        student_module=student_module
    ).order_by('-id')

    # If no history records exist, let's force a save to get history started.
    if not history_entries:
        student_module.save()
        history_entries = StudentModuleHistory.objects.filter(
            student_module=student_module
        ).order_by('-id')

    context = {
        'history_entries': history_entries,
        'username': student.username,
        'location': location,
        'course_id': course_id
    }

    return render_to_response('courseware/submission_history.html', context)

#@begin:View of the newly added page
#@date:2013-11-02        
def my_course_portfolio(request, course_id, student_id=None):
    return False


def resource_library(request, course_id, student_id=None):
    return False

def people(request, course_id, student_id=None):
    return False
#@end
