from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from student.models import UserProfile, CourseEnrollment
import json
import logging
import csv
import gevent
from django import db
from models import *
from StringIO import StringIO
from student.models import District, Cohort, School, State
from student.views import study_time_format, course_from_id
from datetime import datetime
from pytz import UTC
from threading import Thread
from study_time.models import record_time_store
from django.views.decorators import csrf
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError
from courseware.module_render import get_module
from courseware.model_data import FieldDataCache
from courseware.courses import get_courses
from courseware.course_grades_helper import grade
from mail import send_html_mail
from permissions.decorators import user_has_perms
from permissions.utils import check_user_perms

log = logging.getLogger("tracking")

ADJUSTMENT_TIME_CSV_COLS = ('email', 'time', 'type', 'course_number', 'comments')


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


@user_has_perms('time_report')
def main(request):
    return render_to_response('administration/time_report.html', {})


# -------------- Dropdown Lists -------------
def drop_states(request):
    r = list()
    if check_user_perms(request.user, 'time_report', 'district_admin', exclude_superuser=True):
        state_id = UserProfile.objects.get(user_id=request.user.id).district.state_id
        data = State.objects.filter(id=state_id)[0]
        r.append({"id": data.id, "name": data.name})
    else:
        data = State.objects.all()
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_districts(request):
    r = list()
    if check_user_perms(request.user, 'time_report', 'district_admin', exclude_superuser=True):
        data = UserProfile.objects.get(user_id=request.user.id).district
        r.append({"id": data.id, "name": data.name})
    else:
        if request.GET.get('state'):
            data = District.objects.all()
            data = data.filter(state=request.GET.get('state'))
            data = data.order_by("name")
            for item in data:
                r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_schools(request):
    r = list()
    if check_user_perms(request.user, 'time_report', 'district_admin', exclude_superuser=True):
        district = UserProfile.objects.get(user_id=request.user.id).district
        data = School.objects.filter(district=district.id)
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name})
    else:
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
        r.append({"id": course.id, "name": str(course.display_coursenumber) + ' ' + course.display_name})
    r.sort(key=lambda x: x['name'], reverse=False)
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_enroll_courses(request):
    r = list()
    user = User.objects.get(id=request.GET.get('user_id'))
    for enrollment in CourseEnrollment.enrollments_for_user(user):
        try:
            course = course_from_id(enrollment.course_id)
            r.append({"id": course.id, "name": str(course.display_coursenumber) + ' ' + course.display_name})
        except ItemNotFoundError:
            log.error("User {0} enrolled in non-existent course {1}".format(user.username, enrollment.course_id))
    r.sort(key=lambda x: x['name'], reverse=False)
    return HttpResponse(json.dumps(r), content_type="application/json")


# load completed courses / current courses
@csrf.csrf_exempt
@user_has_perms('time_report')
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


@user_has_perms('time_report')
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
        except Exception as e:
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


@user_has_perms('time_report')
def time_report_download_excel(request):
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    FIELDS = ["user_first_name", "user_last_name", "user_email", "district", "school", "total_time", "collaboration_time",
              "discussion_time", "portfolio_time", "external_time", "course_time", "complete_course_num", "current_course_num"]

    TITLES = ["First Name", "Last Name", "Email", "District", "School", "Total Time", "Collaboration Time",
              "Discussion Time", "Portfolio Time", "External Time", "Course Units Time", "Completed Course", "Current Courses"]
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
    except Exception as e:
        message = {'percent': 100, 'success': task.task_read}
    return HttpResponse(json.dumps(message), content_type="application/json")


@user_has_perms('time_report')
def get_time_table_result(request):
    rts = record_time_store()
    rows = rts.get_time_report_result(str(request.user.id))
    return HttpResponse(json.dumps({'rows': rows}), content_type="application/json")


