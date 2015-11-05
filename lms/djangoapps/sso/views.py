from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from saml2.client import Saml2Client
from djangosaml2.cache import IdentityCache, OutstandingQueriesCache
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


@require_POST
@csrf_exempt
def genericsso(request):
    '''Assertion consume service (acs) of pepper'''

    coming_from = request.GET.get('idp', '')
    
    import time
    import calendar

    # print time.gmtime()
    # print calendar.timegm(time.gmtime())
     
    # https://login.microsoftonline.com/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/reprocess?sessionId=fcf22de7-e68e-4740-96a5-1cc1a5020fef&ctx=rQIIAbMSyigpKbDS1ze11DMx1TM21zM1KRLiElCx03jXpDnXcec7iRsrygQ-HmJUykyxTDFIskxMTrVMTDQwMU5OTEy1MEw2Sk42MjZKMTRNS7rAyPiCkfEWE2twYm6O0SMmHjAdEJ6aFFyc_4vJrLQozyo_sTiz2CovMTe12Kok2SrY0dfHylDPECySmaKbll-Um1hilZqbmJnjmJJSlFpcPImZtxhkToEemDLYxKxiYGxpnpSSZqhrkpZmqWtinmqqawF0ja6xcaJZsoFJklmyqcEFFp5dnPIg3xWjek8_PTUvtSgzubg4Xx8A0
    # return HttpResponse(request.META.get('HTTP_REFERER'))

# SAMLResponse:PEF1dGhuQ29udGV4dENsYXNzUmVmPnVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphYzpjbGFzc2VzOlBhc3N3b3JkPC9BdXRobkNvbnRleHRDbGFzc1JlZj48L0F1dGhuQ29udGV4dD48L0F1dGhuU3RhdGVtZW50PjwvQXNzZXJ0aW9uPjwvc2FtbHA6UmVzcG9uc2U
    xmlstr = request.POST.get("SAMLResponse")

    # https://pythonhosted.org/pysaml2/howto/config.html

    BASEDIR = path.dirname("lms/")
    setting = {
        "allow_unknown_attributes": True,
        # full path to the xmlsec1 binary programm
        'xmlsec_binary': '/usr/bin/xmlsec1',
        # your entity id, usually your subdomain plus the url to the metadata view
        'entityid': 'pcg:pepperpd:entity:id',
        # directory with attribute mapping
        'attribute_map_dir': path.join(BASEDIR, 'sso/testsite/attribute-maps'),
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
                path.join(BASEDIR, 'sso/victor/FederationMetadata.xml')
                ],
            },
        # set to 1 to output debugging information
        'debug': 1,

        # certificate
        # 'key_file': path.join(BASEDIR, 'sso/victor/mycert.key'),  # private part
        # 'cert_file': path.join(BASEDIR, 'sso/victor/mycert.pem'),  # public part

        # own metadata settings
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

        # you can set multilanguage information here
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

    email = session_info['ava']['mail'][0]

    # which idp
    print session_info['issuer']

    #** consume the assertion
    users = User.objects.filter(email=email)

    if users.exists():
        user = users.all()[0]
        if not user.is_active:
            registration = Registration.objects.get(user_id=user.id)
            return HttpResponse("xxx")
            return https_redirect(request, reverse('register_sso_user', args=[registration.activation_key]))
        else:
            user.backend = ''  # 'django.contrib.auth.backends.ModelBackend'    
            auth.login(request, user)
            return https_redirect(request, "/dashboard")
    else:
        firstname = session_info['ava']['firstname'][0]
        lastname = session_info['ava']['lastname'][0]
        username = session_info['ava']['username'][0]
        create_unknown_user(request, email, username, firstname, lastname)
        

def https_redirect(request, url):
    '''Force redirect to a https address'''
    absolute_URL = request.build_absolute_uri(url)
    new_URL = "https%s" % absolute_URL[4:]
    return HttpResponseRedirect(new_URL)


def create_unknown_user(request, email, username, firstname, lastname):
    '''Create the sso user who\'s not exists in pepper'''
    user = User(username=username, email=email, is_active=False)
    user.first_name = firstname
    user.last_name = lastname
    user.set_password(username)
    user.save()
    registration = Registration()
    registration.register(user)
    profile = UserProfile(user=user)
    profile.subscription_status = "Imported"
    profile.save()

    cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
    cea.is_active = True
    cea.auto_enroll = True
    cea.save()

    return https_redirect(reverse('register_sso_user', args=[registration.activation_key]))


def register_sso_user(request, activation_key):
    '''Register page for not acitved sso auto created user.'''
    registration = Registration.objects.get(activation_key=activation_key)
    user_id = registration.user_id
    profile = UserProfile.objects.get(user_id=user_id)
    context = {
        'profile': profile,
        'activation_key': activation_key
    }
    return render_to_response('register_sso_user.html', context)
