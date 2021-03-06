from mitxmako.shortcuts import render_to_response, render_to_string
from django.http import HttpResponse
import json
from models import PepRegTraining, PepRegInstructor, PepRegStudent
from django import db
from datetime import datetime, timedelta, date
from pytz import UTC
from django.contrib.auth.models import User

import urllib2
from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from permissions.utils import check_access_level, check_user_perms
from StringIO import StringIO
import xlsxwriter
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School
from training.models import TrainingUsers
from xmodule.modulestore.django import modulestore
import pymongo

from django.conf import settings
import calendar
from django.utils.timezone import datetime, now, timedelta, utc
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from student.models import (Registration, UserProfile, TestCenterUser, TestCenterUserForm,
                            TestCenterRegistration, TestCenterRegistrationForm, State,
                            PendingNameChange, PendingEmailChange, District,
                            CourseEnrollment, unique_id_for_user,
                            get_testcenter_registration, CourseEnrollmentAllowed)

from io import BytesIO

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from xmodule.remindstore import myactivitystore
import logging

@login_required
def index(request):
    # courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    # courses = sorted(courses, key=lambda course: course.display_name.lower())
    tmp = "administration/pepreg.html";
    try:
        courses = get_courses_drop(request.user.profile.district.state.name, request.user.profile.district.code)
    except:
        tmp = "administration/pepreg_district_school_null.html";
        courses = {};

    return render_to_response(tmp, {"courses": courses})


def build_filters(columns, filters):
    """
    Builds the filters for the PepConn report data
    :param columns: the columns in this table
    :param filters: the filters requested
    :return: the arguments to pass to filter()
    """
    kwargs = dict()
    args = None
    # Iterate through the filters.
    for column, value in filters.iteritems():
        # For the numerical columns, just filter that column by the passed value.
        if not column == 'all':
            c = int(column)
            # If the column is an integer value, convert the search term.
            out_value = value
            if columns[c][2] == 'int' and value.isdigit():
                out_value = int(value)
            # Build the actual kwargs to pass to filer(). in this case, we need the column selector ([0]) as well as the
            # type of selection to make ([1] - '__iexact').
            kwargs[columns[c][0] + columns[c][1]] = out_value
        # If this is a search for all, we need to do an OR search, so we build one with Q objects.
        else:
            args_list = list()
            for key, data in columns.iteritems():
                # [2] holds the column type (int, str, or False to ignore).
                if data[2]:
                    # If the column is an integer value, convert the search term (as long as the string is only digits).
                    out_value = value
                    if data[2] == 'int':
                        if value.isdigit():
                            out_value = int(value)
                        else:
                            out_value = None
                    if out_value is not None:
                        # Create the Q object and add it to the list.
                        args_list.append(Q(**{data[0] + data[1]: out_value}))
            # Start the list with the first object, then add the rest with ORs.
            args = args_list.pop()
            for item in args_list:
                args |= item

    return args, kwargs


def get_post_array(post, name, max=None):
    """
    Gets array values from a POST.
    """
    output = dict()
    for key in post.keys():
        value = urllib2.unquote(post.get(key))
        if key.startswith(name + '[') and not value == 'undefined':
            start = key.find('[')
            i = key[start + 1:-1]
            if max and int(i) > max:
                i = 'all'
            output.update({i: value})
    return output


def build_sorts(columns, sorts):
    """
    Builds the sorts for the PepConn report data
    :param columns: the columns in this table
    :param sorts: the sorts requested
    :return: the arguments to pass to order_by()
    """
    order = list()
    # Iterate through the passed sorts.
    for column, sort in sorts.iteritems():
        # Default to an ASC search, but if the sort is 1, change it to DESC by adding a -.
        pre = ''
        if bool(int(sort)):
            pre = '-'
        # We just need the column selector out of the columns, not the type.
        order.append(pre + columns[int(column)][0])
    return order


def reach_limit(training):
    return training.max_registration > 0 and PepRegStudent.objects.filter(
        training=training).count() >= training.max_registration


def instructor_names(training):
    names = []
    for instructor in PepRegInstructor.objects.filter(training=training):
        names.append("%s %s" % (instructor.instructor.first_name, instructor.instructor.last_name))
    return names


