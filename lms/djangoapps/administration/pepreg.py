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
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State
from xmodule.modulestore.django import modulestore
import pymongo

from student.models import (Registration, UserProfile, TestCenterUser, TestCenterUserForm,
                            TestCenterRegistration, TestCenterRegistrationForm,
                            PendingNameChange, PendingEmailChange,
                            CourseEnrollment, unique_id_for_user,
                            get_testcenter_registration, CourseEnrollmentAllowed)



@login_required
def index(request):
    # courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    # courses = sorted(courses, key=lambda course: course.display_name.lower())

    courses = get_courses_drop(request.user.profile.district.state.name, request.user.profile.district.code)
    
    return render_to_response('administration/pepreg.html', {"courses": courses})


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
    return training.max_registration > 0 and PepRegStudent.objects.filter(training=training).count() >= training.max_registration


def instructor_names(training):
    names = ["%s %s" % (training.user_create.first_name, training.user_create.last_name)]
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
        8: ['training_time', '__iexact', 'str'],
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
    if check_access_level(request.user, 'pepreg', 'add_new_training') != "System":
        filters[1] = request.user.profile.district.state.name
        filters[2] = request.user.profile.district.name

    if len(filters):
        args, kwargs = build_filters(columns, filters)
        if args:
            trainings = PepRegTraining.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            trainings = PepRegTraining.objects.prefetch_related().filter(**kwargs).order_by(*order)
    else:
        trainings = PepRegTraining.objects.prefetch_related().all().order_by(*order)

    count = trainings.count()
    json_out = [count]
    rows = list()

    for item in trainings[start:end]:
        arrive = "1" if datetime.now(UTC).date() >= item.training_date else "0"
        allow = "1" if item.allow_registration else "0"
        rl = "1" if reach_limit(item) else "0"
        
        status = ""
        if PepRegStudent.objects.filter(student=request.user, training=item).exists():
            status = PepRegStudent.objects.get(student=request.user, training=item).student_status

        is_belong = PepRegInstructor.objects.filter(instructor=request.user, training=item).exists() or item.user_create == request.user

        if check_access_level(request.user, 'pepreg', 'add_new_training') == 'System' or is_belong:
            managing = "true"
        else:
            managing = ""
        
        row = [
            "",
            item.district.state.name if item.district else "",
            item.district.name if item.district else "",
            item.subject,
            item.pepper_course,
            item.name,
            item.description,
            str('{d:%m/%d/%Y}'.format(d=item.training_date)),
            str('{d:%I:%M %p}'.format(d=item.training_time)).lstrip('0'),
            "<span class='classroom'>%s</span><br><span class='geo_location'>%s</span><input type='hidden' value='%s'>" % (item.classroom, item.geo_location, item.geo_props),
            item.credits,
            "<br>".join(instructor_names(item)),
            "",
            "<input type=hidden value=%s name=id> \
            <input type=hidden value=%s name=managing> \
            <input type=hidden value=%s,%s,%s,%s,%s,%s name=status>" % (
                item.id, managing, arrive, status, allow, item.attendancel_id, rl, "1" if item.allow_student_attendance else "0")
            ]
        rows.append(row)
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
        training.training_time = request.POST.get("training_time", "")
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

        for email in request.POST.get("instructor_emails", "").split(","):
            if User.objects.filter(email=email).exists():
                pi = PepRegInstructor()
                pi.training = training
                pi.instructor = User.objects.get(email=email)
                pi.date_create = datetime.now(UTC)
                pi.user_create = request.user
                pi.save()
        
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_training(request):
    try:
        id = request.POST.get("id", None)
        training = PepRegTraining.objects.get(id=id)
        PepRegInstructor.objects.filter(training=training).delete()
        PepRegStudent.objects.filter(training=training).delete()
        training.delete()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def training_json(request):
    item = PepRegTraining.objects.get(id=request.GET.get("id"))

    instructor_emails = []
    for pi in PepRegInstructor.objects.filter(training=item):
        instructor_emails.append(pi.instructor.email)

    arrive = "1" if datetime.now(UTC).date() >= item.training_date else "0"
        
    data = {
        "id": item.id,
        "type": item.type,
        "district_id": item.district_id,
        "name": item.name,
        "description": item.description,
        "pepper_course": item.pepper_course,
        "subject": item.subject,
        "training_date": str('{d:%m/%d/%Y}'.format(d=item.training_date)),
        "training_time": str('{d:%I:%M %p}'.format(d=item.training_time)).lstrip('0'),
        "classroom": item.classroom,
        "geo_location": item.geo_location,
        "geo_props": item.geo_props,
        "credits": item.credits,
        "attendancel_id": item.attendancel_id,
        "allow_registration": item.allow_registration,
        "max_registration": item.max_registration,
        "allow_attendance": item.allow_attendance,
        "allow_validation": item.allow_validation,
        "instructor_emails": instructor_emails,
        "arrive": arrive
        }
    
    return HttpResponse(json.dumps(data), content_type="application/json")


def remove_student(student):
    if student.training.type == "pepper_course":
        CourseEnrollment.unenroll(student.student, student.training.pepper_course)
        CourseEnrollmentAllowed.objects.filter(email=student.student.email, course_id=student.training.pepper_course).delete()
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

            if training.type == "pepper_course":
                cea, created = CourseEnrollmentAllowed.objects.get_or_create(email=student_user.email, course_id=training.pepper_course)
                cea.is_active = True
                cea.save()
                CourseEnrollment.enroll(student_user, training.pepper_course)
        else:
            student = PepRegStudent.objects.get(training_id=training_id, student=student_user)
            remove_student(student)
    
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


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
    try:
        training_id = request.POST.get("training_id")
        training = PepRegTraining.objects.get(id=training_id)
        students = PepRegStudent.objects.filter(training_id=training_id)
        arrive = datetime.now(UTC).date() >= training.training_date
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

    return HttpResponse(json.dumps({'success': True,
                                    'rows': rows,
                                    'allow_attendance': training.allow_attendance,
                                    'allow_validation': training.allow_validation,
                                    'training_id': training.id,
                                    'training_name': training.name,
                                    'arrive': arrive
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
        'metadata.display_state':  {'$in': matches_district},
        'metadata.display_district': {'$in': matches_state}
        }
    
    courses = modulestore().collection.find(flt).sort("metadata.display_name", pymongo.ASCENDING)
    courses = modulestore()._load_items(list(courses), 0)
    return courses


def show_map(request):
    training_id = request.GET.get("training_id")
    training = PepRegTraining.objects.get(id=training_id)
    return render_to_response('administration/pepreg_map.html', {"training": training})


def delete_student(request):
    try:
        id = int(request.POST.get("id"))
        remove_student(PepRegStudent.objects.get(id=id))
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def download_students_excel(request):
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
        row = row+1
            
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s_users.xlsx' % (training.name)
    workbook.close()
    response.write(output.getvalue())
    return response