# save adjustment time
@csrf.csrf_exempt
@user_has_perms('time_report', 'adjust_time')
def save_adjustment_time(request):
    rts = record_time_store()
    adjustment_type = request.POST.get('type')
    adjustment_time = request.POST.get('time')
    course_id = request.POST.get('course_id')
    user_id = str(request.POST.get('user_id'))
    comments = request.POST.get('comments', None)
    success = validate_adjustment_time(rts, user_id, adjustment_type, adjustment_time, course_id)
    if success:
        rts.set_adjustment_time(user_id, adjustment_type, adjustment_time, course_id)
        save_adjustment_log(request, user_id, adjustment_type, adjustment_time, course_id, comments)
    return HttpResponse(json.dumps({'success': success}), content_type="application/json")


# load adjustment time
@user_has_perms('time_report')
def load_adjustment_time(request):
    rts = record_time_store()
    user_id = str(request.POST.get('user_id'))
    adjustment_time = rts.get_adjustment_time(user_id, request.POST.get('type'), request.POST.get('course_id'))
    return HttpResponse(json.dumps({'time': study_time_format(adjustment_time, True)}), content_type="application/json")


# Refresh modified time
@user_has_perms('time_report')
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


# validate adjustment time / return ture is right
def validate_adjustment_time(rts, user_id, type, adjustment_time, course_id):
    type_time = 0
    external_time = 0
    adjustment_time = int(adjustment_time)
    if adjustment_time < 0:
        if type == 'total':
            user = User.objects.get(id=user_id)
            for enrollment in CourseEnrollment.enrollments_for_user(user):
                try:
                    course = course_from_id(enrollment.course_id)
                    external_time += rts.get_external_time(user_id, course.id)
                except ItemNotFoundError:
                    log.error("User {0} enrolled in non-existent course {1}".format(user.username, enrollment.course_id))

            course_time, discussion_time, portfolio_time = rts.get_stats_time(user_id)
            adjustment_time_totle = rts.get_adjustment_time(user_id, 'total', None)
            type_time = course_time + discussion_time + portfolio_time + external_time + adjustment_time_totle
        else:
            if type == 'external':
                type_time = rts.get_external_time(user_id, course_id)
            else:
                type_time = rts.get_course_time(user_id, course_id, type)
        if type_time + adjustment_time < 0:
            return False
    return True


def save_adjustment_log(request, user_id, type, adjustment_time, course_number, comments=None):
    user = User.objects.get(id=user_id)
    adjustment_log = AdjustmentTimeLog()
    adjustment_log.user_id = user_id
    adjustment_log.user_email = user.email
    adjustment_log.admin_email = request.user.email
    adjustment_log.type = type
    adjustment_log.adjustment_time = adjustment_time
    adjustment_log.create_time = datetime.now(UTC)
    adjustment_log.course_number = course_number
    adjustment_log.comments = comments
    adjustment_log.save()


@user_has_perms('time_report', 'adjust_time')
def load_adjustment_log(request):
    rows = []
    logs = AdjustmentTimeLog.objects.filter(user_id=request.POST.get('user_id')).order_by('-create_date')
    for d in logs:
        create_date = d.create_date.strftime('%b-%d-%y %H:%M:%S')
        rows.append({"user_email": d.user_email,
                     "admin_email": d.admin_email,
                     "adjustment_time": study_time_format(d.adjustment_time, True),
                     "type": d.type,
                     "course_number": d.course_number,
                     "create_date": create_date,
                     "comments": d.comments
                     })
    return HttpResponse(json.dumps({'rows': rows}), content_type="application/json")


