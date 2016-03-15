from mitxmako.shortcuts import render_to_response, render_to_string, reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django_future.csrf import ensure_csrf_cookie
import json
import logging
from courseware.courses import get_courses, course_image_url, get_course_about_section
from .utils import is_facilitator
from .models import CommunityCommunities, CommunityCourses, CommunityResources, CommunityUsers, CommunityDiscussions, CommunityDiscussionReplies
from administration.pepconn import get_post_array
from operator import itemgetter
from student.models import User
from file_uploader.models import FileUploads
from student.models import UserProfile, Registration, CourseEnrollmentAllowed
from django.db.models import Q
from people.views import get_pager
from view_counter.models import view_counter_store
from polls.models import poll_store
from polls.views import poll_data

log = logging.getLogger("tracking")


def index(request):
    return render_to_response('communities/communities.html', {})


def community_ppd(request):
    return render_to_response('communities/community_ppd.html', {})


def community_ngss(request):
    return render_to_response('communities/community_ngss.html', {})


@login_required
def community_manage_member(request, community_id):
    community = CommunityCommunities.objects.get(id=community_id)
    return render_to_response('communities/manage_members.html', {"community": community})


def build_sorts(columns, sorts):
    """
    Builds the sorts for the PepConn report data
    :param columns: the columns in this table
    :param sorts: the sorts requested
    :return: the arguments to pass to order_by()
    """
    order = list()
    # Iterate through the passed sorts.
    for column, sort in sorts.iteritems():
        # Default to an ASC search, but if the sort is 1, change it to DESC by adding a -.
        pre = ''
        if bool(int(sort)):
            pre = '-'
        # We just need the column selector out of the columns, not the type.
        order.append(pre + columns[int(column)][0])
    return order


def build_filters(columns, filters):
    """
    Builds the filters for the PepConn report data
    :param columns: the columns in this table
    :param filters: the filters requested
    :return: the arguments to pass to filter()
    """
    kwargs = dict()
    args = None
    # Iterate through the filters.
    for column, value in filters.iteritems():
        # For the numerical columns, just filter that column by the passed value.
        if not column == 'all':
            c = int(column)
            # If the column is an integer value, convert the search term.
            out_value = value
            if columns[c][2] == 'int' and value.isdigit():
                out_value = int(value)
            # Build the actual kwargs to pass to filer(). in this case, we need the column selector ([0]) as well as the
            # type of selection to make ([1] - '__iexact').
            kwargs[columns[c][0] + columns[c][1]] = out_value
        # If this is a search for all, we need to do an OR search, so we build one with Q objects.
        else:
            args_list = list()
            for key, data in columns.iteritems():
                # [2] holds the column type (int, str, or False to ignore).
                if data[2]:
                    # If the column is an integer value, convert the search term (as long as the string is only digits).
                    out_value = value
                    if data[2] == 'int':
                        if value.isdigit():
                            out_value = int(value)
                        else:
                            out_value = None
                    if out_value is not None:
                        # Create the Q object and add it to the list.
                        args_list.append(Q(**{data[0] + data[1]: out_value}))
            # Start the list with the first object, then add the rest with ORs.
            args = args_list.pop()
            for item in args_list:
                args |= item

    return args, kwargs


