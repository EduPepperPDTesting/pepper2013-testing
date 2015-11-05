"""
True North Logic integration module
"""

# Imports
from courseware.course_grades_helper import get_course_by_id
from mitxmako.shortcuts import render_to_response
from .utils import tnl_get_district, tnl_get_course


def tnl_configuration(request):
    """
    Handles the TNL configuration page
    """
    districts = tnl_get_district()
    tnl_courses = tnl_get_course()
    courses = []
    for course in tnl_courses:
        courses.append(get_course_by_id(course.course_id))

    context = {'districts': districts, 'courses': courses}
    return render_to_response('administration/tnl_configuration.html', context)


def tnl_connection_test(request):
    """
    Test the connection to TNL server
    """
    course = get_course_by_id('')
