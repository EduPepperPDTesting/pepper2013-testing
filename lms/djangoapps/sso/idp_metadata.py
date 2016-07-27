from mitxmako.shortcuts import render_to_response
import xmltodict
import json
from django.conf import settings
from collections import defaultdict
import logging
import os
from os import path
from pepper_utilities.utils import render_json_response
from permissions.decorators import user_has_perms
from django_future.csrf import ensure_csrf_cookie

log = logging.getLogger("tracking")

SSO_DIR = path.join(settings.PROJECT_HOME, "sso")
BASEDIR = SSO_DIR + "/idp"


@user_has_perms('sso', 'administer')
def edit(request):
    return render_to_response('sso/manage/idp_metadata.html')


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
def save(request):
    data = json.loads(request.POST.get('data'))

    entities = []
    for d in data:
        name = d.get('sso_name', '')
        xml_path = BASEDIR + "/" + name
        if not os.path.isdir(xml_path):
            os.makedirs(xml_path)

        typed = d.get('typed')
        if typed.get('saml_metadata'):
            mdfile = open(xml_path + "/FederationMetadata.xml", "w")
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

    return render_json_response({})


def idp_by_name(name):
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
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

    typed_setting = {}
    if 'setting' in entity:
        for attribute in entity['setting']:
            typed_setting[attribute['@name']] = attribute['#text']

    xml_path = BASEDIR + "/" + entity['@name'] + "/FederationMetadata.xml"

    if os.path.isfile(xml_path):
        mdfile = open(xml_path, "r")
        typed_setting['saml_metadata'] = mdfile.read()

    return {
        'sso_type': entity['@type'],
        'sso_name': entity['@name'],
        'attributes': attribute_list,
        'typed': typed_setting
        }


@user_has_perms('sso', 'administer')
def all_json(request):
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))
    entity_list = []

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            entity_list.append(parse_one_idp(entity))

    return render_json_response(entity_list)
