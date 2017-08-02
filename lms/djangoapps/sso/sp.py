from django.conf import settings
from django.db import transaction
from pytz import UTC
from django.contrib.auth import login, logout
from django.utils.translation import ugettext as _
import datetime
import json
from pepper_utilities.utils import random_mark
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from saml2.client import Saml2Client
from cache import IdentityCache, OutstandingQueriesCache
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.config import SPConfig
import copy
from os import path
import saml2
from saml2 import saml
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from student.models import UserProfile, Registration, CourseEnrollmentAllowed, CourseEnrollment
from student.models import SubjectArea, GradeLevel, YearsInEducation
from mitxmako.shortcuts import render_to_response
from student.views import upload_user_photo
import idp_metadata as metadata
import logging
from baseinfo.models import Enum
from django import db
import requests
import base64
from student.models import District, School, State
from django_future.csrf import ensure_csrf_cookie
from django.core.validators import validate_email, validate_slug, ValidationError
import random
from .models import CourseAssignmentCourse
from util import saml_django_response


# *Guess the xmlsec_path
try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None

if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary()
else:
    xmlsec_path = '/usr/local/bin/xmlsec1'

SSO_DIR = settings.PROJECT_HOME + "/sso"
BASEDIR = SSO_DIR + "/idp"
LMS_BASE = settings.LMS_BASE

log = logging.getLogger("audit")


def flat_dict(var, prefix=""):
    out = {}
    if isinstance(var, dict):
        for k, v in var.items():
            p = (prefix + ".") if prefix else ""
            out.update(flat_dict(v, p + k))
    else:
        out[prefix] = var

    return out


def map_data(setting, data):
    parsed_data = {}
    for attr in setting:
        mapped_name = attr['map'] if 'map' in attr else attr['name']
        if attr['name']:
            parsed_data[mapped_name] = data.get(attr['name'])
    return parsed_data


def https_redirect(request, url):
    '''Force redirect to a https address'''
    absolute_URL = request.build_absolute_uri(url)
    new_URL = "https%s" % absolute_URL[4:]
    return HttpResponseRedirect(new_URL)


def login_error(message):
    error_context = {'window_title': 'Login Error',
                     'error_title': 'Login Error',
                     'error_message': message}
    return render_to_response('error.html', error_context)


@csrf_exempt
def genericsso(request):
    """Assertion consume service (acs) of pepper"""
    sso_process = GenericSSO(request)
    return sso_process.acs_processor()


