# Imports
import datetime
import logging
import json

from django.conf import settings

from student.models import District, User
from tnl_integration.models import TNLCourses, TNLCompletionTrack, TNLDistricts
from web_client.crypt import salt_convert, PBEWithMD5AndDES
from web_client.request import WebRequest

# ========== Global variables ==========
# The logging mechanism
AUDIT_LOG = logging.getLogger("audit")

# The base URL for all requests
tnl_base_url = settings.TNL_BASE_URL

# District/endpoint specific values
tnl_adminid = settings.TNL_ADMINID
tnl_grades = settings.TNL_GRADES
tnl_providerid = settings.TNL_PROVIDERID
tnl_edagencyid = settings.TNL_EDAGANECYID
tnl_creditvaluetypeid = settings.TNL_CREDITVALUETYPEID
tnl_creditareaid = settings.TNL_CREDITAREAID
tnl_creditvalue = settings.TNL_CREDITVALUE  # TODO: need to validate this with the customer and/or TNL "the number of credits (CEUs in DPI's case) to be awarded for the course)"

# District/endpoint specific encryption information
tnl_enc_password = settings.TNL_PASSWORD
tnl_enc_salt = salt_convert(settings.TNL_SALT)
tnl_enc_iterations = settings.TNL_ITERATIONS
tnl_encryptor = PBEWithMD5AndDES(tnl_enc_password, tnl_enc_salt, tnl_enc_iterations)


def tnl_get_person(user):
    """
    This gets the TNL personid
    """
    # getPersonId endpoint
    endpoint = '/ia/app/webservices/person/getPersonId'
    # Parameters needed for this request
    data = {'adminid': tnl_adminid,
            'email': user.email}
    # Request object
    tnl_request = WebRequest(tnl_base_url)

    try:
        response = tnl_request.do_request(endpoint, 'get', tnl_encryptor.encrypt(json.dumps(data)))
        return response.personid
    except:
        return False


def tnl_get_grade(percent):
    """
    Matches our grade with the gradeid data from TNL
    """
    grade = round(percent * 100)
    grade_out = False
    for gradeid, grades in tnl_grades:
        if grade in grades:
            grade_out = gradeid

    return grade_out


def tnl_check_district(district_id):
    """
    Checks to see if this district is TNL-enabled
    """
    try:
        TNLDistricts.objects.get(district=district_id)
        return True
    except:
        return False


def tnl_get_course(id=False):
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


def tnl_get_district(id=False):
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


def tnl_register_completion(user, course_instance, percent):
    """
    This registers a competed course for a particular user with TNL
    """

    # Registered course
    course = tnl_get_course(course_instance.course_id)
    # markComplete endpoint
    endpoint = '/ia/app/webservices/section/markComplete'
    # Assign needed parameters
    data = {'adminid': tnl_adminid,
            'personid': tnl_get_person(user),
            'sectionid': course.section_id,
            'gradeid': tnl_get_grade(percent)}
    # Request object
    tnl_request = WebRequest(tnl_base_url)

    try:
        tnl_request.do_request(endpoint, 'put', tnl_encryptor.encrypt(json.dumps(data)))
        track = TNLCompletionTrack(user=user, course=course, registered=1, registration_date=datetime.datetime.utcnow())
    except:
        track = TNLCompletionTrack(user=user, course=course, registered=0)

    track.save()


def tnl_course(user, course_instance):
    """
    Checks to see if this is in fact a course and user registered with TNL.
    """
    course = tnl_get_course(course_instance.course_id)
    user = User.objects.get(id=user.id)
    if course:
        try:
            district = District.objects.get(id=user.profile.district_id)
            if tnl_check_district(district.id):
                return True
            else:
                return False
        except:
            return False


def tnl_register_course(course):
    """
    This registers the course with TNL
    """
    # createSDLCourse endpoint (SDL seems the best fit for our courses)
    endpoint = '/ia/app/webservices/course/createSDLCourse'

    # Parameters needed for the request
    data = {'adminid': tnl_adminid,
            'title': course.name,
            'externalid': course.id,
            'providerid': tnl_providerid,
            'edagencyid': tnl_edagencyid,
            'coursetypeid': 1,
            'creditareaid': tnl_creditareaid,
            'creditvaluetypeid': tnl_creditvaluetypeid,
            'creditvalue': tnl_creditvalue,
            'needsapproval': False,
            'selfpaced': True}

    # Request object
    tnl_request = WebRequest(tnl_base_url)

    try:
        response = tnl_request.do_request(endpoint, 'post', tnl_encryptor.encrypt(json.dumps(data)))
        course_entry = TNLCourses(course=course.id,
                                  tnl_id=response.courseid,
                                  section_id=response.sectionid,
                                  registered=1,
                                  registration_date=datetime.datetime.utcnow())
    except:
        course_entry = TNLCourses(course=course.id, registered=0)

    course_entry.save()

