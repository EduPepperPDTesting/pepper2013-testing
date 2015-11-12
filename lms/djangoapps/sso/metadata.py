from mitxmako.shortcuts import render_to_response
import xmltodict
from django.http import HttpResponse
import json
from django.conf import settings
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import logging

log = logging.getLogger("tracking")


@login_required
def edit(request):
    return render_to_response('sso/manage/metadata.html')


def save(request):
    data = json.loads(request.POST.get('data'))

    entities = []
    for d in data:
        attributes = []
        for a in d['attributes']:
            attributes.append('''
    <attribute name="%s" map="%s"></attribute>''' % (a['name'], a['map']))

        entities.append('''
  <entity type="%s" name="%s">%s
  </entity>''' % (d.get('sso_type', ''),
                  d.get('sso_name', ''),
                  ''.join(attributes)
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
            if entity['@name'] == name:
                return parse_one_idp(entity)


def parse_one_idp(entity):
    attribute_list = []
    
    if 'attribute' in entity:
        for attribute in entity['attribute']:
            attr = {
                # 'type': attribute['@type'],
                'name': attribute['@name'],
                'map': attribute['@map']
                }
            attribute_list.append(attr)

    return {
        'sso_type': entity['@type'],
        'sso_name': entity['@name'],
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
