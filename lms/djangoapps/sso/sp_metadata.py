from mitxmako.shortcuts import render_to_response
import xmltodict
from django.http import HttpResponse
import json
from django.conf import settings
from collections import defaultdict
import os
from OpenSSL import crypto
import re
from path import path
from permissions.decorators import user_has_perms
from django.core.urlresolvers import reverse


BASEDIR = settings.PROJECT_HOME + "/sso/sp"

@user_has_perms('sso', 'administer')
def edit(request):
    return render_to_response('sso/manage/sp_metadata.html')


@user_has_perms('sso', 'administer')
def save(request):
    data = json.loads(request.POST.get('data'))

    print data

    entities = []
    for d in data:
        sso_name = d.get('sso_name', '')
        sso_type = d.get('sso_type')
        path = BASEDIR + "/" + sso_name
        if not os.path.isdir(path):
            os.makedirs(path)

        typed = d.get('typed')
        sso_type = d.get('sso_type')

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
                  sso_name,
                  ''.join(typed_setting),
                  ''.join(attributes)
                  ))

    content = '''<?xml version="1.0"?>
<entities xmlns:ds="http://www.w3.org/2000/09/xmldsig#">%s
</entities>''' % ''.join(entities)

    xmlfile = open(BASEDIR + "/metadata.xml", "w")
    xmlfile.write(content)
    xmlfile.close()

    # post process
    for d in data:
        sso_name = d.get('sso_name', '')
        sso_type = d.get('sso_type')
        if sso_type == 'SAML':
            create_saml_config_files(sso_name)

    return HttpResponse("{}", content_type="application/json")


@user_has_perms('sso', 'administer')
def all_json(request):
    return HttpResponse(json.dumps(get_all_sp()), content_type="application/json")


def sp_by_name(name):
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            if entity['@name'] == name:
                return parse_one_sp(entity)


def get_all_sp():
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))
    entity_list = []

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            entity_list.append(parse_one_sp(entity))
    return entity_list


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
            typed_setting[attribute['@name']] = attribute['#text'] if attribute['#text'] else ""

    # path = BASEDIR + "/" + entity['@name'] + "/FederationMetadata.xml"

    # if os.path.isfile(path):
    #     mdfile = open(path, "r")
    #     typed_setting['saml_metadata'] = mdfile.read()

    return {
        'sso_type': entity['@type'],
        'sso_name': entity['@name'],
        'attributes': attribute_list,
        'typed': typed_setting
        }


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


def create_saml_config_files(name):
    ms = sp_by_name(name)

    cert_file = BASEDIR + '/' + name + "/cert.pem"
    key_file = BASEDIR + '/' + name + "/key.pem"
    if not os.path.isfile(cert_file) or not os.path.isfile(key_file):
        cert, key = create_self_signed_cert(name)
        open(cert_file, "wt").write(cert)
        open(key_file, "wt").write(key)

    cert = open(cert_file, "r").read()
    key = open(key_file, "r").read()

    cert = re.sub('-----.*?-----\n?', '', cert)
    key = re.sub('-----.*?-----\n?', '', key)

    auth = "http://docs.oasis-open.org/wsfed/authorization/200706"

    temp_dir = path(__file__).abspath().dirname()

    template = open(temp_dir + "/metadata_templates/sp.xml", "r").read()

    attr_tags = ""
    for attr in ms.get('attributes'):
        mapped_name = attr['map'] if 'map' in attr else attr['name']
        attr_tags += '''
        <ns0:RequestedAttribute isRequired="true" NameFormat="urn:mace:dir:attribute-def:%s"
             Name="%s" FriendlyName="%s"/>''' % (mapped_name, mapped_name, mapped_name)
    
    content = template.format(cert=cert,
                              entityID=name,
                              auth=auth,
                              attr_tags=attr_tags,
                              slo_post_url=ms.get('typed').get('sso_slo_url'),
                              acs_url=ms.get('typed').get('sso_acs_url'))
    
    f = BASEDIR + '/' + name + "/sp.xml"

    open(f, "wt").write(content)

    template = open(temp_dir + "/metadata_templates/idp.xml", "r").read()
    slo_url = "https://" + settings.SAML_ENTITY_ID + reverse("sso_idp_slo_response_receive")
    content = template.format(cert=cert, entityID=settings.SAML_ENTITY_ID, auth=auth, SingleLogoutService=slo_url, SingleSignOnService="")
    f = BASEDIR + '/' + name + "/idp.xml"
    open(f, "wt").write(content)


def download_saml_federation_metadata(request):
    name = request.GET.get("name")
    ms = sp_by_name(name)
    if not ms:
        return HttpResponse("SP with name '%s' does not exist." % name)

    f = BASEDIR + '/' + name + "/idp.xml"
    response = HttpResponse(content_type='application/x-download')
    response['Content-Disposition'] = ('attachment; filename=idp.xml')
    response.write(open(f, "r").read())
    return response

