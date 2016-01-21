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
# from saml2.authn import is_equal

from cache import IdentityCache, OutstandingQueriesCache

from saml2.saml import NAME_FORMAT_URI
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_PERSISTENT

from saml2.config import IdPConfig
import copy
from django.http import HttpResponse
from django.conf import settings

import sp_metadata as metadata

try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None

logger = logging.getLogger("saml2.idp")
logger.setLevel(logging.WARNING)


class Cache(object):
    def __init__(self):
        self.user2uid = {}
        self.uid2user = {}


def get_saml_setting(sp_name):
    if get_xmlsec_binary:
        xmlsec_path = get_xmlsec_binary(["/opt/local/bin"])
    else:
        xmlsec_path = '/usr/bin/xmlsec1'

    BASE = "http://"

    DIR = settings.PROJECT_HOME + "/sso/sp/" + sp_name

    setting = {
        "entityid": "PepperPD",
        "description": "PepperPD",
        "valid_for": 168,
        "service": {
            "aa": {
                "endpoints": {
                    "attribute_service": [
                        ("%s/attr" % BASE, BINDING_SOAP)
                    ]
                },
                "name_id_format": [NAMEID_FORMAT_TRANSIENT,
                                   NAMEID_FORMAT_PERSISTENT]
            },
            "aq": {
                "endpoints": {
                    "authn_query_service": [
                        ("%s/aqs" % BASE, BINDING_SOAP)
                    ]
                },
            },
            "idp": {
                "name": "Rolands IdP",

                "policy": {
                    "default": {
                        "lifetime": {"minutes": 15},
                        "attribute_restrictions": None,  # means all I have
                        "name_form": NAME_FORMAT_URI,
                        "entity_categories": ["swamid", "edugain"]
                    },
                },
                "subject_data": "./idp.subject",
                "name_id_format": [NAMEID_FORMAT_TRANSIENT,
                                   NAMEID_FORMAT_PERSISTENT]
            },
        },
        "debug": 1,
        "key_file": DIR + "/mykey.pem",
        "cert_file": DIR + "/mycert.pem",
        "metadata": {
            "local": [DIR + "/FederationMetadata.xml"],
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
        # "attribute_map_dir": "../attributemaps",
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


def auth(request):
    # User haven't loged in, use @login_required cause a problem
    if(not request.user.is_authenticated()):
        relative = re.sub(r'^http(s?)://.*?/', '/', request.build_absolute_uri())
        return redirect(reverse("signin_user")+"?next=" + relative)  # urllib.quote(, safe='')

    sp_name = request.GET.get("sp", "")
    if sp_name == "":
        raise Exception("error: No SP name passed")

    metadata_setting = metadata.sp_by_name(sp_name)
    if metadata_setting is None:
        raise Exception("error: Unkonwn SP")

    if metadata_setting.get('sso_type') == 'SAML':
        # log.debug("message: it's SAML")
        return saml_redirect(request, sp_name, metadata_setting)


def saml_redirect(request, sp_name, ms):
    setting = get_saml_setting(sp_name)

    conf = IdPConfig()
    conf.load(copy.deepcopy(setting))

    IDP = server.Server(config=conf, cache=Cache())
    IDP.ticket = {}

    # Get sp entity id from FederationMetadata.xml
    entity_id = IDP.metadata.keys()[0]

    # pass bindings=None, correct?
    binding, destination = IDP.pick_binding("assertion_consumer_service", entity_id=entity_id)

    authn = {'class_ref': 'urn:oasis:names:tc:SAML:2.0:ac:classes:Password'}

    attribute_setting = ms.get('attributes')
    parsed_data = {}
    for attr in attribute_setting:
        if not attr['name']:
            continue
        
        mapped_name = attr['map'] if 'map' in attr else attr['name']
        value = ""
        
        if attr['name'] == "first_name":
            value = request.user.first_name
        elif attr['name'] == "last_name":
            value = request.user.last_name
        elif attr['name'] == "email":
            value = request.user.email
        elif attr['name'] == "username":
            value = request.user.username
        elif attr['name'] == "state":
            value = request.user.district.state.name
        elif attr['name'] == "district":
            value = request.user.district.name
        elif attr['name'] == "school":
            value = request.user.school.name
            
        parsed_data[mapped_name] = value

    identity = parsed_data

    resp = IDP.create_authn_response(identity=identity,
                                     userid="victor",
                                     in_response_to=None,
                                     destination=destination,
                                     sp_entity_id=entity_id,
                                     name_id_policy=None,
                                     authn=authn)

    http_args = IDP.apply_binding(binding=binding,
                                  msg_str=resp.to_string(),
                                  destination=destination,
                                  relay_state="",
                                  response=True)

    return HttpResponse(http_args["data"])
