from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from student.models import ResourceLibrary,StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

import json

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user(request):
    return render_to_response('configuration/import_user.html', {})

from multiprocessing import Process
import logging
log = logging.getLogger("tracking")

import subprocess

from gevent.pool import Pool,Greenlet
from gevent import monkey; monkey.patch_socket()

# Stackless

from greenlet import greenlet

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user_submit(request):
    # num_worker_threads=2
    # pool = Pool(num_worker_threads)
    # g=pool.apply_async(do_import, args=('A',))
    # # pool.start(g)
    # pool.join()
    
    g=Greenlet(do_import,'A')
    g.start_later(2)
    
    log.debug('B')

    return HttpResponse(json.dumps({'success': True}))

def do_import():

    from multiprocessing import Process
    import logging
    log = logging.getLogger("tracking")

    log.debug('C')
    
    curr=""
    while 1:
        now=time.strftime("%Y-%m-%d %X", time.localtime() )
        if now!=curr:
            log.debug(now)
            curr=now
        # time.sleep(1)            
        # log.debug(now)

    # message={}
    # if request.method == 'POST':
    #     f=request.FILES['file']
    #     try:
    #         count_success=0
    #         # --- THIS FAILS ON SING COLUMN CVS ---
    #         # dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
    #         # f.seek(0)
    #         # r=csv.reader(f,dialect)
    #         r=csv.reader(f,delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #         rl = []
    #         rl.extend(r)
    #         cohort_id=request.POST.get("cohort_id")
    #         cohort=Cohort.objects.get(id=cohort_id)
    #         if cohort.licences < UserProfile.objects.filter(~Q(subscription_status = "Inactive"),cohort_id=cohort_id).count() + len(rl):
    #             raise Exception("Licences limit exceeded")
    #         for line in rl:
    #             exist=validate_user_cvs_line(line)
    #             # if(exist):
    #             #     raise Exception("An user already exists, or duplicate lines.")
    #             email=line[USER_CSV_COL_EMAIL]
    #             import random
    #             username="".join(random.sample('abcdefg&#%^*f1234567890',20))
    #             user = User(username=username, email=email, is_active=False)
    #             user.set_password(username)
    #             user.save()
    #             registration = Registration()
    #             registration.register(user)
    #             profile=UserProfile(user=user)
    #             # profile.transaction_id=transaction_id
    #             # profile.email=email
    #             # profile.username=username
    #             profile.cohort_id=cohort_id
    #             profile.subscription_status="Imported"
    #             profile.save()

    #             cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
    #             cea.is_active = True
    #             cea.auto_enroll = True
    #             cea.save()

    #             count_success=count_success+1

    #             # reg = Registration.objects.get(user=user)
    #             # d = {'name': profile.name, 'key': reg.activation_key}
    #             # subject = render_to_string('emails/activation_email_subject.txt', d)
    #             # subject = ''.join(subject.splitlines())
    #             # message = render_to_string('emails/activation_emailh.txt', d)
    #         db.transaction.commit()
    #         message={"success": True,
    #             "message":"Success! %s users imported." % (count_success),
    #             "count_success":count_success,
    #         }            
    #     except Exception as e:
    #         db.transaction.rollback()
    #         message={'success': False,'error':'Import error: %s. At cvs line: %s, Nobody imported.' % (e,count_success+1)}
    # return HttpResponse(json.dumps(message))
