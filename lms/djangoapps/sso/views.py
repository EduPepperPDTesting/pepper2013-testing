from django.conf import settings
from django.db import IntegrityError, transaction
from pytz import UTC
from django.contrib.auth import logout, authenticate, login
from django.utils.translation import ugettext as _
from django.core.validators import validate_email, validate_slug, ValidationError
import datetime
import json
import random
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from saml2.client import Saml2Client
from cache import IdentityCache, OutstandingQueriesCache
from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
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
from student.models import UserProfile, Registration, CourseEnrollmentAllowed
from mitxmako.shortcuts import render_to_response, render_to_string
import time
import calendar
from student.views import upload_user_photo
import metadata
import logging
from student.models import State, District, SubjectArea, GradeLevel, YearsInEducation, School
from baseinfo.models import Enum
from django import db

log = logging.getLogger("tracking")
BASEDIR = path.dirname("lms/")


@require_POST
@csrf_exempt
def genericsso(request):
    '''Assertion consume service (acs) of pepper'''

    log.debug("===== genericsso: receiving a token =====")

    # Both POST and GET method are supported to get IDP name
    idp_name = request.REQUEST.get('idp', '')

    if idp_name == '':
        log.error("error: No IDP name passed")
        raise Http404()

    metadata_setting = metadata.idp_by_name(idp_name)

    if metadata_setting is None:
        log.error("error: Unkonwn IDP")
        raise Http404()

    if metadata_setting.get('sso_type') == 'SAML':
        log.debug("message: it's SAML")
        return samlACS(request, idp_name, metadata_setting)


def samlACS(request, idp_name, ms):
    '''SAML ACS'''

    xmlstr = request.POST.get("SAMLResponse")

    # Refer to: https://pythonhosted.org/pysaml2/howto/config.html
    setting = {
        "allow_unknown_attributes": True,
        # full path to the xmlsec1 binary programm
        'xmlsec_binary': '/usr/bin/xmlsec1',
        # your entity id, usually your subdomain plus the url to the metadata view
        'entityid': 'PCG:PepperPD:Entity:ID',
        # directory with attribute mapping
        'attribute_map_dir': path.join(BASEDIR, 'sso/' + idp_name + '/attribute-maps'),
        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                "allow_unsolicited": True,
                'name': 'Federated Django sample SP',
                'name_id_format': saml.NAMEID_FORMAT_PERSISTENT,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        ('https://59.45.37.54/genericsso/', saml2.BINDING_HTTP_POST),
                        ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        ('https://59.45.37.54/saml2/ls/', saml2.BINDING_HTTP_REDIRECT),
                        ('https://59.45.37.54/saml2/ls/post', saml2.BINDING_HTTP_POST),
                      ]
                    },
                # attributes that this project need to identify a user
                'required_attributes': ['uid'],
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
                path.join(BASEDIR, 'sso/' + idp_name + '/FederationMetadata.xml')
                ],
            },
        # set to 1 to output debugging information
        'debug': 1,
        # ===  CERTIFICATE ===
        # cert_file must be a PEM formatted certificate chain file.
        # example:
        # 'key_file': path.join(BASEDIR, 'sso/' + idp_name + '/mycert.key'),  # private part
        # 'cert_file': path.join(BASEDIR, 'sso/' + idp_name + '/mycert.pem'),  # public part
        # 'key_file': path.join(BASEDIR, 'sso/' + idp_name + '/mycert.key'),  # private part
        # 'cert_file': path.join(BASEDIR, 'sso/' + idp_name + '/customappsso.base64.cer'),  # public part        
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

    #** load IDP config and parse the saml response
    conf = SPConfig()
    conf.load(copy.deepcopy(setting))

    client = Saml2Client(conf, identity_cache=IdentityCache(request.session))
    oq_cache = OutstandingQueriesCache(request.session)
    outstanding_queries = oq_cache.outstanding_queries()

    response = client.parse_authn_request_response(xmlstr, BINDING_HTTP_POST, outstanding_queries)
    session_info = response.session_info()

    # Parse ava as dict
    data = {}
    for k, v in session_info['ava'].items():
        data[k] = v[0]

    # Fetch email
    attribute_setting = ms.get('attributes')
    parsed_data = {}
    for attr in attribute_setting:
        mapped_name = attr['map'] if attr['map'] else attr['name']
        parsed_data[mapped_name] = data[attr['name']]
    email = parsed_data.get('email')

    # which idp
    # print session_info['issuer']

    #** consume the assertion
    users = User.objects.filter(email=email)

    if users.exists():
        user = users.all()[0]
        if not user.is_active:
            registration = Registration.objects.get(user_id=user.id)
            return https_redirect(request, reverse('register_sso', args=[registration.activation_key]))
        else:
            user.backend = ''  # 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return https_redirect(request, "/dashboard")
    else:
        return create_unknown_user(request, ms, data)


def https_redirect(request, url):
    '''Force redirect to a https address'''
    absolute_URL = request.build_absolute_uri(url)
    new_URL = "https%s" % absolute_URL[4:]
    return HttpResponseRedirect(new_URL)


def random_mark(length):
    return "".join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz1234567890@#$%^&*_+{};~') for _ in range(length))


