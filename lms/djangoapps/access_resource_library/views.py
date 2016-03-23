from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from student.models import ResourceLibrary, StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required
from xmodule.modulestore.django import modulestore
from django.views.decorators.cache import cache_control
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State
from .models import Resource, GenericResource
from courseware.courses import get_courses, sort_by_custom


def index_bak(request):

    def custom_compare_key(item):
        category_order = item.category.display_order * 10000
        subclass_order = (item.subclass.display_order if item.subclass is not None else 1) * 100
        display_order = item.display_order
        return category_order + subclass_order + display_order

    resources_librarys = list(ResourceLibrary.objects.prefetch_related())

    resources_librarys.sort(key=lambda x: custom_compare_key(x), reverse=False)
    result = {}
    for resource_library in resources_librarys:
        category = resource_library.category
        subclass = resource_library.subclass if resource_library.subclass is not None else None
        subclass_sites = subclass.sites.get_query_set() if subclass else None

        tmp_item = {}
        tmp_dict = {}
        tmp_sub_items = {}
        tmp_cat_items = {}

        category_key = 'id_{}_{}order_{}'.format(category.id, category.display, category.display_order)
        category_displayorder = category.display_order

        subclass_key = 'id_{}_{}order_{}'.format(subclass.id, subclass.display, subclass.display_order) if subclass is not None else 'nosubclass'
        subclass_name = subclass.display if subclass is not None else 'nosubclass'
        subclass_displayorder = subclass.display_order if subclass else 0

        tmp_item['display'] = resource_library.display
        tmp_item['link'] = resource_library.link

        if result.get(category_key, None) is None:
            tmp_sub_items['display'] = subclass_name
            tmp_sub_items['display_order'] = subclass_displayorder
            tmp_sub_items['items'] = deque()
            tmp_sub_items['items'].append(tmp_item)
            if subclass_sites:
                tmp_sub_items['sites'] = deque()
                for site in subclass_sites:
                    tmp_sit_items = dict()
                    tmp_sit_items['display'] = site.display
                    tmp_sit_items['link'] = site.link
                    tmp_sit_items['display_order'] = site.display_order
                    tmp_sub_items['sites'].append(tmp_sit_items)
            tmp_dict[subclass_key] = tmp_sub_items
            tmp_cat_items['display'] = category.display
            tmp_cat_items['display_order'] = category.display_order
            tmp_cat_items['items'] = tmp_dict
            result[category_key] = tmp_cat_items
        else:
            if result[category_key]['items'].get(subclass_key, None) is None:
                tmp_sub_items['display'] = subclass_name
                tmp_sub_items['display_order'] = subclass_displayorder
                tmp_sub_items['items'] = deque()
                tmp_sub_items['items'].append(tmp_item)
                if subclass_sites:
                    if tmp_sub_items.get('sites', None) is None:
                        tmp_sub_items['sites'] = deque()
                    for site in subclass_sites:
                        tmp_sit_items = dict()
                        tmp_sit_items['display'] = site.display
                        tmp_sit_items['display_order'] = site.display_order
                        tmp_sit_items['link'] = site.link
                        tmp_sub_items['sites'].append(tmp_sit_items)
                result[category_key]['items'][subclass_key] = tmp_sub_items
            else:
                result[category_key]['items'][subclass_key]['items'].append(tmp_item)

    return render_to_response('access_resource_library.html', {'resources': result})


@login_required
def index(request):
    name = request.GET.get('name', 'Pepper Course Libraries')
    try:
        static_content = StaticContent.objects.get(name=name)
        static_html_content = static_content.content
    except Exception:
        static_html_content = 'sorry for maintain...'

    return render_to_response('access_resource_library_.html', {'static_content': static_html_content})


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def states(request):
    """
    Render "find states" page.
    """
    state = request.GET.get('state', '')
    filterDic = {'_id.category': 'course'}
    state_list = []
    if request.user.is_superuser is False:
        filterDic['metadata.display_state'] = state
    items = modulestore().collection.find(filterDic)
    courses = modulestore()._load_items(list(items), 0)
    state_temp = []
    for course in courses:
        if len(course.display_state) > 0 and is_all(course, 'state') is False:
            if request.user.is_superuser is False:
                state_temp.append(state)
            else:
                state_temp.extend(course.display_state)
    state_temp = sorted(set(state_temp), key=lambda x: x[0])
    for sl in state_temp:
        state_list.append({'id': sl, 'name': sl})
    return render_to_response("resource_library/collections.html", {'page_title': 'State',
                                                                    'collection_type': 'state',
                                                                    'items': state_list})