def get_sp_conf(idp_name):
    # Create setting before call pysaml2 method for current IDP
    # Refer to: https://pythonhosted.org/pysaml2/howto/config.html
    return {
        "allow_unknown_attributes": True,
        # full path to the xmlsec1 binary programm
        'xmlsec_binary': xmlsec_path,
        # your entity id, usually your subdomain plus the url to the metadata view
        'entityid': settings.SAML_ENTITY_ID,  # 'PCG:PepperPD:Entity:ID',
        # directory with attribute mapping
        'attribute_map_dir': path.join(SSO_DIR, 'attribute-maps'),
        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                "allow_unsolicited": True,
                'name': 'PepperPD',
                'name_id_format': saml.NAMEID_FORMAT_PERSISTENT,
                'endpoints': {
                    # url and binding to the assertion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        ('https://{0}/genericsso/'.format(LMS_BASE), saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        # ('https://{0}/saml2/ls/'.format(LMS_BASE), saml2.BINDING_HTTP_REDIRECT),
                        # ('https://{0}/saml2/ls/post'.format(LMS_BASE), saml2.BINDING_HTTP_POST),
                        settings.SAML_ENTITY_ID,  # sp's entity id
                    ]
                },
                # attributes that this project need to identify a user
                'required_attributes': ['email'],
                # attributes that may be useful to have but not required
                'optional_attributes': ['eduPersonAffiliation'],
                # in this section the list of IdPs we talk to are defined
                'idp': {
                    # we do not need a WAYF service since there is
                    # only an IdP defined here. This IdP should be
                    # present in our metadata
                    # the keys of this dictionary are entity ids
                    # 'https://idp.example.com/simplesaml/saml2/idp/metadata.php': {
                    #     'single_sign_on_service': {
                    #         saml2.BINDING_HTTP_REDIRECT: 'https://idp.example.com/simplesaml/saml2/idp/SSOService.php',
                    #         },
                    #     'single_logout_service': {
                    #         saml2.BINDING_HTTP_REDIRECT: 'https://idp.example.com/simplesaml/saml2/idp/SingleLogoutService.php',
                    #         },
                    #     },
                },
            },
        },
        # where the remote metadata is stored
        'metadata': {
            'local': [
                path.join(BASEDIR, idp_name, 'FederationMetadata.xml')
            ],
        },
        # set to 1 to output debugging information
        'debug': 1,
        # ===  CERTIFICATE ===
        # cert_file must be a PEM formatted certificate chain file.
        # example:
        # 'key_file': path.join(BASEDIR, 'sso/' + idp_name + 'mycert.key'),  # private part
        # 'cert_file': path.join(BASEDIR, 'sso/' + idp_name + 'mycert.pem'),  # public part
        # 'key_file': path.join(BASEDIR, 'sso/' + idp_name + 'mycert.key'),  # private part
        # 'cert_file': path.join(BASEDIR, 'sso/' + idp_name + 'customappsso.base64.cer'),  # public part
        # === OWN METADATA SETTINGS ===
        # 'contact_person': [
        #     {'given_name': 'Lorenzo',
        #      'sur_name': 'Gil',
        #      'company': 'Yaco Sistemas',
        #      'email_address': 'lgs@yaco.es',
        #      'contact_type': 'technical'},
        #     {'given_name': 'Angel',
        #      'sur_name': 'Fernandez',
        #      'company': 'Yaco Sistemas',
        #      'email_address': 'angel@yaco.es',
        #      'contact_type': 'administrative'},
        #     ],
        # === YOU CAN SET MULTILANGUAGE INFORMATION HERE ===
        # 'organization': {
        #     'name': [('Yaco Sistemas', 'es'), ('Yaco Systems', 'en')],
        #     'display_name': [('Yaco', 'es'), ('Yaco', 'en')],
        #     'url': [('http://www.yaco.es', 'es'), ('http://www.yaco.com', 'en')],
        #     },
        'valid_for': 24,  # how long is our metadata valid
    }


