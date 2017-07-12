"""
Student Views
"""
from __future__ import division
import datetime
import json
import logging
import re

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from courseware.model_data import FieldDataCache
from mitxmako.shortcuts import render_to_response, render_to_string

from xmodule.modulestore.exceptions import ItemNotFoundError
from xmodule.modulestore.django import modulestore
from courseware.access import has_access
from external_auth.models import ExternalAuthMap
from bulk_email.models import Optout
from courseware.module_render import get_module
from study_time.models import record_time_store
from administration.models import site_setting_store, PepRegStudent, PepRegTraining, UserLoginInfo
from feeding import dashboard_feeding_store
from django.db.models import Sum
from reporting.models import reporting_store
from bson import json_util
from views import course_from_id, cert_info, exam_registration_info, study_time_format, upload_user_photo
from django.http import HttpResponse
from datetime import timedelta
from student.models import CourseEnrollment, CourseEnrollmentAllowed, UserProfile
from permissions.utils import check_access_level
from communities.models import CommunityCommunities, CommunityDiscussions, CommunityUsers
from xmodule.remindstore import myactivitystore, myactivitystaticstore, chunksstore
from courseware.courses import get_course_by_id, course_image_url, get_course_about_section 
import comment_client as cc
from reporting.models import Reports
from django.core.urlresolvers import reverse
from student.models import State,District,School,User,UserProfile
from organization.models import OrganizationMetadata, OrganizationDistricts, OrganizationDashboard, OrganizationMenu, OrganizationMenuitem   
from django.http import HttpResponseRedirect
from communities.views import get_trending
from mongo_user_store import MongoUserStore
from django.conf import settings
from bson import ObjectId
from collections import OrderedDict
from courseware import grades

log = logging.getLogger("tracking")


@login_required
@ensure_csrf_cookie
def user_information(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=request.user.id)

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

            courses.append(c)

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

    show_courseware_links_for = frozenset(course.id for course in courses
                                          if has_access(user, course, 'load'))
    courses_complated = sorted(courses_complated, key=lambda x: x.complete_date, reverse=True)
    context = {
        'show_courseware_links_for': show_courseware_links_for,
        'courses_complated': courses_complated,
        'curr_user': user
    }   

    return render_to_response('user_information.html', context)

