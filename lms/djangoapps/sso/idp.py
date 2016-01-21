import argparse
import base64
import importlib
import logging
import os
import re
import time

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
from saml2 import time_util
# from saml2.authn import is_equal

from saml2.authn_context import AuthnBroker
from saml2.authn_context import PASSWORD
from saml2.authn_context import UNSPECIFIED
from saml2.authn_context import authn_context_class_ref
from saml2.httputil import Response
from saml2.httputil import NotFound
from saml2.httputil import geturl
from saml2.httputil import get_post
from saml2.httputil import Redirect
from saml2.httputil import Unauthorized
from saml2.httputil import BadRequest
from saml2.httputil import ServiceError
from saml2.ident import Unknown
from saml2.metadata import create_metadata_string
from saml2.profile import ecp
from saml2.s_utils import rndstr
from saml2.s_utils import exception_trace
from saml2.s_utils import UnknownPrincipal
from saml2.s_utils import UnsupportedBinding
from saml2.s_utils import PolicyError
from saml2.sigver import verify_redirect_signature
from saml2.sigver import encrypt_cert_from_item


from cache import IdentityCache, OutstandingQueriesCache

from saml2.saml import NAME_FORMAT_URI
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_PERSISTENT

logger = logging.getLogger("saml2.idp")
logger.setLevel(logging.WARNING)


class Cache(object):
    def __init__(self):
        self.user2uid = {}
        self.uid2user = {}


try:
    from saml2.sigver import get_xmlsec_binary
except ImportError:
    get_xmlsec_binary = None

if get_xmlsec_binary:
    xmlsec_path = get_xmlsec_binary(["/opt/local/bin"])
else:
    xmlsec_path = '/usr/bin/xmlsec1'


BASE = "http://"

DIR = "/home/fcl/pepper/edx-platform/lms/djangoapps/sso/"

