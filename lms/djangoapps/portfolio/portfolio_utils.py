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
from django_comment_client.utils import (merge_dict, extract, strip_none, get_courseware_context, get_discussion_id_map)
reload(sys)  
sys.setdefaultencoding('utf-8')
DIRECT_ONLY_CATEGORIES = ['course', 'chapter', 'sequential', 'about', 'static_tab', 'course_info']
_active_chapter = {}
class Get_confirm(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.score_urls=[]
        self.state_urls=[]
    def start_section(self, attrs):
        score_attr = [v for k, v in attrs if k=='data-score']
        state_attr = [v for k, v in attrs if k=='data-state']
        if score_attr:
            self.score_urls.extend(score_attr)
        if state_attr:
            self.state_urls.extend(state_attr)

class Get_discussion_id(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.id_urls=[]
    def start_div(self, attrs):
        attr = [v for k, v in attrs if k=='data-discussion-id']
        if attr:
            self.id_urls.extend(attr)

class Get_discussion_visibility(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls=[]
    def start_div(self, attrs):
        attr = [v for k, v in attrs if k=='data-discussion-visibility']
        if attr:
            self.urls.extend(attr)

def Get_combinedopenended_info(con):
    p_title = re.compile('<div[^>]*class="problemtype"[^>]*>([\s\S]*?)<\/div>')
    p_body_a = re.compile('<div*[^>]*class="prompt"[^>]*>[\s\S]*?<\/div>')
    p_body_b = '<span><hr style="border: 1px dashed #ccc; width: 85%; height: 1px;" /></span><span class="section-header section-header-response"><b>Response:</b>    </span>'
    p_body_c = re.compile('<textarea*[^>]*mce_editable="true"[^>]*>([\s\S]*?)<\/textarea>')
    p_body_d = re.compile('<div*[^>]*class="file_url"[^>]*>([\s\S]*?)<\/div>')
    try:
        file_items=''
        for url in p_body_d.findall(con):
            file_item = url.split('##')
            file_items+="<div class='file_upload_item' style='margin:10px;'>"+file_item[1]+" | <a href="+"'"+file_item[0]+"'"+" target='_blank'>Download</a></div>"
        p_body_d = file_items
    except:
        p_body_d=''
    p_body = p_body_a.findall(con)[0] + p_body_b + '<div class="answer">' + p_body_c.findall(con)[0] + '</div>' + p_body_d
    return p_title.findall(con)[0].strip(), p_body

def add_edit_tool(data, course, descriptor):
    return '''<div>{0}<a class="blue_btn" href="{1}">Edit in Course</a>&nbsp;&nbsp;<a class="orange_btn" href="#">View & Join Discussion</a></div>'''.format(data,reverse('jump_to_id',args=(course.id,descriptor.location[4])))

def get_chaper_for_course(request, course, active_chapter,portfolio_user):
    model_data_cache = FieldDataCache.cache_for_descriptor_descendents(
            course.id, portfolio_user, course, depth=2)
    course_module = get_module_for_descriptor(portfolio_user, request, course, model_data_cache, course.id)
    if course_module is None:
        return None

    chapters = list()
    for chapter in course_module.get_display_items():
        chapters.append({'display_name': chapter.display_name_with_default,
                         'url_name': chapter.url_name,
                         'active': chapter.url_name == active_chapter})
        if chapter.url_name == active_chapter:
            _active_chapter['display_name'] = chapter.display_name
    return chapters
def get_module_combinedopenended(request, course, location, portfolio_user):
    location = course.location[0]+'://'+course.location[1]+'/'+course.location[2]+'/chapter/'+location
    section_descriptor = modulestore().get_instance(course.id, location, depth=None)
    field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course.id, portfolio_user, section_descriptor, depth=None)
    descriptor = modulestore().get_instance_items(course.id, location,'combinedopenended',depth=None)
    content = []
    #id_map = get_discussion_id_map(course)
    id_map = {}
    for x in range(len(descriptor)):
        module = get_module_for_descriptor(portfolio_user, request, descriptor[x][1], field_data_cache, course.id,
                                         position=None, wrap_xmodule_display=True, grade_bucket_type=None,
                                         static_asset_path='')
        con = module.runtime.render(module, None, 'student_view').content
        confirm = Get_confirm()
        confirm.feed(con)
        if confirm.score_urls[0] == 'correct' and confirm.state_urls[0] == 'done':
            #content.append(add_edit_tool(con,course,descriptor[x]))
            #import logging
            #log = logging.getLogger("tracking")
            #log.debug("descriptor_location===============================\n:"+str(con)+"\n===========================")
            #c_info = Get_combinedopenended_info()
            #c_info.feed(con)
            title, body = Get_combinedopenended_info(con)
            discussion,visibility=create_discussion(request, course, descriptor[x][1].location[4], location,{'title':title,'body':body,'tags':'portfolio'},portfolio_user,id_map)
            if visibility:
                content.append(discussion)

    return content

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

def create_thread(request, course_id, commentable_id, thread_data, portfolio_user, id_map):
    """
    Given a course and commentble ID, create the thread
    """
    course = get_course_with_access(portfolio_user, course_id, 'load')
   
    if course.allow_anonymous:
        anonymous = thread_data.get('anonymous', 'false').lower() == 'true'
    else:
        anonymous = False

    if course.allow_anonymous_to_peers:
        anonymous_to_peers = thread_data.get('anonymous_to_peers', 'false').lower() == 'true'
    else:
        anonymous_to_peers = False
    thread = cc.Thread(**extract(thread_data, ['body', 'title', 'tags']))
    thread.update_attributes(**{
        'anonymous': anonymous,
        'anonymous_to_peers': anonymous_to_peers,
        'commentable_id': commentable_id,
        'course_id': course_id,
        'user_id': portfolio_user.id,
    })
    
    user = cc.User.from_django_user(portfolio_user)

    #kevinchugh because the new requirement is that all groups will be determined
    #by the group id in the request this all goes away
    #not anymore, only for admins

    # Cohort the thread if the commentable is cohorted.
    if is_commentable_cohorted(course_id, commentable_id):
        user_group_id = get_cohort_id(user, course_id)

        # TODO (vshnayder): once we have more than just cohorts, we'll want to
        # change this to a single get_group_for_user_and_commentable function
        # that can do different things depending on the commentable_id
        if cached_has_permission(portfolio_user, "see_all_cohorts", course_id):
            # admins can optionally choose what group to post as
            group_id = thread_data.get('group_id', user_group_id)
        else:
            # regular users always post with their own id.
            group_id = user_group_id

        if group_id:
            thread.update_attributes(group_id=group_id)

    thread.save()
    #patch for backward compatibility to comments service
    if not 'pinned' in thread.attributes:
        thread['pinned'] = False

    if thread_data.get('auto_subscribe', 'false').lower() == 'true':
        user = cc.User.from_django_user(portfolio_user)
        user.follow(thread)
    #courseware_context = get_courseware_context(thread, course)
    data = thread.to_dict()
    '''
    id = data['commentable_id']
    content_info = None
    if id in id_map:
        location = id_map[id]["location"].url()
        title = id_map[id]["title"]

        url = reverse('jump_to', kwargs={"course_id": course.location.course_id,
                  "location": location})

        data.update({"courseware_url": url, "courseware_title": title})
    '''
    #if courseware_context:
    #    data.update(courseware_context)  
    return ajax_content_response(request, course_id, data, 'discussion/ajax_create_thread.html')
    '''
    if request.is_ajax():
        return ajax_content_response(request, course_id, data, 'discussion/ajax_create_thread.html')
    else:
        return JsonResponse(safe_content(data))
    '''

def get_threads(request, course_id, portfolio_user,discussion_id=None, per_page=20):
    """
    This may raise cc.utils.CommentClientError or
    cc.utils.CommentClientUnknownError if something goes wrong.
    """
    default_query_params = {
        'page': 1,
        'per_page': per_page,
        'sort_key': 'date',
        'sort_order': 'desc',
        'text': '',
        'tags': '',
        'commentable_id': discussion_id,
        'course_id': course_id,
        'user_id': portfolio_user.id,
    }

    if not request.GET.get('sort_key'):
        # If the user did not select a sort key, use their last used sort key
        cc_user = cc.User.from_django_user(portfolio_user)
        cc_user.retrieve()
        # TODO: After the comment service is updated this can just be user.default_sort_key because the service returns the default value
        default_query_params['sort_key'] = cc_user.get('default_sort_key') or default_query_params['sort_key']
    else:
        # If the user clicked a sort key, update their default sort key
        cc_user = cc.User.from_django_user(portfolio_user)
        cc_user.default_sort_key = request.GET.get('sort_key')
        cc_user.save()

    #there are 2 dimensions to consider when executing a search with respect to group id
    #is user a moderator
    #did the user request a group

    #if the user requested a group explicitly, give them that group, othewrise, if mod, show all, else if student, use cohort

    group_id = request.GET.get('group_id')

    if group_id == "all":
        group_id = None

    if not group_id:
        if not cached_has_permission(portfolio_user, "see_all_cohorts", course_id):
            group_id = get_cohort_id(portfolio_user, course_id)

    if group_id:
        default_query_params["group_id"] = group_id

    #so by default, a moderator sees all items, and a student sees his cohort

    query_params = merge_dict(default_query_params,
                              strip_none(extract(request.GET,
                                                 ['page', 'sort_key',
                                                  'sort_order', 'text',
                                                  'tags', 'commentable_ids', 'flagged','portfolio'])))

    threads, page, num_pages = cc.Thread.search(query_params,{'portfolio':'true'})

    #now add the group name if the thread has a group id
    for thread in threads:

        if thread.get('group_id'):
            thread['group_name'] = get_cohort_by_id(course_id, thread.get('group_id')).name
            thread['group_string'] = "This post visible only to Group %s." % (thread['group_name'])
        else:
            thread['group_name'] = ""
            thread['group_string'] = "This post visible to everyone."

        #patch for backward compatibility to comments service
        if not 'pinned' in thread:
            thread['pinned'] = False
    query_params['page'] = page
    query_params['num_pages'] = num_pages
    return threads, query_params

def update_thread(request, course_id, thread_id, thread_data):
    """
    Given a course id and thread id, update a existing thread, used for both static and ajax submissions
    """
    thread = cc.Thread.find(thread_id)
    thread.update_attributes(**extract(thread_data, ['body', 'title', 'tags']))
    thread.save()

def create_comment(request, course_id, comment_data, portfolio_user, thread_id=None, parent_id=None):
    """
    given a course_id, thread_id, and parent_id, create a comment,
    called from create_comment to do the actual creation
    """
    comment = cc.Comment(**extract(comment_data, ['body']))

    course = get_course_with_access(portfolio_user, course_id, 'load')
    anonymous = False
    anonymous_to_peers = False

    comment.update_attributes(**{
        'anonymous': anonymous,
        'anonymous_to_peers': anonymous_to_peers,
        'user_id': portfolio_user.id,
        'course_id': course_id,
        'thread_id': thread_id,
        'parent_id': parent_id,
    })
    comment.save()
    user = cc.User.from_django_user(portfolio_user)
    user.follow(comment.thread)


def create_discussion(request, course, ora_id, parent_location, thread_data, portfolio_user, id_map):
    category = 'discussion'
    context = ''
    display_name = 'Discussion'
    discussion_visibility = True
    '''
    if not has_access(request.user, parent_location):
        raise PermissionDenied()
    '''
    parent = get_modulestore(category).get_item(parent_location)
    #dest_location = parent_location.replace(category=category, name=uuid4().hex)
    dest_location = Location(parent_location).replace(category=category, name=str(portfolio_user.id)+'_'+ora_id)
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
            '''
            discussion_category = _active_chapter['display_name'].split(':')
            if len(discussion_category)>1:
                metadata['discussion_category'] = discussion_category[0]
                metadata['discussion_target'] = discussion_category[1]
            else:
                metadata['discussion_category'] = discussion_category[0]
                metadata['discussion_target'] = 'Course Overview'
            '''
            metadata['discussion_category']=''
            metadata['discussion_target']=''
        get_modulestore(category).create_and_save_xmodule(
            dest_location,
            definition_data=data,
            metadata=metadata,
            system=parent.system,
        )
        '''
        if category not in DETACHED_CATEGORIES:
            get_modulestore(parent.location).update_children(parent_location, parent.children + [dest_location.url()])
        '''

        context = get_discussion_context(request, course, dest_location, parent_location, portfolio_user)
        did = Get_discussion_id()
        did.feed(context)
        create_thread(request, course.id, did.id_urls[0], thread_data, portfolio_user, id_map)
        thread_id = get_threads(request, course.id, portfolio_user, did.id_urls[0], per_page=20)[0][0]['id']
        create_comment(request, course.id, {'body':'Please leave me your feedback by adding a comment below.'}, portfolio_user, thread_id)
    else:
        context = get_discussion_context(request, course, dest_location, parent_location, portfolio_user)
        did = Get_discussion_id()
        did.feed(context)
        try:
            thread_id = get_threads(request, course.id, portfolio_user, did.id_urls[0], per_page=20)[0][0]['id']
        except IndexError:
            if modulestore().has_item(course.id, dest_location):
                modulestore().delete_item(dest_location)
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
                    metadata['discussion_target']=''
                get_modulestore(category).create_and_save_xmodule(
                    dest_location,
                    definition_data=data,
                    metadata=metadata,
                    system=parent.system,
                )
                context = get_discussion_context(request, course, dest_location, parent_location, portfolio_user)
                did = Get_discussion_id()
                did.feed(context)
                create_thread(request, course.id, did.id_urls[0], thread_data, portfolio_user, id_map)
                thread_id = get_threads(request, course.id, portfolio_user, did.id_urls[0], per_page=20)[0][0]['id']
                create_comment(request, course.id, {'body':'Please leave me your feedback by adding a comment below.'}, portfolio_user, thread_id)
        update_thread(request, course.id, thread_id, thread_data)
        context = get_discussion_context(request, course, dest_location, parent_location, portfolio_user)
    #if context=='':
    #    context = get_discussion_context(request, course, dest_location, parent_location)
    new_post_btn_match=re.compile('<a*[^>]*class="new-post-btn"[^>]*>[\s\S]*?<\/a>')
    discussion_show_match=re.compile('<a*[^>]*class="discussion-show control-button*"[^>]*>[\s\S]*?<\/a>')
    #p=re.compile('<a*[^>]*class="new-post-btn"[^>]*>[\s\S]*?<\/a>')
    if request.user.id == portfolio_user.id:
        edit_course_btn = '<a class="edit-course-btn" href="{0}">Edit in Course</a>'.format(reverse('jump_to_id',args=(course.id,ora_id)))
        discussion_visibility=True
    else:
        edit_course_btn =''
        context = context.replace(discussion_show_match.findall(context)[0], '')
        d_vis = Get_discussion_visibility()
        d_vis.feed(context)
        if d_vis.urls[0]=='true':
            discussion_visibility=True
        else:
            discussion_visibility=False
    context = context.replace(new_post_btn_match.findall(context)[0], edit_course_btn)
    return context, discussion_visibility

@require_POST
@login_required
def set_discussion_visibility(request,course_id,comment_id,discussion_visibility):
    
    location = str(request.user.id)+'_'+comment_id
    course_location = course_id.split('/')
    item_location = Location('i4x://'+course_location[0]+'/'+course_location[1]+'/discussion/'+location)
    
    store = get_modulestore(item_location)
    metadata = {}
    metadata['discussion_visibility'] = discussion_visibility
    if metadata is not None:
        # the postback is not the complete metadata, as there's system metadata which is
        # not presented to the end-user for editing. So let's fetch the original and
        # 'apply' the submitted metadata, so we don't end up deleting system metadata
        
        existing_item = modulestore().get_item(item_location)
        # update existing metadata with submitted metadata (which can be partial)
        # IMPORTANT NOTE: if the client passed 'null' (None) for a piece of metadata that means 'remove it'. If
        # the intent is to make it None, use the nullout field
        for metadata_key, value in metadata.items():
            field = existing_item.fields[metadata_key]

            if value is None:
                field.delete_from(existing_item)
            else:
                value = field.from_json(value)
                field.write_to(existing_item, value)
        # Save the data that we've just changed to the underlying
        # MongoKeyValueStore before we update the mongo datastore.
        existing_item.save()
        # commit to datastore
        store.update_metadata(item_location, own_metadata(existing_item))
    
    return JsonResponse({
        'visibility': discussion_visibility
    })
    


    