@login_required
def get_add_user_rows(request, community_id):
    """
    Builds the rows for display in the PepConn Users report.
    :param request: User request
    :return: Table rows for the user table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['user__id', '', 'int'],
               1: ['user__last_name', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['user__profile__school__name', '__iexact', 'str'],
               4: ['user__profile__district__name', '__iexact', 'str'],
               5: ['user__profile__district__state__name', '__iexact', 'str'],
               6: ['user__profile__cohort__code', '__icontains', 'str'],
               7: ['user__email', '__icontains', 'str'],
               8: ['user__profile__subscription_status', '__iexact', 'str'],
               10: ['user__date_joined', '__icontains', False]}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 11)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size - 1

    if filters.get('11'):
        filters['all'] = filters['11']
        del filters['11']
    
    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        args, kwargs = build_filters(columns, filters)
        # If there was a search for all, add the Q arguments.
        if args:
            users = UserProfile.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            users = UserProfile.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        users = UserProfile.objects.prefetch_related().all().order_by(*order)

    members = CommunityUsers.objects.filter(community=community_id).values_list('user_id')
    users = users.exclude(user__in=members)
    
    # The number of results is the first value in the return JSON
    count = users.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in users[start:end]:
        row = list()

        row.append(str(item.user.email))

        row.append(str(item.user.username))
        row.append(str(item.user.first_name))
        row.append(str(item.user.last_name))

        try:
            user_school = item.user.profile.school.name
        except:
            user_school = ""
        try:
            user_district = str(item.user.profile.district.name)
            user_district_state = str(item.user.profile.district.state.name)
        except:
            user_district = ""
            user_district_state = ""
        try:
            user_cohort = str(item.user.profile.cohort.code)
        except:
            user_cohort = ""

        row.append(str(user_district_state))
        row.append(str(user_district))
        # row.append(str(user_cohort))
        row.append(str(user_school))

        # row.append(str(item.user.profile.subscription_status))
        # try:
        #     activation_key = str(Registration.objects.get(user_id=item.user_id).activation_key)
        # except:
        #     activation_key = ''
            
        # row.append(str(item.user.date_joined))
        row.append('<input class="select_box" type="checkbox" name="id" value="' + str(item.user.id) + '"/>')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")

@login_required
def get_remove_user_rows(request, community_id):
    """
    Builds the rows for display in the PepConn Users report.
    :param request: User request
    :return: Table rows for the user table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['user__id', '', 'int'],
               1: ['user__last_name', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['user__profile__school__name', '__iexact', 'str'],
               4: ['user__profile__district__name', '__iexact', 'str'],
               5: ['user__profile__district__state__name', '__iexact', 'str'],
               6: ['user__profile__cohort__code', '__icontains', 'str'],
               7: ['user__email', '__icontains', 'str'],
               8: ['user__profile__subscription_status', '__iexact', 'str'],
               10: ['user__date_joined', '__icontains', False]}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 11)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size - 1

    if filters.get('11'):
        filters['all'] = filters['11']
        del filters['11']
    
    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        args, kwargs = build_filters(columns, filters)
        # If there was a search for all, add the Q arguments.
        if args:
            users = CommunityUsers.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            users = CommunityUsers.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        users = CommunityUsers.objects.prefetch_related().all().order_by(*order)

    users = users.filter(community=community_id)
    
    # The number of results is the first value in the return JSON
    count = users.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in users[start:end]:
        row = list()

        row.append(str(item.user.email))

        row.append(str(item.user.username))
        row.append(str(item.user.first_name))
        row.append(str(item.user.last_name))

        try:
            user_school = item.user.profile.school.name
        except:
            user_school = ""
        try:
            user_district = str(item.user.profile.district.name)
            user_district_state = str(item.user.profile.district.state.name)
        except:
            user_district = ""
            user_district_state = ""
        try:
            user_cohort = str(item.user.profile.cohort.code)
        except:
            user_cohort = ""

        row.append(str(user_district_state))
        row.append(str(user_district))
        # row.append(str(user_cohort))
        row.append(str(user_school))

        # row.append(str(item.user.profile.subscription_status))
        # try:
        #     activation_key = str(Registration.objects.get(user_id=item.user_id).activation_key)
        # except:
        #     activation_key = ''
            
        # row.append(str(item.user.date_joined))
        row.append('<input class="select_box" type="checkbox" name="id" value="' + str(item.user.id) + '"/>')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")


@login_required
def community_join(request, community_id):
    community = CommunityCommunities.objects.get(id=community_id)

    for user_id in request.POST.get("user_ids", "").split(","):
        if not user_id.isdigit():
            continue
        try:
            user = User.objects.get(id=int(user_id))
            mems = CommunityUsers.objects.filter(user=user, community=community)
            if not mems.exists():
                cu = CommunityUsers()
                cu.user = user
                cu.community = community
                cu.save()
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type="application/json")
        
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required
def community_leave(request, community_id):
    community = CommunityCommunities.objects.get(id=community_id)
    
    for user_id in request.POST.get("user_ids", "").split(","):
        if not user_id.isdigit():
            continue
        try:
            user = User.objects.get(id=int(user_id))
            mems = CommunityUsers.objects.filter(user=user, community=community)
            mems.delete()
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type="application/json")
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def get_trending(community_id):
    views_connect = view_counter_store()
    trending_views = views_connect.get_most_viewed('discussion', 5, {'community': str(community_id)})
    trending = list()
    for tv in trending_views:
        trending.append(CommunityDiscussions.objects.get(id=tv['identifier']))
    return trending


