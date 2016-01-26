from mitxmako.shortcuts import render_to_response
import xmltodict
from django.http import HttpResponse
import json
from django.conf import settings
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import logging
import os

BASEDIR = settings.PROJECT_HOME + "/sso/sp"
PEPPER_ENTITY_ID = "www.pepperpd.com"


@login_required
def edit(request):
    return render_to_response('sso/manage/sp_metadata.html')


def save(request):
    data = json.loads(request.POST.get('data'))

    entities = []
    for d in data:
        name = d.get('sso_name', '')
        path = BASEDIR + "/" + name
        if not os.path.isdir(path):
            os.makedirs(path)

        typed = d.get('typed')
        if typed.get('saml_metadata'):
            mdfile = open(path + "/FederationMetadata.xml", "w")
            mdfile.write(typed.get('saml_metadata'))
            del typed['saml_metadata']

        typed_setting = []
        for k, v in typed.items():
            typed_setting.append('''
    <setting name="%s">%s</setting>''' % (k, v))

        attributes = []
        for a in d.get('attributes'):
            attributes.append('''
    <attribute name="%s" map="%s"></attribute>''' % (a['name'], a['map']))

        entities.append('''
  <entity type="%s" name="%s">%s%s
  </entity>''' % (d.get('sso_type', ''),
                  name,
                  ''.join(typed_setting),
                  ''.join(attributes)
                  ))

    content = '''<?xml version="1.0"?>
<entities xmlns:ds="http://www.w3.org/2000/09/xmldsig#">%s
</entities>''' % ''.join(entities)

    xmlfile = open(BASEDIR + "/metadata.xml", "w")
    xmlfile.write(content)

    return HttpResponse("{}", content_type="application/json")


def all_json(request):
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))
    entity_list = []

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            entity_list.append(parse_one_sp(entity))

    return HttpResponse(json.dumps(entity_list), content_type="application/json")


def sp_by_name(name):
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            if entity['@name'] == name:
                return parse_one_sp(entity)


def parse_one_sp(entity):
    attribute_list = []
    if 'attribute' in entity:
        for attribute in entity['attribute']:
            attr = {
                # 'type': attribute['@type'],
                'name': attribute['@name'],
                'map': attribute['@map']
                }
            attribute_list.append(attr)

    typed_setting = {}
    if 'setting' in entity:
        for attribute in entity['setting']:
            typed_setting[attribute['@name']] = attribute['#text']

    path = BASEDIR + "/" + entity['@name'] + "/FederationMetadata.xml"

    if os.path.isfile(path):
        mdfile = open(path, "r")
        typed_setting['saml_metadata'] = mdfile.read()

    return {
        'sso_type': entity['@type'],
        'sso_name': entity['@name'],
        'attributes': attribute_list,
        'typed': typed_setting
        }



from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join
import re

def create_self_signed_cert(CN, C="US", ST="unknown", L="unknown", O="unknown", OU="unknown", serial_number=1, notBefore=0, notAfter=365*24*60*60):
    """
    
    """
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = C
    cert.get_subject().ST = ST
    cert.get_subject().L = L
    cert.get_subject().O = O
    cert.get_subject().OU = OU
    cert.get_subject().CN = CN  # most important part
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
    
    return cert, key


