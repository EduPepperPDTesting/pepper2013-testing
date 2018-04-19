from mitxmako.shortcuts import render_to_response
import json

# from datetime import datetime, timedelta, date
# from pytz import UTC
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# from django.http import HttpResponseForbidden
# import urllib2
# from courseware.courses import (get_courses, get_course_with_access,
#                                 get_courses_by_university, sort_by_announcement)
# from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
# from permissions.utils import check_access_level, check_user_perms
# from StringIO import StringIO
# from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School, CourseEnrollmentAllowed
# from student.models import District, State, School, Cohort
# from xmodule.modulestore.django import modulestore
# import os
# import os.path
# import shutil
# from student.feeding import dashboard_feeding_store
# import csv
# from django.core.validators import validate_email
import logging
log = logging.getLogger('tracking')

# -------------------------------------------------------------------login
def login(request):
    tmp = "mpepreg/sign_in.html"
    try:
        courses = {}
    except:
        courses = {}

    return render_to_response(tmp, {"courses": courses})


# -------------------------------------------------------------------mpepreg
def mpepreg(request):
    if request.user.is_authenticated():
        return render_to_response("mpepreg/mpepreg.html")
    else:
        return HttpResponseRedirect(reverse('mpepreg_login'))
