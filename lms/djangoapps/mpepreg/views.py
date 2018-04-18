from mitxmako.shortcuts import render_to_response
import json

from datetime import datetime, timedelta, date
from pytz import UTC
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
import urllib2
from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from permissions.utils import check_access_level, check_user_perms
from StringIO import StringIO
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School, CourseEnrollmentAllowed
from student.models import District, State, School, Cohort
from xmodule.modulestore.django import modulestore
import os
import os.path
import shutil
from student.feeding import dashboard_feeding_store
import csv
from courseware.courses import get_courses, get_course_about_section
from django.core.validators import validate_email
from pepper_utilities.utils import render_json_response
from xmodule.remindstore import myactivitystore
from reporting.models import reporting_store
import logging
log = logging.getLogger('tracking')

# -------------------------------------------------------------------main
def main(request):
    get_flag = request.GET.get("flag")
    post_flag = request.POST.get("flag")

    if get_flag:
        if get_flag == "organization_list":
            return organization_list(request)

        elif get_flag == "design_list":
            return design_list(request)

    elif post_flag:
        if post_flag == "organization_add":
            return organization_add(request)

        elif post_flag == "organization_register_save":
            return organization_register_save(request)
    else:
        return render_to_response("mpepreg/sign_in.html")
