from mitxmako.shortcuts import render_to_response
import xmltodict
from django.http import HttpResponse
import json
from django.conf import settings
import logging
log = logging.getLogger("tracking")


def metadata(request):
    return render_to_response('saml2/manage/metadata.html')


def metadata_save(request):
    data = json.loads(request.POST.get('data'))
    log.debug("+++++++++++++")
    log.debug(len(data))

    entitys = ""
    for d in data:
        entitys = entitys + '''<md:EntityDescriptor entityID="%s">
    <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
      <md:KeyDescriptor use="signing">
        <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
          <ds:X509Data>
            <ds:X509Certificate>%s</ds:X509Certificate>
          </ds:X509Data>
        </ds:KeyInfo>
      </md:KeyDescriptor>
      <md:KeyDescriptor use="encryption">
        <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
          <ds:X509Data>
            <ds:X509Certificate>%s</ds:X509Certificate>
          </ds:X509Data>
        </ds:KeyInfo>
      </md:KeyDescriptor>
      <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="%s"/>
      <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</md:NameIDFormat>
      <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="%s"/>
    </md:IDPSSODescriptor>
    <md:Organization>
      <md:OrganizationName xml:lang="en">%s</md:OrganizationName>
      <md:OrganizationDisplayName xml:lang="en">%s</md:OrganizationDisplayName>
      <md:OrganizationURL xml:lang="en">%s</md:OrganizationURL>
    </md:Organization>
    <md:ContactPerson contactType="technical">
      <md:SurName>%s</md:SurName>
      <md:EmailAddress>%s</md:EmailAddress>
    </md:ContactPerson>
  </md:EntityDescriptor>''' % (d['EntityID'],
                               d['Key']['Signing'],
                               d['Key']['Encryption'],
                               d['SingleLogoutService']['URL'],
                               d['SingleSignOnService']['URL'],
                               d['Organization']['Name'],
                               d['Organization']['DisplayName'],
                               d['Organization']['URL'],
                               d['ContactPerson']['SurName'],
                               d['ContactPerson']['EmailAddress'])

    content = '''<?xml version="1.0"?>
<md:EntitiesDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
%s
</md:EntitiesDescriptor>''' % entitys

    xmlfile = open(settings.PROJECT_ROOT + "/envs/saml/remote_metadata.xml", "w")
    xmlfile.write(content)

    return HttpResponse("{}", content_type="application/json")


def metadata_json(request):
    xmlfile = open(settings.PROJECT_ROOT + "/envs/saml/remote_metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read())
    entity_list = []
    for entity in parsed_data['md:EntitiesDescriptor']['md:EntityDescriptor']:
        entity_list.append({
            'EntityID': entity['@entityID'],
            'Key': {
                'Signing': entity['md:IDPSSODescriptor']['md:KeyDescriptor'][0]['ds:KeyInfo']['ds:X509Data']['ds:X509Certificate'],
                'Encryption': entity['md:IDPSSODescriptor']['md:KeyDescriptor'][1]['ds:KeyInfo']['ds:X509Data']['ds:X509Certificate']},
            'SingleLogoutService': {'URL': entity['md:IDPSSODescriptor']['md:SingleLogoutService']['@Location']},
            'SingleSignOnService': {'URL': entity['md:IDPSSODescriptor']['md:SingleSignOnService']['@Location']},
            'Organization': {'Name': entity['md:Organization']['md:OrganizationName']['#text'],
                             'DisplayName': entity['md:Organization']['md:OrganizationDisplayName']['#text'],
                             'URL': entity['md:Organization']['md:OrganizationURL']['#text']},
            'ContactPerson': {'SurName': entity['md:ContactPerson']['md:SurName'],
                              'EmailAddress': entity['md:ContactPerson']['md:EmailAddress']}
            })
    return HttpResponse(json.dumps(entity_list), content_type="application/json")