def rows(request):
    columns = {
        1: ['district__state__name', '__iexact', 'str'],
        2: ['district__name', '__iexact', 'str'],
        3: ['subject', '__iexact', 'str'],
        4: ['pepper_course', '__iexact', 'str'],
        5: ['name', '__iexact', 'str'],
        6: ['description', '__iexact', 'str'],
        7: ['training_date', '__iexact', False],
        8: ['training_time_start', '__iexact', 'str'],
        9: ['geo_location', '__iexact', 'str'],
        10: ['credits', '__iexact', 'int']
    }

    sorts = get_post_array(request.GET, 'col')
    order = build_sorts(columns, sorts)

    if not order:
        order = ["-id"]

    filters = get_post_array(request.GET, 'fcol')
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    if filters.get('7'):
        filters['7'] = datetime.strptime(filters['7'], '%m/%d/%Y').strftime('%Y-%m-%d')

    # limit to district trainings for none-system
    is_no_System = False
    if check_access_level(request.user, 'pepreg', 'add_new_training') != "System":
        #filters[1] = request.user.profile.district.state.name
        #filters[2] = request.user.profile.district.name
        is_no_System = True

    if len(filters):
        args, kwargs = build_filters(columns, filters)
        if args:
            trainings = PepRegTraining.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            trainings = PepRegTraining.objects.prefetch_related().filter(**kwargs).order_by(*order)
    else:
        trainings = PepRegTraining.objects.prefetch_related().all().order_by(*order)

    tmp_school_id = 0
    try:
        tmp_school_id = request.user.profile.school.id
    except:
        tmp_school_id = 0

    trainings_set = list()
    for item in trainings:
        if(not(is_no_System)):
            trainings_set.append(item)
        else:
            is_belong = PepRegInstructor.objects.filter(instructor=request.user,
                                                        training=item).exists() or item.user_create == request.user
            if(is_belong):
                trainings_set.append(item)

            elif(item.district.name == request.user.profile.district.name):
                try:
                    if(not(item.school_id) or item.school_id == -1 or item.school_id == tmp_school_id):
                        trainings_set.append(item)
                except:
                    pass

    count = len(trainings_set)
    rows = list()
    for item in trainings_set[start:end]:
        arrive = "1" if datetime.now(UTC).date() >= item.training_date else "0"
        allow = "1" if item.allow_registration else "0"
        rl = "1" if reach_limit(item) else "0"
        remain = item.max_registration - PepRegStudent.objects.filter(
            training=item).count() if item.max_registration > 0 else -1

        status = ""
        all_edit = "0"
        all_delete = "0"

        if PepRegStudent.objects.filter(student=request.user, training=item).exists():
            status = PepRegStudent.objects.get(student=request.user, training=item).student_status

        if item.user_create == request.user:
            all_edit = "1"
            all_delete = "1"
        else:
            if PepRegInstructor.objects.filter(instructor=request.user, training=item).exists():
                for pi in PepRegInstructor.objects.filter(instructor=request.user, training=item):
                    if pi.all_edit:
                        all_edit = "1";

                    if pi.all_delete:
                        all_delete = "1";

                    break;

        is_belong = PepRegInstructor.objects.filter(instructor=request.user,
                                                    training=item).exists() or item.user_create == request.user

        if check_access_level(request.user, 'pepreg', 'add_new_training') == 'System' or is_belong:
            managing = "true"
        else:
            managing = ""

        geo_location_shorter = " ".join(item.geo_location.split(",")[:3])

        row = [
            "",
            item.district.state.name if item.district else "",
            item.district.name if item.district else "",
            item.subject,
            item.pepper_course,
            item.name,
            item.description,
            str('{d:%m/%d/%Y}'.format(d=item.training_date)),
            str('{d:%I:%M %p}'.format(d=item.training_time_start)).lstrip('0'),
            str('{d:%I:%M %p}'.format(d=item.training_time_end)).lstrip('0'),
            "<span class='classroom'>%s</span><br><span class='geo_location'>%s</span><input type='hidden' value='%s'><input type='hidden' name='row_geo_location' value='%s'>" % (
            item.classroom, geo_location_shorter, item.geo_props, item.geo_location),
            item.credits,
            "<br>".join(instructor_names(item)),
            "%s %s" % (item.user_create.first_name, item.user_create.last_name),
            "",
            "<input type=hidden value=%s name=id> \
            <input type=hidden value=%s name=managing> \
            <input type=hidden value=%s name=all_edit> \
            <input type=hidden value=%s name=all_delete> \
            <input type=hidden value=%s,%s,%s,%s,%s,%s,%s name=status>" % (
                item.id, managing, all_edit, all_delete, arrive, status, allow,
                item.attendancel_id, rl, "1" if item.allow_student_attendance else "0",
                remain
            )
        ]
        rows.append(row)

    json_out = [count]
    json_out.append(rows)
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def save_training(request):
    try:
        id = request.POST.get("id", None)
        if id:
            training = PepRegTraining.objects.get(id=id)
            PepRegInstructor.objects.filter(training=training).delete()
        else:
            training = PepRegTraining()
            training.date_create = datetime.now(UTC)
            training.user_create = request.user

        training.type = request.POST.get("type", "")
        training.district_id = request.POST.get("district_id")
        if(request.POST.get("school_id")):
            training.school_id = request.POST.get("school_id")
        training.name = request.POST.get("name", "")
        training.description = request.POST.get("description", "")

        if training.type == "pepper_course":
            training.pepper_course = request.POST.get("pepper_course", "")
        else:
            training.pepper_course = ""
            training.credits = request.POST.get("credits", 0)
            training.attendancel_id = request.POST.get("attendancel_id", "")

        training.subject = request.POST.get("subject")
        training.training_date = request.POST.get("training_date", "")
        training.training_time_start = request.POST.get("training_time_start", "")
        training.training_time_end = request.POST.get("training_time_end", "")
        training.classroom = request.POST.get("classroom", "")
        training.geo_location = request.POST.get("geo_location", "")
        training.geo_props = request.POST.get("geo_props", "")

        training.allow_registration = request.POST.get("allow_registration", False)
        training.max_registration = request.POST.get("max_registration", 0)
        training.allow_attendance = request.POST.get("allow_attendance", False)
        training.allow_student_attendance = request.POST.get("allow_student_attendance", False)
        training.allow_validation = request.POST.get("allow_validation", False)
        training.user_modify = request.user
        training.date_modify = datetime.now(UTC)
        training.save()

        emails_get = request.POST.get("instructor_emails");
        if(emails_get):
            for emails in request.POST.get("instructor_emails", "").split(","):
                tmp1 = emails.split("::");
                email = tmp1[0];
                all_edit = True if tmp1[1] == "1" else False;
                all_delete = True if tmp1[2] == "1" else False;

                if User.objects.filter(email=email).exists():
                    pi = PepRegInstructor()
                    pi.training = training
                    pi.instructor = User.objects.get(email=email)
                    pi.date_create = datetime.now(UTC)
                    pi.user_create = request.user
                    pi.all_edit = all_edit;
                    pi.all_delete = all_delete;
                    pi.save()

    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_training(request):
    try:
        id = request.POST.get("id", None)
        training = PepRegTraining.objects.get(id=id)
        tid = training.id
        tname = training.name
        tdate = training.training_date
        PepRegInstructor.objects.filter(training=training).delete()
        PepRegStudent.objects.filter(training=training).delete()
        TrainingUsers.objects.filter(training=training).delete()
        training.delete()

        ma_db = myactivitystore()
        ma_db.set_item_pd(tid, tname, str(tdate))

    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def training_json(request):
    item = PepRegTraining.objects.get(id=request.GET.get("id"))

    instructor_emails = []
    for pi in PepRegInstructor.objects.filter(training=item):
        all_edit = "1" if pi.all_edit else "0"
        all_delete = "1" if pi.all_delete else "0"

        instructor_emails.append(pi.instructor.email + "::" + all_edit  + "::" + all_delete)

    arrive = "1" if datetime.now(UTC).date() >= item.training_date else "0"

    data = {
        "id": item.id,
        "type": item.type,
        "district_id": item.district_id,
        "school_id": item.school_id,
        "name": item.name,
        "description": item.description,
        "pepper_course": item.pepper_course,
        "subject": item.subject,
        "training_date": str('{d:%m/%d/%Y}'.format(d=item.training_date)),
        "training_time_start": str('{d:%I:%M %p}'.format(d=item.training_time_start)).lstrip('0'),
        "training_time_end": str('{d:%I:%M %p}'.format(d=item.training_time_end)).lstrip('0'),
        "classroom": item.classroom,
        "geo_location": item.geo_location,
        "geo_props": item.geo_props,
        "credits": item.credits,
        "attendancel_id": item.attendancel_id,
        "allow_registration": item.allow_registration,
        "max_registration":  '' if (item.max_registration == 0 or item.allow_registration == False) else item.max_registration,
        "allow_attendance": item.allow_attendance,
        "allow_validation": item.allow_validation,
        "instructor_emails": instructor_emails,
        "arrive": arrive
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def getCalendarInfo(request):
    name_dict = {};
    name_dict["title"] = now().strftime("%B %Y");
    name_dict["year"] = now().year;
    name_dict["month"] = now().month;

    return HttpResponse(json.dumps(name_dict), content_type="application/json");


def getCalendarMonth(request):
    SHIFT_WEEKSTART = 0;

    _year = request.GET.get('year');
    _month = request.GET.get('month');
    _year_n = request.GET.get('year_n');
    _month_n = request.GET.get('month_n');
    _day = request.GET.get('day');
    _day_n = request.GET.get('day_n');
    _getrange = request.GET.get('daterange'); #akogan
    _catype = request.GET.get('catype');

    _cal_view = request.GET.get('calview')

    if (_year):
        _year = int(_year);

    if (_month):
        _month = int(_month);

    if (_year_n):
        _year_n = int(_year_n);

    if (_month_n):
        _month_n = int(_month_n);

    if (_day):
        _day = int(_day);

    if (_day_n):
        _day_n = int(_day_n);

    if not _getrange:
        _getrange = "0"

    if not(_catype):
        _catype = "0";

    firstweekday = 0 + SHIFT_WEEKSTART
    while firstweekday < 0:
        firstweekday += 7
    while firstweekday > 6:
        firstweekday -= 7

    start = datetime(year=_year, month=_month, day=1, tzinfo=utc)  # 2016-08-01
    end = datetime(year=_year, month=_month, day=1, tzinfo=utc) + relativedelta(months=1)  # 2016-09-01

    name_dict = {"title": start.strftime("%B %Y")};

    columns = {
        # 1: ['district__state__name', '__iexact', 'str'],
        2: ['district__name', '__iexact', 'str']
    }
    filters = get_post_array(request.GET, 'fcol')
    #filters[1] = request.user.profile.district.state.name
    filters[2] = request.user.profile.district.name
    if len(filters):
        args, kwargs = build_filters(columns, filters)
        if args:
            all_occurrences = PepRegTraining.objects.prefetch_related().filter(args, **kwargs)
        else:
            all_occurrences = PepRegTraining.objects.prefetch_related().filter(**kwargs)
    else:
        all_occurrences = PepRegTraining.objects.prefetch_related().all()

    cal = calendar.Calendar()
    cal.setfirstweekday(firstweekday)

    current_day = datetime(year=_year_n, month=_month_n, day=_day_n, tzinfo=utc)  # 2016-08-01
    try:
        tmp_school_id = request.user.profile.school.id
    except:
        tmp_school_id = 0

    daterangelist = []
    #akogan datetime.
    if(_getrange=="0"):
        daterange = cal.itermonthdays(_year, _month)
    elif(_getrange=="1" or _getrange=="3"):
        weekNumber = date(year=_year, month=_month, day=_day).isocalendar()[1]
        daterange = getweekdays(_year, weekNumber, _getrange)
    else:
        getDay = datetime(year=_year, month=_month, day=_day)
        daterangelist.append(getDay)

    if not daterangelist:
        daterangelist = list(daterange)

    userObj = request.user
    request.session['user_obj'] = userObj

    # akogan
    if(_cal_view == 'screen'):
        name_dict["table_tr_content"] = build_screen_rows(request, _year, _month, _catype, all_occurrences, current_day, tmp_school_id, daterangelist)
    elif(_cal_view == 'print'):
        name_dict["table_tr_content"] = build_print_rows(request, _year, _month, _catype, all_occurrences, current_day, tmp_school_id, daterangelist)

    return HttpResponse(json.dumps(name_dict), content_type="application/json")

#akogan
def getweekdays(year, weekNumber, getrange):
    firstday = datetime.strptime('%04d-%02d-1' % (year, weekNumber), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        firstday -= timedelta(days=7)

    i = 0
    while (i < 7):
        yieldDay = firstday + timedelta(days=i)
        if(yieldDay.isoweekday() in (6, 7) and getrange == "3"):
            yield 0
        else:
            yield yieldDay
        i += 1

def build_print_rows(request, _year, _month, _catype, all_occurrences, current_day, tmp_school_id, daterangelist):
    print_row = [[]]
    i = 0
    array_length = len(all_occurrences)
    for item in all_occurrences:

        training_start_time = str('{d:%I:%M %p}'.format(d=item.training_time_start)).lstrip('0')

        print_row[i].append(item.name)
        print_row[i].append(item.description)
        print_row[i].append(item.training_date)
        print_row[i].append(training_start_time)
        print_row[i].append(item.classroom)
        print_row[i].append(item.geo_location)

        if(i < array_length - 1):
            i += 1
            print_row.append([])

    if(print_row):
        i = 0
        table_tr_content = ""
        while(i < array_length):
            table_tr_content += "<tr class='printview'>"

            table_tr_content += "<td style='position: relative; height: 100%; width: auto; border: 1px #ccc solid;'>" + str(print_row[i][0]) + "<br/>" + str(print_row[i][1]) +"</td>"
            table_tr_content += "<td style='position: relative; height: 100%; width: auto; border: 1px #ccc solid;'>" + str(print_row[i][2]) + "</td>"
            table_tr_content += "<td style='position: relative; height: 100%; width: auto; border: 1px #ccc solid;'>" + str(print_row[i][3]) + "</td>"
            table_tr_content += "<td style='position: relative; height: 100%; width: auto; border: 1px #ccc solid;'>" + str(print_row[i][4]) + "<br/>" + str(print_row[i][5]) + "</td>"

            table_tr_content += "</tr>"

            i += 1

        return table_tr_content

#akogan
def build_screen_rows(request, year, month, catype, all_occurrences, current_day, tmp_school_id, daterange):
    isweek = 1 if len(daterange) == 7 else 0
    isday = 1 if len(daterange) == 1 else 0
    rangedates = [[]]
    week = 0

    for day in daterange:
        current = False
        occurrences = []
        trainingStartTime = ""
        trainingEndTime = ""
        trainingStartHour = ""
        trainingEndHour = ""
        trainingStartHours = []
        trainingEndHours = []

        if day:
            if (isweek or isday):
                date = utc.localize(day)
            else:
                date = datetime(year=year, month=month, day=day, tzinfo=utc)
            for item in all_occurrences:
                if (item.training_date == date.date()):
                    if (item.school_id and item.school_id != -1 and item.school_id != tmp_school_id):
                        continue;

                    arrive = "1" if datetime.now(UTC).date() >= item.training_date else "0"
                    allow = "1" if item.allow_registration else "0"
                    r_l = "1" if reach_limit(item) else "0"
                    allow_student_attendance = "1" if item.allow_student_attendance else "0"
                    attendancel_id = item.attendancel_id

                    status = ""
                    try:
                        userObj = request.session.get('user_obj', None)
                        if PepRegStudent.objects.filter(student=userObj, training=item).exists():
                            status = PepRegStudent.objects.get(student=userObj, training=item).student_status
                    except:
                        status = ""
                    trainingStartTime = str('{d:%I:%M %p}'.format(d=item.training_time_start)).lstrip('0')
                    trainingEndTime = str('{d:%I:%M %p}'.format(d=item.training_time_end)).lstrip('0')

                    itemData = ""

                    if isday:
                        trainingStartMinutes = int(trainingStartTime[-5:-3])
                        if(trainingStartMinutes)<30:
                            trainingStartHour = trainingStartTime[0:-5] + "00" + trainingStartTime[-3:]
                        else:
                            trainingStartHour = trainingStartTime[0:-5] + "30" + trainingStartTime[-3:]

                        trainingEndMinutes = int(trainingEndTime[-5:-3])
                        if (trainingEndMinutes) < 30:
                            trainingEndHour = trainingEndTime[0:-5] + "00" + trainingEndTime[-3:]
                        else:
                            trainingEndHour = trainingEndTime[0:-5] + "30" + trainingEndTime[-3:]

                        trainingStartHours.append(trainingStartHour)
                        trainingEndHours.append(trainingEndHour)

                        itemData = "<br/><div>From: " + trainingStartTime + "<br/>\nTo: " + trainingEndTime

                    # &#13;
                    titlex = item.name + "::" + trainingStartTime + "::" + trainingEndTime

                    if item.classroom:
                        titlex = titlex + "::" + item.classroom
                        if isday: itemData += "<br/>\nClassroom: " + item.classroom

                    if item.geo_location:
                        titlex = titlex + "::" + item.geo_location
                        if isday: itemData += "<br/>\nLocation: " + item.geo_location

                    if isday: itemData += "</div>"

                    if (arrive == "0" and allow == "0"):
                        if (catype == "0" or catype == "4"):
                            occurrences.append("<span class='alert al_4' titlex='" + titlex + "'>" + item.name + "</span>"+itemData);

                    elif (arrive == "0" and allow == "1"):
                        if (status == "" and r_l == "1"):
                            if (catype == "0" or catype == "5"):
                                occurrences.append("<span class='alert al_7' titlex='" + titlex + "'>" + item.name + "</span>"+itemData);
                        else:
                            if (status == "Registered"):
                                # checked true
                                if (catype == "0" or catype == "3"):
                                    tmp_ch = "<input type = 'checkbox' class ='calendar_check_would' training_id='" + str(item.id) + "' checked /> ";
                                    occurrences.append("<label class='alert al_6' titlex='" + titlex + "'>" + tmp_ch + "<span>" + item.name + "</span>"+itemData+"</label>");

                            else:
                                # checked false
                                if (catype == "0" or catype == "2"):
                                    tmp_ch = "<input type = 'checkbox' class ='calendar_check_would' training_id='" + str(item.id) + "' /> ";
                                    occurrences.append("<label class='alert al_5' titlex='" + titlex + "'>" + tmp_ch + "<span>" + item.name + "</span>"+itemData+"</label>");

                    elif (arrive == "1" and status == "" and allow == "1"):
                        # The registration date has passed for this training
                        pass

                    elif (arrive == "1" and allow_student_attendance == "0"):
                        # Instructor records attendance.
                        pass

                    elif (arrive == "1" and allow_student_attendance == "1"):
                        if (status == "Attended" or status == "Validated"):
                            # checked true
                            if (catype == "0" or catype == "1"):
                                tmp_ch = "<input type = 'checkbox' class ='calendar_check_attended' training_id='" + str(item.id) + "' attendancel_id='" + attendancel_id + "' checked /> ";
                                occurrences.append("<label class='alert al_3' titlex='" + titlex + "'>" + tmp_ch + "<span>" + item.name + "</span>"+itemData+"</label>");

                        else:
                            # checked false
                            if (catype == "0" or catype == "3"):
                                tmp_ch = "<input type = 'checkbox' class ='calendar_check_attended' training_id='" + str(item.id) + "' attendancel_id='" + attendancel_id + "' /> ";
                                occurrences.append("<label class='alert al_6' titlex='" + titlex + "'>" + tmp_ch + "<span>" + item.name + "</span>"+itemData+"</label>");

            if date.__str__() == current_day.__str__():
                current = True

        rangedates[week].append([day, occurrences, current, trainingStartHours, trainingEndHours])

        if (not isweek and not isday):
            if len(rangedates[week]) == 7:
                rangedates.append([])
                week += 1

    table_tr_content = ""
    if isweek:
        colstyle = "style='min-height: 355px !important;'"
    elif isday:
        colstyle = "style='min-height: 590px !important;'"
    else:
        colstyle = "style='min-height: 60px;'"

    if isday:
        dayHours = []
        for p in range(2):
            for i in range(0, 13):
                if((p == 0 and i < 6) or i == 0): continue
                if (p == 0 and i < 12):
                    d = "AM"
                elif (p == 1 and i < 12) or (p == 0 and i == 12):
                    d = "PM"
                getHour = str(i) if i > 0 else "12"
                if ((p == 0) or i < 6): getHalfHour = getHour + ":30 " + d
                getHour += ":00 " + d
                dayHours.append(getHour)
                if ((p == 0) or i < 6): dayHours.append(getHalfHour)
                if (p == 1 and i == 6): break

    weekLen = len(rangedates) - 2
    for weekNum, week in enumerate(rangedates):
        if((not isweek and not isday) and weekNum == weekLen):
            addBorder = "border-bottom: 1px #ccc solid;"
        else:
            addBorder = ""

        table_tr_content += "<tr class='calendar-tr-tmp'>"

        if isday:
            table_tr_content += "<td style='position: relative; height: 100%; width: -moz-calc(2.5%) !important; width: -webkit-calc(2.5%) !important; width: calc(2.5%) !important;'>" \
                                "<div style='display: flex; flex-direction: column; justify-content: space-between; position: absolute; top:0px; bottom:0px; left:0px; width: 100%;'>";

            for dayHour in dayHours:
                table_tr_content += "<div style='display: block; width: 100%; box-sizing: border-box; height: 27px; padding: 5px; border-bottom: 1px solid #ccc; text-align: right; padding-right: 50px;'>" + dayHour + "</div>"

            table_tr_content += "</div></td>";

        for day in week:
            if(isweek or isday):
                if day[0] != 0: day[0]=day[0].day
            class_name = "";
            cell_border = "border-right: 1px solid #ccc;border-bottom: 1px solid #ccc;"
            if (day[0] == 0):
                class_name = "calendarium-empty";
                cell_border = ""
            elif (day[2]):
                class_name = "calendarium-current";
            else:
                class_name = "calendarium-day";

            if(not isday and day[0]):
                if(isweek and week[0][0] > day[0]):
                    nextMonth = "true"
                else:
                    nextMonth = "false"

                if(type(week[6][0]) is not datetime):
                    dateToCompare = week[6][0]
                else:
                    dateToCompare = week[6][0].day
                if (isweek and dateToCompare < day[0]):
                    prevMonth = "true"
                else:
                    prevMonth = "false"

                clickFunc = " onclick='pickDayOnClick(event, " + str(day[0]) + ", " + nextMonth + "," + prevMonth + "," + str(dateToCompare) + ")'"
            else:
                clickFunc = ""

            if(not (day[0] == 0 and isweek)):

                table_tr_content += "<td class='" + class_name + "' style='position: relative; height: 100%;"+cell_border+"'" + clickFunc +">"
                if (day[0]):
                    table_tr_content += "<div class='calendarium-relative' "+ colstyle +"><span class='calendarium-date'>" + str(day[0]) + "</span>";

                    if not isday:
                        for tmp1 in day[1]:
                            table_tr_content += tmp1;

                    if isday:
                        table_tr_content += "<div style='display: flex; flex-direction: column; justify-content: space-between; position: absolute; top:0px; bottom:0px; left:0px; width: 100%;'>";

                        for dayHour in dayHours:

                            divAdded = 0

                            if day[1]:
                                i = 0

                                table_tr_content += "<div class='training-row' style='display: block; width: 100%; box-sizing: border-box; padding: 0px; padding-left: 5px; border-bottom: 1px solid #ccc; height: 24px !important; text-align: right;' id='" + dayHour + "'>&nbsp;"
                                divAdded = 1

                                for tmp1 in day[1]:

                                    if(day[4][i] != "" and (day[3][i] != day[4][i])):
                                        h = 0
                                        endHour = 0
                                        startHour = int(day[3][i][:day[3][i].index(":")])
                                        startHourAMPM = day[3][i][-2:]
                                        startHour = startHour if(startHourAMPM == "AM" and startHour >= 6) else 6

                                        if((startHourAMPM == "PM" and (startHour == 12 or startHour <= 6)) or (startHourAMPM == "AM" and startHour >= 6)):
                                            endHour = int(day[4][i][:day[4][i].index(":")])
                                            endHourAMPM = day[4][i][-2:]

                                            h = startHour
                                            hourAMPM = "AM"

                                            if(startHourAMPM != endHourAMPM):
                                                endHourLast = endHour if(endHour == 12 or endHour <= 6) else 6
                                                endHour = 12
                                            else:
                                                endHour = endHour if(endHourAMPM == "AM" or endHour == 12 or endHour <= 6) else 6
                                                endHourLast = endHour

                                            while(h <= endHour):

                                                fullHour = str(h) + ":00 " + hourAMPM
                                                midHour = str(h) + ":30 " + hourAMPM

                                                firstHalfHour = int(day[3][i][day[3][i].index(":")+1:day[3][i].index(" ")]) < 30
                                                if ((fullHour == dayHour and firstHalfHour) or (midHour == dayHour and not firstHalfHour)): break

                                                h += 1
                                                if(h == endHour and endHour != endHourLast):
                                                    h = 1
                                                    endHour = endHourLast
                                                    hourAMPM = "PM"

                                        if (h <= endHour):
                                            t = day[3][i][-2:]
                                            dh = day[3][i][:day[3][i].index(":")] if len(day[3][i][:day[3][i].index(":")]) == 2 else "0" + day[3][i][:day[3][i].index(":")]
                                            table_tr_content += "<span class='" + t + " " + dh + " span-" + str(i) + "'>" + tmp1 + "</span>"

                                    i += 1

                            if ( not divAdded ):
                                table_tr_content += "<div class='training-row' style='display: block; width: 100%; box-sizing: border-box; padding: 5px; border-bottom: 1px solid #ccc; height: 26px !important; text-align: right;' id='" + dayHour + "'>&nbsp;"

                            table_tr_content += "</div>"

                        table_tr_content += "</div>"

                    table_tr_content += "</div>";

                table_tr_content += "</td>";

        table_tr_content += "</tr>";

    return table_tr_content;

def remove_student(student):
    if student.training.type == "pepper_course":
        CourseEnrollment.unenroll(student.student, student.training.pepper_course)
        CourseEnrollmentAllowed.objects.filter(email=student.student.email,
                                               course_id=student.training.pepper_course).delete()
    student.delete()


def register(request):
    try:
        join = request.POST.get("join", "false") == "true"
        training_id = request.POST.get("training_id")
        user_id = request.POST.get("user_id")
        training = PepRegTraining.objects.get(id=training_id)

        if user_id:
            student_user = User.objects.get(id=int(user_id))
        else:
            student_user = request.user

        if join:
            if reach_limit(training):
                raise Exception("Maximum number of users have registered for this training.")

            try:
                student = PepRegStudent.objects.get(training_id=training_id, student=student_user)
            except:
                student = PepRegStudent()
                student.user_create = request.user
                student.date_create = datetime.now(UTC)

            student.student = student_user
            student.student_status = "Registered"
            student.training_id = int(training_id)
            student.user_modify = request.user
            student.date_modify = datetime.now(UTC)
            student.save()

            ma_db = myactivitystore()
            my_activity = {"GroupType": "PDPlanner", "EventType": "PDTraining_registration", "ActivityDateTime": datetime.utcnow(), "UsrCre": request.user.id,
            "URLValues": {"training_id": training.id},
            "TokenValues": {"training_id": training.id},
            "LogoValues": {"training_id": training.id}}
            ma_db.insert_item(my_activity)

            if training.type == "pepper_course":
                cea, created = CourseEnrollmentAllowed.objects.get_or_create(email=student_user.email,
                                                                             course_id=training.pepper_course)
                cea.is_active = True
                cea.save()
                CourseEnrollment.enroll(student_user, training.pepper_course)

            #akogan
            mem = TrainingUsers.objects.filter(user=student_user, training=training)

            if not mem.exists():
                tu = TrainingUsers(user=student_user, training=training)
                tu.save()
        else:
            student = PepRegStudent.objects.get(training_id=training_id, student=student_user)
            remove_student(student)

            #akogan
            mem = TrainingUsers.objects.filter(user=student_user, training=training)
            
            if mem.exists():
                mem.delete()

    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True, 'training_id': training_id}), content_type="application/json")