#test for new style of dashboard
@login_required
@ensure_csrf_cookie
def newdashboard(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=request.user.id)

    OrganizationOK = False
    try:
        state_id = user.profile.district.state.id
    except:
        state_id = -1
    try:
        district_id = user.profile.district.id
    except:
        district_id = -1
    try:
        school_id = user.profile.school.id
    except:
        school_id = -1

    organization_obj = OrganizationMetadata()
    if (school_id != -1):
        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=school_id, EntityType="School"):
            organization_obj = tmp1.organization
            OrganizationOK = True
            break;

    if (not(OrganizationOK) and district_id != -1):
        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=district_id, EntityType="District"):
            organization_obj = tmp1.organization
            OrganizationOK = True
            break;
    
    if (not(OrganizationOK) and state_id != -1):
        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=state_id, EntityType="State"):
            OrganizationOK = True
            organization_obj = tmp1.organization
            break;
            
    data = {}
    if OrganizationOK:
        data["org_id"] = organization_obj.id;
        for tmp1 in OrganizationDashboard.objects.filter(organization=organization_obj):
            data[tmp1.itemType] = tmp1.itemValue

    if OrganizationOK and data["Dashboard option etc"] == "0":
        return HttpResponseRedirect('/dashboard')

    # Build our courses list for the user, but ignore any courses that no longer
    # exist (because the course IDs have changed). Still, we don't delete those
    # enrollments, because it could have been a data push snafu.

    courses_complated = []
    courses_incomplated = []
    courses = []

    external_time = 0
    external_times = {}
    exists = 0

    allowedcourses_id = []
    allowedcourses_id = list(CourseEnrollmentAllowed.objects.filter(email=user.email, is_active=True).order_by('-id').values_list('course_id', flat=True))
    
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
        if enrollment.course_id in allowedcourses_id:
            allowedcourses_id.remove(enrollment.course_id)
        try:
            c = course_from_id(enrollment.course_id)
            c.student_enrollment_date = enrollment.created

            if enrollment.course_id in allowed:
                exists = exists - 1
            courses.append(c)

            #external_time
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

    #@begin:get My Courses
    #@date:2017-02-19
    #Just choose the last 2 courses_incomplated of the user.
    courses_incomplated_list = list()
    for k, v in enumerate(courses_incomplated):
        courses_incomplated_list.append(v)
        if k > 0:
            break
    #@end

    #@begin:get My Learning Communities
    #@date:2017-02-16
    community_list = list()
    # Just choose the last 2 communities the user belongs to.
    items = CommunityUsers.objects.select_related().filter(user=request.user).order_by('-id')[0:2]
    if items:
        for item in items:
            community_list.append({'id': item.community.id,
                                'name': item.community.name,
                                'logo': item.community.logo.upload.url if item.community.logo else '',
                                'private': item.community.private})
        if len(items) < 2:
            itmes_all = CommunityCommunities.objects.select_related().filter().order_by('name')[0:2]
            if itmes_all:
                if itmes_all[0].id != items[0].community.id:
                    community_list.append({'id': itmes_all[0].id,
                               'name': itmes_all[0].name,
                               'logo': itmes_all[0].logo.upload.url if itmes_all[0].logo else '',
                               'private': itmes_all[0].private})
                else:
                    if len(itmes_all) > 1:
                        community_list.append({'id': itmes_all[1].id,
                               'name': itmes_all[1].name,
                               'logo': itmes_all[1].logo.upload.url if itmes_all[1].logo else '',
                               'private': itmes_all[1].private})

    else:
         items = CommunityCommunities.objects.select_related().filter().order_by('name')[0:2]
         for item in items:
            community_list.append({'id': item.id,
                               'name': item.name,
                               'logo': item.logo.upload.url if item.logo else '',
                               'private': item.private})
    #@end

    #@begin:get Recommended For You
    #@date:2017-05-1
    allowedcourses = []
    for course_id in allowedcourses_id:
        try:
            course = course_from_id(course_id)
            allowedcourses.append(course)
        except:
            pass
    allowedcourse_list = []
    if allowedcourses:
        allowedcourse_list.append(allowedcourses[0])
    #@end

    #@begin:get Community Trending Topics
    #@date:2017-05-18
    communit_tt_list = []
    community_joined_p = CommunityUsers.objects.select_related().filter(user=request.user,community__private__exact=1).order_by('community__name')
    community_joined_p = list(community_joined_p.values_list('community__id', flat=True))
    communit_tt_list_add(community_joined_p,1,communit_tt_list)

    if len(communit_tt_list) < 3:
        community_joined_not_p = CommunityUsers.objects.select_related().filter(user=request.user,community__private__exact=0).order_by('community__name')
        community_joined_not_p = list(community_joined_not_p.values_list('community__id', flat=True))
        communit_tt_list_add(community_joined_not_p,1,communit_tt_list)

    if len(communit_tt_list) < 3:
        community_joined = list(CommunityUsers.objects.select_related().filter(user=request.user).values_list('community__id', flat=True))
        community_all = list(CommunityCommunities.objects.select_related().filter().order_by('name').values_list('id', flat=True))
        for cid in community_joined:
            if cid in community_all:
                community_all.remove(cid)
        communit_tt_list_add(community_all,0,communit_tt_list)
    #@end

    store = dashboard_feeding_store()
    feeding_year_start, feeding_year_end = store.get_post_year_range(request.user.id)
    #feeding_year_start, feeding_year_end = False, False

    #@begin:get my_activity filter year range
    #@date:2017-05-27
    my_activity_year_start, my_activity_year_end = myactivitystore().get_my_activity_year_range()
    #@end

    #@begin:get user last logged in time
    #@date:2017-06-12
    user_last_logged_in = ''
    user_log_info = UserLoginInfo.objects.filter(user_id=user.id)
    for d in user_log_info:
        #user_last_logged_in = datetime.datetime.strptime(d.login_time,"%Y-%m-%d %H:%M:%S")
        #user_last_logged_in = user_last_logged_in.strftime('%m') + "/" +  user_last_logged_in.strftime('%d') + "/" + user_last_logged_in.strftime('%Y')
        user_last_logged_in = d.login_time[5:7] + "/" + d.login_time[8:10] + "/" + d.login_time[0:4]
        break
    #@end

    '''
    get user stats time
    2017-06-12
    '''
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

    context = {
        'courses_complated': courses_complated,
        'courses_complated_all_count':len(courses_complated),
        'courses_incomplated_top2': courses_incomplated_list,
        'courses_incomplated_all_count':len(courses_incomplated),
        'show_courseware_links_for': show_courseware_links_for,
        'all_course_time': study_time_format(all_course_time),
        'collaboration_time': study_time_format(collaboration_time),
        'total_time_in_pepper': study_time_format(total_time_in_pepper),
        'pd_time': study_time_format(pd_time),
        'user_last_logged_in': user_last_logged_in,
        'curr_user': user,
        'communities': community_list,
        'allowedcourses': allowedcourse_list,
        'community_trending_topics': communit_tt_list,
        'feeding_year_start': feeding_year_start,
        'feeding_year_end': feeding_year_end,
        'my_activity_year_start': my_activity_year_start,
        'my_activity_year_end': my_activity_year_end
    }    
    
    return render_to_response('dashboard_new.html', context)

def communit_tt_list_add(community_ids,joined,communit_tt_list):
    for c in community_ids:
        if len(communit_tt_list) < 3:
            trending_topic = get_tt(c,joined)
            if trending_topic:
                communit_tt_list.append(trending_topic)
        else:
            break

