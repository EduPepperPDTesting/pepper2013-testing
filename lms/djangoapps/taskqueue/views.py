from mitxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from util.json_request import JsonResponse
import json
import requests
from django.http import HttpResponse
from django.conf import settings
from student.models import User, UserProfile, Registration
from mitxmako.shortcuts import render_to_string
from models import Job, Tasks
from django import db
from pepconn import render_from_string
from mail import send_html_mail
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def pop_queue(request):
    return "Done."


#
# Creates a job with a provided function name and the amount
# of tasks that will be associated with the job.
# The total is the initial total - checks will still need to happen against
# the tasks table to verify that that many tasks are actually created/exist.
#
def create_job(fname, size):
    job = Job()
    job.function = fname
    job.completed = 0
    job.total = size
    job.save()
    return job.id


def push_reg_email(job_id, email_data):
    job = Job.object.get(id=job_id)
    task = Tasks()
    task.job = job
    task.data = email_data
    task.save()


def run_registration_email(task):
    job = task.job
    email_json = json.loads(task.data)
    try:
        user_id = email_json.id
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
        profile.subscription_status = 'Unregistered'

        reg = Registration.objects.get(user=user)
        props = {'key': reg.activation_key, 'district': user.profile.district.name, 'email': user.email}

        use_custom = email_json.custom_email
        if use_custom == 'true':
            custom_email = email_json.custom_email_body
            custom_email_subject = email_json.custom_email_subject
            subject = render_from_string(custom_email_subject, props)
            body = render_from_string(custom_email, props)
        else:
            subject = render_to_string ('emails/acivation_email_subject.txt', props)
            body = render_to_string('emails/activation_email.txt', props)
        subject = ''.join(subject.splitLines())
        send_html_mail (subject, body, settings.SUPPORT_EMAIL, [user.email])

        job.completed = job.completed + 1

    except Exception as e:
        db.transaction.rollback()