def download_saml_federation_metadata(request):
    name = request.GET.get("name")
    
    if not sp_by_name(name):
        return HttpResponse("SP with name '%s' is not exist. Did you have it saved?" % name)
        
    f = settings.PROJECT_HOME + "/sso/sp/" + name + "/FederationMetadata.xml"
    
    if not os.path.isfile(f) or 1:
        cert, key = create_self_signed_cert(name)
        cert = re.sub('-----.*?-----\n?', '', cert)

        auth = "http://docs.oasis-open.org/wsfed/authorization/200706"
        content = '''<?xml version="1.0" encoding="utf-8"?>
<EntityDescriptor ID="_f4737183-218b-4a44-a5c4-a3b12477f580" entityID="{entityID}" xmlns="urn:oasis:names:tc:SAML:2.0:metadata">

  <RoleDescriptor xsi:type="fed:SecurityTokenServiceType"
    xmlns:fed="http://docs.oasis-open.org/wsfed/federation/200706"
    protocolSupportEnumeration="http://docs.oasis-open.org/wsfed/federation/200706" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  
    <KeyDescriptor use="signing">
      <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
        <X509Data>
          <X509Certificate>{cert}</X509Certificate>
        </X509Data>
      </KeyInfo>
    </KeyDescriptor>
    
    <fed:ClaimTypesOffered>
      <auth:ClaimType Uri="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Name</auth:DisplayName>
        <auth:Description>The mutable display name of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Subject</auth:DisplayName>
        <auth:Description>An immutable, globally unique, non-reusable identifier of the user that is unique to the application for which a token is issued.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Given Name</auth:DisplayName>
        <auth:Description>First name of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Surname</auth:DisplayName>
        <auth:Description>Last name of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/displayname" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Display Name</auth:DisplayName>
        <auth:Description>Display name of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/nickname" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Nick Name</auth:DisplayName>
        <auth:Description>Nick name of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/ws/2008/06/identity/claims/authenticationinstant" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Authentication Instant</auth:DisplayName>
        <auth:Description>The time (UTC) when the user is authenticated to Windows Azure Active Directory.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/ws/2008/06/identity/claims/authenticationmethod" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Authentication Method</auth:DisplayName>
        <auth:Description>The method that Windows Azure Active Directory uses to authenticate users.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/objectidentifier" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>ObjectIdentifier</auth:DisplayName>
        <auth:Description>Primary identifier for the user in the directory. Immutable, globally unique, non-reusable.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/tenantid" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>TenantId</auth:DisplayName>
        <auth:Description>Identifier for the user\'s tenant.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/identityprovider" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>IdentityProvider</auth:DisplayName>
        <auth:Description>Identity provider for the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Email</auth:DisplayName>
        <auth:Description>Email address of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/ws/2008/06/identity/claims/groups" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Groups</auth:DisplayName>
        <auth:Description>Groups of the user.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/accesstoken" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>External Access Token</auth:DisplayName>
        <auth:Description>Access token issued by external identity provider.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/ws/2008/06/identity/claims/expiration" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>External Access Token Expiration</auth:DisplayName>
        <auth:Description>UTC expiration time of access token issued by external identity provider.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/identity/claims/openid2_id" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>External OpenID 2.0 Identifierd</auth:DisplayName>
        <auth:Description>OpenID 2.0 identifier issued by external identity provider.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/claims/groups.link" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>GroupsOverageClaim</auth:DisplayName>
        <auth:Description>Issued when number of user\'s group claims exceeds return limit.</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/ws/2008/06/identity/claims/role" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>Role Claim</auth:DisplayName>
        <auth:Description>Roles that the user or Service Principal is attached to</auth:Description>
      </auth:ClaimType>
      <auth:ClaimType Uri="http://schemas.microsoft.com/ws/2008/06/identity/claims/wids" Optional="true" xmlns:auth="{auth}">
        <auth:DisplayName>RoleTemplate Id Claim</auth:DisplayName>
        <auth:Description>Role template id of the Built-in Directory Roles that the user is a member of</auth:Description>
      </auth:ClaimType>
    </fed:ClaimTypesOffered>
    <fed:SecurityTokenServiceEndpoint>
      <EndpointReference xmlns="http://www.w3.org/2005/08/addressing">
        <Address>https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/wsfed</Address>
      </EndpointReference>
    </fed:SecurityTokenServiceEndpoint>
    <fed:PassiveRequestorEndpoint>
      <EndpointReference xmlns="http://www.w3.org/2005/08/addressing">
        <Address>https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/wsfed</Address>
      </EndpointReference>
    </fed:PassiveRequestorEndpoint>
  </RoleDescriptor>
  
  <RoleDescriptor xsi:type="fed:ApplicationServiceType" xmlns:fed="http://docs.oasis-open.org/wsfed/federation/200706"
    protocolSupportEnumeration="http://docs.oasis-open.org/wsfed/federation/200706" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <KeyDescriptor use="signing">
      <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
        <X509Data>
          <X509Certificate>{cert}</X509Certificate>
        </X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <fed:TargetScopes>
      <EndpointReference xmlns="http://www.w3.org/2005/08/addressing">
        <Address>https://sts.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/
        </Address>
      </EndpointReference>
    </fed:TargetScopes>
    <fed:ApplicationServiceEndpoint>
      <EndpointReference xmlns="http://www.w3.org/2005/08/addressing">
        <Address>https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/wsfed
        </Address>
      </EndpointReference>
    </fed:ApplicationServiceEndpoint>
    <fed:PassiveRequestorEndpoint>
      <EndpointReference xmlns="http://www.w3.org/2005/08/addressing">
        <Address>https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/wsfed
        </Address>
      </EndpointReference>
    </fed:PassiveRequestorEndpoint>
  </RoleDescriptor>
  <IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <KeyDescriptor use="signing">
      <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
        <X509Data>
          <X509Certificate>{cert}</X509Certificate>
        </X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/saml2" />
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/saml2" />
    <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://login.windows.net/0397bdf1-4ff9-47e5-8aae-33a6c04b6c50/saml2" />
  </IDPSSODescriptor>
</EntityDescriptor>'''.format(cert=cert, entityID=PEPPER_ENTITY_ID, auth=auth)
        open(f, "wt").write(content)
        
    response = HttpResponse(content_type='application/x-download')
    response['Content-Disposition'] = ('attachment; filename=FederationMetadata.xml')
    response.write(open(f, "r").read())
    return response
    
