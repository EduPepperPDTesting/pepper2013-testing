import argparse
import base64
import importlib
import logging
import os
import re
import time
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from Cookie import SimpleCookie
from hashlib import sha1
from urlparse import parse_qs
from cherrypy import wsgiserver
from cherrypy.wsgiserver import ssl_pyopenssl
from saml2 import BINDING_HTTP_ARTIFACT
from saml2 import BINDING_URI
from saml2 import BINDING_PAOS
from saml2 import BINDING_SOAP
from saml2 import BINDING_HTTP_REDIRECT
from saml2 import BINDING_HTTP_POST
from saml2 import server  # A class that does things that IdPs or AAs do
from cache import IdentityCache, OutstandingQueriesCache

from saml2.saml import NAME_FORMAT_URI, NAMEID_FORMAT_TRANSIENT, NAMEID_FORMAT_PERSISTENT, NameID

from saml2.config import IdPConfig
from saml2.config import SPConfig

import copy
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import sp_metadata as metadata
from os import path
import urllib

from saml2.s_utils import sid
from saml2.samlp import SessionIndex
from django.views.decorators.csrf import csrf_exempt
from util import saml_django_response
from django.contrib.auth import login, logout
from student.views import logout_user

# *Guess the xmlsec_path
try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None

if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary()
else:
    xmlsec_path = '/usr/local/bin/xmlsec1'

SSO_DIR = path.join(settings.PROJECT_HOME, "sso")

log = logging.getLogger("tracking")


def get_full_reverse(name, request, **kwargs):
    p = "https" if request.is_secure() else "http"
    return "%s://%s%s" % (p, request.get_host(), reverse(name, args=kwargs))


class Cache(object):
    def __init__(self):
        self.user2uid = {}
        self.uid2user = {}


def get_saml_setting(sp_name):
    BASE = "http://"
    DIR = path.join(SSO_DIR, "sp", sp_name)
    setting = {
        "entityid": settings.SAML_ENTITY_ID,
        "description": "PepperPD",
        "valid_for": 168,
        "service": {
            "idp": {
                "name": "Rolands IdP",
                "endpoints": {
                    "attribute_service": [
                        ("%s/attr" % BASE, BINDING_SOAP)
                    ],
                    "single_logout_service": []
                },
                "policy": {
                    "default": {
                        "lifetime": {"minutes": 15},
                        "attribute_restrictions": None,  # means all I have
                        "name_form": NAME_FORMAT_URI,
                        "entity_categories": ["swamid", "edugain"]
                    },
                },
                "subject_data": "./idp.subject",
                "session_storage": ("mongodb", "saml"),
                "name_id_format": [NAMEID_FORMAT_TRANSIENT,
                                   NAMEID_FORMAT_PERSISTENT]
            },
        },
        "debug": 1,
        "key_file": DIR + "/key.pem",  # for encrypt?
        "cert_file": DIR + "/cert.pem",  # for encrypt?
        "metadata": {
            "local": [DIR + "/sp.xml"],  # the sp metadata
        },
        "organization": {
            "display_name": "Rolands Identiteter",
            "name": "Rolands Identiteter",
            "url": "http://www.example.com",
        },
        "contact_person": [
            {
                "contact_type": "technical",
                "given_name": "Roland",
                "sur_name": "Hedberg",
                "email_address": "technical@example.com"
            }, {
                "contact_type": "support",
                "given_name": "Support",
                "email_address": "support@example.com"
            },
        ],
        # This database holds the map between a subject's local identifier and
        # the identifier returned to a SP
        "xmlsec_binary": xmlsec_path,
        'attribute_map_dir': SSO_DIR + "/attribute-maps",
        "logger": {
            "rotating": {
                "filename": "idp.log",
                "maxBytes": 500000,
                "backupCount": 5,
            },
            "loglevel": "debug",
        }
    }
    return setting


def get_first_sp_logout_url():
    for sp in metadata.get_all_sp():
        slo_url = sp.get('typed').get('sso_slo_url')
        if slo_url:
            return slo_url