def get_tt(c,joined):
    tt = {}
    trending = get_trending(c)
    if trending:
        tt['cname'] = trending[0].community.name
        if joined:
            tt['btntext'] = 'Reply'
        else:
            tt['btntext'] = 'Add Me'

        if hasattr(trending[0], "subject"):
            tt['date_reply'] = trending[0].date_reply
            tt['content'] = trending[0].subject
            tt['btnurl'] = '/community/discussion/' + str(trending[0].id)
        else:
            tt['date_reply'] = trending[0].date_update
            tt['content'] = trending[0].post
            tt['btnurl'] = '/community/' + str(trending[0].community.id)
        return tt

def get_my_course_in_progress(request):
    user = User.objects.get(id=request.user.id)
    course_type = request.POST.get('course_type')
    get_more = request.POST.get('get_more')

    courses_complated = []
    courses_incomplated = []
    courses = []
    exists = 0

    allowed = CourseEnrollmentAllowed.objects.filter(email=user.email, is_active=True).values_list('course_id', flat=True)
    # make sure the course exists
    for course_id in allowed:
        try:
            # course=course_from_id(course_id)
            exists = exists + 1
        except:
            pass

    orig_external_times = {}
    rts = record_time_store()
    for enrollment in CourseEnrollment.enrollments_for_user(user):
        try:
            c = course_from_id(enrollment.course_id)
            c.student_enrollment_date = enrollment.created

            if enrollment.course_id in allowed:
                exists = exists - 1
            courses.append(c)
            if user.is_superuser:
                orig_external_times[c.id] = 0
            else:
                orig_external_times[c.id] = rts.get_external_time(str(user.id), c.id)

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

    course_unfin_list = list()
    student = User.objects.prefetch_related("groups").get(id=user.id)
    rs = reporting_store()
    rs.set_collection('UserCourseView')
    if course_type == "incompleted":
        for k,course in enumerate(courses_incomplated):
            if get_more == 'yes':
                if k > 2:
                    couser_dict = {}
                    #set user course percent
                    field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course.id, student, course, depth=None)
                    grade_summary = grades.grade(student, request, course, field_data_cache)
                    couser_dict['p'] = grade_summary['percent']

                    #set user course total time
                    if user.is_superuser:
                        couser_dict['time'] = 0
                    else:
                        results = rs.collection.find({"user_id":request.user.id,"course_id":course.id},{"_id":0,"total_time":1})
                        total_time_user = 0
                        for v in results:
                            total_time_user = total_time_user + v['total_time']
                        current_time = rts.get_course_time(str(user.id), course.id, 'courseware') + orig_external_times[course.id]
                        if not current_time:
                            current_time = 0
                        couser_dict['time'] = study_time_format(total_time_user + current_time)

                    #set user course title
                    couser_dict['name'] = get_course_about_section(course, 'title')

                    #set user course number
                    couser_dict['number'] = course.display_number_with_default

                    #set user course url
                    couser_dict['url'] = "/courses/" + course.id + "/courseware"

                    couser_dict['close_course'] = course.close_course

                    course_unfin_list.append(couser_dict)
            else:
                couser_dict = {}
                #set user course percent
                field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course.id, student, course, depth=None)
                grade_summary = grades.grade(student, request, course, field_data_cache)
                couser_dict['p'] = grade_summary['percent']

                #set user course total time
                if user.is_superuser:
                    couser_dict['time'] = 0
                else:
                    results = rs.collection.find({"user_id":request.user.id,"course_id":course.id},{"_id":0,"total_time":1})
                    total_time_user = 0
                    for v in results:
                        total_time_user = total_time_user + v['total_time']
                    current_time = rts.get_course_time(str(user.id), course.id, 'courseware') + orig_external_times[course.id]
                    if not current_time:
                        current_time = 0
                    couser_dict['time'] = study_time_format(total_time_user + current_time)

                #set user course title
                couser_dict['name'] = get_course_about_section(course, 'title')

                #set user course number
                couser_dict['number'] = course.display_number_with_default

                #set user course url
                couser_dict['url'] = "/courses/" + course.id + "/courseware"

                couser_dict['close_course'] = course.close_course

                course_unfin_list.append(couser_dict)
                if k > 1:
                    break
    else:
        for k,course in enumerate(courses_complated):
            if get_more == 'yes':
                if k > 1:
                    couser_dict = {}
                    #set user course total time
                    if user.is_superuser:
                        couser_dict['time'] = 0
                    else:
                        results = rs.collection.find({"user_id":request.user.id,"course_id":course.id},{"_id":0,"total_time":1})
                        total_time_user = 0
                        for v in results:
                            total_time_user = total_time_user + v['total_time']
                        current_time = rts.get_course_time(str(user.id), course.id, 'courseware') + orig_external_times[course.id]
                        if not current_time:
                            current_time = 0
                        couser_dict['time'] = study_time_format(total_time_user + current_time)

                    #set user course title
                    couser_dict['name'] = get_course_about_section(course, 'title')

                    #set user course number
                    couser_dict['number'] = course.display_number_with_default

                    #set user course url
                    couser_dict['url'] = "/courses/" + course.id + "/courseware"

                    #set user course certificate url
                    couser_dict['url_c'] = "/" + course.id + "/" + str(course.complete_date)[0:10] + "/download_certificate"

                    couser_dict['close_course'] = course.close_course
                    couser_dict['issue_certificate'] = course.issue_certificate

                    course_unfin_list.append(couser_dict)
            else:
                couser_dict = {}
                #set user course total time
                if user.is_superuser:
                    couser_dict['time'] = 0
                else:
                    results = rs.collection.find({"user_id":request.user.id,"course_id":course.id},{"_id":0,"total_time":1})
                    total_time_user = 0
                    for v in results:
                        total_time_user = total_time_user + v['total_time']
                    current_time = rts.get_course_time(str(user.id), course.id, 'courseware') + orig_external_times[course.id]
                    if not current_time:
                        current_time = 0
                    couser_dict['time'] = study_time_format(total_time_user + current_time)

                #set user course title
                couser_dict['name'] = get_course_about_section(course, 'title')

                #set user course number
                couser_dict['number'] = course.display_number_with_default

                #set user course url
                couser_dict['url'] = "/courses/" + course.id + "/courseware"

                #set user course certificate url
                couser_dict['url_c'] = "/" + course.id + "/" + str(course.complete_date)[0:10] + "/download_certificate"

                couser_dict['close_course'] = course.close_course
                couser_dict['issue_certificate'] = course.issue_certificate

                course_unfin_list.append(couser_dict)
                if k > 0:
                    break

    return HttpResponse(json.dumps({'data': course_unfin_list,'Success': 'True'}), content_type='application/json')


