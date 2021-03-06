"""
True North Logic integration module
"""

# Imports
from student.views import course_from_id
from student.models import District
from mitxmako.shortcuts import render_to_response
from xmodule.modulestore.django import modulestore
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .utils import *
import json


def tnl_table_data():
    """
    Returns the data needed to build the tables on the config page
    """
    # Get the Domains.
    domains = tnl_get_domain()
    # Get the districts.
    districts = tnl_get_district()
    # Get the list of course ids.
    courses = tnl_get_course()
    # Load the courses and add the name to the objects.
    for x in range(0, len(courses)):
        course = course_from_id(courses[x].course)
        courses[x].name = course.display_name_with_default
    return domains, districts, courses


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_tables(request):
    """
    Handles the TNL configuration table updates
    """
    # Get the table data
    domains, districts, courses = tnl_table_data()
    domains_out = list()
    districts_out = list()
    courses_out = list()
    # The domain, district, and course data as returned don't make for good JSON, so rebuild them.
    for domain in domains:
        domains_out.append({'state': domain.state.name,
                            'name': domain.name,
                            'id': domain.id})
    for district in districts:
        districts_out.append({'name': district.district.name,
                              'state': district.district.state.name,
                              'code': district.district.code,
                              'domain': district.domain.name,
                              'id': district.id})
    for course in courses:
        courses_out.append({'name': course.name,
                            'domain': course.domain.name,
                            'id': course.course})
    # Build the context and return the template.
    context = {'domains': domains_out, 'districts': districts_out, 'courses': courses_out}
    return HttpResponse(json.dumps(context), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_configuration(request):
    """
    Handles the TNL configuration page
    """
    # Get the initial table data.
    domains, districts, courses = tnl_table_data()
    # Build the context and return the template.
    context = {'domains': domains, 'districts': districts, 'courses': courses}
    return render_to_response('tnl/configuration.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_domain_add(request):
    """
    Adds the domain.
    """
    try:
        data = {'password': request.POST.get('password'),
                'salt': request.POST.get('salt'),
                'base_url': request.POST.get('base_url'),
                'admin_id': request.POST.get('admin_id'),
                'provider_id': int(request.POST.get('provider_id')),
                'edagency_id': int(request.POST.get('edagency_id')),
                'credit_area_id': int(request.POST.get('credit_area_id')),
                'credit_value_type_id': int(request.POST.get('credit_value_type_id')),
                'credit_value': int(request.POST.get('credit_value')),
                'state': int(request.POST.get('state')),
                'name': request.POST.get('name')}
        id = request.POST.get('id')
        edit = bool(request.POST.get('edit') == 'true')
        tnl_add_domain(id, edit, data)
        return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({'success': 'Error: {0}'.format(e)}), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_domain_delete(request):
    """
    Deletes the requested domain from the DB.
    """
    try:
        ids = get_post_array(request.POST, 'ids')
        tnl_delete_domain(ids)
        return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_district_add(request):
    """
    Adds the requested district to the TNL enabled districts.
    """
    try:
        # Add the course to the enabled list.
        tnl_add_district(request.POST.get('district'), request.POST.get('domain'))
        return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_district_delete(request):
    """
    Deletes the requested districts from the TNL enabled districts.
    """
    try:
        ids = get_post_array(request.POST, 'ids')
        tnl_delete_district(ids)
        return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_course_add(request):
    """
    Adds the requested course to the TNL enabled courses and registers it with TNL.
    """
    try:
        # Load the selected course.
        course = course_from_id(request.POST.get('course'))
        # Load the selected Domain.
        domain = request.POST.get('domain')
        # Create a TNL Instance.
        tnl_instance = TNLInstance(domain)
        # Register the course with TNL.
        tnl_instance.register_course(course)
        return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_course_delete(request):
    """
    Deletes the requested courses from the TNL enabled courses.
    """
    try:
        ids = get_post_array(request.POST, 'ids')
        tnl_delete_course(ids)
        return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_drop_courses(request):
    """
    Returns a list of course IDs for a course selection dropdown.
    """
    # Only select courses.
    filter_dict = {'_id.category': 'course'}
    # Do the selection.
    items = modulestore().collection.find(filter_dict)
    # Load the objects.
    courses = modulestore()._load_items(list(items), 0)
    course_ids = list()
    # Build a list of id and name dicts to return as JSON.
    for course in courses:
        course_ids.append({'id': course.id,
                           'name': course.display_number_with_default + ' - ' + course.display_name_with_default
                           })
    return HttpResponse(json.dumps(course_ids), mimetype='application/json')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_drop_districts(request):
    """
    Returns a list of unused districts for the district selection dropdown.
    """
    r = list()
    if request.GET.get('state'):
        # Select districts with the specified district, which haven't been added to the TNLDistricts.
        data = District.objects.filter(state=request.GET.get('state'),
                                       tnldistricts__date_added__isnull=True).order_by("name")
        # Build a list of dicts with id, name, and code to return as JSON.
        for item in data:
            r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_drop_domains(request):
    r = list()
    data = tnl_get_domain()

    for item in data:
        r.append({"id": item.id, "name": item.name})

    return HttpResponse(json.dumps(r), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def tnl_domain_data(request):
    domain = tnl_get_domain(int(request.GET.get('domain')))
    data = {'password': domain.password,
            'salt': domain.salt,
            'base_url': domain.base_url,
            'admin_id': domain.admin_id,
            'provider_id': domain.provider_id,
            'edagency_id': domain.edagency_id,
            'credit_area_id': domain.credit_area_id,
            'credit_value_type_id': domain.credit_value_type_id,
            'credit_value': domain.credit_value,
            'state': domain.state.id,
            'name': domain.name,
            'id': domain.id}
    return HttpResponse(json.dumps(data), content_type='application/json')
