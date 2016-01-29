# Imports
import datetime
import logging
import json

from django.conf import settings

from student.models import District, User, State
from tnl_integration.models import TNLCourses, TNLCompletionTrack, TNLDistricts, TNLDomains
from web_client.crypt import salt_convert, PBEWithMD5AndDES
from web_client.request import WebRequest

# ========== Global variables ==========
# The logging mechanism
AUDIT_LOG = logging.getLogger("audit")


class TNLInstance:
    def __init__(self, domain_id):
        try:
            self.domain = TNLDomains.objects.get(id=domain_id)
            # Domain specific encryption information
            tnl_enc_password = self.domain.password
            tnl_enc_salt = salt_convert(self.domain.salt)
            tnl_enc_iterations = 22
            self.encryptor = PBEWithMD5AndDES(tnl_enc_password, tnl_enc_salt, tnl_enc_iterations)
            self.request = WebRequest(self.domain.base_url, 'success', True, 'message')
        except:
            raise Exception('This domain is invalid')

    def get_person(self, user):
        """
        This gets the TNL personid
        """
        # getPersonId endpoint
        endpoint = 'ia/app/webservices/person/getPersonId'
        # Parameters needed for this request
        data = {'adminid': self.domain.admin_id,
                'email': user.email}

        try:
            # Need to encrypt the data we send to TNL. Encryption adds a trailing newline, so get rid of it.
            response = self.request.do_request(endpoint, 'post', self.encryptor.encrypt(json.dumps(data)).rstrip("\n"))
            return response['personid']
        except:
            return False

    def get_grade(self, percent):
        """
        Matches our grade with the gradeid data from TNL
        """
        # Get the percent value from the decimal grade.
        grade = round(percent * 100)
        grade_out = False
        # Compare our percent grade to the list of values for this TNL setup and return the matched value.
        for gradeid, grades in self.domain.grades:  # TODO: need to fix this for the new storage
            if grade in grades:
                grade_out = gradeid

        return grade_out

    def register_completion(self, user, course_id, percent):
        """
        This registers a competed course for a particular user with TNL
        """

        # Registered course.
        course = tnl_get_course(course_id)
        # markComplete endpoint.
        endpoint = 'ia/app/webservices/section/markComplete'
        # Get the TNL user id.
        personid = self.get_person(user)
        if personid:
            # Assign needed parameters.
            data = {'adminid': self.domain.admin_id,
                    'personid': personid,
                    'sectionid': course.section_id,
                    'gradeid': self.get_grade(percent),
                    'sectionrosterid': ''}

            try:
                # Need to encrypt the data we send to TNL. Encryption adds a trailing newline, so get rid of it.
                self.request.do_request(endpoint, 'post', self.encryptor.encrypt(json.dumps(data)).rstrip("\n"))
                # Store the completion locally for tracking, with the date.
                track = TNLCompletionTrack(user=user,
                                           course=course,
                                           registered=1,
                                           registration_date=datetime.datetime.utcnow())
            except:
                # If the TNL completion registration failed, we still want to store that we tried so we can follow up.
                track = TNLCompletionTrack(user=user, course=course, registered=0)

            track.save()
            return True
        else:
            return False

    def register_course(self, course):
        """
        This registers the course with TNL
        """
        # createSDLCourse endpoint (SDL seems the best fit for our courses)
        endpoint = 'ia/app/webservices/course/createSDLCourse'

        # Parameters needed for the request
        data = {'adminid': self.domain.admin_id,
                'title': course.display_name_with_default,
                'number': course.display_number_with_default,
                'externalid': course.id,
                'providerid': self.domain.provider_id,
                'edagencyid': self.domain.edagency_id,
                'coursetypeid': 1,
                'creditareaid': self.domain.credit_area_id,
                'creditvaluetypeid': self.domain.credit_value_type_id,
                'creditvalue': self.domain.credit_value,
                'needsapproval': False,
                'selfpaced': True}

        try:
            # Need to encrypt the data we send to TNL. Encryption adds a trailing newline, so get rid of it.
            response = self.request.do_request(endpoint, 'post', self.encryptor.encrypt(json.dumps(data)).rstrip("\n"))
            # Build the registration info for the local table.
            course_entry = TNLCourses(course=course.id,
                                      domain=self.domain,
                                      tnl_id=response['courseid'],
                                      section_id=response['sectionid'],
                                      registered=1,
                                      registration_date=datetime.datetime.utcnow())
        except:
            response = {'success': False}
            # If the registration with TNL failed, we still want to track it locally so we can follow up.
            course_entry = TNLCourses(course=course.id, registered=0)

        course_entry.save()
        return response


