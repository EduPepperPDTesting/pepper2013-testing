from mitxmako.shortcuts import render_to_response, render_to_string
from django.http import HttpResponse
import json
from models import ProtfolioPermissions
from django import db
from datetime import datetime, timedelta, date
from pytz import UTC
from django.contrib.auth.models import User

import urllib2
from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from permissions.utils import check_access_level, check_user_perms
from StringIO import StringIO
import xlsxwriter
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School
from xmodule.modulestore.django import modulestore
import pymongo

from django.conf import settings
import calendar
from django.utils.timezone import datetime, now, timedelta, utc
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from student.models import (Registration, UserProfile, TestCenterUser, TestCenterUserForm,
                            TestCenterRegistration, TestCenterRegistrationForm, State,
                            PendingNameChange, PendingEmailChange, District,
                            CourseEnrollment, unique_id_for_user,
                            get_testcenter_registration, CourseEnrollmentAllowed)

@login_required
def index(request):
    tmp = "portfolio_settings/protfolio_settings.html";
    courses = {};
    try:
        pass
        #courses = get_courses_drop(request.user.profile.district.state.name, request.user.profile.district.code)
    except:
        tmp = "portfolio_settings/protfolio_settings.html";
        courses = {};

    return render_to_response(tmp, {"courses": courses})