def create_unknown_user(request, ms, data):
    '''Create the sso user who\'s not exists in pepper'''

    try:
        attribute_setting = ms.get('attributes')

        parsed_data = {}

        for attr in attribute_setting:
            mapped_name = attr['map'] if attr['map'] else attr['name']
            parsed_data[mapped_name] = data[mapped_name]

        if not parsed_data.get('username'):
            username = random_mark(20)
        else:
            username = parsed_data['username']

        email = parsed_data['email']

        user = User(username=username, email=email, is_active=False)

        # Set password the same with username
        user.set_password(username)
        user.save()

        registration = Registration()
        registration.register(user)

        profile = UserProfile(user=user)
        profile.subscription_status = "Imported"
        profile.sso_type = ms.get('sso_type')
        profile.sso_idp = ms.get('sso_name')

        for k, v in parsed_data.items():
            if k == 'first_name':
                user.first_name = parsed_data['first_name']
            if k == 'last_name':
                user.last_name = parsed_data['last_name']
            if k == 'district':
                profile.district = District.object.get(name=parsed_data['district'])
            if k == 'school':
                profile.school = School.object.get(name=parsed_data['school'])
            if k == 'grade_level':
                profile.district = GradeLevel.object.get(name=parsed_data['grade_level'])
            if k == 'major_subject_area':
                ids = SubjectArea.object.filter(name__in=parsed_data['major_subject_area'].split(',')).values_list('id', flat=True)
                profile.major_subject_area = ','.join(ids)
            if k == 'years_in_education':
                profile.years_in_education = YearsInEducation.object.get(name=parsed_data['years_in_education'])
            if k == 'percent_lunch':
                profile.percent_lunch = Enum.object.get(name='percent_lunch', content=parsed_data['percent_lunch'])
            if k == 'percent_iep':
                profile.percent_iep = Enum.object.get(name='percent_iep', content=parsed_data['percent_iep'])
            if k == 'percent_eng_learner':
                profile.percent_eng_learner = Enum.object.get(name='percent_eng_learner', content=parsed_data['percent_eng_learner'])

        user.save()
        profile.save()

        cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
        cea.is_active = True
        cea.auto_enroll = True
        cea.save()

    except Exception as e:
        db.transaction.rollback()
        log.error("error: failed to create SSO user: %s" % e)

    return https_redirect(request, reverse('register_sso', args=[registration.activation_key]))


def register_sso(request, activation_key):
    '''Register page for not acitved sso auto created user.'''
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
    '''Process posted data from registeration form'''
    vars = request.POST

    #** fetch user by activation_key
    registration = Registration.objects.get(activation_key=vars.get('activation_key', ''))
    user_id = registration.user_id
    profile = UserProfile.objects.get(user_id=user_id)

    #** validate username
    try:
        validate_slug(vars['username'])
    except ValidationError:
        js = {'success': False}
        js['value'] = _("Username should only consist of A-Z and 0-9, with no spaces.")
        js['field'] = 'username'
        return HttpResponse(json.dumps(js), content_type="application/json")

    #** validate if user exists
    if User.objects.filter(username=vars['username']).exclude(email=profile.user.email).exists():
        js = {'success': False}
        js['value'] = _("An account with the Public Username '{username}' already exists.").format(username=vars['username'])
        js['field'] = 'username'
        return HttpResponse(json.dumps(js), content_type="application/json")

    #** validate fields
    required_post_vars_dropdown = [
        'state_id',
        'district_id',
        'school_id',
        'major_subject_area_id',
        # 'grade_level_id',
        'years_in_education_id',
        'percent_lunch', 'percent_iep', 'percent_eng_learner']

    for a in required_post_vars_dropdown:
        if len(vars[a]) < 1:
            error_str = {
                'major_subject_area_id': 'Major Subject Area is required',
                # 'grade_level_id':'Grade Level-heck is required',
                'state_id': 'State is required',
                'district_id': 'District is required',
                'school_id': 'School is required',
                'years_in_education_id': 'Number of Years in Education is required',
                'percent_lunch': 'Free/Reduced Lunch is required',
                'percent_iep': 'IEPs is required',
                'percent_eng_learner': 'English Learners is required'
            }
            js = {'success': False}
            js['value'] = error_str[a]
            js['field'] = a
            return HttpResponse(json.dumps(js), content_type="application/json")

    #** validate terms_of_service
    if vars.get('terms_of_service', 'false') != u'true':
        js = {'success': False}
        js['value'] = _("You must accept the terms of service.")
        js['field'] = 'terms_of_service'
        return HttpResponse(json.dumps(js), content_type="application/json")

    try:
        #** update user
        profile.user.username = vars.get('username', '')
        profile.user.is_active = True
        profile.user.save()

        #** update profile
        profile.district_id = vars.get('district_id', '')
        profile.school_id = vars.get('school_id', '')
        profile.subscription_status = 'Registered'
        profile.major_subject_area_id = vars.get('major_subject_area_id', '')
        profile.years_in_education_id = vars.get('years_in_education_id', '')
        profile.percent_lunch = vars.get('percent_lunch', '')
        profile.percent_iep = vars.get('percent_iep', '')
        profile.percent_eng_learner = vars.get('percent_eng_learner', '')
        profile.bio = vars.get('bio', '')
        profile.activate_date = datetime.datetime.now(UTC)
        profile.save()

        #** upload photo
        photo = request.FILES.get("photo")
        upload_user_photo(profile.user.id, photo)
        js = {'success': True}
    except Exception as e:
        transaction.rollback()
        js = {'success': False}
        js['error'] = "%s" % e

    #** log the user in
    profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, profile.user)

    return HttpResponse(json.dumps(js), content_type="application/json")
    
    