@login_required
def community(request, community_id):
    """
    Returns a single community page.
    :param request: Request object.
    :param community_id: The machine name of the community.
    :return: The Community page.
    """
    views_connect = view_counter_store()
    page = request.GET.get('page', '')
    if page.isdigit() and int(page) > 0:
        page = int(page)
    else:
        page = 1
    start = (page - 1) * 5

    community = CommunityCommunities.objects.get(id=community_id)
    facilitator = CommunityUsers.objects.select_related().filter(facilitator=True, community=community)
    users = CommunityUsers.objects.filter(community=community)
    discussions = CommunityDiscussions.objects.filter(community=community).order_by('-date_reply')[start:start + 5]
    total = CommunityDiscussions.objects.filter(community=community).count()
    # mems = CommunityUsers.objects.select_related().filter(user=request.user, community=community)
    resources = CommunityResources.objects.filter(community=community)
    courses = CommunityCourses.objects.filter(community=community)
    
    for d in discussions:
        d.replies = CommunityDiscussionReplies.objects.filter(discussion=d).count()
        views = views_connect.get_item('discussion', str(d.id))
        if views is None:
            d.views = 0
        else:
            d.views = views['views']

    trending = get_trending(community_id)

    data = {"community": community,
            "facilitator": facilitator[0] if len(facilitator) else None,
            "discussions": discussions,
            "trending": trending,
            "users": users,
            "resources": resources,
            "courses": courses,
            # "mem": mems[0] if mems.count() else None,
            "pager": get_pager(total, 5, page, 5),
            "total_discussions": total}
    
    return render_to_response('communities/community.html', data)


@login_required
def discussion_list(request, community_id):
    try:
        page = int(request.GET.get('page'))
        start = (page - 1) * 5
        community = CommunityCommunities.objects.get(id=community_id)
        discussions = CommunityDiscussions.objects.filter(community=community).order_by('-date_reply')[start:start + 5]
        total = CommunityDiscussions.objects.filter(community=community).count()
        views_connect = view_counter_store()

        data = {'pager': get_pager(total, 5, page, 5), 'discussions': list()}
        for discussion in discussions:
            views_object = views_connect.get_item('discussion', str(discussion.id))
            if views_object is None:
                views = 0
            else:
                views = views_object['views']
            data['discussions'].append({'url': reverse('community_discussion_view', args=[discussion.id]),
                                        'subject': discussion.subject,
                                        'replies': CommunityDiscussionReplies.objects.filter(discussion=discussion).count(),
                                        'views': views,
                                        'date_create': '{dt:%b}. {dt.day}, {dt.year}'.format(dt=discussion.date_create),
                                        'first_name': discussion.user.first_name,
                                        'last_name': discussion.user.last_name,
                                        'avatar': reverse('user_photo', args=[discussion.user.id])
                                        })
    except Exception as e:
        data = {'Error': e}

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def discussion(request, discussion_id):
    discussion = CommunityDiscussions.objects.select_related().get(id=discussion_id)
    replies = CommunityDiscussionReplies.objects.select_related().filter(discussion=discussion_id)
    total = CommunityDiscussions.objects.filter(community=discussion.community).count()
    users = CommunityUsers.objects.filter(community=discussion.community).count()
    mems = CommunityUsers.objects.select_related().filter(user=request.user, community=discussion.community)

    views_connect = view_counter_store()
    views_connect.set_item('discussion', discussion_id, 1, {'community': str(discussion.community.id)})

    poll_connect = poll_store()
    has_poll = poll_connect.poll_exists('discussion', discussion_id)

    trending = get_trending(discussion.community.id)

    data = {'discussion': discussion,
            'replies': replies,
            'community': discussion.community,
            'has_poll': has_poll,
            'total_discussions': total,
            'total_users': users,
            'trending': trending,
            'mem': mems[0] if mems.count() else None}

    if has_poll:
        data.update({'poll': poll_data('discussion', discussion_id, request.user.id)})

    return render_to_response('communities/discussion.html', data)


@login_required
@ensure_csrf_cookie
def discussion_add(request):
    error = ''

    try:
        community = CommunityCommunities.objects.get(id=request.POST.get('community_id'))
        discussion = CommunityDiscussions()
        discussion.community = community
        discussion.user = request.user
        discussion.post = request.POST.get('post')
        discussion.subject = request.POST.get('subject')
        discussion.save()
        if request.FILES.get('attachment') is not None and request.FILES.get('attachment').size:
            try:
                attachment = FileUploads()
                attachment.type = 'discussion_attachment'
                attachment.sub_type = discussion.id
                attachment.upload = request.FILES.get('attachment')
                attachment.save()
            except:
                attachment = None
        else:
            attachment = None
        if attachment:
            discussion.attachment = attachment
            discussion.save()
        success = True
        discussion_id = discussion.id
    except Exception as e:
        error = e
        success = False
        discussion_id = None
    return HttpResponse(json.dumps({'Success': success, 'DiscussionID': discussion_id, 'Error': 'Error: {0}'.format(error)}), content_type='application/json')