@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def districts(request):
    """
    Render "find districts" page.
    """
    district = request.GET.get('district', '')
    filterDic = {'_id.category': 'course'}

    district_name = {}
    district_temp = []
    district_list = []

    if request.user.is_superuser is False:
        filterDic['metadata.display_district'] = district
    items = modulestore().collection.find(filterDic)
    courses = modulestore()._load_items(list(items), 0)
    for course in courses:
        if len(course.display_district) > 0 and is_all(course, 'district') is False:
            if request.user.is_superuser is False:
                district = filterDic['metadata.display_district']
                districts = District.objects.filter(code=district)
                district_temp.append(district)
            else:
                districts = District.objects.filter(code__in=course.display_district)
                district_temp.extend(course.display_district)

            for district in districts:
                district_name[district.code] = district.name
                
    district_temp = sorted(set(district_temp), key=lambda x: x[0])
    
    for dl in district_temp:
        district_list.append({'id': dl, 'name': district_name[dl]})
        
    return render_to_response("resource_library/collections.html", {'page_title': 'District',
                                                                    'collection_type': 'district',
                                                                    'items': district_list})


def is_all(course, type):
    if type == 'collection':
        if 'All' in course.content_collections:
            return True
    elif type == 'state':
        if 'All' in course.display_state:
            return True
    elif type == 'district':
        if 'All' in course.display_district:
            return True
    return False


@login_required
def index_list(request):
    state_temp = []
    district_temp = []
    district_name = {}
    district_list = []
    
    courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    courses = sort_by_custom(courses)
    
    for course in courses:
        if request.user.is_superuser is False:
            if request.user.profile.district.state.name in course.display_state:
                state_temp.append(request.user.profile.district.state.name)

            if request.user.profile.district.code in course.display_district:
                district = District.objects.filter(code=request.user.profile.district.code)[0]
                district_temp.append(request.user.profile.district.code)
                district_name[request.user.profile.district.code] = district.name
        else:
            if len(course.display_state) > 0 and is_all(course, 'state') is False:
                state_temp.extend(course.display_state)

            if len(course.display_district) > 0 and is_all(course, 'district') is False:
                districts = District.objects.filter(code__in=course.display_district)
                district_temp.extend(course.display_district)
                for district in districts:
                    district_name[district.code] = district.name

        state_list = sorted(set(state_temp), key=lambda x: x[0])
        district_temp = sorted(set(district_temp), key=lambda x: x[0])
        for dl in district_temp:
            district_list.append({'id': dl, 'name': district_name[dl]})
    
    return render_to_response('access_resource_library_list.html', {
                                                          "states": state_list,
                                                          "districts": district_list})


@login_required
def resources(request):
    collection_type = request.GET.get("collection_type")
    collection = request.GET.get("collection")
    items = Resource.objects.filter(collection_type=collection_type, collection=collection)
    
    collection_name = collection
    if collection_type == "district":
        names = District.objects.filter(code=collection).values_list('name', flat=True)
        if len(names):
            collection_name = names[0] 
        
    return render_to_response('resource_library/resources.html', {
        'page_title': collection_name,
        'collection_type': collection_type,
        'items': items})


@login_required
def generic_resources(request):
    resource_id = request.GET.get("resource")
    resource = Resource.objects.get(id=resource_id)
    items = GenericResource.objects.filter(resource=resource)
    return render_to_response('resource_library/generic_resources.html', {
        'page_title': resource.title,
        'collection_type': generic_resources,
        'items': items})

    