def set_student_attended(request):
    try:
        training_id = int(request.POST.get("training_id"))
        student_id = int(request.POST.get("student_id"))
        yn = request.POST.get("yn", False)

        training = PepRegTraining.objects.get(id=training_id)
        try:
            student = PepRegStudent.objects.get(training_id=training_id, student_id=student_id)
        except:
            student = PepRegStudent()
            student.user_create = request.user
            student.date_create = datetime.now(UTC)
            student.training = training
            student.student = request.user

        student.user_modify = request.user
        student.date_modify = datetime.now(UTC)

        if yn == "true":
            student.student_status = "Attended"
            if not training.allow_validation:
                student.student_credit = training.credits
            student.save()
        else:
            if training.allow_registration:
                student.student_status = "Registered"
                student.student_credit = 0
                student.save()
            else:
                student.delete()
                student = None

        if student:
            data = {"id": student.id,
                    "email": student.student.email,
                    "status": student.student_status,
                    "is_attended": student.student_status == "Validated" or student.student_status == "Attended",
                    "is_validated": student.student_status == "Validated",
                    "student_credit": student.student_credit,
                    "student_id": student.student_id,
                    }
        else:
            data = None

    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True, 'data': data}), content_type="application/json")


def set_student_validated(request):
    try:
        training_id = int(request.POST.get("training_id"))
        student_id = int(request.POST.get("student_id"))
        yn = request.POST.get("yn", False)

        training = PepRegTraining.objects.get(id=training_id)
        student = PepRegStudent.objects.get(training_id=training_id, student_id=student_id)

        student.user_modify = request.user
        student.date_modify = datetime.now(UTC)

        if yn == "true":
            student.student_status = "Validated"
            student.student_credit = training.credits
            student.save()
        else:
            student.student_status = "Attended"
            student.student_credit = 0

        student.save()

        data = {"id": student.id,
                "email": student.student.email,
                "status": student.student_status,
                "is_attended": student.student_status == "Validated" or student.student_status == "Attended",
                "is_validated": student.student_status == "Validated",
                "student_credit": student.student_credit,
                "student_id": student.student_id,
                }

    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True, 'data': data}), content_type="application/json")


