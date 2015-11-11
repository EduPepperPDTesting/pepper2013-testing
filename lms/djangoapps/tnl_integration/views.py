"""
True North Logic integration module
"""

# Imports
from student.views import course_from_id
from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .utils import tnl_get_district, tnl_get_course, tnl_register_course
import json


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_configuration(request):
    """
    Handles the TNL configuration page
    """
    districts = tnl_get_district()
    tnl_courses = tnl_get_course()
    courses = []
    for course in tnl_courses:
        courses.append(course_from_id(course.course_id))

    context = {'districts': districts, 'courses': courses}
    return render_to_response('tnl/configuration.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_connection_test(request):
    """
    Test the connection to TNL server
    """
    return render_to_response('tnl/test.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_test_register(request):
    """
    Carries out the actual registration
    """
    try:
        course = course_from_id('PCG/PEP101x/2014_Spring')
        response = tnl_register_course(course)
    except Exception, e:
        raise e
    return HttpResponse(json.dumps(response), mimetype='application/json')
    # return HttpResponse(response)
