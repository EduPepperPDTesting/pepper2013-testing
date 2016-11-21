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
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School, CourseEnrollment
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
    request_flag = request.GET.get("flag")
    if(request_flag):
        if(request_flag == "getCourses"):
            s_txt = request.GET.get("s_txt")
            if(s_txt):
                Courses = CourseEnrollment.objects.filter(user_id=request.user.id).filter(course_id__contains=s_txt).order_by('course_id')
            else:
                Courses = CourseEnrollment.objects.filter(user_id=request.user.id).order_by('course_id')

            rows = []
            try:
                for item in Courses:
                    ppBeans = ProtfolioPermissions.objects.filter(user_id=request.user.id).filter(course_id=item.id)
                    level = "1"
                    ppid = "-1"
                    for ppx in ppBeans:
                        level = ppx.permission_level
                        ppid = ppx.id
                        break;

                    rows.append({
                        "id": item.id,
                        "course": item.course_id,
                        "level": level,
                        "ppid": ppid
                    })
            except Exception as e:
                return HttpResponse(json.dumps({'success': True, 'error': '%s' % e}), content_type="application/json")

            return HttpResponse(json.dumps({'success': True, 'rows': rows}), content_type="application/json")

        elif(request_flag == "saveCourse"):
            content = request.GET.get("content")
            if(content):
                for tmp1 in content.split(","):
                    tmp2 = tmp1.split(":");
                    cid = int(tmp2[0]);
                    level = tmp2[1];
                    ppid = tmp2[2];

                    protfolio_1 = ProtfolioPermissions()
                    if ppid != "-1":
                        protfolio_1 = ProtfolioPermissions.objects.get(id=ppid)

                    protfolio_1.user_id = request.user.id
                    protfolio_1.course_id = cid
                    protfolio_1.permission_level = level
                    protfolio_1.save();

            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    else:
        tmp = "portfolio_settings/protfolio_settings.html";
        courses = {};
        try:
            pass
            #courses = get_courses_drop(request.user.profile.district.state.name, request.user.profile.district.code)
        except:
            tmp = "portfolio_settings/protfolio_settings.html";
            courses = {};

        return render_to_response(tmp, {"courses": courses})