def student_list(request):
    print "student_list"
    logging.warning('student_list')
    try:
        training_id = request.POST.get("training_id")
        print training_id
        training = PepRegTraining.objects.get(id=training_id)
        students = PepRegStudent.objects.filter(training_id=training_id)
        arrive = datetime.now(UTC).date() >= training.training_date
        student_limit = reach_limit(training) # akogan
        rows = []
        for item in students:
            rows.append({
                "id": item.id,
                "email": item.student.email,
                "status": item.student_status,
                "is_attended": item.student_status == "Validated" or item.student_status == "Attended",
                "is_validated": item.student_status == "Validated",
                "student_credit": item.student_credit,
                "student_id": item.student_id,
            })
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    last_date = training.last_date
    if last_date:
        last_date = str('{d:%m/%d/%Y}'.format(d=training.last_date));

    return HttpResponse(json.dumps({'success': True,
                                    'rows': rows,
                                    'allow_attendance': training.allow_attendance,
                                    'allow_validation': training.allow_validation,
                                    'allow_registration': training.allow_registration,
                                    'training_id': training.id,
                                    'training_name': training.name,
                                    'last_date': last_date,
                                    'training_type': training.type,
                                    'training_date': str('{d:%m/%d/%Y}'.format(d=training.training_date)),
                                    'arrive': arrive,
                                    'student_limit': student_limit # akogan
                                    }),
                        content_type="application/json")