def send_acs(request):
    '''
    Request a redirect to a certain sp
    '''
    # ** Get sp name from uri args
    sp_name = request.GET.get("sp", "")
    if sp_name == "":
        raise Exception("error: No SP name passed")

    # Get the RelayState
    relay_state = request.GET.get('RelayState', '')

    # ** Get config of the sp
    metadata_setting = metadata.sp_by_name(sp_name)
    if metadata_setting is None:
        raise Exception("error: Unknown SP")

    # ** User haven't loged in, redirect to login page
    # BTW, use @login_required cause a problem
    if not request.user.is_authenticated():
        relative = re.sub(r'^http(s?)://.*?/', '/', request.build_absolute_uri())
        return redirect(reverse("signin_user") + "?next=" + urllib.quote(relative, safe=''))

    # ** Add to sso participants session
    if not request.session.get("sso_participants"):
        request.session["sso_participants"] = {}

    request.session["sso_participants"][sp_name] = True

    # ** Now call a relative direction function
    if metadata_setting.get('sso_type') == 'SAML':
        return saml_send_acs(request, sp_name, metadata_setting, relay_state)


def saml_send_acs(request, sp_name, ms, rs):
    '''
    Redirect to a saml sp acs
    '''
    # ** Init SAML IDP
    setting = get_saml_setting(sp_name)

    conf = IdPConfig()
    conf.load(copy.deepcopy(setting))

    IDP = server.Server(config=conf, cache=Cache())
    IDP.ticket = {}

    # ** Get sp entity id from sp.xml
    entity_id = IDP.metadata.keys()[0]

    # ** Get binding and acs destination
    # pass bindings=None, correct?
    binding, destination = IDP.pick_binding("assertion_consumer_service", entity_id=entity_id)

    authn = {'class_ref': 'urn:oasis:names:tc:SAML:2.0:ac:classes:Password'}

    # ** Prepare attributes
    attribute_setting = ms.get('attributes')
    parsed_data = {}
    for attr in attribute_setting:
        if not attr['name']:
            continue

        mapped_name = attr['map'] if 'map' in attr else attr['name']
        value = None

        try:
            if attr['name'] == "email":
                value = request.user.email
            elif attr['name'] == "first_name":
                value = request.user.first_name
            elif attr['name'] == "last_name":
                value = request.user.last_name
            elif attr['name'] == "username":
                value = request.user.username
            elif attr['name'] == "state":
                value = request.user.profile.district.state.name
            elif attr['name'] == "district":
                value = request.user.profile.district.name
            elif attr['name'] == "school":
                value = request.user.profile.school.name
            elif attr['name'] == "grades":
                value = request.user.profile.grade_level_id
            elif attr['name'] == "bio":
                value = request.user.profile.bio
            elif attr['name'] == "id":
                value = str(request.user.id)
            elif attr['name'] == "avatar":
                value = request.build_absolute_uri(reverse('user_photo', args=[request.user.id]))
        except:
            value = None
        if value is not None:
            parsed_data[mapped_name] = [value]
        else:
            parsed_data[mapped_name] = ['']

    # ** Get the X509Certificate string from sp.xml
    sign = IDP.metadata.certs(entity_id, "any", "signing")

    nid = NameID(sp_name, format=NAMEID_FORMAT_PERSISTENT, text=request.user.email)

    # ** Create authn response
    identity = parsed_data

    print identity
    resp = IDP.create_authn_response(
        issuer=setting.get('entityid'),
        identity=identity,
        sign_response=sign,
        sign_assertion=sign,
        in_response_to=None,
        destination=destination,
        sp_entity_id=entity_id,
        name_id=nid,
        authn=authn,
        encrypt_cert="",
        encrypt_assertion="",
    )

    # ** Translate to http response
    http_args = IDP.apply_binding(
        binding=binding,
        msg_str=resp,
        destination=destination,
        relay_state=rs,
        response=True)

    resp = "\n".join(http_args["data"])
    resp = resp.replace("<body>", "<body style='display:none'>")
    return HttpResponse(resp)