def get_my_activities(request):
    #filter_condition
    filter_con = {}
    filter_con["user_id"] = int(request.POST.get('user_id'))
    filter_con["year"] = request.POST.get('filter_year')
    filter_con["month"] = request.POST.get('filter_month')
    filter_con["group"] = request.POST.get('filter_group')
    
    filter_key = create_filter_key(filter_con)
    order_key = "ActivityDateTime"
    order_order = -1
    skip_rows = int(request.POST.get('skip_rows'))
    get_rows = int(request.POST.get('get_rows'))

    my_activities_count = myactivitystore().get_item_count(filter_key)
    my_activities = myactivitystore().get_item(filter_key,order_key,order_order,skip_rows,get_rows)

    ma_list = list()
    for data in my_activities:
        ma_dict = {}

        #URL
        ma_dict["URL"] =  re.sub("{([\w ]*)}", lambda x: str(data["URLValues"].get(x.group(1))), data["URL"])
       
        #GroupType
        ma_dict["g_type"] = data["GroupType"]

        #time
        ma_dict["time"] = str(data["ActivityDateTime"])[0:19]

        ma_dict["DisplayInfo"] = get_displayInfo(data).replace('href=#','href=' + ma_dict["URL"])

        get_logoInfo(data,ma_dict)

        ma_list.append(ma_dict)
    return HttpResponse(json.dumps({'data': ma_list,'data_count':my_activities_count,'Success': 'True'}), content_type='application/json')

def get_displayInfo(data):
    displayInfo_values = {}
    info_list = re.findall("{([\w |,.()'_/]*)}", data["DisplayInfo"])
    dt = {}
    for d in info_list:
        t1 =  d.split(',')
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

def get_logoInfo(data,ma_dict):
    ma_dict['logoUrl'] = ''
    ma_dict['logoName'] = ''
    logo_list = re.findall("{([\w |,.()'_/]*)}", data["Logo"])
    dt = {}
    for d in logo_list:
        t1 =  d.split(',')
        value = ''
        if t1[0] == 'mysql':
            dt = {}
            t21 = t1[1].split('|')
            t22 = t1[2].split('|')
            dt['db'] = t1[0]
            dt['models'] = t21[0]
            dt['models2'] = t21[1]
            dt['getby'] = t22[0]
            dt['key'] = data['LogoValues'][t22[1]]
            dt['key_name'] = t1[3]
            try:
                value = data['LogoValues'][dt['key_name']]
            except:
                str_get = dt['models'] + '.objects.filter(' + dt['getby'] + '=' + str(dt['key']) + ')'
                e1 = eval(str_get)
                for d in e1:
                    try:
                        value = eval("d." + dt['models2'])
                    except:
                        pass
        else:
            dt = {}
            dt['db'] = t1[0]
            dt['models'] = re.sub("/([\w _]*)/", lambda x: str(data['LogoValues'].get(x.group(1))), t1[1])
            dt['key_name'] = t1[2]
            value = eval(dt['models'])

        ma_dict[dt['key_name']] = value
    if not logo_list:
        ma_dict['logoUrl'] = data["Logo"]

