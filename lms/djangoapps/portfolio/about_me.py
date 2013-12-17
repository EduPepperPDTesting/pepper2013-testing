from xmodule.modulestore.django import modulestore
from xmodule.modulestore.inheritance import own_metadata
from xmodule.modulestore import Location
from courseware.module_render import toc_for_course, get_module_for_descriptor
from courseware.model_data import FieldDataCache
from courseware.views import jump_to_id
from django.core.urlresolvers import reverse
from HTMLParser import HTMLParser
from sgmllib import SGMLParser

from django_comment_client.base.views import ajax_content_response
#from django_comment_client.forum.views import inline_discussion,get_threads
from django_comment_client.utils import JsonResponse, JsonError, extract, get_courseware_context, safe_content
from django_comment_client.permissions import check_permissions_by_view, cached_has_permission
from util.json_request import expect_json, JsonResponse
from course_groups.cohorts import get_cohort_id, is_commentable_cohorted
from courseware.courses import get_course_with_access
import comment_client as cc
import sys, re
import urllib
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from course_groups.cohorts import (is_course_cohorted, get_cohort_id, is_commentable_cohorted,
                                   get_cohorted_commentables, get_course_cohorts, get_cohort_by_id)
from django_comment_client.utils import (merge_dict, extract, strip_none, get_courseware_context)
reload(sys)  
sys.setdefaultencoding('utf-8')
DIRECT_ONLY_CATEGORIES = ['course', 'chapter', 'sequential', 'about', 'static_tab', 'course_info']

def get_modulestore(category_or_location):
    """
    Returns the correct modulestore to use for modifying the specified location
    """
    if isinstance(category_or_location, Location):
        category_or_location = category_or_location.category

    if category_or_location in DIRECT_ONLY_CATEGORIES:
        return modulestore('direct')
    else:
        return modulestore()

def get_discussion_context(request, course, location, parent_location,portfolio_user):
        section_descriptor = modulestore().get_instance(course.id, parent_location, depth=None)
        field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course.id, portfolio_user, section_descriptor, depth=None)
        descriptor = modulestore().get_item(location)
        module = get_module_for_descriptor(portfolio_user, request, descriptor, field_data_cache, course.id,
                                     position=None, wrap_xmodule_display=True, grade_bucket_type=None,
                                     static_asset_path='')
        return module.runtime.render(module, None, 'student_view').content


def create_discussion_about_me(request, course, portfolio_user):
    category = 'discussion'
    context = ''
    display_name = 'Discussion'
    discussion_visibility = True
    '''
    if not has_access(request.user, parent_location):
        raise PermissionDenied()
    '''
    course_location = course.id.split('/')
    #parent_location = Location('i4x://'+course_location[0]+'/'+course_location[1]+'/'+course_location[2])
    parent_location = course.location
    parent = get_modulestore(category).get_item(parent_location)
    #dest_location = parent_location.replace(category=category, name=uuid4().hex)

    dest_location = Location(parent_location).replace(category=category,name=course_location[0]+'_'+course_location[1]+'_'+course_location[2]+'_'+str(portfolio_user.id)+'__am')
    #dest_location = Location('i4x://'+course_location[0]+'/'+course_location[1]+'/discussion/'+course_location[0]+'_'+course_location[1]+'_'+course_location[2]+'_'+str(portfolio_user.id)+'_am')
    # get the metadata, display_name, and definition from the request
    #if modulestore().has_item(course.id, dest_location):
    #    modulestore().delete_item(dest_location)
    if modulestore().has_item(course.id, dest_location) == False:
  
        metadata = {}
        data = None
        template_id = request.POST.get('boilerplate')
        if template_id is not None:
            clz = XModuleDescriptor.load_class(category)
            if clz is not None:
                template = clz.get_template(template_id)
                if template is not None:
                    metadata = template.get('metadata', {})
                    data = template.get('data')

        if display_name is not None:
            metadata['display_name'] = display_name
            metadata['discussion_category']=''
            metadata['discussion_target'] = ''
        get_modulestore(category).create_and_save_xmodule(
            dest_location,
            definition_data=data,
            metadata=metadata,
            system=parent.system,
        )
    context = get_discussion_context(request, course, dest_location, parent_location, portfolio_user)
    new_post_btn_match=re.compile('<a*[^>]*class="new-post-btn"[^>]*>[\s\S]*?<\/a>')
    if request.user.id != portfolio_user.id:
        context = context.replace(new_post_btn_match.findall(context)[0], '')
    return context

    


    