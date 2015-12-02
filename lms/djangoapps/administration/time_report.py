from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse

from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from django.contrib.auth.models import User
from student.models import UserProfile, CourseEnrollment
# from django import db
import json
import time
import logging
import csv
import gevent
from django import db
from models import *
from StringIO import StringIO
from student.models import District, Cohort, School, State
from student.views import study_time_format, course_from_id
from datetime import datetime, timedelta
from pytz import UTC

from multiprocessing import Process
from threading import Thread
from mako.template import Template
import mitxmako

from django.db.models import F
from study_time.models import record_time_store
from django.views.decorators import csrf
from xmodule.modulestore.exceptions import ItemNotFoundError
from courseware.module_render import get_module
from courseware.model_data import FieldDataCache
from courseware.courses import get_courses
log = logging.getLogger("tracking")


def attstr(obj, attr):
    r = obj
    try:
        for a in attr.split("."):
            r = getattr(r, a)
    except:
        r = ""

    if r is None:
        r = ""
    return r


def postpone(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
    return render_to_response('administration/time_report.html', {})


#* -------------- Dropdown List -------------


def drop_states(request):
    r = list()
    data = State.objects.all()
    data = data.order_by("name")
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_districts(request):
    r = list()
    if request.GET.get('state'):
        data = District.objects.all()
        data = data.filter(state=request.GET.get('state'))
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_schools(request):
    r = list()
    if request.GET.get('district'):
        data = School.objects.all()
        data = data.filter(district=request.GET.get('district'))
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_cohorts(request):
    data = Cohort.objects.all()
    if request.GET.get('district'):
        data = data.filter(district=request.GET.get('district'))
    elif request.GET.get('state'):
        data = data.filter(district__state=request.GET.get('state'))
    r = list()
    for item in data:
        r.append({"id": item.id, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_courses(request):
    r = list()
    courses = get_courses(None)
    for course in courses:
        course = course_from_id(course.id)
        r.append({"id": course.id, "name": course.display_name_with_default})
    r.sort(key=lambda x: x['name'], reverse=False)
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_enroll_courses(request):
    r = list()
    user = User.objects.get(id=request.GET.get('user_id'))
    for enrollment in CourseEnrollment.enrollments_for_user(user):
        try:
            course = course_from_id(enrollment.course_id)
            r.append({"id": course.id, "name": course.display_name_with_default})
        except ItemNotFoundError:
            log.error("User {0} enrolled in non-existent course {1}".format(user.username, enrollment.course_id))
    r.sort(key=lambda x: x['name'], reverse=False)
    return HttpResponse(json.dumps(r), content_type="application/json")


# load completed courses / current courses
@csrf.csrf_exempt
@login_required
def load_enrollment_courses(request):
    r = list()
    complete_course = list()
    current_course = list()
    user = User.objects.get(id=request.POST.get('user_id'))
    enrollment_type = request.POST.get('type')
    for enrollment in CourseEnrollment.enrollments_for_user(user):
        try:
            course = course_from_id(enrollment.course_id)
            field_data_cache = FieldDataCache([course], course.id, user)
            course_instance = get_module(user, request, course.location, field_data_cache, course.id, grade_bucket_type='ajax')
            item = {'name': str(course.display_coursenumber) + ' ' + course.display_name}
            if course_instance.complete_course:
                complete_course.append(item)
            else:
                current_course.append(item)
        except ItemNotFoundError:
            log.error("User {0} enrolled in non-existent course {1}".format(user.username, enrollment.course_id))
    if enrollment_type == 'complete':
        r = complete_course
    else:
        r = current_course
    r.sort(key=lambda x: x['name'], reverse=False)
    return HttpResponse(json.dumps(r), content_type="application/json")


def filter_user(vars, data):
    if vars.get('state', None):
        data = data.filter(Q(district__state_id=vars.get('state')))
    if vars.get('district', None):
        data = data.filter(Q(district_id=vars.get('district')))
    if vars.get('school', None):
        data = data.filter(Q(school_id=vars.get('school')))
    data = data.filter(~Q(subscription_status='Imported'))
    return data


#@csrf.csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_table(request):
    data = UserProfile.objects.all()
    data = filter_user(request.GET, data)
    task = TimeReportTask()
    task.total_num = data.count()
    task.user = request.user
    task.save()
    db.transaction.commit()
    from django.db import connection
    connection.close()

    course_id = str(request.GET.get('course', None))
    if course_id:
        f = []
        for i, p in enumerate(data):
            if CourseEnrollment.is_enrolled(p.user, course_id):
                f.append(p)
        task.total_num = len(f)
        task.save()
        db.transaction.commit()
        from django.db import connection
        connection.close()
        do_get_report_data(task, f, request, course_id)
    else:
        do_get_report_data(task, data, request)
    return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")


@postpone
def do_get_report_data(task, data, request, course_id=None):
    gevent.sleep(0)
    count_success = 0
    rows = []
    rts = record_time_store()
    for i, p in enumerate(data):
        try:
            external_time = 0
            all_external_time = 0
            complete_course_num = 0
            current_course_num = 0
            user_id = str(p.user.id)
            if course_id:
                for enrollment in CourseEnrollment.enrollments_for_user(p.user):
                    try:
                        course = course_from_id(enrollment.course_id)
                        all_external_time += rts.get_external_time(user_id, course.id)
                        field_data_cache = FieldDataCache([course], course.id, p.user)
                        course_instance = get_module(p.user, request, course.location, field_data_cache, course.id, grade_bucket_type='ajax')

                        if course_instance.complete_course:
                            complete_course_num += 1
                        else:
                            current_course_num += 1
                    except ItemNotFoundError:
                        #log.error("User {0} enrolled in non-existent course {1}".format(p.user.username, enrollment.course_id))
                        pass
                all_course_time, all_discussion_time, portfolio_time = rts.get_stats_time(user_id)
                external_time = rts.get_external_time(user_id, course_id)
                course_time = rts.get_course_time(user_id, course_id, 'courseware')
                discussion_time = rts.get_course_time(user_id, course_id, 'discussion')
                collaboration_time = all_discussion_time + portfolio_time
                all_course_time = all_course_time + all_external_time
                total_time = all_course_time + collaboration_time + rts.get_adjustment_time(user_id, 'total')
            else:
                for enrollment in CourseEnrollment.enrollments_for_user(p.user):
                    try:
                        course = course_from_id(enrollment.course_id)
                        external_time += rts.get_external_time(user_id, course.id)
                        field_data_cache = FieldDataCache([course], course.id, p.user)
                        course_instance = get_module(p.user, request, course.location, field_data_cache, course.id, grade_bucket_type='ajax')

                        if course_instance.complete_course:
                            complete_course_num += 1
                        else:
                            current_course_num += 1
                    except ItemNotFoundError:
                        #log.error("User {0} enrolled in non-existent course {1}".format(p.user.username, enrollment.course_id))
                        pass
                course_time, discussion_time, portfolio_time = rts.get_stats_time(user_id)
                all_course_time = course_time + external_time
                collaboration_time = discussion_time + portfolio_time
                total_time = all_course_time + collaboration_time + rts.get_adjustment_time(user_id, 'total')

            rows.append({'id': p.user.id,
                         'user_first_name': p.user.first_name,
                         'user_last_name': p.user.last_name,
                         'user_email': p.user.email,
                         'district': attstr(p, "district.name"),
                         'school': attstr(p, "school.name"),
                         "total_time": study_time_format(total_time, True),
                         "collaboration_time": study_time_format(collaboration_time, True),
                         "discussion_time": study_time_format(discussion_time, True),
                         "portfolio_time": study_time_format(portfolio_time, True),
                         "external_time": study_time_format(external_time, True),
                         "course_time": study_time_format(course_time, True),
                         "complete_course_num": complete_course_num,
                         "current_course_num": current_course_num
                         })
            task.process_num = i + 1
        except Exception, e:
            db.transaction.rollback()
        finally:
            count_success += 1
            task.success_num = count_success
            task.update_time = datetime.now(UTC)
            task.save()
    rts.set_time_report_result(str(request.user.id), rows)
    task.task_read = True
    task.save()
    db.transaction.commit()


@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_report_download_excel(request):
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    FIELDS = ["user_first_name", "user_last_name", "user_email", "district", "school", "total_time", "collaboration_time",
              "discussion_time", "portfolio_time", "external_time", "course_time", "complete_course_num", "current_course_num"]

    TITLES = ["First Name", "Last Name", "Email", "District", "School", "Total Time", "Collaboration Time",
              "Discussion Time", "Portfolio Time", "External Time", "Course Time", "Completed Course", "Current Courses"]
    for i, k in enumerate(TITLES):
        worksheet.write(0, i, k)
    row = 1
    rts = record_time_store()
    results = rts.get_time_report_result(str(request.user.id))
    for p in results:
        for i, k in enumerate(FIELDS):
            worksheet.write(row, i, p[k])
        row += 1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.now().strftime('attachment; filename=users-time-report-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())
    return response


def time_table_progress(request):
    try:
        task = TimeReportTask.objects.get(id=request.POST.get('taskId'))
        message = {'percent': '%.2f' % (task.process_num * 100 / task.total_num), 'success': task.task_read}
    except Exception, e:
        message = {'percent': 100, 'success': task.task_read}
    return HttpResponse(json.dumps(message), content_type="application/json")


def get_time_table_result(request):
    rts = record_time_store()
    rows = rts.get_time_report_result(str(request.user.id))
    return HttpResponse(json.dumps({'rows': rows}), content_type="application/json")


# save adjustment time
@login_required
def save_adjustment_time(request):
    rts = record_time_store()
    user_id = str(request.POST.get('user_id'))
    rts.set_adjustment_time(user_id, request.POST.get('type'), request.POST.get('time'), request.POST.get('course_id'))
    return HttpResponse(json.dumps({}), content_type="application/json")


# load adjustment time
@login_required
def load_adjustment_time(request):
    rts = record_time_store()
    user_id = str(request.POST.get('user_id'))
    adjustmen_time = rts.get_adjustment_time(user_id, request.POST.get('type'), request.POST.get('course_id'))
    return HttpResponse(json.dumps({'time': study_time_format(adjustmen_time, True)}), content_type="application/json")


# Refresh modified time
@login_required
def load_single_user_time(request):
    user = User.objects.get(id=request.POST.get('user_id'))
    row = {}
    rts = record_time_store()
    external_time = 0
    all_external_time = 0
    user_id = str(user.id)
    course_id = str(request.POST.get('course_id', None))
    if course_id:
        for enrollment in CourseEnrollment.enrollments_for_user(user):
            try:
                course = course_from_id(enrollment.course_id)
                all_external_time += rts.get_external_time(user_id, course.id)
            except ItemNotFoundError:
                #log.error("User {0} enrolled in non-existent course {1}".format(p.user.username, enrollment.course_id))
                pass
        all_course_time, all_discussion_time, portfolio_time = rts.get_stats_time(user_id)
        adjustment_time_totle = rts.get_adjustment_time(user_id, 'total', None)
        external_time = rts.get_external_time(user_id, course_id)
        course_time = rts.get_course_time(user_id, course_id, 'courseware')
        discussion_time = rts.get_course_time(user_id, course_id, 'discussion')
        collaboration_time = all_discussion_time + portfolio_time
        all_course_time = all_course_time + all_external_time
        total_time = all_course_time + collaboration_time + adjustment_time_totle
    else:
        for enrollment in CourseEnrollment.enrollments_for_user(user):
            try:
                course = course_from_id(enrollment.course_id)
                external_time += rts.get_external_time(user_id, course.id)
            except ItemNotFoundError:
                #log.error("User {0} enrolled in non-existent course {1}".format(p.user.username, enrollment.course_id))
                pass
        adjustment_time_totle = rts.get_adjustment_time(user_id, 'total', None)
        course_time, discussion_time, portfolio_time = rts.get_stats_time(user_id)
        all_course_time = course_time + external_time
        collaboration_time = discussion_time + portfolio_time
        total_time = all_course_time + collaboration_time + adjustment_time_totle

    row = {"id": user_id,
           "total_time": study_time_format(total_time, True),
           "collaboration_time": study_time_format(collaboration_time, True),
           "discussion_time": study_time_format(discussion_time, True),
           "portfolio_time": study_time_format(portfolio_time, True),
           "external_time": study_time_format(external_time, True),
           "course_time": study_time_format(course_time, True)
           }

    return HttpResponse(json.dumps({'row': row}), content_type="application/json")