def replace_values(body, values):
    return re.sub("{[\w |,.()'_/]*,([\w ]*)}", lambda x: str(values.get(x.group(1))), body)

def create_filter_key(filter_con):
    filter_key = {"UsrCre":filter_con["user_id"]}

    if filter_con["group"]:
        filter_key["GroupType"] = filter_con["group"]

    filter_year = filter_con["year"]
    filter_month = filter_con["month"]
    if filter_year:
        year1 = "%02d" %int(filter_year)
        year2 = "%02d" %(int(filter_year) + 1)
        month1 = "01"
        month2 = "01"
        if filter_month:
            if filter_month == "12":
                year2 = "%02d" %(int(filter_year) + 1)
                month1 = "%02d" %int(filter_month)
                month2 = "01"
            else:
                year2 = "%02d" %int(filter_year)
                month1 = "%02d" %int(filter_month)
                month2 =  "%02d" %(int(filter_month) + 1)
        s1 = year1 + "-" + month1 + "-01 00:00:00"
        s2 = year2 + "-" + month2 + "-01 00:00:00"
        time_start = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
        time_end = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
        filter_key["ActivityDateTime"] = {'$gte': time_start, '$lt': time_end}
    elif filter_month:
        year_0, year_now = myactivitystore().get_my_activity_year_range()
        if not year_0:
            year_0 = 2000
        if not year_now:
            year_now = 2000

        filter_key["$or"] = []
        while year_0 <= year_now:
            if filter_month == "12":
                month1 = "%02d" %int(filter_month)
                month2 = "01"
                year1 = str(year_0)
                year2 = str(year_0 + 1)
            else:
                month1 = "%02d" %int(filter_month)
                month2 = "%02d" %(int(filter_month)+1)
                year1 = str(year_0)
                year2 = str(year_0)
            s1 = year1 + "-" + month1 + "-01 00:00:00"
            s2 = year2 + "-" + month2 + "-01 00:00:00"
            time_start = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
            time_end = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
            year_0 += 1
            filter_key["$or"].append({"ActivityDateTime":{'$gte': time_start, '$lt': time_end}})
    return filter_key


@login_required
@ensure_csrf_cookie
def my_courses(request, user_id=None):
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

            courses.append(c)

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
        course_times = {course.id: study_time_format(rts.get_course_time(str(user.id), course.id, 'courseware')) for course in courses}

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

    return render_to_response('my_courses.html', context)


def attach_post_info(p, time_diff_m, user):
    store = dashboard_feeding_store()

    def format_feeding_date(post_time_utc):
        if int(time_diff_m) != 0:
            post_time_local = time_to_local(post_time_utc, time_diff_m)
            # now_local = time_to_local(now_utc, time_diff_m)
        else:
            post_time_local = post_time_utc

        # now_local_last_str = now_local.strftime('%Y-%m-%d') + ' 23:59:59'
        # post_time_local_str = post_time_local.strftime('%Y-%m-%d %H:%M:%S')

        unow = datetime.datetime.utcnow()
        diff = unow - post_time_utc.replace(tzinfo=None)

        post_year = post_time_local.strftime("%Y")
        post_month = post_time_local.strftime("%b")
        post_day = post_time_local.strftime("%d")

        if diff.days == 0 and post_day == unow.strftime("%d"):
            post_date = 'Today'
            # post_date = post_year + '-' + post_month + '-' + post_day
        else:
            post_date = post_month + ' ' + post_day + ", " + post_year
        post_h = str(int(post_time_local.strftime("%I")))
        post_m = post_time_local.strftime("%M")
        post_ampm = post_time_local.strftime("%p")

        hour_diff = int((diff.days * 86400 + diff.seconds) / (60 * 60))
        return post_date, post_h, post_m, post_ampm, hour_diff

    def format_like(likes):
        if not likes:
            return ""
        buf = []
        for lk in likes:
            if lk["user_id"] == user.id:
                buf.insert(0, "You")
            else:
                author = User.objects.get(id=lk["user_id"])
                buf.append(user.first_name + " " + author.last_name)
        ending = ""
        if len(buf) > 3:
            buf = buf[:3]
            ending = " and more"

        return ", ".join(buf) + ending

    author = User.objects.get(id=p["user_id"])
    (post_date, post_h, post_m, post_ampm, debug) = format_feeding_date(p["date"])

    p["content"] = filter_at(p["content"])
    p["first_name"] = author.first_name
    p["last_name"] = author.last_name
    p["username"] = author.username
    p["email"] = author.email
    p["district_name"] = author.profile.district.name
    p["sub"] = store.get_sub(p["_id"])
    p["is_my_like"] = store.is_like(p["_id"], user.id)
    p["who_like_text"] = format_like(p.get("likes"))
    p["likes"] = len(p.get("likes")) if p.get("likes") else 0
    p["expiration_date"] = p["expiration_date"].strftime('%Y-%m-%d %H:%M:%S') if p.get("expiration_date") else ''
    p["post_date"] = post_date
    p["post_h"] = post_h
    p["post_m"] = post_m
    p["post_ampm"] = post_ampm
    p["post_date_debug"] = debug
    p["is_owner"] = (author == user)
    p["removable"] = user.id == author.id or user.is_superuser
    if p["type"] == "post":
        pl = [int(e) if e.isdigit() else e for e in user.profile.people_of.split(',')]
        p["comment_disabled"] = not ((author.id in pl) or (author.id == user.id))
    else:
        p["comment_disabled"] = True  # disable announcement comment

    if active_recent(author) and user != author:
        p["online"] = 1
        if author.profile.skype_username:
            p["skype_username"] = author.profile.skype_username
        else:
            p["skype_username"] = "Not Set."

    for s in p["sub"]:
        attach_post_info(s, time_diff_m, user)


