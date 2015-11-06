from mitxmako.shortcuts import render_to_response
import xmltodict
from django.http import HttpResponse
import json
from django.conf import settings
from collections import defaultdict

import logging
log = logging.getLogger("tracking")


def edit(request):
    return render_to_response('sso/manage/metadata.html')


def save(request):
    data = json.loads(request.POST.get('data'))

    entities = []
    for d in data:
        attributes = []
        for a in d['attributes']:
            attributes.append('''
    <attribute type="%s" name="%s" map="%s"></attribute>''' % (a['type'], a['name'], a['map']))

        entities.append('''
  <entity type="%s" name="%s" entityID="%s">
    <issuerUrl location="%s"></issuerUrl>
    <singleSignOnService location="%s"></singleSignOnService>
    <singleLogoutService location="%s"></singleLogoutService>%s
    <request>
<![CDATA[
%s
]]>
    </request>
    <response>
<![CDATA[
%s
]]>
    </response>
  </entity>''' % (d.get('sso_type', ''),
                  d.get('sso_name', ''),
                  d.get('sso_entity_id', ''),
                  d.get('sso_issuer_url', ''),
                  d.get('sso_single_sign_on', ''),
                  d.get('sso_single_sign_out', ''),
                  ''.join(attributes),
                   d.get('sso_request', ''),
                  d.get('sso_response', '')
                  ))

    content = '''<?xml version="1.0"?>
<entities xmlns:ds="http://www.w3.org/2000/09/xmldsig#">%s
</entities>''' % ''.join(entities)

    xmlfile = open(settings.PROJECT_ROOT + "/sso/metadata.xml", "w")
    xmlfile.write(content)

    return HttpResponse("{}", content_type="application/json")


def idp_by_name(name):
    xmlfile = open(settings.PROJECT_ROOT + "/sso/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            if entity['sso_name'] == name:
                return parse_one_idp(entity)


def parse_one_idp(entity):
    attribute_list = []
    if 'attribute' in entity:
        for attribute in entity['attribute']:
            attribute_list.append({
                'type': attribute['@type'],
                'name': attribute['@name'],
                'map': attribute['@map']
                })
    return {
        'sso_entity_id': entity['@entityID'],
        'sso_type': entity['@type'],
        'sso_name': entity['@name'],
        'sso_issuer_url': entity['issuerUrl'][0]['@location'],
        'sso_single_sign_on': entity['singleSignOnService'][0]['@location'],
        'sso_single_sign_out': entity['singleLogoutService'][0]['@location'],
        'sso_request': entity['request'][0].strip() if 'request' in entity else '',
        'sso_response': entity['response'][0].strip() if 'response' in entity else '',
        'attributes': attribute_list
        }


def all_json(request):
    xmlfile = open(settings.PROJECT_ROOT + "/sso/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))
    entity_list = []

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            entity_list.append(parse_one_idp(entity))

    return HttpResponse(json.dumps(entity_list), content_type="application/json")
