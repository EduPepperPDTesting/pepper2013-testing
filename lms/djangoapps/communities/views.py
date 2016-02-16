from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
import json
import logging
from courseware.courses import get_courses, course_image_url, get_course_about_section
from .utils import is_facilitator
from .models import CommunityCommunities, CommunityCourses, CommunityResources, CommunityUsers, CommunityDiscussions, CommunityDiscussionReplies
from administration.pepconn import get_post_array
from operator import itemgetter

log = logging.getLogger("tracking")


def index(request):
    return render_to_response('communities/communities.html', {})


def community_ppd(request):
    return render_to_response('communities/community_ppd.html', {})


def community_ngss(request):
    return render_to_response('communities/community_ngss.html', {})


@login_required
def community(request, community):
    """
    Returns a single community page.
    :param request: Request object.
    :param community: The machine name of the community.
    :return: The Community page.
    """

    community = CommunityCommunities.objects.get(community=community)
    facilitator = CommunityUsers.objects.select_related().filter(facilitator=True)
    users = CommunityUsers.objects.select_related().filter(facilitator=False)
    discussions = CommunityDiscussions.objects.filter(community=community)
    me = CommunityUsers.objects.select_related().get(user=request.user)

    for d in discussions:
        d.repiles = CommunityDiscussionReplies.objects.filter(discussion=d).count()
        d.views = 0  # todo: how to get view count?
        
    data = {"community": community,
            "facilitator": facilitator[0] if len(facilitator) else None,
            "discussions": discussions,
            "users": users,
            "me": me}
    
    return render_to_response('communities/community.html', data)


@login_required
def communities(request):
    """
    Returns the communities page.
    :param request: Request object.
    :return: The Communities page.
    """
    community_list = list()
    filter_dict = dict()

    # If this is a regular user, we only want to show public communities and private communities to which they belong.
    if not request.user.is_superuser:
        # Filter the normal query to only show public communities.
        filter_dict.update({'private': False})

        # Do a separate filter to grab private communities this user belongs to.
        items = CommunityUsers.objects.select_related().filter(user=request.user, community__private=True)
        for item in items:
            community_list.append({'id': item.community.community,
                                   'name': item.community.name,
                                   'logo': item.community.logo,
                                   'private': item.community.private})
    # Query for the communities this user is allowed to see.
    items = CommunityCommunities.objects.filter(**filter_dict)
    for item in items:
        community_list.append({'id': item.community,
                               'name': item.name,
                               'logo': item.logo,
                               'private': item.private})

    # Set up the data to send to the communities template, with the communities sorted by name.
    data = {'communities': sorted(community_list, key=itemgetter('name'))}
    return render_to_response('communities/communities.html', data)


@login_required
def community_edit(request, community='new'):
    """
    Sets up the community add/edit form.
    :param request: Request object.
    :param community: Which community to edit, or 'new' if adding one.
    :return: Form page.
    """
    # Get a list of courses for the course drop-down in the form.
    courses_drop = get_courses(request.user)
    data = {'courses_drop': []}
    for course in courses_drop:
        data['courses_drop'].append({'id': course.id,
                                     'number': course.display_number_with_default,
                                     'name': get_course_about_section(course, 'title'),
                                     'logo': course_image_url(course)})

    # If we are adding a new community, and the user making the request is a superuser, return a blank form.
    if community == 'new' and request.user.is_superuser:
        data.update({'community': '',
                     'name': '',
                     'motto': '',
                     'logo': '',
                     'facilitator': '',
                     'private': '',
                     'courses': [''],
                     'resources': [{'name': '', 'link': '', 'logo': ''}]})
        return render_to_response('communities/community_edit.html', data)
    # If we are editing a community, make sure the user is either a superuser or facilitator for this community, and if
    # so, return a populated form for editing.
    elif community != 'new' and (request.user.is_superuser or is_facilitator(request.user, community)):
        # Grab the data from the DB.
        community_object = CommunityCommunities.objects.get(community=community)
        courses = CommunityCourses.objects.filter(community=community_object)
        resources = CommunityResources.objects.filter(community=community_object)
        facilitator = CommunityUsers.objects.get(community=community_object, facilitator=True)

        # Build the lists of courses and resources.
        course_list = list()
        resource_list = list()
        for course in courses:
            course_list.append(course['course'])
        if not len(course_list):
            course_list.append('')
        for resource in resources:
            resource_list.append({'name': resource['name'],
                                  'link': resource['link'],
                                  'logo': resource['logo']})
        if not len(resource_list):
            resource_list.append({'name': '', 'link': '', 'logo': ''})

        # Put together the data to send to the template.
        data.update({'community': community_object['community'],
                     'name': community_object['name'],
                     'motto': community_object['motto'],
                     'logo': community_object['logo'],
                     'facilitator': facilitator.user.email,
                     'private': community_object['private'],
                     'courses': course_list,
                     'resources': resource_list})

        return render_to_response('communities/community_edit.html', data)

    # If neither of the other tests worked, the user isn't allowed to do this.
    return HttpResponseForbidden()


@login_required
def community_edit_process(request):
    """
    Processes the form data from the community add/edit form.
    :param request: Request object.
    :return: JSON response.
    """
    courses = get_post_array(request.POST, 'course')
    resource_names = get_post_array(request.POST, 'resource_name')
    resource_links = get_post_array(request.POST, 'resource_link')
    resource_logos_existing = get_post_array(request.POST, 'resource_logo')
    resource_logos_new = get_post_array(request.FILES, 'resource_logo')

