from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse

from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from django.contrib.auth.models import User
from student.models import UserProfile, CourseEnrollment
# from django import db
import json
import time
import logging
import csv
import gevent
from django import db
from StringIO import StringIO
from student.models import District, Cohort, School, State
from student.views import study_time_format, course_from_id
from datetime import datetime, timedelta
from pytz import UTC

from multiprocessing import Process
from threading import Thread
from mako.template import Template
import mitxmako

from django.db.models import F
from study_time.models import record_time_store
from django.views.decorators import csrf
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError
from courseware.module_render import get_module
from courseware.model_data import FieldDataCache
from courseware.courses import get_courses
from courseware.course_grades_helper import grade
from mail import send_html_mail
log = logging.getLogger("tracking")


def index(request):
    return render_to_response('communities/communities.html', {})
    
def community(request):
    return render_to_response('communities/community.html', {})
    
def community_ngss(request):
    return render_to_response('communities/community_ngss.html', {})

