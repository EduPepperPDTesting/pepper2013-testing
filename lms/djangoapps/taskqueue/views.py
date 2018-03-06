from mitxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from util.json_request import JsonResponse
import json
from mako.template import Template
import mitxmako
import requests
from django.http import HttpResponse
from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link
from django.template import Context
from django.conf import settings
from student.models import User, UserProfile, Registration
from models import Job, Tasks
from django import db
import logging
from mail import send_html_mail
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

log = logging.getLogger("taskqueue")

def pop_queue(request):
    size = settings.TASK_QUEUE_SIZE
    total = Tasks.objects.all().count()
    if total >= size:
        tasks = Tasks.objects.order_by("id")[:size]
    else:
        tasks = Tasks.objects.all()
    for task in tasks:
        job = task.job
        if job.function == "email":
            run_registration_email(task)
    return HttpResponse(json.dumps({"pop": "done"}), content_type="application/json")


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
    job = Job.objects.get(id=job_id)
    task = Tasks()
    task.job = job
    task.data = email_data
    task.save()


def remove_task (task):
    try:
        task.delete()
        update_job (task.job)
    except Exception as e:
        db.transaction.rollback()
        log.error("Couldn't delete task. %s" % e.message)


def update_job(job):
    job.completed = job.completed + 1
    job.save()


def run_registration_email(task):
    log.debug("Sending TaskQueue task email.")
    email_data = json.loads(task.data)
    try:
        user_id = email_data['ids']
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
        profile.subscription_status = 'Unregistered'

        reg = Registration.objects.get(user=user)
        props = {'key': reg.activation_key, 'district': user.profile.district.name, 'email': user.email}

        use_custom = email_data['custom_email']
        if use_custom == 'true':
            custom_email = email_data['custom_message']
            custom_email_subject = email_data['custom_message_subject']
            subject = render_from_string(custom_email_subject, props)
            body = render_from_string(custom_email, props)
        else:
            subject = render_to_string ('emails/acivation_email_subject.txt', props)
            body = render_to_string('emails/activation_email.txt', props)

        send_html_mail(subject, body, settings.SUPPORT_EMAIL, [user.email])

        log.info("Registration email sent using data: %s" % task.data)

        remove_task(task)

    except Exception as e:
        db.transaction.rollback()
        log.debug("Email error: %s" % e.message)
        log.debug("Failed data: %s" % task.data)



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