def get_courses_drop(state_name, district_code):
    matches_state = [None, "ALL", district_code]
    matches_district = [None, "ALL", state_name]

    courses = modulestore().collection.find({'_id.category': 'course', 'metadata.display_state': state_name})

    if courses.count() > 0:
        matches_state.append('ALL')

    courses = modulestore().collection.find({'_id.category': 'course', 'metadata.display_district': district_code})
    if courses.count() > 0:
        matches_district.append('ALL')

    flt = {
        '_id.category': 'course',
        'metadata.display_state': {'$in': matches_district},
        'metadata.display_district': {'$in': matches_state}
    }


    courses = modulestore().collection.find(flt).sort("metadata.display_name", pymongo.ASCENDING)
    courses = modulestore()._load_items(list(courses), 0)
    return courses


def show_map(request):
    training_id = request.GET.get("training_id")
    district_id = request.GET.get("district_id")

    if (district_id):
        r = list()
        district = District.objects.get(id=district_id)
        if district:
            data = School.objects.filter(district=district).order_by('name')
            for item in data:
                r.append({'id': item.id, 'name': item.name, 'code': item.code});

        return HttpResponse(json.dumps(r), content_type="application/json")
    else:
        training = PepRegTraining.objects.get(id=training_id)
        return render_to_response('administration/pepreg_map.html', {"training": training})


