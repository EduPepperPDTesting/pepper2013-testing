from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse
# from django.shortcuts import redirect
# from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link
# from student.models import ResourceLibrary,StaticContent
# from collections import deque
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

# from django.contrib.auth.models import User
from student.models import UserProfile,Registration,CourseEnrollmentAllowed
# from django import db
import random
import json
# import time
import logging
import csv

# import multiprocessing
from multiprocessing import Process, Queue, Pipe
from django.core.validators import validate_email, validate_slug, ValidationError

import gevent
from django import db
from models import *
from io import StringIO
from student.models import Transaction, District, Cohort, School, State
from mail import send_html_mail
from datetime import datetime, timedelta
from pytz import UTC

from mako.template import Template
import mitxmako

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.db.models import F

log = logging.getLogger("tracking")
USER_CSV_COLS = ('email', 'state_name', 'district_name',)

# from gevent import monkey


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


def render_from_string(template_string, dictionary, context=None, namespace='main'):
    context_instance = Context(dictionary)
    # add dictionary to context_instance
    context_instance.update(dictionary or {})
    # collapse context_instance to a single dictionary for mako
    context_dictionary = {}
    context_instance['settings'] = settings
    context_instance['MITX_ROOT_URL'] = settings.MITX_ROOT_URL
    context_instance['marketing_link'] = marketing_link

    # In various testing contexts, there might not be a current request context.
    if mitxmako.middleware.requestcontext is not None:
        for d in mitxmako.middleware.requestcontext:
            context_dictionary.update(d)
    for d in context_instance:
        context_dictionary.update(d)
    if context:
        context_dictionary.update(context)
    # fetch and render template
    raw_template = Template(template_string)
    return raw_template.render_unicode(**context_dictionary)


def random_mark(length):
    assert(length>0)
    return "".join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890@#$%^&*_+{};~', length))


def paging(all, size, page):
    try:
        page = int(page)
    except Exception:
        page = 1
    try:
        size = int(size)
    except Exception:
        size = 1
    paginator = Paginator(all, size)
    if page < 1:
        page = 1
    if page > paginator.num_pages:
        page = paginator.num_pages
    data = paginator.page(page)
    return data