@login_required
@ensure_csrf_cookie
def discussion_reply(request, discussion_id):
    discussion = CommunityDiscussions.objects.get(id=discussion_id)
    reply = CommunityDiscussionReplies()
    reply.discussion = discussion
    reply.user = request.user
    reply.post = request.POST.get('post')
    reply.subject = request.POST.get('subject')
    if request.FILES.get('attachment') is not None and request.FILES.get('attachment').size:
        try:
            attachment = FileUploads()
            attachment.type = 'discussion_attachment'
            attachment.sub_type = discussion_id
            attachment.upload = request.FILES.get('attachment')
            attachment.save()
        except:
            attachment = None
    else:
        attachment = None
    if attachment:
        reply.attachment = attachment
    reply.save()
    discussion.date_reply = reply.date_create
    discussion.save()
    return redirect(reverse('community_discussion_view', kwargs={'discussion_id': discussion_id}))


@login_required()
def discussion_delete(request, discussion_id):
    discussion = CommunityDiscussions.objects.get(id=discussion_id)
    redirect_url = reverse('community_view', args=[discussion.community.id])
    # try:
    view_connect = view_counter_store()
    view_connect.delete_item('discussion', discussion_id)

    poll_connect = poll_store()
    if poll_connect.poll_exists('discussion', discussion_id):
        poll_connect.delete_poll('discussion', discussion_id)

    discussion.delete()
    # except Exception as e:
    #     log.warning('There was an error deleting a discussion: {0}'.format(e))

    return redirect(redirect_url)


@login_required()
def discussion_reply_delete(request, reply_id):
    reply = CommunityDiscussionReplies.objects.get(id=reply_id)
    redirect_url = reverse('community_discussion_view', args=[reply.discussion.id])
    try:
        reply.delete()
    except Exception as e:
        log.warning('There was an error deleting a reply: {0}'.format(e))

    return redirect(redirect_url)


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
            community_list.append({'id': item.community.id,
                                   'name': item.community.name,
                                   'logo': item.community.logo.upload.url if item.community.logo else '',
                                   'private': item.community.private})
    # Query for the communities this user is allowed to see.
    items = CommunityCommunities.objects.filter(**filter_dict)
    for item in items:
        community_list.append({'id': item.id,
                               'name': item.name,
                               'logo': item.logo.upload.url if item.logo else '',
                               'private': item.private})

    # Set up the data to send to the communities template, with the communities sorted by name.
    data = {'communities': sorted(community_list, key=itemgetter('name'))}
    return render_to_response('communities/communities.html', data)


@login_required
def community_delete(request, community_id):
    try:
        CommunityCommunities.objects.get(id=community_id).delete()
        return redirect(reverse('communities'))
    except Exception as e:
        data = {'error_title': 'Problem Deleting Community',
                'error_message': 'Error: {0}'.format(e),
                'window_title': 'Problem Deleting Community'}
        return render_to_response('error.html', data)