def delete_student(request):
    try:
        id = int(request.POST.get("id"))
        user = PepRegStudent.objects.get(id=id).student
        remove_student(PepRegStudent.objects.get(id=id))
        TrainingUsers.objects.filter(user=user).delete()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def download_students_excel(request):
    training_id = request.GET.get("training_id")
    last_date = request.GET.get("last_date")
    flag_pdf = request.GET.get("pdf")

    training = PepRegTraining.objects.get(id=training_id)

    if(last_date):
        name_dict = {};
        _res = "0";
        try:
            EMAIL_TEMPLATE_DICT = {'training_email': ('emails/training_student_email_subject.txt', 'emails/training_student_email_message.txt')}

            subject_template, message_template = EMAIL_TEMPLATE_DICT.get("training_email", (None, None))

            email_students = [];

            for reg_stu in PepRegStudent.objects.filter(training_id=training_id, student_status="Registered"):
                userx = User.objects.get(id=reg_stu.student_id)
                email_students.append(userx.email);

                param_dict = {};
                param_dict["training_name"] = training.name;
                param_dict["training_date"] = str('{d:%m-%d-%Y}'.format(d=training.training_date));
                param_dict["first_name"] = userx.first_name;
                param_dict["last_name"] = userx.last_name;
                param_dict["district_name"] = training.district.name;
                param_dict["training_time_start"] = str('{d:%I:%M %p}'.format(d=training.training_time_start)).lstrip('0');

                if training.classroom == "" and training.geo_location == "":
                    param_dict["classroom"] = "";
                    param_dict["geo_location"] = "";

                elif not training.classroom == "" and training.geo_location == "":
                    param_dict["classroom"] = training.classroom;
                    param_dict["geo_location"] = "";

                elif training.classroom == "" and not training.geo_location == "":
                    param_dict["classroom"] = "";
                    param_dict["geo_location"] = training.geo_location;

                else:
                    param_dict["classroom"] = training.classroom + ", ";
                    param_dict["geo_location"] = training.geo_location;

                subject = render_to_string(subject_template, param_dict)
                message = render_to_string(message_template, param_dict)

                # _res = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [userx.email], fail_silently=False)
                msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [userx.email])
                msg.content_subtype = "html"
                msg.send()

            training.last_date = last_date;
            training.save()

            _res = "1";
        except Exception as e:
            _res = '%s' % e

        name_dict["_res"] = _res;
        return HttpResponse(json.dumps(name_dict), content_type="application/json");

    elif(flag_pdf):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + training.name + flag_pdf + '.pdf"'

        buffer = BytesIO()

        c = canvas.Canvas(buffer, pagesize=A4)

        # ------------------------------------------------------------------------------------logo
        try:
            logo = ImageReader("https://" + request.get_host() + '/static/images/pd_pdf2.png')
        except:
            logo = ImageReader("http://" + request.get_host() + '/static/images/pd_pdf2.png')

        c.drawImage(logo, 330, 750, 200, 73);

        c.setFont("Helvetica", 20)
        c.drawString(370, 710, "PD Planner")
        c.drawString(370, 680, "SignUp")

        styleSheet = getSampleStyleSheet()
        style = styleSheet['BodyText']
        style.fontName = "Helvetica"
        style.fontSize = 16
        style.leading = 15
        training_name = "Training Name: " + training.name
        content_width = stringWidth(training_name, "Helvetica", 16)
        p = Paragraph(training_name, style)
        w1 = 520
        h1 = 800
        w2, h2 = p.wrap(w1, h1)
        p.drawOn(c, 50, 625)

        c.setFont("Helvetica", 16)
        c.drawString(50, 600, "Training Date: " + str('{d:%m/%d/%Y}'.format(d = training.training_date)))
        # c.drawString(50, 578, "Instructor:")

        instructor_y = 575

        tmp_flag = 0;
        instructor_name = "Instructor: ";
        for reg_stu in PepRegInstructor.objects.filter(training_id=training_id):
            if tmp_flag == 0:
                tmp_flag += 1;
                instructor_name += reg_stu.instructor.first_name + " " + reg_stu.instructor.last_name;
            else:
                instructor_name += ", " + reg_stu.instructor.first_name + " " + reg_stu.instructor.last_name;

        style1 = styleSheet['BodyText']
        style1.fontName = "Helvetica"
        style1.fontSize = 16
        style1.leading = 15

        p1 = Paragraph(instructor_name, style1)
        w2 = 520
        h2 = 800
        w2, h2 = p1.wrap(w2, h2)
        if (h2 == 15):
            p1.drawOn(c, 50, instructor_y + 3)
        elif (h2 == 30):
            p1.drawOn(c, 50, instructor_y - 13)
        elif (h2 == 45):
            p1.drawOn(c, 50, instructor_y - 23)

        # ------------------------------------------------------------------------------------head
        c.setFillColor(colors.lawngreen)  # C7,F4,65

        base_table_y = 510;
        c.rect(10, base_table_y, 80, 30, fill=1)
        c.rect(90, base_table_y, 80, 30, fill=1)
        c.rect(170, base_table_y, 90, 30, fill=1)
        c.rect(260, base_table_y, 90, 30, fill=1)
        c.rect(350, base_table_y, 70, 30, fill=1)
        c.rect(420, base_table_y, 160, 30, fill=1)

        c.setStrokeColor(colors.black)
        c.setFillColor(colors.black)  # C7,F4,65
        c.setFont("Helvetica", 10)

        c.drawCentredString(50, base_table_y + 10, "First Name")
        c.drawCentredString(130, base_table_y + 10, "Last Name")
        c.drawCentredString(215, base_table_y + 10, "Email Address")
        c.drawCentredString(305, base_table_y + 10, "School Site")
        c.drawCentredString(385, base_table_y + 10, "Employee ID")
        c.drawCentredString(505, base_table_y + 10, "Signature")

        # ------------------------------------------------------------------------------------tr
        base_font_size = 8;
        ty = base_table_y;
        student_index = 0;
        studentList = PepRegStudent.objects.filter(training_id=training_id);
        lastpos = len(studentList) - 1;

        table_style = styleSheet['BodyText']
        table_style.fontName = "Helvetica"
        table_style.fontSize = base_font_size
        table_style.leading = 10
        c.setFont("Helvetica", base_font_size)
        for reg_stu in studentList:
            tr_height = 30

            pro = UserProfile.objects.get(user_id=reg_stu.student.id)

            if (pro):
                tmp_name = "";
                try:
                    tmp_name = pro.school.name
                except:
                    tmp_name = ""

                if (tmp_name.find("Elementary") > -1):
                    tmp_name = tmp_name.split("Elementary")[0];

                elif (tmp_name.find("Middle") > -1):
                    tmp_name = tmp_name.split("Middle")[0];

                elif (tmp_name.find("High") > -1):
                    tmp_name = tmp_name.split("High")[0];

                tmp_email_width = stringWidth(tmp_name, "Helvetica", base_font_size)
                if (tmp_email_width > 80):
                    p = Paragraph(tmp_name, table_style)
                    w2, h2 = p.wrap(80, 100)
                    h2 += 10
                    if (h2 > tr_height):
                        tr_height = h2

                    p.drawOn(c, 265, ty - tr_height + 5)
                else:
                    c.drawCentredString(305, ty - 15, tmp_name)

            ty -= tr_height;

            c.rect(10, ty, 80, tr_height, fill=0)
            c.rect(90, ty, 80, tr_height, fill=0)
            c.rect(170, ty, 90, tr_height, fill=0)
            c.rect(260, ty, 90, tr_height, fill=0)
            c.rect(350, ty, 70, tr_height, fill=0)
            c.rect(420, ty, 160, tr_height, fill=0)

            if (reg_stu.student.first_name):
                tmp_email_width = stringWidth(reg_stu.student.first_name, "Helvetica", base_font_size)
                if (tmp_email_width > 75):
                    frist_tmp1 = int(len(reg_stu.student.first_name) / 3)
                    while 1:
                        frist_tmp2 = stringWidth(reg_stu.student.first_name[0: frist_tmp1], "Helvetica", base_font_size)
                        if(frist_tmp2 > 70):
                            break;
                        else:
                            frist_tmp1 += 1

                    c.drawString(13, ty + tr_height - 13, reg_stu.student.first_name[0: frist_tmp1])
                    c.drawString(13, ty + tr_height - 23, reg_stu.student.first_name[frist_tmp1:])
                else:
                    c.drawCentredString(50, ty + tr_height - 15, reg_stu.student.first_name)

            if (reg_stu.student.last_name):
                tmp_email_width = stringWidth(reg_stu.student.last_name, "Helvetica", base_font_size)
                if (tmp_email_width > 75):
                    frist_tmp1 = int(len(reg_stu.student.last_name) / 3)
                    while 1:
                        frist_tmp2 = stringWidth(reg_stu.student.last_name[0: frist_tmp1], "Helvetica", base_font_size)
                        if (frist_tmp2 > 70):
                            break;
                        else:
                            frist_tmp1 += 2

                    c.drawString(93, ty + tr_height - 13, reg_stu.student.last_name[0: frist_tmp1])
                    c.drawString(93, ty + tr_height - 23, reg_stu.student.last_name[frist_tmp1:])
                else:
                    c.drawCentredString(130, ty + tr_height - 15, reg_stu.student.last_name)

            if (reg_stu.student.email):
                tmp_email_width = stringWidth(reg_stu.student.email, "Helvetica", base_font_size)
                if (tmp_email_width > 80):
                    frist_tmp1 = len(reg_stu.student.email) / 2
                    while 1:
                        frist_tmp2 = stringWidth(reg_stu.student.email[0: frist_tmp1], "Helvetica", base_font_size)
                        if (frist_tmp2 > 80):
                            break;
                        else:
                            frist_tmp1 += 2

                    c.drawString(173, ty + tr_height - 13, reg_stu.student.email[0: frist_tmp1])
                    c.drawString(173, ty + tr_height - 23, reg_stu.student.email[frist_tmp1:])
                else:
                    c.drawCentredString(215, ty + tr_height - 15, reg_stu.student.email)

            if student_index == lastpos:
                c.showPage()
            else:
                if (ty < 60):
                    ty = 790;
                    pdf_first_flag = False;
                    c.showPage()
                    c.setStrokeColor(colors.black)
                    c.setFillColor(colors.black)  # C7,F4,65s
                    c.setFont("Helvetica", base_font_size)

                student_index += 1;

        c.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        students = PepRegStudent.objects.filter(training_id=training_id)

        output = StringIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        FIELDS = ["email", "status", "attendance", "validation", "credits"]
        TITLES = ["User", "Status", "Attendance", "Validation", "Credits"]

        for i, k in enumerate(TITLES):
            worksheet.write(0, i, k)

        row = 1

        for item in students:
            if training.allow_attendance:
                attendance = "Y" if (item.student_status == "Validated" or item.student_status == "Attended") else "N"
            else:
                attendance = ""

            if training.allow_validation:
                validation = "Y" if (item.student_status == "Validated") else "N"
            else:
                validation = ""

            data_row = {'email': item.student.email,
                        'status': item.student_status,
                        'attendance': attendance,
                        'validation': validation,
                        'credits': item.student_credit
                        }

            for i, k in enumerate(FIELDS):
                worksheet.write(row, i, data_row[k])
            row = row + 1

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s_users.xlsx' % (training.name)
        workbook.close()
        response.write(output.getvalue())
        return response

def download_students_pdf(request):
    training_id = request.GET.get("training_id")
    training = PepRegTraining.objects.get(id=training_id)

    students = PepRegStudent.objects.filter(training_id=training_id)

    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    FIELDS = ["email", "status", "attendance", "validation", "credits"]
    TITLES = ["User", "Status", "Attendance", "Validation", "Credits"]

    for i, k in enumerate(TITLES):
        worksheet.write(0, i, k)

    row = 1

    for item in students:
        if training.allow_attendance:
            attendance = "Y" if (item.student_status == "Validated" or item.student_status == "Attended") else "N"
        else:
            attendance = ""

        if training.allow_validation:
            validation = "Y" if (item.student_status == "Validated") else "N"
        else:
            validation = ""

        data_row = {'email': item.student.email,
                    'status': item.student_status,
                    'attendance': attendance,
                    'validation': validation,
                    'credits': item.student_credit
                    }

        for i, k in enumerate(FIELDS):
            worksheet.write(row, i, data_row[k])
        row = row + 1

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s_users.xlsx' % (training.name)
    workbook.close()
    response.write(output.getvalue())
    return response
