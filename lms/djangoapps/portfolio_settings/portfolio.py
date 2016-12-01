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
#import calendar
#from django.utils.timezone import datetime, now, timedelta, utc
#from django.utils.translation import ugettext_lazy as _
#from dateutil.relativedelta import relativedelta

#from student.models import (Registration, UserProfile, District)

from people.people_in_es import gen_people_search_query, search_people, add_user_people_of, del_user_people_of

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
                    ppBeans = ProtfolioPermissions.objects.filter(user_id=request.user.id).filter(course_id=item.course_id)
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
                    cid = tmp2[0];
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

        elif (request_flag == "saveOneCourse"):
            content = request.GET.get("content")
            if (content):
                for tmp1 in content.split(","):
                    tmp2 = tmp1.split(":");
                    cid = tmp2[0];
                    level = tmp2[1];
                    uid = tmp2[2];

                    protfolio_1 = ProtfolioPermissions()
                    ppBeans = ProtfolioPermissions.objects.filter(user_id=uid).filter(course_id=cid)
                    for ppx in ppBeans:
                        protfolio_1 = ppx
                        break;

                    protfolio_1.user_id = uid
                    protfolio_1.course_id = cid
                    protfolio_1.permission_level = level
                    protfolio_1.save();

            return HttpResponse(json.dumps({'success': True}), content_type="application/json")

        elif (request_flag == "getCourseLevel"):
            course_id = request.GET.get("course_id")
            user_id = request.GET.get("user_id")
            user_profile = UserProfile.objects.get(user_id=user_id)
            linkx = request.GET.get("linkx")
            #current_user_id = request.user

            if (course_id and user_id):
                level = 1
                ppBeans = ProtfolioPermissions.objects.filter(user_id=user_id).filter(course_id=course_id)
                for ppx in ppBeans:
                    level = ppx.permission_level
                    break;

                total = 0
                if(level != "1"):
                    if(user_id == request.user.id):
                        level = "1";
                    else:
                        if(level == "2"):
                            if(user_profile.district.state.name == request.user.profile.district.state.name):
                                level = "1";

                        elif(level == "3"):
                            if (user_profile.district.name == request.user.profile.district.name):
                                level = "1";

                        elif (level == "4"):
                            if (user_profile.school.name == request.user.profile.school.name):
                                level = "1";

                        elif (level == "5"):
                            cond = gen_people_search_query(
                                must={
                                    'people_of': user_id,
                                    'user_id': request.user.id
                                })

                            profiles, total = search_people(cond)
                            if(int(total) > 0):
                                level = "1";

                        elif (level == "6"):
                            if (user_profile.district.name == request.user.profile.district.name):
                                level = "1"

                            else:
                                cond = gen_people_search_query(
                                    must={
                                        'people_of': user_id,
                                        'user_id': request.user.id
                                    })

                                profiles, total = search_people(cond)
                                if(total > 0):
                                    level = "1";


                return HttpResponse(json.dumps({'success': True, 'linkx': linkx, 'level': level}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'success': False}), content_type="application/json")
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