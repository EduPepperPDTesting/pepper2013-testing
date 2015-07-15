from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from student.models import ResourceLibrary,StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth.models import User
from student.models import UserProfile,Registration,CourseEnrollmentAllowed
from django import db
import random
import json
import time
import logging
import csv
from multiprocessing import Process
from django.core.validators import validate_email, validate_slug, ValidationError

log = logging.getLogger("tracking")

def postpone(function):
    def decorator(*args, **kwargs):
        p = Process(target = function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()
    return decorator

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user(request):
    return render_to_response('configuration/import_user.html', {})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user_submit(request):
    if request.method == 'POST':
        do_import_user(request.FILES['file'])
        return HttpResponse(json.dumps({'success': True}))
    else:
        return HttpResponse('')

USER_CSV_COLS=('email',)

@postpone
def do_import_user(file):
    #** ==================== testing 
    # curr=""
    # while 1:
    #     now=time.strftime("%Y-%m-%d %X", time.localtime() )
    #     if now!=curr:
    #         log.debug(now)
    #         curr=now
    
    #** ==================== importing
    # message={}
    try:
        count_success=0
        r=csv.reader(file,delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        rl = []
        rl.extend(r)

        #** import into cohort
        # cohort_id=request.POST.get("cohort_id")
        # cohort=Cohort.objects.get(id=cohort_id)
        # if cohort.licences < UserProfile.objects.filter(~Q(subscription_status = "Inactive"),cohort_id=cohort_id).count() + len(rl):
        #     raise Exception("Licences limit exceeded")
        
        for line in rl:
            validate_user_cvs_line(line)

            email=line[USER_CSV_COLS.index('email')]

            #** generating origin username
            username="".join(random.sample('abcdefg&#%^*1234567890',20))

            #** user
            user = User(username=username, email=email, is_active=False)
            user.set_password(username)
            user.save()

            #** registration
            registration = Registration()
            registration.register(user)

            #** profile
            profile=UserProfile(user=user)
            # profile.cohort_id=cohort_id
            profile.subscription_status="Imported"
            profile.save()

            #** course enroll
            cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
            cea.is_active = True
            cea.auto_enroll = True
            cea.save()

            #** email
            # reg = Registration.objects.get(user=user)
            # d = {'name': profile.name, 'key': reg.activation_key}
            # subject = render_to_string('emails/activation_email_subject.txt', d)
            # subject = ''.join(subject.splitlines())
            # message = render_to_string('emails/activation_emailh.txt', d)
            # send_html_mail(subject, body, settings.SUPPORT_EMAIL, [email])

            #** count success
            count_success=count_success+1
            
        db.transaction.commit()
    except Exception as e:
        db.transaction.rollback()
        log.debug("import error: %s" % e)

def validate_user_cvs_line(line):
    #** check field count
    n=0
    for item in line:
        if len(item.strip()):
            n=n+1
    if n != len(USER_CSV_COLS):
        raise Exception("Wrong fields count")

    #** email
    email=line[USER_CSV_COLS.index('email')]
    validate_email(email)

    #** check user exists
    if len(User.objects.filter(email=email)) > 0:
        raise Exception("An account with the Email '{email}' already exists".format(email=email))