def get_post(request):
    _id = request.POST.get("_id")
    store = dashboard_feeding_store()
    post = store.get_feeding(_id)
    time_diff_m = request.POST.get('local_utc_diff_m', 0)
    attach_post_info(post, time_diff_m, request.user)
    return HttpResponse(json_util.dumps(post), content_type='application/json')


def get_comment(request):
    _id = request.POST.get("_id")
    store = dashboard_feeding_store()
    post = store.get_feeding(_id)
    time_diff_m = request.POST.get('local_utc_diff_m', 0)
    attach_post_info(post, time_diff_m, request.user)
    return HttpResponse(json_util.dumps(post), content_type='application/json')


def download_attachment(request):
    feeding_id = request.GET.get("feeding_id")

    store = dashboard_feeding_store()
    feeding = store.get_feeding(feeding_id)
    
    options = settings.USERSTORE.get("OPTIONS")
    us = MongoUserStore(**options)
    content = us.find_one(ObjectId(feeding_id), 'feeding_attachment')
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % feeding["attachment_file"]
    if content:
        response.write(content.get("data"))
    return response


def get_attachment_image(request):
    feeding_id = request.GET.get("feeding_id")

    store = dashboard_feeding_store()
    feeding = store.get_feeding(feeding_id)
    
    options = settings.USERSTORE.get("OPTIONS")
    us = MongoUserStore(**options)
    content = us.find_one(ObjectId(feeding_id), 'feeding_attachment')
    
    image = feeding["attachment_file"]
    image = image.rstrip('/')
    image = image.rstrip('\\')
    ext = image[-3:]
    
    if ext == "png" or ext == "jpg" or ext == "gif":
        response = HttpResponse(content_type='image/' + ext.upper())
        
    if content:
        response.write(content.get("data"))
    return response


def get_posts(request):
    filter_year = request.POST.get("filter_year")
    filter_month = request.POST.get("filter_month")
    # last_id = request.POST.get("last_id")
    page = request.POST.get("page", 0)
    page_size = request.POST.get("page_size", 5)
    time_diff_m = request.POST.get('local_utc_diff_m', 0)

    now_utc = datetime.datetime.utcnow()
    if int(time_diff_m) != 0:
        now_utc = time_to_local(now_utc, time_diff_m)

    store = dashboard_feeding_store()
    posts = store.get_posts(request.user.id, year=filter_year, month=filter_month,
                            page_size=int(page_size), page=int(page), after=now_utc)

    for a in posts:
        attach_post_info(a, time_diff_m, request.user)

    return HttpResponse(json_util.dumps(posts), content_type='application/json')


def dismiss_announcement(request):
    _id = request.POST.get("_id")
    try:
        store = dashboard_feeding_store()
        store.dismiss(_id, request.user.id)
    except Exception as e:
        return HttpResponse(json_util.dumps({"success": False, "error": str(e)}), content_type='application/json')
    
    return HttpResponse(json_util.dumps({"success": True}), content_type='application/json')


def get_org_announcements(request):
    org = request.POST.get("org")
    store = dashboard_feeding_store()

    time_diff_m = request.POST.get('local_utc_diff_m', 0)

    now_utc = datetime.datetime.utcnow()
    if int(time_diff_m) != 0:
        now_utc = time_to_local(now_utc, time_diff_m)

    kwargs = {"after": now_utc}

    posts = store.get_announcements(request.user.id, org, **kwargs)

    for a in posts:
        attach_post_info(a, time_diff_m, request.user)

    return HttpResponse(json_util.dumps(posts), content_type='application/json')