def validate_adjustment_time_cvs_line(line, tasklog):
    adjustment_type_list = ['courseware', 'discussion', 'portfolio', 'external']
    '''
    n = 0
    for item in line:
        if len(item.strip()):
            n += 1
    if n != len(ADJUSTMENT_TIME_CSV_COLS):
        raise Exception("Wrong column count %s" % n)
    '''
    email = line[ADJUSTMENT_TIME_CSV_COLS.index('email')]
    time = line[ADJUSTMENT_TIME_CSV_COLS.index('time')]
    type = line[ADJUSTMENT_TIME_CSV_COLS.index('type')]
    course_number = line[ADJUSTMENT_TIME_CSV_COLS.index('course_number')]
    if len(User.objects.filter(email=email)) < 1:
        tasklog.username = ''
        raise Exception("An account with the Email '{email}' does not exist".format(email=email))
    else:
        tasklog.username = email
    if type not in adjustment_type_list:
        raise Exception("type:'{type}' does not exist".format(type=type))
    if not (time[0] == '-' and time[1:] or time).isdigit():
        raise Exception("adjustment time:'{time}' is not an integer".format(time=time))
    try:
        #course_name = course_from_id(course_id).display_name
        course_id = get_course_id(course_number)
    except:
        raise Exception("course number:'{number}' does not exist".format(number=course_number))


# Adjustment time import
@csrf.csrf_exempt
@user_has_perms('time_report', 'adjust_time')
def import_adjustment_time_submit(request):
    if request.method == 'POST':

        file = request.FILES.get('file', None)
        r = csv.reader(file, dialect=csv.excel)
        r1 = []
        r1.extend(r)

        task = ImportTask()
        task.filename = file.name
        task.total_lines = len(r1)
        task.user = request.user
        task.save()
        db.transaction.commit()

        from django.db import connection
        connection.close()

        do_import_adjustment_time(task, r1, request)

        return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success_linescess': False}), content_type="application/json")


@postpone
def do_import_adjustment_time(task, csv_lines, request):
    gevent.sleep(0)

    count_success = 0
    rts = record_time_store()
    for i, line in enumerate(csv_lines):
        tasklog = ImportTaskLog()
        tasklog.create_date = datetime.now(UTC)
        tasklog.line = i + 1
        tasklog.task = task
        tasklog.import_data = line
        try:
            task.process_lines = i + 1
            validate_adjustment_time_cvs_line(line, tasklog)
            email = line[ADJUSTMENT_TIME_CSV_COLS.index('email')]
            adjustment_time = int(line[ADJUSTMENT_TIME_CSV_COLS.index('time')]) * 60
            adjustment_type = line[ADJUSTMENT_TIME_CSV_COLS.index('type')]
            course_number = line[ADJUSTMENT_TIME_CSV_COLS.index('course_number')]
            try:
                comments = line[ADJUSTMENT_TIME_CSV_COLS.index('comments')]
            except:
                comments = ''
            user_id = str(User.objects.get(email=email).id)
            course_id = str(get_course_id(course_number))
            success = validate_adjustment_time(rts, user_id, adjustment_type, adjustment_time, course_id)
            if success:
                rts.set_adjustment_time(user_id, adjustment_type, adjustment_time, course_id)
                save_adjustment_log(request, user_id, adjustment_type, adjustment_time, course_number, comments)
            tasklog.error = 'ok'
        except Exception as e:
            tasklog.error = "%s" % e
            log.debug("import error %s" % e)
        finally:
            count_success += 1
            task.success_lines = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            tasklog.save()

    tasklogs = ImportTaskLog.objects.filter(task=task).exclude(error='ok')
    if len(tasklogs):
        FIELDS = ["line", "username", "import_data", "create_date", "error"]
        TITLES = ["Line", "Useremail", "Import Data", "Create Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row = {"line": d.line,
                   "username": d.username,
                   "import_data": d.import_data,
                   "create_date": d.create_date,
                   "error": d.error
                   }
            writer.writerow(row)
        output.seek(0)
        attach = [{'filename': 'log.csv', 'mimetype': 'text/csv', 'data': output.read()}]
        send_html_mail("Adjustment Time Import Report",
                       "Report of importing %s, see attachment." % task.filename,
                       settings.SUPPORT_EMAIL, [request.user.email], attach)
        output.close()


def get_course_id(course_number):
    return modulestore().course_from_course_number(course_number).id