def slo_request_send_one(request, sp_name):
    BASE = "http://"
    DIR = path.join(SSO_DIR, "sp", sp_name)

    setting = {
        "entityid": settings.SAML_ENTITY_ID,
        "service": {
            "idp": {
                "name": "Rolands IdP",
                "endpoints": {
                    "attribute_service": [
                        ("%s/attr" % BASE, BINDING_SOAP)
                    ],
                    "single_logout_service": []
                },
                "policy": {
                    "default": {
                        "lifetime": {"minutes": 15},
                        "attribute_restrictions": None,  # means all I have
                        "name_form": NAME_FORMAT_URI,
                        "entity_categories": ["swamid", "edugain"]
                    },
                },
                "subject_data": "./idp.subject",
                "session_storage": ("mongodb", "saml"),
                "name_id_format": [NAMEID_FORMAT_TRANSIENT,
                                   NAMEID_FORMAT_PERSISTENT]
            },
        },
        "debug": 1,
        "key_file": DIR + "/key.pem",  # for encrypt?
        "cert_file": DIR + "/cert.pem",  # for encrypt?
        "metadata": {
            "local": [DIR + "/sp.xml"],  # the sp metadata
        }
    }

    conf = IdPConfig()
    conf.load(copy.deepcopy(setting))
    IDP = server.Server(config=conf, cache=Cache())
    IDP.ticket = {}

    entity_id = IDP.metadata.keys()[0]
    nid = NameID(name_qualifier=sp_name, format=NAMEID_FORMAT_PERSISTENT, text=request.user.email)
    reqid, slo_request = IDP.create_logout_request(sp_name,
                                                   settings.SAML_ENTITY_ID,
                                                   # subject_id=subject_id,
                                                   name_id=nid,
                                                   sign=False)

    # ** Retrieve session id associated with sp-entity and user's name-id
    # ** CAUTION, get_authn_statements() is for mongo session store only
    assertion = IDP.session_db.get_authn_statements(nid)[0]
    slo_request.session_index = SessionIndex(text=assertion[0].session_index)

    binding, destination = IDP.pick_binding("single_logout_service", entity_id=entity_id, bindings=[BINDING_HTTP_POST, BINDING_HTTP_REDIRECT])

    http_args = IDP.apply_binding(
        binding=binding,
        msg_str=slo_request,
        destination=destination,
        relay_state='',
        response=True)

    return saml_django_response(binding, http_args)


def slo_request_send(request):
    """
    Return a slo request (a redirect/post to sp), this is used for slo issused by IDP
    """

    if not request.user.is_authenticated() or not request.session.get("sso_participants"):
        return HttpResponseRedirect(reverse("signin_user"))

    if request.GET.get("sp"):
        sp = request.GET.get("sp")
        return slo_request_send_one(request, sp)
    else:
        sso_participants = request.session.get("sso_participants")
        if sso_participants:
            for sp in sso_participants:
                return slo_request_send_one(request, sp)


@csrf_exempt
def slo_response_receive(request):
    """
    Receive a slo response (from sp), for slo issused by IDP
    """

    # ** todo: we can get sp name from saml body, because the body's not encrypted ?
    # sp_name = request.GET.get("sp", "")
    # setting = get_saml_setting("127.0.0.1-local")

    slo_url = get_full_reverse("sso_idp_slo_response_receive", request)
    setting = {"service": {"idp": {"endpoints": {"single_logout_service": [
        (slo_url, BINDING_HTTP_POST), (slo_url, BINDING_HTTP_REDIRECT)
    ]}}}}

    conf = IdPConfig()
    conf.load(copy.deepcopy(setting))
    IDP = server.Server(config=conf, cache=Cache())

    # relay_state = request.REQUEST.get("RelayState")
    saml_response = request.REQUEST.get("SAMLResponse")

    if request.method == "POST":
        binding = BINDING_HTTP_POST
    else:
        binding = BINDING_HTTP_REDIRECT

    r = IDP.parse_logout_request_response(saml_response, binding)
    sp_name = r.issuer()

    if not r.status_ok():
        raise Exception("SP %s return an error for slo." % sp_name)

    # nid = NameID(name_qualifier=sp_name, format=NAMEID_FORMAT_PERSISTENT, text=request.user.email)
    # IDP.session_db.remove_authn_statements(nid)  # name_id

    sso_participants = request.session.get("sso_participants")
    if sso_participants:
        if sso_participants.get(sp_name):
            del request.session["sso_participants"][sp_name]

        for sp in sso_participants:
            return slo_request_send_one(request, sp)

        if len(sso_participants) == 0:
            del request.session["sso_participants"]
            return logout_user(request)
    else:
        return logout_user(request)