def get_announcements(request):
    filter_year = request.POST.get("filter_year")
    filter_month = request.POST.get("filter_month")
    # last_id = request.POST.get("last_id")
    page = request.POST.get("page", 0)
    page_size = request.POST.get("page_size", 5)
    time_diff_m = request.POST.get('local_utc_diff_m', 0)

    now_utc = datetime.datetime.utcnow()
    if int(time_diff_m) != 0:
        now_utc = time_to_local(now_utc, time_diff_m)

    store = dashboard_feeding_store()
    # posts = store.top_level_for_user(request.user.id, type=filter_group,
    #                                  year=filter_year, month=filter_month,
    #                                  page_size=int(page_size), page=int(page), after=now_utc)

    kwargs = {"year": filter_year, "month": filter_month, "after": now_utc}
    data = {"orgs": []}
    data["orgs"].append(store.get_announcements(request.user.id, "Pepper", **kwargs))
    data["orgs"].append(store.get_announcements(request.user.id, "System", **kwargs))
    data["orgs"].append(store.get_announcements(request.user.id, "State", **kwargs))
    data["orgs"].append(store.get_announcements(request.user.id, "District", **kwargs))
    data["orgs"].append(store.get_announcements(request.user.id, "School", **kwargs))

    for o in data["orgs"]:
        for a in o:
            attach_post_info(a, time_diff_m, request.user)

    return HttpResponse(json_util.dumps(data), content_type='application/json')


def submit_new_like(request):
    user_id = request.user.id
    feeding_id = request.POST.get('feeding_id')

    store = dashboard_feeding_store()

    if store.is_like(feeding_id, user_id):
        store.remove_like(feeding_id, request.user.id)
    else:
        postPublisher_id = int(store.get_feeding(feeding_id)['user_id'])
        rs = myactivitystore()
        my_activity = {"GroupType": "MyFeed", "EventType": "myFeed_likePost", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
        "URLValues": {"postPublisher_id": postPublisher_id},
        "TokenValues": {"postPublisher_id":postPublisher_id}, 
        "LogoValues": {"postPublisher_id": postPublisher_id}}
        rs.insert_item(my_activity)
        
        date = datetime.datetime.utcnow()
        store.add_like(feeding_id, request.user.id, date)

    return HttpResponse(json.dumps({'Success': 'True'}), content_type='application/json')


def delete_announcement(request):
    feeding_id = request.POST.get("_id")
    store = dashboard_feeding_store()
    store.remove_feeding(feeding_id)
    return HttpResponse(json.dumps({"Success": "True"}), content_type='application/json')


def delete_post(request):
    feeding_id = request.POST.get("_id")
    store = dashboard_feeding_store()
    store.remove_feeding(feeding_id)
    return HttpResponse(json.dumps({"Success": "True"}), content_type='application/json')


def delete_comment(request):
    feeding_id = request.POST.get("_id")
    store = dashboard_feeding_store()
    store.remove_feeding(feeding_id)
    return HttpResponse(json.dumps({"Success": "True"}), content_type='application/json')


def get_receivers(user, post_type):
    receiver_ids = None
    if post_type == "announcement":
        up = user.profile
        level = check_access_level(user, "dashboard_announcement", "create")
        if level == "System":
            receiver_ids = [0]
        elif level == "State":
            receiver_ids = list(UserProfile.objects.filter(district__state_id=up.district.state.id).values_list('user_id', flat=True))
        elif level == "District":
            receiver_ids = list(UserProfile.objects.filter(district_id=up.district_id).values_list('user_id', flat=True))
        elif level == "School":
            receiver_ids = list(UserProfile.objects.filter(school_id=up.school_id).values_list('user_id', flat=True))
    else:
        receiver_ids = list(UserProfile.objects.extra(where=['FIND_IN_SET(%s, people_of)' % user.id]).values_list('user_id', flat=True))
        receiver_ids.append(user.id)
    return receiver_ids


def submit_new_comment(request):
    store = dashboard_feeding_store()
    post_id = request.POST.get('post_id', '')
    content = request.POST.get('content')

    postPublisher_id = int(store.get_feeding(post_id)['user_id'])
    rs = myactivitystore()
    my_activity = {"GroupType": "MyFeed", "EventType": "myFeed_commentPost", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id,
                   "URLValues": {"postPublisher_id": postPublisher_id},
                   "TokenValues": {"postPublisher_id": postPublisher_id},
                   "LogoValues": {"postPublisher_id": postPublisher_id}}
    rs.insert_item(my_activity)

    _id = store.create(user_id=request.user.id,
                       type="comment",
                       content=content,
                       sub_of=post_id, top_level=post_id,
                       date=datetime.datetime.utcnow())

    return HttpResponse(json_util.dumps({'Success': 'True', '_id': _id}), content_type='application/json')


def lookup_name(request):
    name = request.POST.get("name").split()
    if len(name) > 1:
        fname = name[0]
        lname = name[1]
    else:
        fname = name[0]
        lname = ""
    users = User.objects.filter(first_name__istartswith=fname).filter(last_name__istartswith=lname)
    str = []
    for user in users:
        str.append(user.first_name + " " + user.last_name)
    return HttpResponse(json.dumps({'Success': 'True', 'content': str}), content_type='application/json')