setting = {
    "entityid": "idp.xml",
    "description": "My IDP",
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
            "endpoints": {
                "single_sign_on_service": [
                    ("%s/sso/redirect" % BASE, BINDING_HTTP_REDIRECT),
                    ("%s/sso/post" % BASE, BINDING_HTTP_POST),
                    ("%s/sso/art" % BASE, BINDING_HTTP_ARTIFACT),
                    ("%s/sso/ecp" % BASE, BINDING_SOAP)
                ],
                "single_logout_service": [
                    ("%s/slo/soap" % BASE, BINDING_SOAP),
                    ("%s/slo/post" % BASE, BINDING_HTTP_POST),
                    ("%s/slo/redirect" % BASE, BINDING_HTTP_REDIRECT)
                ],
                "artifact_resolve_service": [
                    ("%s/ars" % BASE, BINDING_SOAP)
                ],
                "assertion_id_request_service": [
                    ("%s/airs" % BASE, BINDING_URI)
                ],
                "manage_name_id_service": [
                    ("%s/mni/soap" % BASE, BINDING_SOAP),
                    ("%s/mni/post" % BASE, BINDING_HTTP_POST),
                    ("%s/mni/redirect" % BASE, BINDING_HTTP_REDIRECT),
                    ("%s/mni/art" % BASE, BINDING_HTTP_ARTIFACT)
                ],
                "name_id_mapping_service": [
                    ("%s/nim" % BASE, BINDING_SOAP),
                ],
            },
            "policy": {
                "default": {
                    "lifetime": {"minutes": 15},
                    "attribute_restrictions": None, # means all I have
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
    "key_file": DIR + "/pki/mykey.pem",
    "cert_file": DIR + "/pki/mycert.pem",
    "metadata": {
        "local": [DIR + "/sp.xml"],
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
    #"attribute_map_dir": "../attributemaps",
    "logger": {
        "rotating": {
            "filename": "idp.log",
            "maxBytes": 500000,
            "backupCount": 5,
        },
        "loglevel": "debug",
    }
}

from saml2.config import IdPConfig
import copy

conf = IdPConfig()
conf.load(copy.deepcopy(setting))

IDP = server.Server(config=conf, cache=Cache())
IDP.ticket = {}


entity_id = "http://localhost:8087/sp.xml"

response_bindings = [BINDING_PAOS]

binding, destination = IDP.pick_binding("assertion_consumer_service", entity_id=entity_id)  # pass bindings=None, correct?

print(binding)
print(destination)


# ****************************
# resp_args
# 'name_id_policy': <saml2.samlp.NameIDPolicy object at 0x7faf120a0f50>,
# 'destination': 'http://localhost:8087/acs/post',
# 'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
# 'authn': {'authn_auth': 'https://localhost:8088',
#           'level': 10,
#           'method': <function username_password_authn at 0x7faf0b201aa0>,
#           'class_ref': 'urn:oasis:names:tc:SAML:2.0:ac:classes:Password'},
# 'sp_entity_id': 'http://localhost:8087/sp.xml',
# 'in_response_to': 'id-PS8o3CtYimlh5J6Cf'

# ****************************

def username_password_authn():
    pass

authn = {'authn_auth': 'https://localhost:8088',
         'level': 10,
         'method': username_password_authn,
         'class_ref': 'urn:oasis:names:tc:SAML:2.0:ac:classes:Password'}

# /home/fcl/.virtualenvs/edx-platform/lib/python2.7/site-packages/saml2/server.py

identity = {'labeledURL': 'http://www.example.com/rohe My homepage', 'eduPersonTargetedID': 'one!for!all', 'displayName': 'P. Roland Hedberg', 'uid': 'roland', 'c': 'SE', 'eduPersonScopedAffiliation': 'staff@example.com', 'o': 'Example Co.', 'eduPersonPrincipalName': 'rohe@example.com', 'sn': 'Hedberg', 'mail': 'roland@example.com', 'ou': 'IT', 'givenName': 'Roland', 'norEduPersonNIN': 'SE197001012222', 'initials': 'P'}

resp = IDP.create_authn_response(identity=identity,
                                 userid="victor",
                                 in_response_to=None,
                                 destination=destination,
                                 sp_entity_id=entity_id,
                                 name_id_policy=None,
                                 authn=authn)

# dir(resp)
# ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_members_to_element_tree', '_convert_element_attribute_to_member', '_convert_element_tree_to_member', '_get_all_c_children_with_order', '_to_element_tree', 'add_extension_attribute', 'add_extension_element', 'add_extension_elements', 'assertion', 'become_child_element_of', 'c_any', 'c_any_attribute', 'c_attribute_type', 'c_attributes', 'c_cardinality', 'c_child_order', 'c_children', 'c_namespace', 'c_ns_prefix', 'c_tag', 'c_value_type', 'child_cardinality', 'child_class', 'children_with_values', 'clear_text', 'consent', 'destination', 'empty', 'encrypted_assertion', 'extension_attributes', 'extension_elements', 'extensions', 'extensions_as_elements', 'find_extensions', 'harvest_element_tree', 'id', 'in_response_to', 'issue_instant', 'issuer', 'keys', 'keyswv', 'loadd', 'set_text', 'signature', 'status', 'text', 'to_string', 'verify', 'version']

print(resp.to_string())

# apply_binding, args
# name_id_policy <?xml version='1.0' encoding='UTF-8'?>
# <ns0:NameIDPolicy xmlns:ns0="urn:oasis:names:tc:SAML:2.0:protocol" AllowCreate="false" Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent" />
# destination http://localhost:8087/acs/post
# binding urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST
# authn {'authn_auth': 'https://localhost:8088', 'level': 10, 'method': <function username_password_authn at 0x7fd62a0aeaa0>, 'class_ref': 'urn:oasis:names:tc:SAML:2.0:ac:classes:Password'}
# sp_entity_id http://localhost:8087/sp.xml
# in_response_to id-nIra29dsTqPwqL5Xl


http_args = IDP.apply_binding(binding=binding,
                              msg_str=resp.to_string(),
                              destination=destination,
                              relay_state="",
                              response=True
                              )

print http_args

from django.http import HttpResponse

def go(request):
    # return HttpResponse(resp.to_string())
    return HttpResponse(http_args["data"])

# /home/fcl/.virtualenvs/pysaml-test/lib/python2.7/site-packages/pysaml2-4.0.1-py2.7.egg/saml2/response.py
# 513: self.allow_unsolicited=True

# <ns0:Response xmlns:ns0="urn:oasis:names:tc:SAML:2.0:protocol" xmlns:ns1="urn:oasis:names:tc:SAML:2.0:assertion" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Destination="http://localhost:8087/acs/post" ID="id-1ZeQ6TmG0CtB2ecGQ" InResponseTo="id-HgLnhRXNg4cGuCya0" IssueInstant="2016-01-20T06:14:15Z" Version="2.0">
#   <ns1:Issuer Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity">https://localhost:8088/idp.xml
#   </ns1:Issuer>
#   <ns0:Status>
#     <ns0:StatusCode Value="urn:oasis:names:tc:SAML:2.0:status:Success" />
#   </ns0:Status>
#   <ns1:Assertion ID="id-FeWw526RQsoRWUyG0" IssueInstant="2016-01-20T06:14:15Z" Version="2.0">
#     <ns1:Issuer Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity">https://localhost:8088/idp.xml
#     </ns1:Issuer>
#     <ns1:Subject>
#       <ns1:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent" NameQualifier="https://localhost:8088/idp.xml" SPNameQualifier="http://localhost:8087/sp.xml">roland
#       </ns1:NameID>
#       <ns1:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
#         <ns1:SubjectConfirmationData InResponseTo="id-HgLnhRXNg4cGuCya0" NotOnOrAfter="2016-01-20T06:29:15Z" Recipient="http://localhost:8087/acs/post" />
#       </ns1:SubjectConfirmation>
#     </ns1:Subject>
#     <ns1:Conditions NotBefore="2016-01-20T06:14:15Z" NotOnOrAfter="2016-01-20T06:29:15Z">
#       <ns1:AudienceRestriction>
#         <ns1:Audience>http://localhost:8087/sp.xml
#         </ns1:Audience>
#       </ns1:AudienceRestriction>
#     </ns1:Conditions>
#     <ns1:AuthnStatement AuthnInstant="2016-01-20T06:14:15Z" SessionIndex="id-DYazRiOv98OcoA6Yg">
#       <ns1:AuthnContext>
#         <ns1:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:Password
#         </ns1:AuthnContextClassRef>
#         <ns1:AuthenticatingAuthority>https://localhost:8088
#         </ns1:AuthenticatingAuthority>
#       </ns1:AuthnContext>
#     </ns1:AuthnStatement>
#     <ns1:AttributeStatement>
#       <ns1:Attribute FriendlyName="displayName" Name="urn:oid:2.16.840.1.113730.3.1.241" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
#         <ns1:AttributeValue xsi:type="xs:string">P. Roland Hedberg
#         </ns1:AttributeValue>
#       </ns1:Attribute>
#       <ns1:Attribute FriendlyName="eduPersonScopedAffiliation" Name="urn:oid:1.3.6.1.4.1.5923.1.1.1.9" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
#         <ns1:AttributeValue xsi:type="xs:string">staff@example.com
#         </ns1:AttributeValue>
#       </ns1:Attribute>
#       <ns1:Attribute FriendlyName="eduPersonPrincipalName" Name="urn:oid:1.3.6.1.4.1.5923.1.1.1.6" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
#         <ns1:AttributeValue xsi:type="xs:string">rohe@example.com
#         </ns1:AttributeValue>
#       </ns1:Attribute>
#       <ns1:Attribute FriendlyName="mail" Name="urn:oid:0.9.2342.19200300.100.1.3" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
#         <ns1:AttributeValue xsi:type="xs:string">roland@example.com
#         </ns1:AttributeValue>
#       </ns1:Attribute>
#       <ns1:Attribute FriendlyName="eduPersonTargetedID" Name="urn:oid:1.3.6.1.4.1.5923.1.1.1.10" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
#         <ns1:AttributeValue xsi:type="xs:string">one!for!all
#         </ns1:AttributeValue>
#       </ns1:Attribute>
#     </ns1:AttributeStatement>
#   </ns1:Assertion>
# </ns0:Response>
