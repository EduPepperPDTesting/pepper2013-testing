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
from student.models import User

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
    mems = CommunityUsers.objects.select_related().filter(user=request.user)

    for d in discussions:
        d.repiles = CommunityDiscussionReplies.objects.filter(discussion=d).count()
        d.views = 0  # todo: how to get view count?
        
    data = {"community": community,
            "facilitator": facilitator[0] if len(facilitator) else None,
            "discussions": discussions,
            "users": users,
            "mem": mems[0] if mems.count() else None}
    
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
        data.update({'community_id': 'new',
                     'community': '',
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
        data.update({'community_id': community_object['id'],
                     'community': community_object['community'],
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
    # Get all of the form data.
    community_id = request.POST.get('community_id', '')
    community = request.POST.get('community', '')
    name = request.POST.get('name', '')
    motto = request.POST.get('motto', '')
    # The logo needs special handling. If the path isn't passed in in the post, we'll look to see if it's a new file.
    if request.POST.get('logo', 'nothing') == 'nothing':
        # Try to grab the new file, and if it isn't there, just make it blank.
        try:
            logo = request.FILES.get('logo')
            logo_path = 'some/file/area/' + logo.name  # TODO: Need to get the right path in here.
            destination = open(logo_path, 'wb+')
            for chunk in logo.chunks():
                destination.write(chunk)
            destination.close()
        except Exception as e:
            logo_path = ''
            log.warning('Error uploading logo: {0}'.format(e))
    else:
        # If the path was passed in, just use that.
        logo_path = request.POST.get('logo', '')
    facilitator = request.POST.get('facilitator', '')
    private = request.POST.get('private', 0)
    # These all have multiple values, so we'll use the get_post_array function to grab all the values.
    courses = get_post_array(request.POST, 'course')
    resource_names = get_post_array(request.POST, 'resource_name')
    resource_links = get_post_array(request.POST, 'resource_link')
    resource_logos_existing = get_post_array(request.POST, 'resource_logo')
    resource_logos_new = get_post_array(request.FILES, 'resource_logo')

    # If this is a new community, create a new entry, otherwise, load from the DB.
    if community_id == 'new':
        community_object = CommunityCommunities()
    else:
        community_object = CommunityCommunities.objects.get(id=community_id)

    # Set all the community values and save to the DB.
    community_object.community = community
    community_object.name = name
    community_object.motto = motto
    community_object.logo = logo_path
    community_object.private = int(private)
    community_object.save()

    # Load the main user object for the facilitator user.
    user_object = False
    try:
        user_object = User.objects.get(email=facilitator)
    except Exception as e:
        log.warning('Invalid email for facilitator: {0}'.format(e))

    # As long as the object loaded correctly, make sure this user is set as the facilitator.
    if user_object:
        # First we need to make sure if there is already a facilitator set, we unset them.
        try:
            old_facilitator = CommunityUsers.objects.get(facilitator=True)
            old_facilitator.facilitator = True
            old_facilitator.save()
        except:
            pass
        # Now we try to load the new user in case they are already a member.
        try:
            community_user = CommunityUsers.objects.get(user=user_object, community=community_object)
        # If they aren't a member already, create a new entry.
        except:
            community_user = CommunityUsers()
            community_user.community = community_object
            community_user.user = user_object
        # Set the facilitator flag to true.
        community_user.facilitator = True

    # Drop all of the courses before adding those in the form. Otherwise there is a lot of expensive checking.
    CommunityCourses.objects.filter(community=community_object).delete()
    # Go through the courses and add them to the DB.
    for course in courses:
        course_object = CommunityCourses()
        course_object.community = community_object
        course_object.course = course
        course_object.save()

    # Drop all of the resources before adding those  in the form. Otherwise there is a lot of expensive checking.
    CommunityResources.objects.filter(community=community_object).delete()
    # Go through the resource links, with the index so we can directly access the names and logos.
    for idx, resource_link in enumerate(resource_links):
        resource_object = CommunityResources()
        resource_object.community = community_object
        resource_object.link = resource_link
        resource_object.name = resource_names[idx]
        # The logo needs special handling since we might need to upload the file. First we try the entry in the FILES
        # and try to upload it.
        try:
            resource_logo = resource_logos_new[idx]
            logo_path = 'some/file/area/' + resource_logo.name
            destination = open(logo_path, 'wb+')
            for chunk in resource_logo.chunks():
                destination.write(chunk)
            destination.close()
            resource_object.logo = logo_path
        except:
            # If that didn't work, we look to see if the path was passed in.
            try:
                resource_object.logo = resource_logos_existing[idx]
            except:
                # If it wasn't, we set it to nothing.
                resource_object.logo = ''
        resource_object.save()