def tnl_check_district(district_id):
    """
    Checks to see if this district is TNL-enabled
    """
    try:
        # Tries to load the district in question from the TNL table.
        TNLDistricts.objects.get(district=district_id)
        return True
    except:
        return False


def tnl_get_domain(id='all'):
    """
    Gets the domain(s) from the domain table.
    """
    try:
        if not id == 'all':
            # Just select the specified course.
            domain = TNLDomains.objects.get(id=id)
        else:
            # Select all the courses.
            domain = TNLDomains.objects.all()
    except:
        domain = False

    return domain


def tnl_get_course(id='all', domain=False):
    """
    Gets the course(s) from the registered course table.
    """
    try:
        if not id == 'all':
            filters = {'course': id}
            if domain:
                filters.update({'domain': domain})
            # Just select the specified course.
            course = TNLCourses.objects.get(**filters)
        else:
            # Select all the courses.
            course = TNLCourses.objects.all()
    except:
        course = False

    return course


def tnl_add_domain(id, edit, data):
    """
    Adds the domain to the table.
    """
    try:
        data['state'] = State.objects.get(id=data['state'])
        if edit:
            TNLDomains.objects.filter(id=int(id)).update(**data)
        else:
            domain_entry = TNLDomains(**data)
            domain_entry.save()
    except Exception, e:
        raise Exception('Problem adding/updating domain: {0}'.format(e))


def tnl_delete_domain(ids):
    """
    Deletes selected domains from the DB.
    """
    try:
        for id in ids:
            TNLDomains.objects.filter(id=id).delete()
    except Exception, e:
        raise Exception('Problem deleting domain(s): {0}'.format(e))


def tnl_get_district(id='all'):
    """
    Gets the district(s) from the configured districts, along with other district data.
    """
    try:
        if not id == 'all':
            # Just select the specified district, with related items so we cache the actual district data.
            district = TNLDistricts.objects.get(course=id).select_related()
        else:
            # Select all the districts, with related items so we cache the actual district data.
            district = TNLDistricts.objects.all().select_related()
    except:
        district = False

    return district


def tnl_add_district(id, domain):
    """
    Adds a district to the TNL-enabled districts
    """
    # Load the actual district data.
    district = District.objects.get(id=id)
    # Load the Domain.
    domain = TNLDomains.objects.get(id=domain)
    # Store this district as enabled.
    district_entry = TNLDistricts(district=district, domain=domain)
    district_entry.save()


def tnl_delete_district(ids):
    """
    Deletes district(s) from the TNL-enabled districts.
    """
    try:
        for id in ids:
            TNLDistricts.objects.filter(id=id).delete()
    except Exception, e:
        raise Exception('Problem deleting district(s): {0}'.format(e))


def tnl_delete_course(ids):
    """
    Deletes course(s) from the list of enabled ones (doesn't remove from TNL).
    """
    try:
        for id in ids:
            TNLCourses.objects.filter(id=id).delete()
    except Exception, e:
        raise Exception('Problem deleting course(s): {0}'.format(e))


def tnl_course(user, course_id):
    """
    Checks to see if this is in fact a course and user registered with TNL.
    """
    # Get the specified user and then their domain, if they have one.
    user = User.objects.get(id=user.id)
    try:
        domain = tnl_domain_from_user(user)
    except Exception as e:
        AUDIT_LOG.warning(u"There was no domain for this user: {0}.".format(e))
        return False

    # Get the course, if registered.
    course = tnl_get_course(course_id, domain)
    if course:
        try:
            # Make sure that the user belongs to a district that is registered with TNL.
            district = District.objects.get(id=user.profile.district_id)
            if tnl_check_district(district.id):
                return True
            else:
                AUDIT_LOG.warning(u"This user's district is not TNL-enabled.")
                return False
        except Exception as e:
            AUDIT_LOG.warning(u"There was an error while determining whether TNL-enabled: {0}.".format(e))
            return False
    else:
        AUDIT_LOG.warning(u"This course is not TNL-enabled for this user/domain.")
        return False


def tnl_domain_from_user(user):
    """
    Gets the domain associated with the district of the current user.
    """
    user = User.objects.get(id=user.id)
    try:
        district = District.objects.get(id=user.profile.district_id)
        tnl_district = TNLDistricts.objects.get(district=district)
        domain = tnl_district.domain.id
    except Exception as e:
        raise Exception(u"Unable to find a domain for this user: {0}".format(e))
    return domain


def get_post_array(post, name):
    """
    Gets array values from a jQuery POST.
    """
    output = list()
    for k in post.keys():
        if k.startswith(name):
            output.append(post.get(k))
    return output