@login_required
def community_edit(request, community_id='new'):
    """
    Sets up the community add/edit form.
    :param request: Request object.
    :param community_id: Which community to edit, or 'new' if adding one.
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
    if community_id == 'new' and request.user.is_superuser:
        data.update({'community_id': 'new',
                     'community': '',
                     'name': '',
                     'motto': '',
                     'logo': '',
                     'facilitator': '',
                     'private': '',
                     'courses': [''],
                     'resources': [{'name': '', 'link': '', 'logo': ''}],
                     'user_type': 'super'})
        return render_to_response('communities/community_edit.html', data)
    # If we are editing a community, make sure the user is either a superuser or facilitator for this community, and if
    # so, return a populated form for editing.
    elif community_id != 'new' and (request.user.is_superuser or is_facilitator(request.user, community_id)):
        if request.user.is_superuser:
            user_type = 'super'
        elif is_facilitator(request.user, community_id):
            user_type = 'facilitator'
        # Grab the data from the DB.
        community_object = CommunityCommunities.objects.get(id=community_id)
        courses = CommunityCourses.objects.filter(community=community_object)
        resources = CommunityResources.objects.filter(community=community_object)
        facilitator = CommunityUsers.objects.filter(community=community_object, facilitator=True)

        # Build the lists of courses and resources.
        course_list = list()
        resource_list = list()
        for course in courses:
            course_list.append(course.course)
        if not len(course_list):
            course_list.append('')
        for resource in resources:
            resource_list.append({'name': resource.name,
                                  'link': resource.link,
                                  'logo': resource.logo})
        if not len(resource_list):
            resource_list.append({'name': '', 'link': '', 'logo': ''})

        # Put together the data to send to the template.
        data.update({'community_id': community_object.id,
                     'community': community_object.id,
                     'name': community_object.name,
                     'motto': community_object.motto,
                     'logo': community_object.logo.upload.url if community_object.logo else '',
                     'facilitator': facilitator[0].user.email if len(facilitator) else None,
                     'private': community_object.private,
                     'courses': course_list,
                     'resources': resource_list,
                     'user_type': user_type})

        return render_to_response('communities/community_edit.html', data)

    # If neither of the other tests worked, the user isn't allowed to do this.
    return HttpResponseForbidden()


@login_required
@ensure_csrf_cookie
def community_edit_process(request):
    """
    Processes the form data from the community add/edit form.
    :param request: Request object.
    :return: JSON response.
    """
    try:
        # Get all of the form data.
        community_id = request.POST.get('community_id', '')
        name = request.POST.get('name', '')
        motto = request.POST.get('motto', '')
        hangout = request.POST.get('hangout', '')
        # The logo needs special handling. If the path isn't passed in the post, we'll look to see if it's a new file.
        if request.POST.get('logo', 'nothing') == 'nothing':
            # Try to grab the new file, and if it isn't there, just make it blank.
            try:
                logo = FileUploads()
                logo.type = 'community_logos'
                logo.sub_type = community_id
                logo.upload = request.FILES.get('logo')
                logo.save()
            except Exception as e:
                logo = None
                log.warning('Error uploading logo: {0}'.format(e))
        else:
            # If the path was passed in, just use that.
            logo = None
        facilitator = request.POST.get('facilitator', '')
        private = request.POST.get('private', 0)
        # These all have multiple values, so we'll use the get_post_array function to grab all the values.
        courses = get_post_array(request.POST, 'course')
        resource_names = get_post_array(request.POST, 'resource_name')
        resource_links = get_post_array(request.POST, 'resource_link')

        # If this is a new community, create a new entry, otherwise, load from the DB.
        if community_id == 'new':
            community_object = CommunityCommunities()
        else:
            community_object = CommunityCommunities.objects.get(id=community_id)

        # Set all the community values and save to the DB.
        community_object.name = name
        community_object.motto = motto
        if logo:
            community_object.logo = logo
        community_object.hangout = hangout
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
                old_facilitator = CommunityUsers.objects.filter(facilitator=True, community=community_object)
                for f in old_facilitator:
                    f.facilitator = False
                    f.save()
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
            community_user.save()
        else:
            raise Exception('A valid facilitator is required to create a community.')

        # Drop all of the courses before adding those in the form. Otherwise there is a lot of expensive checking.
        CommunityCourses.objects.filter(community=community_object).delete()
        # Go through the courses and add them to the DB.
        for key, course in courses.iteritems():
            # We only want to save an entry if there's something in it.
            if course:
                course_object = CommunityCourses()
                course_object.community = community_object
                course_object.course = course
                course_object.save()

        # Drop all of the resources before adding those  in the form. Otherwise there is a lot of expensive checking.
        CommunityResources.objects.filter(community=community_object).delete()
        # Go through the resource links, with the index so we can directly access the names and logos.
        for key, resource_link in resource_links.iteritems():
            # We only want to save an entry if there's something in it.
            if resource_link:
                resource_object = CommunityResources()
                resource_object.community = community_object
                resource_object.link = resource_link
                resource_object.name = resource_names[key]
                # The logo needs special handling since we might need to upload the file. First we try the entry in the
                # FILES and try to upload it.
                if request.POST.get('resource_logo[{0}]'.format(key)):
                    file_id = int(request.POST.get('resource_logo[{0}]'.format(key)))
                    logo = FileUploads.objects.get(id=file_id)
                else:
                    try:
                        logo = FileUploads()
                        logo.type = 'community_resource_logos'
                        logo.sub_type = community_id
                        logo.upload = request.FILES.get('resource_logo[{0}]'.format(key))
                        logo.save()
                    except Exception as e:
                        logo = None
                        log.warning('Error uploading logo: {0}'.format(e))

                if logo:
                    resource_object.logo = logo
                resource_object.save()

        return redirect(reverse('community_view', kwargs={'community_id': community_object.id}))
    except Exception as e:
        data = {'error_title': 'Problem Saving Community',
                'error_message': 'Error: {0}'.format(e),
                'window_title': 'Problem Saving Community'}
        return render_to_response('error.html', data)


@login_required
def community_check_user(request):
    try:
        User.objects.get(email=request.GET.get('email'))
        valid = True
    except:
        valid = False
    return HttpResponse(json.dumps({'Valid': valid}), content_type='application/json')