class GenericSSO:
    request = None
    sso_type = ''
    idp_name = ''
    token = ''
    url = ''
    metadata_setting = {}
    acs_processor = None
    data = None
    parsed_data = {}
    user = None

    def __init__(self, request):
        log.debug("===== genericsso: receiving a token =====")
        self.request = request

        # Both POST and GET method are supported to get IDP name
        self.idp_name = request.REQUEST.get('idp', False)
        self.token = request.GET.get('easyieptoken', False)
        self.url = request.GET.get('auth_link', False)

        if not self.idp_name and not self.token:
            raise Exception("error: No IDP name passed")
        elif not self.idp_name and self.token:
            self.idp_name = 'EasyIEP'
            self.sso_type = 'EasyIEP'

        if self.idp_name == 'EasyIEP':
            self.acs_processor = self.easyiep_acs
        else:
            self.metadata_setting = metadata.idp_by_name(self.idp_name)

            if self.metadata_setting is None:
                raise Exception("error: Unknown IDP")

            # Call different type of ACS separately
            self.sso_type = self.metadata_setting.get('sso_type')
            if self.sso_type == 'SAML':
                log.debug("message: it's SAML")
                self.acs_processor = self.saml_acs
            elif self.sso_type == 'OAuth2':
                self.acs_processor = self.oauth2_acs
            else:
                raise Exception("error: No SSO Type set.")

    def easyiep_acs(self):
        debug = self.request.GET.get('debug', False)
        # request json
        data = {'token': self.token}
        try:
            response = requests.request('post', self.url, data=data, timeout=15)
            text = response.text
        except Exception as e:
            log.warning(u"There was an EasyIEP SSO login error: {0}.".format(e))
            return login_error('''An error occurred while creating your user, please contact support at
                <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')

        if debug == 'true':
            return HttpResponse(text)

        # parse json
        parsed = json.loads(text)

        sso_error = parsed.get('lErrors')
        if sso_error:
            log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
                        .format("EasyIEP returned an error", text))
            return login_error('''An error occurred while creating your user, please contact support at
                <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')

        self.data = parsed.get('User')

        sso_id = self.data.get('idp_user_id', '')
        # sso_email = self.data.get('Email', '')
        sso_usercode = self.data.get('UserCode', '')
        self.data['Unique'] = str(sso_usercode) + '--' + str(sso_id)
        self.data['UserName'] = "EasyIEP{0}".format(random.randint(10000000000, 99999999999))

        if not self.data:
            log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
                        .format("No SSO User loaded", text))
            return login_error('''An error occurred while creating your user, please contact support at
                <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')

        self.request.session['idp'] = sso_usercode

        return self.post_acs()

        # try:
        #     validate_email(sso_email)
        # except ValidationError as e:
        #     log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
        #                 .format(e, text))
        #     return login_error('''The supplied email is invalid. Please contact support at
        #         <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')

        # try:
        #     profile = UserProfile.objects.get(sso_type='EasyIEP', sso_id=sso_unique)
        #     user = profile.user
        # except UserProfile.DoesNotExist:
        #     user = None
        #
        # if not user:
        #     try:
        #         username = "EasyIEP{0}".format(random.randint(10000000000, 99999999999))
        #
        #         # user
        #         user = User(username=username, email=sso_email, is_active=False)
        #         user.save()
        #
        #         # registration
        #         registration = Registration()
        #         registration.register(user)
        #
        #         # profile
        #         profile = UserProfile(user=user, sso_type='EasyIEP', sso_idp=sso_unique)
        #         profile.save()
        #
        #         # update user
        #         self.update_sso_usr(user, profile, parsed)
        #
        #         # allow courses
        #         cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG_Education/PEP101.1/S2016', email=sso_email)
        #         cea.is_active = True
        #         cea.auto_enroll = True
        #         cea.save()
        #
        #         # add courses above (cause user will not finish registration himself to trigger auto course enroll)
        #         CourseEnrollment.enroll(user, 'PCG_Education/PEP101.1/S2016')
        #
        #     except Exception as e:
        #         db.transaction.rollback()
        #         log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
        #                     .format(e, text))
        #         return login_error('''An error occurred while creating your user, please contact support at
        #             <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')
        #
        #     return redirect(reverse('register_user_easyiep', args=[registration.activation_key]))
        #
        # elif not user.is_active:
        #     try:
        #         self.update_sso_usr(user, user.profile, parsed)
        #     except Exception as e:
        #         db.transaction.rollback()
        #         log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
        #                     .format(e, text))
        #         return login_error('''An error occurred while updating your user, please contact support at
        #             <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')
        #     registration = Registration.objects.get(user_id=user.id)
        #     return redirect(reverse('register_user_easyiep', args=[registration.activation_key]))
        # else:
        #     # update user
        #     try:
        #         # update_sso_usr(user, parsed, False)
        #         pass
        #     except Exception as e:
        #         db.transaction.rollback()
        #         log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
        #                     .format(e, text))
        #         return login_error('''An error occurred while updating your user, please contact support at
        #             <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')
        #
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
        # user = authenticate(username=post_vars['username'], password=post_vars['password'])
        # login(self.request, user)
        # return redirect(reverse('dashboard'))
        # return HttpResponse("<textarea style='width:100%;height:100%'>"+json.dumps(parsed, indent=4, sort_keys=True)+"</textarea>")

    def oauth2_acs(self):
        request_token_url = self.metadata_setting.get('typed').get("oauth2_request_token_url")
        client_id = self.metadata_setting.get('typed').get("oauth2_client_id")
        client_secret = self.metadata_setting.get('typed').get("oauth2_client_secret")
        redirect_url = self.metadata_setting.get('typed').get("oauth2_redirect_url")

        basic = base64.b64encode(client_id + ":" + client_secret)
        headers = {'Authorization': "Basic " + basic, 'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            req = requests.request('POST', request_token_url,
                                   data={'code': self.request.GET.get('code'),
                                         'grant_type': 'authorization_code',
                                         'redirect_uri': redirect_url}, timeout=15,
                                   headers=headers)

            content = json.loads(req.text)

            me_url = self.metadata_setting.get('typed').get("oauth2_me_url")
            api_url = self.metadata_setting.get('typed').get("oauth2_api_url")
            # tokeninfo_url = self.metadata_setting.get('typed').get("oauth2_tokeninfo_url")

            # -----------------------
            # req = requests.request('GET', tokeninfo_url, timeout=15,
            #                        headers={'Authorization': 'Bearer '+content.get('access_token')})
            # # {"client_id":"172ddae01da8b5f08e6b","scopes":["read:teachers","read:students","read:school_admins","read:district_admins","read:user_id"]}
            # print req.text
            # tokeninfo = json.loads(req.text)

            # -----------------------
            req = requests.request('GET', api_url + me_url, timeout=15,
                                   headers={'Authorization': 'Bearer ' + content.get('access_token')})
            me = json.loads(req.text)

            # -----------------------
            profile_url = ""
            for link in me.get("links"):
                if link["rel"] == "canonical":
                    profile_url = link["uri"]

            req = requests.request('GET', api_url + profile_url, timeout=15,
                                   headers={'Authorization': 'Bearer ' + content.get('access_token')})

            profile = json.loads(req.text)
        except Exception as e:
            return HttpResponse(str(e))

        self.data = flat_dict(profile)
        return self.post_acs()

    def saml_acs(self):
        '''SAML ACS'''

        xmlstr = self.request.REQUEST.get("SAMLResponse")

        # ** load IDP config and parse the saml response
        conf = SPConfig()
        conf.load(copy.deepcopy(get_sp_conf(self.idp_name)))

        SP = Saml2Client(conf, identity_cache=IdentityCache(self.request.session))
        oq_cache = OutstandingQueriesCache(self.request.session)
        outstanding_queries = oq_cache.outstanding_queries()

        response = SP.parse_authn_request_response(xmlstr, BINDING_HTTP_POST, outstanding_queries)
        if not response:
            response = SP.parse_authn_request_response(xmlstr, BINDING_HTTP_REDIRECT, outstanding_queries)
            
        session_info = response.session_info()

        # Parse ava (received attributes) as dict
        self.data = {}
        for k, v in session_info['ava'].items():
            self.data[k] = v[0]

        return self.post_acs()

    def post_acs(self):
        # Fetch attributes
        if self.sso_type == 'EasyIEP':
            attribute_setting = [{'map': 'email', 'name': 'Email'},
                                 {'map': 'idp_user_id', 'name': 'Unique'},
                                 {'map': 'username', 'name': 'UserName'}]
        else:
            attribute_setting = self.metadata_setting.get('attributes')

        for attr in attribute_setting:
            mapped_name = attr['map'] if 'map' in attr else attr['name']
            if attr['name']:
                self.parsed_data[mapped_name] = self.data.get(attr['name'])

        idp_user_id = self.parsed_data.get('idp_user_id', False)
        email = self.parsed_data.get('email', False)
 
        if email:
            try:
                self.user = User.objects.get(email=email)
                # self.user_profile = UserProfile.objects.prefetch_related('user').get(sso_user_id=idp_user_id,
                #                                                                      sso_type=self.sso_type,
                #                                                                      sso_idp=self.idp_name)
            except:
                self.create_unknown_user()

            # self.user = User.objects.get(id=self.user.id)
            
            self.update_user()

            if not self.user.is_active:
                registration = Registration.objects.get(user_id=self.user.id)
                if self.sso_type == 'EasyIEP':
                    return reverse('register_user_easyiep', args=[registration.activation_key])
                return reverse('register_sso_user', args=[registration.activation_key])
            else:
                self.user.backend = ''  # 'django.contrib.auth.backends.ModelBackend'
                auth.login(self.request, self.user)
                return reverse("/dashboard")
        else:
            raise Exception('Invalid Email')

    
    def update_user(self):
        # Save mapped attributes
        for k, v in self.parsed_data.items():
            if k == 'first_name':
                self.user.first_name = self.parsed_data['first_name']
            elif k == 'last_name':
                self.user.last_name = self.parsed_data['last_name']
            elif k == 'email':
                self.user.email = self.parsed_data['email']
            elif k == 'district':
                self.user.profile.district = District.objects.get(name=self.parsed_data['district'])
            elif k == 'school':
                self.user.profile.school = School.objects.get(name=self.parsed_data['school'])
            elif k == 'grade_level':
                ids = GradeLevel.objects.filter(name__in=self.parsed_data['grade_level'].split(',')).values_list(
                    'id', flat=True)
                self.user.profile.grade_level = ','.join(ids)
            elif k == 'major_subject_area':
                ids = SubjectArea.objects.filter(name__in=self.parsed_data['major_subject_area'].split(',')).values_list(
                    'id', flat=True)
                self.user.profile.major_subject_area = ','.join(ids)
            elif k == 'years_in_education':
                self.user.profile.years_in_education = YearsInEducation.objects.get(
                    name=self.parsed_data['years_in_education'])
            elif k == 'percent_lunch':
                self.user.profile.percent_lunch = Enum.objects.get(name='percent_lunch',
                                                                   content=self.parsed_data['percent_lunch'])
            elif k == 'percent_iep':
                self.user.profile.percent_iep = Enum.objects.get(name='percent_iep',
                                                                 content=self.parsed_data['percent_iep'])
            elif k == 'percent_eng_learner':
                self.user.profile.percent_eng_learner = Enum.objects.get(
                    name='percent_eng_learner', content=self.parsed_data['percent_eng_learner'])

            self.user.profile.sso_type = self.sso_type
            self.user.profile.sso_idp = self.idp_name
            self.user.profile.sso_user_id = self.parsed_data.get('idp_user_id')

            self.user.save()
            self.user.profile.save()

    def create_unknown_user(self):
        """Create the sso user who does not exist in pepper"""

        try:
            # Generate username if not provided
            if not self.parsed_data.get('username'):
                username = random_mark(20)
            else:
                username = self.parsed_data['username']

            # Email must be provided
            email = self.parsed_data['email']

            self.user = User(username=username, email=email, is_active=False)
            self.user.set_password(username)  # Set password the same with username
            self.user.save()

            registration = Registration()
            registration.register(self.user)

            self.user.profile = UserProfile(user=self.user)
            self.user.profile.subscription_status = "Imported"

            self.update_user()

            courses = []
            try:
                cas = CourseAssignmentCourse.objects.filter(assignment__sso_name=self.user.profile.sso_idp)
                for course in cas:
                    courses.append(course.course)
            except:
                pass
            for course in courses:
                cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id=course, email=email)
                cea.is_active = True
                cea.auto_enroll = True
                cea.save()

            if self.sso_type == 'EasyIEP':
                return reverse('register_user_easyiep', args=[registration.activation_key])
            return reverse('register_sso_user', args=[registration.activation_key])

        except Exception as e:
            db.transaction.rollback()
            log.error("error: failed to create SSO user: {0}".format(e))
            raise e

    def update_sso_usr(self, user, profile, parsed):
        sso_user = json.get('User')
        sso_id = sso_user.get('idp_user_id', '')
        sso_district_code = json.get('SchoolSystemCode')
        sso_email = sso_user.get('Email', '')
        sso_usercode = sso_user.get('UserCode', '')
        sso_unique = str(sso_usercode) + '--' + str(sso_id)

        try:
            sso_state = State.objects.get(name=json.get('State'))
        except State.DoesNotExist as e:
            log.warning(u"There was an EasyIEP SSO login error: {0}."
                              .format(e))
            return login_error('''An error occurred while updating your user, please contact support at
                <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')

        try:
            validate_email(sso_email)
        except ValidationError as e:
            log.warning(u"There was an EasyIEP SSO login error: {0}. This is the user info from EasyIEP: {1}"
                              .format(e, json))
            return login_error('''The supplied email is invalid. Please contact support at
                <a href="mailto:peppersupport@pcgus.com">peppersupport@pcgus.com</a> for further assistance.''')

        # user
        user.set_password('EasyIEPSSO')
        user.email = sso_email
        # if update_first_name:
        #     user.first_name = sso_user.get('FirstName', '')
        # user.last_name = sso_user.get('LastName', '')
        user.save()

        # district
        # profile.district = District.objects.get(state=sso_state.id, code=sso_district_code)

        # school
        # safe_state = re.sub(' ', '', sso_state.name)
        # multi_school_id = 'pepper' + safe_state + str(sso_district_code)
        # if len(sso_user['SchoolCodes']) == 1:
        #     try:
        #         school = School.objects.get(code=sso_user['SchoolCodes'][0], district=profile.district.id)
        #     except School.DoesNotExist:
        #         school = School.objects.get(code=multi_school_id)
        # else:
        #     school = School.objects.get(code=multi_school_id)

        # profile.school = school

        # unique ID for our records
        profile.sso_idp = sso_unique

        # save
        profile.save()


@ensure_csrf_cookie
def register_user_easyiep(request, activation_key):

    registration = Registration.objects.get(activation_key=activation_key)
    user_id = registration.user_id

    profile = UserProfile.objects.get(user_id=user_id)

    context = {
        'profile': profile,
        'activation_key': activation_key
    }

    return render_to_response('register_easyiep.html', context)


def register_sso(request, activation_key):
    '''Register page for non-activated sso auto created user.'''
    registration = Registration.objects.get(activation_key=activation_key)
    user_id = registration.user_id
    profile = UserProfile.objects.get(user_id=user_id)

    ms = metadata.idp_by_name(profile.sso_idp)
    attribute_setting = ms.get('attributes')

    attribute_mapping = {}
    for attr in attribute_setting:
        mapped_name = attr['map'] if attr['map'] else attr['name']
        attribute_mapping[mapped_name] = attr

    context = {
        'profile': profile,
        'activation_key': activation_key,
        'attribute_mapping': attribute_mapping
    }
    return render_to_response('register_sso.html', context)


def activate_account(request):
    '''Process posted data from registration form'''
    vars = request.POST

    # ** fetch user by activation_key
    registration = Registration.objects.get(activation_key=vars.get('activation_key', ''))
    user_id = registration.user_id
    profile = UserProfile.objects.get(user_id=user_id)

    # ** validate username
    try:
        validate_slug(vars['username'])
    except ValidationError:
        js = {'success': False}
        js['value'] = _("Username should only consist of A-Z and 0-9, with no spaces.")
        js['field'] = 'username'
        return HttpResponse(json.dumps(js), content_type="application/json")

    # ** validate if user exists
    if User.objects.filter(username=vars['username']).exclude(email=profile.user.email).exists():
        js = {'success': False}
        js['value'] = _("An account with the Public Username '{username}' already exists.").format(
            username=vars['username'])
        js['field'] = 'username'
        return HttpResponse(json.dumps(js), content_type="application/json")

    # ** validate fields
    required_post_vars_dropdown = [
        'first_name',
        'last_name',
        'state_id',
        'district_id',
        'school_id',
        'major_subject_area_id',
        # 'grade_level_id',
        'years_in_education_id',
        'percent_lunch',
        'percent_iep',
        'percent_eng_learner']

    for a in required_post_vars_dropdown:
        if len(vars[a]) < 1:
            error_str = {
                'first_name': 'Your first name is required.',
                'last_name': 'Your last name is required.',
                'major_subject_area_id': 'Major Subject Area is required.',
                # 'grade_level_id':'Grade Level-Check is required',
                'state_id': 'State is required.',
                'district_id': 'District is required.',
                'school_id': 'School is required.',
                'years_in_education_id': 'Number of Years in Education is required.',
                'percent_lunch': 'Free/Reduced Lunch is required.',
                'percent_iep': 'IEPs is required.',
                'percent_eng_learner': 'English Learners is required.'
            }
            js = {'success': False}
            js['value'] = error_str[a]
            js['field'] = a
            return HttpResponse(json.dumps(js), content_type="application/json")

    # ** validate terms_of_service
    if vars.get('terms_of_service', 'false') != u'true':
        js = {'success': False}
        js['value'] = _("You must accept the terms of service.")
        js['field'] = 'terms_of_service'
        return HttpResponse(json.dumps(js), content_type="application/json")

    try:
        # ** update user
        profile.user.username = vars.get('username', '')
        profile.user.first_name = vars.get('first_name', '')
        profile.user.last_name = vars.get('last_name', '')
        profile.user.is_active = True
        profile.user.save()

        # ** update profile
        profile.district_id = vars.get('district_id', '')
        profile.school_id = vars.get('school_id', '')
        profile.subscription_status = 'Registered'
        profile.grade_level_id = vars.get('grade_level_id', '')
        profile.major_subject_area_id = vars.get('major_subject_area_id', '')
        profile.years_in_education_id = vars.get('years_in_education_id', '')
        profile.percent_lunch = vars.get('percent_lunch', '')
        profile.percent_iep = vars.get('percent_iep', '')
        profile.percent_eng_learner = vars.get('percent_eng_learner', '')
        profile.bio = vars.get('bio', '')
        profile.activate_date = datetime.datetime.now(UTC)
        profile.save()

        # ** upload photo
        photo = request.FILES.get("photo")
        upload_user_photo(profile.user.id, photo)

        # ** auto enroll courses
        ceas = CourseEnrollmentAllowed.objects.filter(email=profile.user.email)
        for cea in ceas:
            if cea.auto_enroll:
                CourseEnrollment.enroll(profile.user, cea.course_id)

        js = {'success': True}
    except Exception as e:
        transaction.rollback()
        js = {'success': False}
        js['error'] = "%s" % e

    # ** log the user in
    profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, profile.user)

    return HttpResponse(json.dumps(js), content_type="application/json")


@csrf_exempt
def slo_request_receive(request):    
    """
    Receive a saml slo request (from IDP)
    """
    # ** todo: is it possible to get idp name just from saml request body?
    # ** by: idp_name = req_info.issuer.text
    # ** but we need to parse_logout_request at first
    # ** that requires idp's FederationMetadata.xml
    # ** so we need to know idp's name before that
    idp_name = request.REQUEST.get("idp")
    relay_state = request.REQUEST.get("RelayState")
    saml_request = request.REQUEST.get("SAMLResponse")
    saml_setting = {
        'entityid': settings.SAML_ENTITY_ID,  # sp's entity id
        'service': {
            'sp': {
                'endpoints': {
                    'single_logout_service': [
                        settings.SAML_ENTITY_ID  # sp's entity id
                    ]
                }
            }
        },
        'metadata': {
            'local': [
                path.join(BASEDIR, idp_name, 'FederationMetadata.xml')  # metadata of idp
            ]
        },
        # 'valid_for': 24,  # how long is our metadata valid
    }

    conf = SPConfig()
    conf.load(copy.deepcopy(saml_setting))

    SP = Saml2Client(conf, identity_cache=IdentityCache(request.session))
    binding, destination = SP.pick_binding("single_logout_service", entity_id=idp_name)
    req_info = SP.parse_logout_request(saml_request, binding)

    if request.user.is_authenticated() and request.user.email == req_info.message.name_id.text:
        logout(request)
    
    saml_response = SP.create_logout_response(req_info.message, [binding])

    http_args = SP.apply_binding(
        binding=binding,
        msg_str=saml_response,
        destination=destination,
        relay_state=relay_state,
        response=True)
    
    return saml_django_response(binding, http_args)
