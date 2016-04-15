# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.shortcuts import redirect
# from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response, render_to_string
# from student.models import ResourceLibrary,StaticContent
# from collections import deque
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from administration.models import site_setting_store

# from django.contrib.auth.models import User
# from django import db
# import random
import json
# import time
import logging

from django import db
from models import *
# from StringIO import StringIO
from student.models import Transaction, District, Cohort, School, State, UserProfile, Registration, CourseEnrollmentAllowed
# from mail import send_html_mail
# import datetime
# from pytz import UTC
import urllib
#log = logging.getLogger("tracking")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
	site_settings = site_setting_store()

	al_text = "__NONE__"
	try:
		al_text = site_settings.get_item('alert_text')['value']
	except Exception as e:
		pass

	if al_text == "__NONE__":
		al_text = ""

	al_enabled = "un_enabled"
	try:
		al_enabled = site_settings.get_item('alert_enabled')['value']
	except Exception as e:
		pass

	return render_to_response("administration/alert_message.html", {"alert_text":al_text,"alert_enabled":al_enabled})

def alert_message_post(request):
    al_text = ""
    al_enabled = ""
    site_settings = site_setting_store()
    if 'alert_text' in request.POST:
        al_text = request.POST['alert_text']
    if 'alert_enabled' in request.POST:
        al_enabled = request.POST['alert_enabled']

    site_settings.set_item('alert_text', al_text)
    site_settings.set_item('alert_enabled', al_enabled)
    
    if al_text == "__NONE__":
    	al_text = ""

    return HttpResponse(json.dumps({"alert_text":al_text,
                                    "alert_enabled":al_enabled}))

