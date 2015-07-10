from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from student.models import ResourceLibrary,StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required

def import_user(request):
    return render_to_response('configuration/import_user.html', {})

from multiprocessing import Process
import logging
log = logging.getLogger("tracking")

def import_user_submit(request):
    log.debug('')
    p = Process(target = do_import, args = ('A',))
    p.start()
    log.debug('B')

def do_import(x):
    while 1:
        log.debug(x)
        pass

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
