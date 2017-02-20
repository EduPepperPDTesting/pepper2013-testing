from mitxmako.shortcuts import render_to_response
import xmltodict
import json
from django.conf import settings
from collections import defaultdict
import logging
import os
from os import path
from courseware.courses import get_courses, get_course_about_section
from .models import CourseAssignment, CourseAssignmentCourse
from pepper_utilities.utils import render_json_response
from permissions.decorators import user_has_perms
from django_future.csrf import ensure_csrf_cookie
from django.db import transaction

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


def _get_course_assignment_data():
    data = []
    assignments = CourseAssignment.objects.all()
    courses = CourseAssignmentCourse.objects.all()
    for assignment in assignments:
        course_list = []
        for course in courses.filter(assignment=assignment.id):
            course_list.append(course.course)
        data.append({'id': assignment.id,
                     'type': assignment.sso_name,
                     # 'param': assignment.param_name,
                     # 'param_value': assignment.param_value,
                     'courses': course_list})
    return data


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
def course_assignment(request):
    courses_drop = get_courses(request.user)
    md = _get_metadata()
    sso_names = ['EasyIEP']
    for d in md:
        sso_names.append(d['sso_name'])
    data = {'sso_names': sso_names, 'courses_drop': [], 'assignments': _get_course_assignment_data()}
    for course in courses_drop:
        data['courses_drop'].append({'id': course.id,
                                     'name': get_course_about_section(course, 'title')})
    # raise Exception('{0}'.format(sso_metadata))
    return render_to_response('sso/manage/course_selection.html', data)


@user_has_perms('sso', 'administer')
def course_assignment_list(request):
    return render_json_response(_get_course_assignment_data())


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
@transaction.commit_manually
def course_assignment_save(request):
    # ca_id = request.POST.get('ca_id', False)
    courses = request.POST.getlist('courses', False)
    sso_name = request.POST.get('sso_name', False)
    try:
        ca = CourseAssignment()
        ca.sso_name = sso_name
        ca.save()
        for course in courses:
            cac = CourseAssignmentCourse()
            cac.assignment = ca
            cac.course = course
            cac.save()
    except Exception as e:
        data = {'success': False, 'error': '{0}'.format(e)}
        transaction.rollback()
    else:
        data = {'success': True}
        transaction.commit()
    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
@transaction.commit_manually
def course_assignment_delete(request):
    assignment_id = request.POST.get('assignment_id', False)
    try:
        if assignment_id:
            CourseAssignment.objects.get(id=int(assignment_id)).delete()
        else:
            raise Exception('No Assignment selected.')
    except Exception as e:
        data = {'success': False, 'error': '{0}'.format(e)}
        transaction.rollback()
    else:
        data = {'success': True}
        transaction.commit()
    return render_json_response(data)


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


def _get_metadata():
    xmlfile = open(BASEDIR + "/metadata.xml", "r")
    parsed_data = xmltodict.parse(xmlfile.read(),
                                  dict_constructor=lambda *args, **kwargs: defaultdict(list, *args, **kwargs))
    entity_list = []

    if 'entity' in parsed_data['entities'][0]:
        for entity in parsed_data['entities'][0]['entity']:
            entity_list.append(parse_one_idp(entity))

    return entity_list


@user_has_perms('sso', 'administer')
def all_json(request):
    return render_json_response(_get_metadata())
