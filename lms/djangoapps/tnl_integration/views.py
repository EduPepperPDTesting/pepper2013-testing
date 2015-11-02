"""
True North Logic integration module

TODO: These questions need answers to complete this:
  1) What is the specific method for encrypting the course creation data?
  2) Is this encryption needed for any other sent data?
  3) What are the gradeid values?
  4) What are the providerid, edagencyid, coursetypeid, creditareaid, creditvaluetypeid, and creditvalue, and are they
     all required for the createSDLCourse?
  5) What is the sectionid for a course created using the createSDLCourse endpoint? Presumably I would use the
     getSectionId endpoint for that data, but the statement "include enough parameters to uniquely identify the section"
     is somewhat vague. What parameters would be required for this case?
"""

# Imports
from django.conf import settings
import requests
import logging
import json
import datetime
from tnl_integration.models import TNLCourses, TNLCompletionTrack, TNLDistricts
from student.models import District, User
from mitxmako.shortcuts import render_to_response
from courseware.course_grades_helper import get_course_by_id

# Global variables
base_url = settings.TNLBASEURL
adminid = settings.TNLADMINID
grades = {}  # TODO: need to enter the gradeid data from TNL when I get it
AUDIT_LOG = logging.getLogger("audit")


class TNLRequest:
    """
    Class for creating and carrying out requests to TNL
    """
    def __init__(self, endpoint, method, data):
        self.url = base_url + endpoint
        self.method = method
        self.data = data

    def do_request(self):
        """
        Makes the request to TNL. Returns parsed JSON object on success. Raises exceptions on error.
        """
        try:
            response = requests.request(self.method, self.url, data=self.data, timeout=15)
            parsed = json.loads(response.text)
            if parsed.success == 'false':
                raise Exception(u"Unsuccessful request: {0}".format(parsed.message))
            return parsed
        except Exception as e:
            AUDIT_LOG.warning(u"There was a TNL connection error: {0}.".format(e))
            raise


def get_person(user):
    """
    This gets the TNL personid
    """
    # getPersonId endpoint
    endpoint = '/ia/app/webservices/person/getPersonId'
    # Parameters needed for this request
    data = {'adminid': adminid,
            'email': user.email}
    # Request object
    tnl_request = TNLRequest(endpoint, 'get', data)

    try:
        response = tnl_request.do_request()
        return response.personid
    except:
        return False


def get_section():
    """
    This gets the TNL sectionid
    """


def get_grade():
    """
    Matches our grade with the gradeid data from TNL
    """


def check_district(district_id):
    """
    Checks to see if this district is TNL-enabled
    """
    try:
        TNLDistricts.objects.get(district=district_id)
        return True
    except:
        return False


def tnl_course(user, course_instance):
    """
    Checks to see if this is in fact a course and user registered with TNL.
    """
    course = get_course(course_instance.course_id)
    user = User.objects.get(id=user.id)
    if course:
        try:
            district = District.objects.get(id=user.profile.district_id)
            if check_district(district.id):
                return True
            else:
                return False
        except:
            return False


def get_course(id=False):
    """
    Gets the course(s) from the registered course table.
    """
    try:
        if id:
            course = TNLCourses.objects.get(course=id)
        else:
            course = TNLCourses.objects.all()

    except:
        course = False

    return course


def get_district(id=False):
    """
    Gets the district(s) from the configured districts, along with other district data.
    """
    try:
        if id:
            district = TNLDistricts.objects.get(course=id).select_related()
        else:
            district = TNLDistricts.objects.all().select_related()

    except:
        district = False

    return district


def register_course(course):
    """
    This registers the course with TNL
    """
    # createSDLCourse endpoint (SDL seems the best fit for our courses)
    endpoint = '/ia/app/webservices/course/createSDLCourse'
    # Get all the needed data
    # TODO: These need real data, obviously. Need more info from TNL.
    providerid = ''
    edagencyid = ''
    coursetypeid = ''
    creditareaid = ''
    creditvaluetypeid = ''
    creditvalue = ''
    # Parameters needed for the request
    data = {'adminid': adminid,
            'title': course.name,
            'externalid': course.id,
            'providerid': providerid,
            'edagencyid': edagencyid,
            'coursetypeid': coursetypeid,
            'creditareaid': creditareaid,
            'creditvaluetypeid': creditvaluetypeid,
            'creditvalue': creditvalue,
            'needsapproval': False,
            'selfpaced': True}
    # Request object
    # TODO: the data needs to be encrypted prior to sending, according to the TNL doc.
    tnl_request = TNLRequest(endpoint, 'post', data)

    try:
        response = tnl_request.do_request()
        course_entry = TNLCourses(course=course.id,
                                  tnl_id=response.courseid,
                                  registered=1,
                                  registration_date=datetime.datetime.utcnow())
    except:
        course_entry = TNLCourses(course=course.id, registered=0)

    course_entry.save()


def register_completion(user, course_instance, percent):
    """
    This registers a competed course for a particular user with TNL
    """

    # Registered course
    course = get_course(course_instance.course_id)
    # markComplete endpoint
    endpoint = '/ia/app/webservices/section/markComplete'
    # Assign needed parameters
    data = {'adminid': adminid,
            'personid': get_person(user),
            'sectionid': get_section(),  # TODO: add our ID
            'gradeid': get_grade(percent)}
    # Request object
    tnl_request = TNLRequest(endpoint, 'put', data)

    try:
        tnl_request.do_request()
        track = TNLCompletionTrack(user=user, course=course, registered=1, registration_date=datetime.datetime.utcnow())
    except:
        track = TNLCompletionTrack(user=user, course=course, registered=0)

    track.save()


def tnl_configuration(request):
    """
    Handles the TNL configuration page
    """
    districts = get_district()
    tnl_courses = get_course()
    courses = []
    for course in tnl_courses:
        courses.append(get_course_by_id(course.course_id))

    context = {'districts': districts, 'courses': courses}
    return render_to_response('administration/tnl_configuration.html', context)