def get_full_likes(request):
    feeding_id = request.POST.get('feeding_id')
    html = "<table>"

    store = dashboard_feeding_store()
    likes = store.get_likes(feeding_id)
    
    for like in likes:
        user = User.objects.get(id=like["user_id"])
        html += " <tr><td><img src='"+reverse('user_photo', args=[user.id])+"' width='24px'></img></td><td>"+user.first_name + " " + user.last_name + "</td></tr>"
    html += "</table>"
    return HttpResponse(json.dumps({'Success': 'True', 'html': html}), content_type='application/json')


def upload_attachment(feeding_id, attachment):
    options = settings.USERSTORE.get("OPTIONS")
    us = MongoUserStore(**options)
    _id = OrderedDict([("ref_id", ObjectId(feeding_id)), ("type", "feeding_attachment")])
    us.save(_id, attachment.read())


def submit_new_post(request):
    store = dashboard_feeding_store()
    content = request.POST.get("post", "")
    attachment = request.FILES.get('attachment')

    type = request.POST.get("type")
    expiration_date = request.POST.get("expiration_date", None)
    expiration_date = datetime.datetime.strptime(expiration_date + " 23:59:59", "%m/%d/%Y %H:%M:%S") if expiration_date else None

    rs = myactivitystore()
    my_activity = {"GroupType": "MyFeed", "EventType": "myFeed_publishPost", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id,
                   "URLValues": {"postPublisher_id": request.user.id},
                   "TokenValues": {"postPublisher_id": request.user.id},
                   "LogoValues": {"postPublisher_id": request.user.id}}
    rs.insert_item(my_activity)

    attachment_file = attachment.name if (attachment is not None) else None
    
    if type == "post":
        _id = store.create(type=type, user_id=request.user.id, content=content, attachment_file=attachment_file,
                           receivers=get_receivers(request.user, type), date=datetime.datetime.utcnow(),
                           expiration_date=expiration_date)
    else:
        if request.user.is_superuser:
            organization_type = "Pepper"
        else:
            organization_type = check_access_level(request.user, "dashboard_announcement", "create")
        _id = store.create(type=type, user_id=request.user.id, content=content, attachment_file=attachment_file,
                           receivers=get_receivers(request.user, type), date=datetime.datetime.utcnow(),
                           expiration_date=expiration_date, organization_type=organization_type)

    if attachment_file:
        upload_attachment(_id, attachment)

    return HttpResponse(json.dumps({'Success': 'True', "_id": str(_id), 'post': request.POST.get('post'),
                                    'master_id': request.POST.get('master_id')}), content_type='application/json')

def parse_urls(content):
    final = ""
    url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    for word in content.split():
        try:
            if url.match(word):
                final += '<a href = "'+word+'">'+word+'</a> '
            else:
                final += word + " "
        except Exception as e:
            final = e
    return final

def filter_at(content):
    at = content.find("@")
    final = content
    tests=" Tests: "
    if at >= 0:
        string = content[at:]
        while string.find("@") > -1:
            s=string[1:]
            x=s.find("@")
            try:
                if x > -1:
                    working = s[:x].split(' ')
                else:
                    working = s.split(' ')
                try:
                    working.remove('')
                except:
                    None
                working[1] = re.sub('[!.?,:)(]', '', working[1])
                try:
                    user = User.objects.filter(first_name=working[0], last_name=working[1])[0]
                    addition = "<a class='in-comment-link' target='_blank' href = '../dashboard/"+str(user.id)+"'>"+working[0]+" "+working[1]+"</a>"
                    final=final.replace("@"+working[0]+" "+working[1], addition)
                except Exception as e:
                    tests+="<br>Failed: "+str(e)
            except Exception as e:
                None
            string = s[x:]
    return final


def active_recent(user):
    use = user
    utc_month = datetime.datetime.utcnow().strftime("%m")
    utc_day = datetime.datetime.utcnow().strftime("%d")
    utc_h = datetime.datetime.utcnow().strftime("%H")
    utc_m = datetime.datetime.utcnow().strftime("%M")
    d_min = 60*int(utc_h) + int(utc_m)
    if use.profile.last_activity:
        usr = use.profile.last_activity
        u_min = 60*int(usr.strftime("%H")) + int(usr.strftime("%M"))
        close = int(d_min) - int(u_min) < 1
        active = usr.strftime("%d") == utc_day and usr.strftime("%m") == utc_month and close
    else:
        active = False
    return active


def time_to_local(user_time,time_diff_m):
    '''
    Return datetime type
    '''
    if type(user_time) == str:
        user_time_time = datetime.datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S')
    else:
        user_time_time = user_time

    plus_sub = 1
    time_diff_m_int = int(time_diff_m)
    if time_diff_m_int >= 0:
        plus_sub = 1
    else:
        plus_sub = -1
    
    user_time_dt = user_time_time + timedelta(seconds=abs(time_diff_m_int)*60)*plus_sub
    return user_time_dt
#@end

def new_upload_photo(request):
    upload_user_photo(request.user.id,request.FILES.get('photo'))
    return redirect(reverse('user_information',args=[request.user.id]))
