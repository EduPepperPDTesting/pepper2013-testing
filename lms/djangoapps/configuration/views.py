from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
import mako
import mitxmako
from mitxmako.shortcuts import render_to_response, render_to_string
from student.models import ResourceLibrary, StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from student.models import UserProfile, Registration, CourseEnrollmentAllowed
from django import db
import random
import json
import time
import logging
import csv

import multiprocessing
from multiprocessing import Process, Queue, Pipe
from django.core.validators import validate_email, validate_slug, ValidationError

import gevent
from django import db
from models import *
from StringIO import StringIO
from student.models import Transaction, District, Cohort, School, State
from mail import send_html_mail
import datetime
from pytz import UTC

log = logging.getLogger("tracking")

from gevent import monkey


def postpone(function):
    def decorator(*args, **kwargs):
        p = Process(target=function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()

    return decorator


@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user(request):
    from django.contrib.sessions.models import Session
    return render_to_response('configuration/import_user.html', {})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user_submit(request):
    # monkey.patch_all(socket=False)

    if request.method == 'POST':
        district_id = request.POST.get("district_id")
        school_id = request.POST.get("school_id")

        # output_pipe,input_pipe=multiprocessing.Pipe()
        # request.session['task']=''

        # ** readlines from csv
        file = request.FILES.get('file')
        r = csv.reader(file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        rl = []
        rl.extend(r)

        # ** create task
        task = ImportTask()
        task.filename = file.name
        # task.total_lines=100
        task.total_lines = len(rl)
        task.save()
        db.transaction.commit()

        # ** close connection before import
        # http://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
        from django.db import connection
        connection.close()

        # ** begin import
        do_import_user(task.id, rl, request)

        return HttpResponse(json.dumps({'success': True, 'taskId': task.id}))
    else:
        return HttpResponse('')


USER_CSV_COLS = ('email',)


def random_mark(length):
    assert (length > 0)
    return "".join(random.sample('abcdefg&#%^*1234567890', length))


def task_status(request):
    task = ImportTask.objects.get(id=request.POST.get('taskId'))

    if task:
        j = json.dumps({'task': task.filename, 'precent': '%.2f' % ((float(task.process_lines) / float(task.total_lines)) * 100)})  # output_pipe.recv()
    else:
        j = json.dumps({'task': 'no'})
    return HttpResponse(j)


@postpone
def do_import_user(taskid, csv_lines, request):
    gevent.sleep(0)

    district_id = request.POST.get("district_id")
    school_id = request.POST.get("school_id")
    send_registration_email = request.POST.get('send_registration_email') == 'true'
    task = ImportTask.objects.get(id=taskid)

    # ** ==================== testing
    # curr=""
    # process=0

    # while 1:
    #     now=time.strftime("%Y-%m-%d %X", time.localtime())
    #     if now!=curr:
    #         process=process+1

    #         task.filename=now
    #         task.process_lines=process
    #         task.save()
    #         db.transaction.commit()

    #         log.debug(now)
    #         curr=now

    # ** ==================== importing
    count_success = 0

    # ** import into district
    district = District.objects.get(id=district_id)
    for i, line in enumerate(csv_lines):
        # ** record csv lines process
        task.process_lines = i + 1
        task.save()
        db.transaction.commit()

        tasklog = ImportTaskLog()

        email = line[USER_CSV_COLS.index('email')]

        # ** generating origin username
        username = random_mark(20)

        tasklog.username = username
        tasklog.email = email
        tasklog.create_date = datetime.datetime.now(UTC)
        tasklog.district = district
        tasklog.line = i + 1
        tasklog.import_task = task

        try:
            validate_user_cvs_line(line)

            # ** user
            user = User(username=username, email=email, is_active=False)
            user.set_password(username)
            user.save()

            # ** registration
            registration = Registration()
            registration.register(user)

            # ** profile
            profile = UserProfile(user=user)
            profile.district = district
            profile.subscription_status = "Imported"
            if school_id:
                profile.school = School.objects.get(id=school_id)
            profile.save()

            # ** course enroll
            cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
            cea.is_active = True
            cea.auto_enroll = True
            cea.save()

            # ** send activation email if required
            if send_registration_email:
                try:
                    reg = Registration.objects.get(user=user)
                    props = {'key': reg.activation_key, 'district': district.name}
                    use_custom = request.POST.get("customize_email")
                    if use_custom == 'true':
                        custom_email = request.POST.get("custom_email")
                        custom_email_subject = request.POST.get("custom_email_subject")
                        subject = render_from_string(custom_email_subject, props)
                        body = render_from_string(custom_email, props)
                    else:
                        subject = render_to_string('emails/activation_email_subject.txt', props)
                        body = render_to_string('emails/activation_email.txt', props)

                    subject = ''.join(subject.splitlines())
                    send_html_mail(subject, body, settings.SUPPORT_EMAIL, [email])
                except Exception as e:
                    raise Exception("Failed to send registration email")

            # ** count success
            count_success = count_success + 1
            task.success_lines = count_success
            task.save()

            tasklog.save()

            db.transaction.commit()
        except Exception as e:
            db.transaction.rollback()

            tasklog.error = "%s" % e
            tasklog.save()

            db.transaction.commit()

            log.debug("import error: %s" % e)

    # ** post process
    tasklogs = ImportTaskLog.objects.filter(import_task=task)
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
                   "district": d.district.name,
                   "create_date": d.create_date,
                   "error": d.error
                   }
            writer.writerow(row)
        output.seek(0)
        attachs = [{'filename': 'log.csv', 'minetype': 'text/csv', 'data': output.read()}]
        send_html_mail("User Data Import Report",
                       "Report of importing %s, see attachment." % task.filename,
                       settings.SUPPORT_EMAIL, [request.user.email], attachs)
        output.close()


def validate_user_cvs_line(line):
    # ** check field count
    n = 0
    for item in line:
        if len(item.strip()):
            n = n + 1
    if n != len(USER_CSV_COLS):
        raise Exception("Wrong fields count")

    # ** email
    email = line[USER_CSV_COLS.index('email')]
    validate_email(email)

    # ** check user exists
    if len(User.objects.filter(email=email)) > 0:
        raise Exception("An account with the Email '{email}' already exists".format(email=email))


def render_from_string(template_string, dictionary, context=None, namespace='main'):
    context_instance = Context(dictionary)
    # add dictionary to context_instance
    context_instance.update(dictionary or {})
    # collapse context_instance to a single dictionary for mako
    context_dictionary = {}
    context_instance['settings'] = settings
    context_instance['MITX_ROOT_URL'] = settings.MITX_ROOT_URL

    # In various testing contexts, there might not be a current request context.
    if mitxmako.middleware.requestcontext is not None:
        for d in mitxmako.middleware.requestcontext:
            context_dictionary.update(d)
    for d in context_instance:
        context_dictionary.update(d)
    if context:
        context_dictionary.update(context)
    # fetch and render template
    raw_template = mako.Template(text=template_string)
    return raw_template.render_unicode(**context_dictionary)