def postpone(function):
    def decorator(*args, **kwargs):
        p = Process(target=function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()
    return decorator


def log_task_executor(user, operation):
    executor_log = TaskExecutorLog()
    executor_log.user = user
    executor_log.operation = operation
    executor_log.execute_date = datetime.now(UTC)
    executor_log.save()


@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
    # from django.contrib.sessions.models import Session
    return render_to_response('administration/pepconn.html', {})


#* -------------- User Data Import -------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user_submit(request):
    log_task_executor(request.user,'user data import')
    
    # monkey.patch_all(socket=False)
    
    if request.method == 'POST':
        # district_id=request.POST.get("district")
        # school_id=request.POST.get("school")

        # output_pipe,input_pipe=multiprocessing.Pipe()
        # request.session['task']=''

        #** readlines from csv
        output = StringIO(newline=None)
        file = request.FILES.get('file')
        output.write(unicode(file.read()))
        r = csv.reader(output.getvalue(), dialect=csv.excel)

        rl = []
        rl.extend(r)

        #** create task
        task = ImportTask()
        task.filename = file.name
        # task.total_lines=100
        task.total_lines = len(rl);
        task.save()
        db.transaction.commit()

        #** close connection before import
        # http://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
        from django.db import connection 
        connection.close()

        #** begin import
        do_import_user(task, rl, request)
        
        return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")


def import_user_progress(request):
    try:
        task = ImportTask.objects.get(id=request.POST.get('taskId'))
        j = json.dumps({'task': task.filename, 'percent': '%.2f' % (task.process_lines*100/task.total_lines)})
    except Exception as e:
        j = json.dumps({'task': 'no', 'percent':100})
    return HttpResponse(j, content_type="application/json")


@postpone
def do_import_user(task, csv_lines, request):
    gevent.sleep(0)

    # district_id=request.POST.get("district")
    # school_id=request.POST.get("school")

    #** import into district
    # district=District.objects.get(id=district_id)
    
    send_registration_email = request.POST.get('send_registration_email') == 'true'

    #** ==================== importing
    count_success = 0
    
    for i, line in enumerate(csv_lines):
        try:
            #** record processed count
            task.process_lines = i + 1
            
            email = line[USER_CSV_COLS.index('email')]
            state_name = line[USER_CSV_COLS.index('state_name')]
            district_name = line[USER_CSV_COLS.index('district_name')]
            
            #** generating origin username
            username = random_mark(20)
            
            #** create log
            tasklog = ImportTaskLog()
            tasklog.username = username
            tasklog.email = email
            tasklog.create_date = datetime.now(UTC)
            tasklog.district_name = district_name
            tasklog.line = i + 1
            tasklog.task = task
            tasklog.error = "ok"
              
            validate_user_cvs_line(line)

            state = State.objects.get(name=state_name)
            district = District.objects.get(state=state, name=district_name)

            #** user
            user = User(username=username, email=email, is_active=False)
            user.set_password(username)
            user.save()

            #** registration
            registration = Registration()
            registration.register(user)

            #** profile
            profile = UserProfile(user=user)
            profile.district = district
            profile.subscription_status = "Imported"
            # if school_id:
            #     profile.school=School.objects.get(id=school_id)
            profile.save()

            #** course enroll
            cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
            cea.is_active = True
            cea.auto_enroll = True
            cea.save()

            #** send activation email if required
            if send_registration_email:
                try:
                    reg = Registration.objects.get(user=user)
                    props = {'key': reg.activation_key, 'district': district.name, 'email': email}

                    use_custom = request.POST.get("customize_email")
                    if use_custom == 'true':
                        custom_email = request.POST.get("custom_email_001")
                        custom_email_subject = request.POST.get("custom_email_subject")
                        subject = render_from_string(custom_email_subject, props)
                        body = render_from_string(custom_email, props)
                    else:
                        subject = render_to_string('emails/activation_email_subject.txt', props)
                        body = render_to_string('emails/activation_email.txt', props)

                    subject = ''.join(subject.splitlines())

                    send_html_mail(subject, body, settings.SUPPORT_EMAIL, ['mailfcl@126.com', email])
                except Exception as e:
                    raise Exception("Failed to send registration email %s" % e)
            
        except Exception as e:
            db.transaction.rollback()
            tasklog.error = "%s" % e
            log.debug("import error: %s" % e)

        finally:
            count_success += 1
            task.success_lines = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            try:
                tasklog.save()
            except UnboundLocalError:
                log.debug("line error: %s" % line)
            db.transaction.commit()

    #** post process
    tasklogs = ImportTaskLog.objects.filter(task=task)
    if len(tasklogs):
        FIELDS = ["line", "username", "email", "district", "create_date", "error"]
        TITLES = ["Line", "Username", "Email", "District", "Create Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row = {"line": d.line,
                   "username": d.username,
                   "email": d.email,
                   "district": d.district_name,
                   "create_date": d.create_date,
                   "error": d.error
                   }
            writer.writerow(row)
        output.seek(0)
        attach = [{'filename': 'log.csv', 'mimetype': 'text/csv', 'data': output.read()}]
        send_html_mail("User Data Import Report",
                       "Report of importing %s, see attachment." % task.filename,
                       settings.SUPPORT_EMAIL, ['mailfcl@126.com', request.user.email], attach)
        output.close()


def validate_user_cvs_line(line):
    #** check field count
    n = 0
    for item in line:
        if len(item.strip()):
            n += 1
    if n != len(USER_CSV_COLS):
        raise Exception("Wrong fields count")

    #** email
    email = line[USER_CSV_COLS.index('email')]
    validate_email(email)

    #** check user exists
    if len(User.objects.filter(email=email)) > 0:
        raise Exception("An account with the Email '{email}' already exists".format(email=email))


def import_user_tasks(request):
    tasks = []
    recent = datetime.now(UTC) - timedelta(seconds=300)
    timeout = datetime.now(UTC) - timedelta(minutes=5)
    for t in ImportTask.objects.filter(Q(process_lines__lt=F('total_lines')) | Q(update_time__gte=recent)).order_by("-id"):
        task = {"type": "import", "id": t.id, "filename": t.filename, "progress": t.process_lines*100/t.total_lines, "error": False}
        if t.update_time <= timeout:
            task['error'] = True
        tasks.append(task)

    for t in EmailTask.objects.filter(Q(process_emails__lt=F('total_emails')) | Q(update_time__gte=recent)).order_by("-id"):
        task = {"type": "email", "id": t.id, "progress": t.process_emails*100/t.total_emails, "error": False}
        if t.update_time <= timeout:
            task['error'] = True
        tasks.append()
     
    return HttpResponse(json.dumps({'success': True, 'tasks': tasks}), content_type="application/json")


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


def registration_table(request):
    data = UserProfile.objects.all().select_related('User')

    data = UserProfile.objects.all()
    data = registration_filter_user(request.GET, data)

    if request.GET.get('sortField', None):
        if request.GET.get('sortOrder') == 'desc':
            data = data.order_by("-" + request.GET.get('sortField'))
        else:
            data = data.order_by(request.GET.get('sortField'))
    
    page = request.GET.get('page')
    size = request.GET.get('size')
    data = paging(data, size, page)

    rows = []
    pagingInfo = {'page': data.number, 'pages': data.paginator.num_pages, 'total': data.paginator.count}

    for p in data:
        date = p.activate_date.strftime('%b-%d-%y %H:%M:%S') if p.activate_date else ''
        
        rows.append({'id': p.user.id,
                     'user__email': p.user.email,
                     'user__first_name': p.user.first_name,
                     'user__last_name': p.user.last_name,
                     'district': p.district.name if p.district_id else '',
                     'activate_date': date,
                     "subscription_status": p.subscription_status
                     })

    return HttpResponse(json.dumps({'rows': rows, 'paging': pagingInfo}), content_type="application/json")


#* -------------- Favorite Filter -------------

@login_required
@user_passes_test(lambda u: u.is_superuser)    
def favorite_filter_load(request):
    favs = []
    
    # favs=[{'id':1,'name':'Alabama','filter':{'state':1,'district':34,'school':1406}}]

    for ff in FilterFavorite.objects.filter(user=request.user).order_by('name'):
        favs.append({'id': ff.id,
                     'name': ff.name,
                     'filter': ff.filter_json
                     })
    
    return HttpResponse(json.dumps(favs), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def favorite_filter_save(request):
    name = request.GET.get('name')
    FilterFavorite.objects.filter(name=name).delete()
    ff = FilterFavorite()
    ff.user = request.user
    ff.name = name
    ff.filter_json = request.GET.get('filter')
    ff.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def favorite_filter_delete(request):
    FilterFavorite.objects.filter(id=request.GET.get('id')).delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


#* -------------- Registration -------------

def registration_filter_user(vars, data):
    if vars.get('state',None):
        data = data.filter(Q(district__state_id=vars.get('state')))
    if vars.get('district',None):
        data = data.filter(Q(district_id=vars.get('district')))
    if vars.get('school',None):
        data = data.filter(Q(school_id=vars.get('school')))
    return data


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration_send_email(request):
    log_task_executor(request.user, 'send registration email')
    
    ids=[]
    if request.POST.get('ids'):
        ids = [int(s) for s in request.POST.get('ids').split(',') if s.isdigit()]
    else:
        data = UserProfile.objects.all()
        data = registration_filter_user(request.POST, data)
        ids = data.values_list('user_id', flat=True)

    task = EmailTask()
    task.total_emails = len(ids)
    task.save()
    
    do_send_registration_email(task, ids, request)
    return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")


@postpone
def do_send_registration_email(task, user_ids, request):
    gevent.sleep(0)

    count_success=0
    for i, user_id in enumerate(user_ids):
        try:
            user = User.objects.get(id=user_id)

            #** record processed count
            task.process_emails = i + 1

            #** create log
            tasklog = EmailTaskLog()
            tasklog.task = task
            tasklog.send_date = datetime.now(UTC)
            tasklog.username = user.username
            tasklog.email = user.email
            tasklog.district_name = user.profile.district.name
            tasklog.error = "ok"
            
            reg = Registration.objects.get(user=user)
            props = {'key': reg.activation_key, 'district': user.profile.district.name}

            use_custom = request.POST.get("customize_email")
            if use_custom == 'true':
                custom_email = request.POST.get("custom_email_002")
                custom_email_subject = request.POST.get("custom_email_subject")
                subject = render_from_string(custom_email_subject, props)
                body = render_from_string(custom_email, props)
            else:
                subject = render_to_string('emails/activation_email_subject.txt', props)
                body = render_to_string('emails/activation_email.txt', props)
            
            subject = ''.join(subject.splitlines())
            
            send_html_mail(subject, body, settings.SUPPORT_EMAIL, ['mailfcl@126.com', user.email])
        except Exception as e:
            db.transaction.rollback()
            tasklog.error = "%s" % e
        finally:
            count_success += 1
            task.success_emails = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            tasklog.save()
            db.transaction.commit()

    #** post process
    tasklogs = EmailTaskLog.objects.filter(task=task)
    if len(tasklogs):
        FIELDS = ["username", "email", "district", "send_date", "error"]
        TITLES = ["Username", "Email", "District", "Send Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row = {"username": d.username,
                   "email": d.email,
                   "district": d.district_name,
                   "send_date": d.send_date,
                   "error": d.error
                   }
            writer.writerow(row)
        output.seek(0)
        attach = [{'filename': 'log.csv', 'mimetype': 'text/csv', 'data': output.read()}]
        send_html_mail("Sending Registration Email Report",
                       "Report of sending registration email, see attachment.",
                       settings.SUPPORT_EMAIL, ['mailfcl@126.com', request.user.email], attach)
        output.close()


def registration_email_progress(request):
    try:
        task = EmailTask.objects.get(id=request.POST.get('taskId'))
        message = {'percent': '%.2f' % (task.process_emails * 100 / task.total_emails)}
    except Exception as e:
        message = {'percent': 100}
    return HttpResponse(json.dumps(message), content_type="application/json")


def registration_invite_count(request):
    data = UserProfile.objects.all().select_related('User')
    data = registration_filter_user(request.POST, data)
            
    count = data.filter(subscription_status='Imported').count()
    return HttpResponse(json.dumps({'success': True, 'count': count}), content_type="application/json")


def registration_modify_user_status(request):
    message = {'success': True}
    for id in request.POST.get("ids").split(","): 
        user = User.objects.get(id=id)
        profile = UserProfile.objects.get(user_id=id)
        try:
            if request.POST['subscription_status'] == 'Registered':
                user.is_active = True
            else:
                user.is_active = False
            user.save()
            profile.subscription_status = request.POST['subscription_status']
            profile.save()
        except Exception as e:
            db.transaction.rollback()
            message = {'success': False}
            break
            
    return HttpResponse(json.dumps(message), content_type="application/json")


def registration_delete_users(request):
    message = {'success': True}
    ids = request.POST.get("ids").split(",")
    try:
        User.objects.filter(id__in=ids).delete()
        UserProfile.objects.filter(user_id__in=ids).delete()
        db.transaction.commit()
    except Exception as e:
        db.transaction.rollback()
        message = {'success': False, 'error': '%s' % (e)}
    return HttpResponse(json.dumps(message), content_type="application/json")    


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration_download_csv(request):
    FIELDS = ['user_id', "activate_link", "first_name", "last_name", "username", "email",
              "district", "cohort", "school", "invite_date", "activate_date", "subscription_status"]
    
    TITLES = ["User ID", "Activate Link", "First Name", "Last Name", "Username", "Email",
              "District", "Cohort", "School", "Invite Date", "Activate Date", "Status"]

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    
    writer.writerow(dict(zip(FIELDS, TITLES)))

    data = UserProfile.objects.all()
    data = registration_filter_user(request.POST, data)

    domain = "http://" + request.META['HTTP_HOST']

    for d in data:
        key, link = "", ""
        if Registration.objects.filter(user_id=d.user_id).count():
            key = Registration.objects.get(user_id=d.user_id).activation_key

        if key:
            link = domain + reverse('register_user', args=[key])

        writer.writerow({
            "user_id":attstr(d, "user_id"),
            "activate_link": link,
            "first_name": attstr(d, "user.first_name"),
            "last_name": attstr(d, "user.last_name"),
            "username": attstr(d, "user.username"),
            "email": attstr(d, "user.email"),
            "district": attstr(d, "district.name"),
            "cohort": attstr(d, "cohort.code"),
            "school": attstr(d, "school.name"),
            "invite_date": attstr(d, "invite_date"),
            "activate_date": attstr(d, "activate_date"),
            "subscription_status": attstr(d, "subscription_status")
            })

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.csv')
    output.seek(0)
    response.write(output.read())
    output.close()
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration_download_excel(request):
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    
    FIELDS = ['user_id', "activate_link", "first_name", "last_name", "username", "email",
              "_district", "_cohort", "_school", "_invite_date", "_activate_date", "subscription_status"]
    
    TITLES = ["User ID", "Activate Link", "First Name", "Last Name", "Username", "Email",
              "District", "Cohort", "School", "Invite Date", "Activate Date", "Status"]
    
    for i, k in enumerate(TITLES):
        worksheet.write(0, i, k)
    row = 1

    data = UserProfile.objects.all()
    data = registration_filter_user(request.POST, data)
    
    domain = "http://" + request.META['HTTP_HOST']
    for d in data:
        if Registration.objects.filter(user_id=d.user_id).count():
            key = Registration.objects.get(user_id=d.user_id).activation_key
        else:
            key = None
        d.activate_link = ""
        d.username = attstr(d, "user.username")
        d.first_name = attstr(d, "user.first_name")
        d.last_name = attstr(d, "user.last_name")
        d._school = attstr(d, "school.name")
        d._cohort = attstr(d, "cohort.code")
        d._district = attstr(d, "district.name")
        d.email = attstr(d, "user.email")
        d._invite_date = "%s" % attstr(d, "invite_date")
        d._activate_date = "%s" % attstr(d, "activate_date")
        
        for i, k in enumerate(FIELDS):
            if k == "activate_link" and key:
                d.activate_link = domain + reverse('register_user', args=[key])
                worksheet.write_url(row, i, getattr(d, k), None, key)
            else:
                worksheet.write(row, i, getattr(d, k))

        row += 1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())    
    return response

