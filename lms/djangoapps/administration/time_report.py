from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse

from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

# from django.contrib.auth.models import User
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

from mako.template import Template
import mitxmako

from django.db.models import F
from study_time.models import record_time_store
from django.views.decorators import csrf
from xmodule.modulestore.exceptions import ItemNotFoundError
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
        p = Process(target=function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()
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


def filter_user(vars, data):
    if vars.get('state', None):
        data = data.filter(Q(district__state_id=vars.get('state')))
    if vars.get('district', None):
        data = data.filter(Q(district_id=vars.get('district')))
    if vars.get('school', None):
        data = data.filter(Q(school_id=vars.get('school')))
    return data


@csrf.csrf_exempt
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
    do_get_report_data(task, data, request)
    return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")


@postpone
def do_get_report_data(task, data, request):
    gevent.sleep(0)
    count_success = 0
    rows = []
    rts = record_time_store()
    for i, p in enumerate(data):
        try:
            external_time = 0
            if p.subscription_status != 'Imported':
                for enrollment in CourseEnrollment.enrollments_for_user(p.user):
                    try:
                        course = course_from_id(enrollment.course_id)
                        external_time += rts.get_external_time(str(p.user.id), course.id)
                    except ItemNotFoundError:
                        log.error("User {0} enrolled in non-existent course {1}".format(p.user.username, enrollment.course_id))

                course_time, discussion_time, portfolio_time = rts.get_stats_time(str(p.user.id))
                all_course_time = course_time + external_time
                collaboration_time = discussion_time + portfolio_time
                total_time = all_course_time + collaboration_time
            else:
                total_time = 0
                course_time = 0
                collaboration_time = 0

            rows.append({'id': p.user.id,
                         'user_first_name': p.user.first_name,
                         'user_last_name': p.user.last_name,
                         'user_email': p.user.email,
                         'district': attstr(p, "district.name"),
                         'school': attstr(p, "school.name"),
                         "total_time": study_time_format(total_time),
                         "collaboration_time": study_time_format(collaboration_time),
                         "external_time": study_time_format(external_time),
                         "course_time": study_time_format(course_time)
                         })
            task.process_num = i + 1

        except Exception, e:
            db.transaction.rollback()
        finally:
            count_success += 1
            task.success_num = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            db.transaction.commit()
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
              "external_time", "course_time"]

    TITLES = ["First Name", "Last Name", "Email", "District", "School", "Total Time", "Collaboration Time",
              "External Time", "Course Time"]
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
