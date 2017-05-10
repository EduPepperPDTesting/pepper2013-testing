from courseware.courses import get_course_by_id
from mitxmako.shortcuts import render_to_response, render_to_string, reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django_future.csrf import ensure_csrf_cookie
import json
import re
import logging
import datetime
from django.core.mail import send_mail
from courseware.courses import get_courses, course_image_url, get_course_about_section
from .utils import is_facilitator
from .models import CommunityComments, CommunityPostsImages, CommunityCommunities, CommunityLikes, CommunityCourses, CommunityResources, CommunityUsers, CommunityDiscussions, CommunityDiscussionReplies, CommunityPosts
# from .models import CommunityPostTops
from administration.pepconn import get_post_array
from operator import itemgetter
from student.models import User, People
from file_uploader.models import FileUploads
from student.models import UserProfile, Registration, CourseEnrollmentAllowed, State, District
from django.db.models import Q
from people.views import get_pager
from view_counter.models import view_counter_store
from polls.models import poll_store
from polls.views import poll_data
from notification import send_notification
# from student.views import course_from_id
from courseware.courses import get_course_by_id
from xmodule.remindstore import myactivitystore

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
    columns = {0: ['user__email', '__icontains', 'str'],
               1: ['user__username', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['user__last_name', '__iexact', 'str'],
               4: ['user__profile__district__state__name', '__iexact', 'str'],
               5: ['user__profile__district__name', '__iexact', 'str'],
               6: ['user__profile__cohort__code', '__icontains', 'str'],
               7: ['user__profile__school__name', '__icontains', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 8)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    if filters.get('8'):
        filters['all'] = filters['8']
        del filters['8']
    
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

    members = CommunityUsers.objects.filter(community=community_id).values_list('user_id', flat=True)

    users = users.exclude(user__in=members)
    users = users.exclude(activate_date__isnull=True)

    if not request.user.is_superuser:
        users = users.filter(user__profile__district=request.user.profile.district)

    # Add the row data to the list of rows.
    rows = list()
    count = users.count()
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
        row.append(str(user_cohort))
        row.append(str(user_school))

        row.append('<input class="select_box" type="checkbox" name="id" value="' + str(item.user.id) + '"/>')

        rows.append(row)

    # The number of results is the first value in the return JSON
    json_out = [count]

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
    columns = {0: ['user__email', '__icontains', 'str'],
               1: ['user__username', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['user__last_name', '__iexact', 'str'],
               4: ['user__profile__district__state__name', '__iexact', 'str'],
               5: ['user__profile__district__name', '__iexact', 'str'],
               6: ['user__profile__cohort__code', '__icontains', 'str'],
               7: ['user__profile__school__name', '__icontains', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 8)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size - 1

    if filters.get('8'):
        filters['all'] = filters['8']
        del filters['8']
    
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
        row.append(str(user_cohort))
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
    domain_name = request.META['HTTP_HOST']
    community = CommunityCommunities.objects.get(id=community_id)
    manage = request.POST.get("manage", "")
    users = []
    for user_id in request.POST.get("user_ids", "").split(","):
        if not user_id.isdigit():
            continue
        try:
            user = User.objects.get(id=int(user_id))
            users.append(user)
            mems = CommunityUsers.objects.filter(user=user, community=community)
            if not mems.exists():
                cu = CommunityUsers()
                cu.user = user
                cu.community = community
                cu.save()
                
                if manage == "1":
                    ma_db = myactivitystore()
                    my_activity = {"GroupType": "Community", "EventType": "community_registration_User", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": user.id, 
                    "URLValues": {"community_id": community.id},
                    "TokenValues": {"community_id":community.id}, 
                    "LogoValues": {"community_id": community.id}}    
                    ma_db.insert_item(my_activity)                    
                else:
                    ma_db = myactivitystore()
                    my_activity = {"GroupType": "Community", "EventType": "community_addMe", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
                    "URLValues": {"community_id": community.id},
                    "TokenValues": {"community_id":community.id}, 
                    "LogoValues": {"community_id": community.id}}
                    ma_db.insert_item(my_activity)

        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type="application/json")

    if manage == "1":
        ma_db = myactivitystore()
        my_activity = {"GroupType": "Community", "EventType": "community_registration_Admin", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
        "URLValues": {"community_id": community.id},
        "TokenValues": {"community_id":community.id, "user_ids": request.POST.get("user_ids", "")}, 
        "LogoValues": {"community_id": community.id}}
        ma_db.insert_item(my_activity)

    send_notification(request.user, community.id, members_add=users, domain_name=domain_name)
        
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required
def community_leave(request, community_id):
    domain_name = request.META['HTTP_HOST']
    community = CommunityCommunities.objects.get(id=community_id)
    users = []
    for user_id in request.POST.get("user_ids", "").split(","):
        if not user_id.isdigit():
            continue
        try:
            user = User.objects.get(id=int(user_id))
            users.append(user)
            mems = CommunityUsers.objects.filter(user=user, community=community)
            mems.delete()
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type="application/json")
    send_notification(request.user, community.id, members_del=users, domain_name=domain_name)
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def get_trending(community_id):
    views_connect = view_counter_store()
    trending_views = views_connect.get_most_viewed('discussion', 5, {'community': str(community_id)})
    trending = list()
    c = CommunityCommunities.objects.get(id=community_id)
    posts = CommunityPosts.objects.filter(community=c).order_by('-date_update')[0:5]
    for tv in trending_views:
        trending.append(CommunityDiscussions.objects.get(id=tv['identifier']))
    for post in posts:
        trending.append(post)
    trending = list(trending)
    trending = sorted(trending, key=lambda x: x.date_create, reverse=True)
    trending = trending[0:5]
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
def discussion_edit(request):
    discussion = CommunityDiscussions.objects.get(id=request.POST.get('id'))
    discussion.post = request.POST.get('post')
    discussion.subject = request.POST.get('subject')
    discussion.save()
    data = {'Success': True}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def reply_edit(request):
    reply = CommunityDiscussionReplies.objects.get(id=request.POST.get('id'))
    reply.subject = request.POST.get('subject')
    reply.post = request.POST.get('post')
    reply.save()
    data = {'Success': True}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def discussion(request, discussion_id):
    try:
        discussion = CommunityDiscussions.objects.select_related().get(id=discussion_id)
    except CommunityDiscussions.DoesNotExist:
        data = {'error_title': 'Discussion Removed',
                'error_message': 'The discussion has been removed.',
                'contact_info':  'Please contact Pepper Support for any questions at <a href="mailto:PepperSupport@pcgus.com">PepperSupport@pcgus.com</a>.',
                'window_title': 'Discussion Removed'}
        return render_to_response('error.html', data)

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
    domain_name = request.META['HTTP_HOST']
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

        rs = myactivitystore()
        my_activity = {"GroupType": "Community", "EventType": "community_creatediscussion", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
        "URLValues": {"discussion_id": discussion.id},
        "TokenValues": {"discussion_id":discussion.id, "community_id": community.id}, 
        "LogoValues": {"discussion_id": discussion.id, "community_id": community.id}}
        rs.insert_item(my_activity)

        discussion_id = discussion.id
        send_notification(request.user, community.id, discussions_new=[discussion], domain_name=domain_name)
    except Exception as e:
        error = e
        success = False
        discussion_id = None
    return HttpResponse(json.dumps({'Success': success, 'DiscussionID': discussion_id, 'Error': 'Error: {0}'.format(error)}), content_type='application/json')


@login_required
@ensure_csrf_cookie
def discussion_reply(request, discussion_id):
    domain_name = request.META['HTTP_HOST']
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

    rs = myactivitystore()
    my_activity = {"GroupType": "Community", "EventType": "community_replydiscussion", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
    "URLValues": {"discussion_id": discussion.id},
    "TokenValues": {"discussion_id":discussion.id, "reply_id": reply.id, "community_id": discussion.community.id}, 
    "LogoValues": {"discussion_id": discussion.id, "community_id": discussion.community.id}}
    rs.insert_item(my_activity)
    
    send_notification(request.user, discussion.community.id, discussions_reply=[reply], domain_name=domain_name)
    discussion.date_reply = reply.date_create
    discussion.save()
    return redirect(reverse('community_discussion_view', kwargs={'discussion_id': discussion_id}))


@login_required()
def discussion_delete(request, discussion_id):
    domain_name = request.META['HTTP_HOST']
    discussion = CommunityDiscussions.objects.get(id=discussion_id)
    did = discussion.id
    dname = discussion.subject
    cid = discussion.community.id

    redirect_url = reverse('community_view', args=[discussion.community.id])
    # try:
    view_connect = view_counter_store()
    view_connect.delete_item('discussion', discussion_id)

    poll_connect = poll_store()
    if poll_connect.poll_exists('discussion', discussion_id):
        poll_connect.delete_poll('discussion', discussion_id)

    discussion.delete()
    
    ma_db = myactivitystore()                
    ma_db.set_item_community_discussion(cid, did, dname)

    send_notification(request.user, discussion.community_id, discussions_delete=[discussion], domain_name=domain_name)
    # except Exception as e:
    #     log.warning('There was an error deleting a discussion: {0}'.format(e))

    return redirect(redirect_url)


@login_required()
def discussion_reply_delete(request, reply_id):
    domain_name = request.META['HTTP_HOST']
    reply = CommunityDiscussionReplies.objects.get(id=reply_id)
    redirect_url = reverse('community_discussion_view', args=[reply.discussion.id])
    try:
        reply.delete()
        send_notification(request.user, reply.discussion.community_id, replies_delete=[reply], domain_name=domain_name)
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
        community = CommunityCommunities.objects.get(id=community_id)
        cid = community.id
        cname = community.name

        discussions = CommunityDiscussions.objects.filter(community=community)
        ma_db = myactivitystore()                
        ma_db.set_item_community(cid, cname, discussions)
        
        community.delete()

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
                     'state': '',
                     'district': '',
                     'hangout': '',
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
                     'state': community_object.state.id if community_object.state else '',
                     'district': community_object.district.id if community_object.district else '',
                     'hangout': community_object.hangout if community_object.hangout else '',
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
        domain_name = request.META['HTTP_HOST']
        community_id = request.POST.get('community_id', '')
        name = request.POST.get('name', '')
        motto = request.POST.get('motto', '')
        hangout = request.POST.get('hangout', '')
        try:
            district_id = request.POST.get('district-dropdown', False)
            if district_id:
                district = District.objects.get(id=int(district_id))
            else:
                district = None
        except:
            district = None
        try:
            state_id = request.POST.get('state-dropdown', False)
            if state_id:
                state = State.objects.get(id=int(state_id))
            else:
                state = None
        except:
            state = None
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
        priority_id = request.POST.get('priority_id',0)
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
        community_object.district = district
        community_object.state = state
        community_object.discussion_priority = int(priority_id)
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
            if old_facilitator:
                if old_facilitator[0].user_id != community_user.user_id:
                    ma_db = myactivitystore()
                    my_activity = {"GroupType": "Community", "EventType": "community_facilitator", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": community_user.user_id, 
                    "URLValues": {"community_id": community_object.id},
                    "TokenValues": {"community_id":community_object.id}, 
                    "LogoValues": {"community_id": community_object.id}}    
                    ma_db.insert_item(my_activity)
            else:
                ma_db = myactivitystore()
                my_activity = {"GroupType": "Community", "EventType": "community_facilitator", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": community_user.user_id, 
                "URLValues": {"community_id": community_object.id},
                "TokenValues": {"community_id":community_object.id}, 
                "LogoValues": {"community_id": community_object.id}}    
                ma_db.insert_item(my_activity)
        else:
            raise Exception('A valid facilitator is required to create a community.')

        # Init lists for notification
        courses_add = []
        courses_cur = dict((x.course, get_course_by_id(x.course)) for x in CommunityCourses.objects.filter(community=community_object))
        resources_add = []
        resources_cur = dict((x.link, x) for x in CommunityResources.objects.filter(community=community_object))

        # Drop all of the courses before adding those in the form. Otherwise there is a lot of expensive checking.
        CommunityCourses.objects.filter(community=community_object).delete()
        # Go through the courses and add them to the DB.
        for key, course in courses.iteritems():
            # We only want to save an entry if there's something in it.
            if course:

                # Assign properties
                course_object = CommunityCourses()
                course_object.community = community_object
                course_object.course = course
                course_object.save()

                # Record notification about modify courses
                if courses_cur.get(course):
                    del courses_cur[course]
                else:
                    courses_add.append(get_course_by_id(course_object.course))

        # Drop all of the resources before adding those  in the form. Otherwise there is a lot of expensive checking.
        CommunityResources.objects.filter(community=community_object).delete()
        # Go through the resource links, with the index so we can directly access the names and logos.
        for key, resource_link in resource_links.iteritems():
            # We only want to save an entry if there's something in it.
            if resource_link:

                # Assign properties
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

                # Record notification about modify resources
                if resources_cur.get(resource_link):
                    del resources_cur[resource_link]
                else:
                    resources_add.append(resource_object)

        send_notification(request.user,
                          community_object.id,
                          courses_add=courses_add,
                          courses_del=courses_cur.values(),
                          resources_add=resources_add,
                          resources_del=resources_cur.values(),
                          domain_name=domain_name)

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


def community_in_district(community_id, user_id_val):
    try:
        user_val = UserProfile.objects.get(user__id=user_id_val)
        district = user_val.district
        if CommunityCommunities.objects.filter(id=community_id, district=district).exists():
            return True
        else:
            return False
    except:
        return False


def community_in_state(community_id, user_id_val):
    try:
        user_val = UserProfile.objects.get(user__id=user_id_val)
        state_id = user_val.district.state
        if CommunityCommunities.objects.filter(id=community_id, state=state_id).exists():
            return True
        else:
            return False
    except:
        return False

def user_in_community(community_id, user_id):
    try:
        user_val = User.objects.get(id=user_id)
        community_val = CommunityCommunities.objects.get(id=community_id)
        if CommunityUsers.objects.filter(user=user_val, community=community_val).exists():
            return True
        else:
            return False
    except:
        return False


def get_full_likes(request):
    comment_id = request.POST.get('comment')
    post_id = request.POST.get('post')
    html = "<table>"
    if comment_id != '':
        likes = CommunityLikes.objects.filter(comment__id=comment_id)
    else:
        likes = CommunityLikes.objects.filter(post__id=post_id)
    for like in likes:
        html += " <tr><td><img src='"+reverse('user_photo', args=[like.user.id])+"' width='24px'></img></td><td>"+like.user.first_name + " " + like.user.last_name + "</td></tr>"
    html += "</table>"
    return HttpResponse(json.dumps({'Success': 'True', 'html': html}), content_type='application/json')


def delete_comment(request):
    domain_name = request.META['HTTP_HOST']
    community_id = request.POST.get('community_id')
    cid = request.POST.get("comment_id")
    comment = CommunityComments.objects.get(id=cid)
    comment.delete()
    send_notification(request.user, community_id, posts_reply_delete=[comment], domain_name=domain_name)
    return HttpResponse(json.dumps({"Success": "True"}), content_type='application/json')


def delete_post(request):
    domain_name = request.META['HTTP_HOST']
    community_id = request.POST.get('community_id')
    pid = request.POST.get("post_id")
    post = CommunityPosts.objects.get(id=pid)
    post.delete()
    send_notification(request.user, community_id, posts_delete=[post], domain_name=domain_name)
    return HttpResponse(json.dumps({"Success": "True"}), content_type='application/json')


def email_expert(request):
    sub = request.POST.get('subject')
    message = request.POST.get('message')
    to = request.POST.get('facilitator')
    result=""
    try:
        send_mail(sub, message, request.user.email, [to], fail_silently=False)
        result="Mail sent successfully!"
    except:
        result="There was a problem sending the message."
    return HttpResponse(json.dumps({'Subject': sub, 'Message': message, 'result':result,'to':to}), content_type='application/json')


def get_discussions(request):
    id = 0
    size = request.POST.get('size')
    c = CommunityCommunities.objects.get(id=request.POST.get('community_id'))
    html = ""
    total = int(CommunityDiscussions.objects.filter(community=c).count())
    if total >= int(size):
        all = "NO"
    elif total == 0:
        all = "DONE"
    else:
        all = "DONE"
    discussions = CommunityDiscussions.objects.filter(community=c).order_by('-date_create')[0:size]
    views_connect = view_counter_store()
    for disc in discussions:
        views_object = views_connect.get_item('discussion', str(disc.id))
        if views_object is None:
            views = 0
        else:
            views = views_object['views']

        html += "<div class = 'discussion'><img class='discussion-avatar' src ='" + reverse('user_photo', args=[disc.user_id]) + "'>"
        re = int(CommunityDiscussionReplies.objects.filter(discussion=disc).count())
        html += "<div class = 'discussion-stats'><span>Replies: "+str(re)+"</span><span>Views: "+str(views)+"</span>"
        html += "</div><h2><a href='"+reverse('community_discussion_view', args=[disc.id])+"'>" + disc.subject + "</a></h2>"
        html += "<div class='discussion-post-info'><div class='discussion-byline'><span>Posted By: </span>"+disc.user.first_name + " " + disc.user.last_name + "</div>"
        html += "<div class='discussion-date'><span> On: </span>" + '{dt:%b}. {dt.day}, {dt.year}'.format(dt=disc.date_create) + "</div>"
        html += "</div><div class='community-clear'></div></div>"
    return HttpResponse(json.dumps({'id':id, 'Success': 'True', 'all':all, 'content': html, 'community': request.POST.get('community_id')}), content_type='application/json')


def get_posts(request):
    id = 0
    size=request.POST.get('size')
    c = CommunityCommunities.objects.get(id=request.POST.get('community_id'))
    html = ""
    extra_data = ""
    total = int(CommunityPosts.objects.filter(community=c).count())
    if total >= int(size):
        all = "NO"
        extra_data += str(CommunityPosts.objects.filter(community=c).count()) + " ||| " + str(size)
    elif total == 0:
        all="DONE"
        extra_data += "No Posts"
    else:
        all = "DONE"
        extra_data += str(CommunityPosts.objects.filter(community=c).count()) + " ||| " + str(size)
    # @author:scott
    # @date:2017-02-27
    # tops = CommunityPostTops.objects.filter(user__id=request.user.id, comment=None)
    filter = request.POST.get('filter')
    if filter == "newest_post":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', '-date_create')[0:size]
    elif filter == "oldest_post":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', 'date_create')[0:size]
    elif filter == "latest_reply":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', '-date_update')[0:size]
    elif filter == "oldest_reply":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', 'date_update')[0:size]
    elif filter == "alphabetical":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', 'user__last_name')[0:size]
    elif filter == "reversealpha":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', '-user__last_name')[0:size]
    elif filter == "alphauname":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', 'user__username')[0:size]
    elif filter == "ralphauname":
        posts = CommunityPosts.objects.filter(community=c).order_by('-top', '-user__username')[0:size]
    #@end
    usr_img=reverse('user_photo', args=[request.user.id])
    for post in posts:
        img = reverse('user_photo', args=[post.user.id])
        active = active_recent(post.user)
        id=post.user.first_name
        comments = CommunityComments.objects.filter(post=post)
        likes = CommunityLikes.objects.filter(post=post, comment=None)
        # top = CommunityPostTops.objects.filter(post=post, user=request.user, comment=None)
        user_like = len(CommunityLikes.objects.filter(post=post, user__id=request.user.id))
        html+="<tr class='post-content-row' id='post_content_new_row_"+str(post.id)+"'><td class='post-content-left'>"
        if active and not (request.user == post.user):
            html+="<img src='/static/images/online-3.png' class='smallcircle'></img>"
            if post.user.profile.skype_username:
                skype_username = post.user.profile.skype_username
            else:
                skype_username = "Not Set."
            html+="<img src='"+img+"' class='post-profile-image hoverable-profile' data-skype='"+skype_username+"' data-name='"+post.user.first_name+" "+post.user.last_name+"' data-uname='"+post.user.username+"' data-email='"+post.user.email+"' data-id='"+str(post.user.id)+"'></img></td><td class='post-content-right'>"
        else:
           html+="<img src='"+img+"' class='post-profile-image hoverable-profile' data-name='"+post.user.first_name+" "+post.user.last_name+"' data-uname='"+post.user.username+"' data-email='"+post.user.email+"' data-id='"+str(post.user.id)+"'></img></td><td class='post-content-right'>"
        if request.user.id == post.user.id or request.user.is_superuser or is_facilitator(request.user, c):
            delete_code = "<img src='../static/images/trash-small.png' data-postid='"+str(post.id)+"' class='delete-something'></img>"
        else:
            delete_code = ""
        # @author:scott
        # @date:2017-02-27
        if request.user.is_superuser or is_facilitator(request.user, c):
            if (post.top == 1):
                top_code = "<img src='/static/images/post_pinned.png' top='True' data-postid='"+str(post.id)+"' class='top-something'></img>"
            else:
                top_code = "<img src='/static/images/post_unpin.png' top='False' data-postid='"+str(post.id)+"' class='top-something'></img>"
        else:
            top_code = ""
        html+="<a style='font-size:12px; font-weight:bold;' href='/dashboard/"+str(post.user.id)+"' class='post-name-link'>"+post.user.first_name+" "+post.user.last_name+"</a>"+delete_code+top_code+"<br>"
        #@end
        if len(likes) > 0:
            like_text="<a class='like-members-anchor' data-post='"+str(post.id)+"' data-comment=''><img src='/static/images/like.png' class='like-button-image'></img>"
            if user_like == 1:
                like_text += "You, "
            if len(likes) > 2:
                for like in likes[:2]:
                    if like.user.username != request.user.username:
                        like_text += like.user.username+", "
                if len(likes) == 3 and user_like == 1:
                    like_text = like_text[:-2]
                else:
                    like_text += " and " + str(len(likes)-2) + "more."
            else:
                for like in likes:
                    if like.user.username != request.user.username:
                        like_text += like.user.username + ", "
                like_text = like_text[:-2]
            like_text += "</a>"
        else:
            like_text = ""
        images = CommunityPostsImages.objects.filter(post=post)
        img_code = ""
        for img in images:
            if "youtube" in img.link and img.embed:
                img_code += "<br><br><iframe src='"+img.link.replace('watch?v=', 'embed/')+"' width='384' height='216' allowfullscreen></iframe>"
            elif "youtu.be" in img.link and img.embed:
                img_code += "<br><br><iframe src='"+img.link.replace('youtu.be', 'youtube.com/embed/')+"' width='384' height='216' allowfullscreen></iframe>"
            elif "youtube" in img.link or "youtu.be" in img.link:
                img_code += "<p><a style='word-wrap:break-word;' href='"+img.link+"'>"+img.link+"</a></p>"
            elif img.embed:
                img_code += "<span class='img-span-code'><img src='" + img.link + "' style='max-width:400px;max-height:400px;'></img></span>"
            else:
                img_code += "<p><a style='word-wrap: break-word;' href='" + img.link + "'>" + img.link + "</a></p>"
        if user_like == 1:
            html+="<div id='post_textarea' class='post-textarea'>"+filter_at(post.post)+img_code+"</div><a data-id='"+str(post.id)+"' class='post-like-text'><img src='/static/images/unlike.png' class='like-button-image'></img>Unlike</a>"
        else:
            html+="<div id='post_textarea' class='post-textarea'>"+filter_at(post.post)+img_code+"</div><a data-id='"+str(post.id)+"' class='post-like-text'><img src='/static/images/like.png' class='like-button-image'></img>Like</a>"
        html+="<a data-id='"+str(post.id)+"' data-name='' class='post-comment-text'><img src='/static/images/comment.png' class='comment-image'></img>Comment</a>"
        html+="<a data-id='"+str(post.id)+"' data-type='post' data-community='"+str(post.community.id)+"' data-content='"+post.post+"' data-poster='"+post.user.first_name+" "+post.user.last_name+"' class='post-share-text'><img src='/static/images/share.png' class='share-image'></img>Share</a>"+like_text+"<br><div class='comment-section'>"
        for comment in comments:
            active = active_recent(comment.user)
            try:
                c_likes = CommunityLikes.objects.filter(comment=comment)
            except Exception as e:
                c_likes = dict()
            c_user_like = len(CommunityLikes.objects.filter(comment=comment, user__id=request.user.id))
            comment_img = reverse('user_photo', args=[comment.user.id])
            c_like_html=""
            html+="<table><tr><td>"
            if c_user_like == 1:
                c_like_html+="<a data-id='"+str(comment.id)+"' class='comment-like-text'><img src='/static/images/unlike.png' class='like-button-image'></img>Unlike</a>"
            else:
                c_like_html+="<a data-id='"+str(comment.id)+"' class='comment-like-text'><img src='/static/images/like.png' class='like-button-image'></img>Like</a>"
            if len(c_likes) > 0:
                like_text="<a class='like-members-anchor comment-like-anchor' data-post='' data-comment='"+str(comment.id)+"'><img src='/static/images/like.png' class='like-button-image'></img>"
                if c_user_like == 1:
                    like_text += "You, "
                if len(c_likes) > 2:
                    for like in c_likes[:2]:
                        if like.user.username != request.user.username:
                            like_text += like.user.username+", "
                    if len(c_likes) == 3 and c_user_like == 1:
                        like_text = like_text[:-2]
                    else:
                        like_text += " and " + str(len(c_likes)-2) + "more."
                else:
                    for like in c_likes:
                        if like.user.username != request.user.username:
                            like_text += like.user.username + ", "
                    like_text = like_text[:-2]
                like_text += "</a>"
            else:
                like_text = ""
            if active and not (request.user == post.user):
                html+="<img src='/static/images/online-3.png' class='smallcircle'></img>"
                if comment.user.profile.skype_username:
                    skype_username = comment.user.profile.skype_username
                else:
                    skype_username = "Not Set."
                html += "<a href='/dashboard/"+str(comment.user.id)+"' class='comment-anchor-text'><img class='comment-profile-image hoverable-profile' data-skype='"+skype_username+"' data-id='"+str(post.user.id)+"' data-name='"+comment.user.first_name+" "+comment.user.last_name+"' data-uname='"+comment.user.username+"' data-email='"+comment.user.email+"' src='"+comment_img+"'></img></a></td><td>"
            else:
                html += "<a href='/dashboard/"+str(comment.user.id)+"' class='comment-anchor-text'><img class='comment-profile-image hoverable-profile' data-name='"+comment.user.first_name+" "+comment.user.last_name+"' data-id='"+str(post.user.id)+"' data-uname='"+comment.user.username+"' data-email='"+comment.user.email+"' src='"+comment_img+"'></img></a></td><td>"
            if request.user.id == post.user.id or request.user.id == comment.user.id or request.user.is_superuser or is_facilitator(request.user, c):
                delete_code = "<img src='../static/images/trash-small.png' data-commentid='"+str(comment.id)+"' class='delete-something comment-delete'></img>"
            else:
                delete_code = ""
            html += "<a href='/dashboard/"+str(comment.user.id)+"' class='comment-anchor-text'>"+comment.user.first_name+" "+comment.user.last_name+"</a><span>"+filter_at(comment.comment)+"</span><br>" + c_like_html
            html += "<a data-id='"+str(post.id)+"' data-name='"+comment.user.first_name+" "+comment.user.last_name+"' class='post-comment-text'><img src='/static/images/comment.png' class='comment-image'></img>Reply</a><a data-id='"+str(post.id)+"' data-community='"+str(post.community.id)+"' data-type='comment' data-content='"+comment.comment+"' data-poster='"+post.user.first_name+" "+post.user.last_name+"' class='post-share-text'><img src='/static/images/share.png' class='share-image'></img>Share</a>"+delete_code+like_text+"</td></tr></table>"
        html+="<img src='"+usr_img+"' class='comment-profile-image'></img><textarea class='add-comment-text' data-id='"+str(post.id)+"' placeholder='Add a comment...' id='focus"+str(post.id)+"'></textarea></div>"
        html+="</td></tr>"
    return HttpResponse(json.dumps({'data': extra_data,'id':id, 'len': len(posts), 'Success': 'True', 'all':all, 'post': html, 'community': request.POST.get('community_id')}), content_type='application/json')


def submit_new_comment(request):
    domain_name = request.META['HTTP_HOST']
    community_id = request.POST.get('community_id')
    comment = CommunityComments()
    post = CommunityPosts.objects.get(id=request.POST.get('post_id'))
    post.date_update = datetime.datetime.now()
    post.save()
    comment.post = post
    comment.user = User.objects.get(id=request.user.id)
    comment.comment = request.POST.get('content')
    comment.save()

    ma_db = myactivitystore()
    my_activity = {"GroupType": "Community", "EventType": "community_commentPost", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
    "URLValues": {"community_id": long(community_id)},
    "TokenValues": {"community_id":long(community_id), "post_id": post.id}, 
    "LogoValues": {"community_id": long(community_id)}}
    ma_db.insert_item(my_activity)

    send_notification(request.user, community_id, posts_reply=[comment], domain_name=domain_name)
    return HttpResponse(json.dumps({'Success': 'True', 'post':request.POST.get('content')}), content_type='application/json')


def submit_new_like(request):
    pid=request.POST.get('post_id')
    comment = None
    post = None
    try:
        post = CommunityPosts.objects.get(id=request.POST.get('post_id'))
    except:
        None
    try:
        comment = CommunityComments.objects.get(id=request.POST.get('comment_id'))
    except:
        None
    if post:
        found=len(CommunityLikes.objects.filter(post=post, user__id=request.POST.get('user_id')))
    else:
        found=len(CommunityLikes.objects.filter(comment=comment, user__id=request.POST.get('user_id')))
    if found == 1:
        CommunityLikes.objects.filter(post=post, comment=comment, user__id=request.user.id).delete()
        return HttpResponse(json.dumps({'Success': 'True', 'Liked':'Removed'}), content_type='application/json')
    else:
        like = CommunityLikes()
        if comment:
            like.comment = comment
        if post:
            like.post = post
        like.user = User.objects.get(id=request.user.id)
        like.save()
        return HttpResponse(json.dumps({'Success': 'True', 'Liked': str(found)}), content_type='application/json')


def check_content_priority(request):
    community = CommunityCommunities.objects.filter(id=request.POST.get('community_id'))
    return HttpResponse(json.dumps({'Success': 'True',  'result': community[0].discussion_priority}), content_type='application/json')


def submit_new_post(request):
    domain_name = request.META['HTTP_HOST']
    community_id = request.POST.get('community_id')
    post = CommunityPosts()
    content = request.POST.get('post')
    content = parse_urls(content)
    post.community = CommunityCommunities.objects.get(id=request.POST.get('community_id'))
    post.user = User.objects.get(id=request.user.id)
    post.post = content
    post.save()

    ma_db = myactivitystore()
    my_activity = {"GroupType": "Community", "EventType": "community_createPost", "ActivityDateTime": datetime.datetime.utcnow(), "UsrCre": request.user.id, 
    "URLValues": {"community_id": post.community.id},
    "TokenValues": {"community_id":post.community.id, "post_id": post.id}, 
    "LogoValues": {"community_id": post.community.id}}
    ma_db.insert_item(my_activity)   

    if request.POST.get('include_images') == "yes":
        images = request.POST.get('images').split(',')
        for image in images:
            image = image.rstrip('/')
            image = image.rstrip('\\')
            ext = image[-3:]
            if ext == "png" or ext == "jpg" or ext == "gif" or ("youtube" in image) or ("youtu.be" in image):
                img = CommunityPostsImages()
                img.post = post
                img.link = image
                img.embed = int(request.POST.get('embed'))
                img.save()
            else:
                img = CommunityPostsImages()
                img.post = post
                img.link = image
                img.embed = 0
                img.save()
    send_notification(request.user, community_id, posts_new=[post], domain_name=domain_name)
    return HttpResponse(json.dumps({'Success': 'True', 'post': request.POST.get('post'), 'community': request.POST.get('community_id')}), content_type='application/json')


def parse_urls(content):
    final = ""
    url = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    for word in content.split():
        try:
            if url.match(word):
                final += '<a href = "'+word+'">'+word+'</a> '
            else:
                final += word + " "
        except Exception as e:
            final = e
    return final


def lookup_name(request):
    name = request.POST.get("name").split()
    if len(name) > 1:
        fname = name[0]
        lname = name[1]
    else:
        fname = name[0]
        lname = ""
    users = User.objects.filter(first_name__istartswith=fname).filter(last_name__istartswith=lname)
    str = []
    for user in users:
        str.append(user.first_name + " " + user.last_name)
    return HttpResponse(json.dumps({'Success': 'True', 'content': str}), content_type='application/json')


def filter_at(content):
    at = content.find("@")
    final = content
    tests=" Tests: "
    if at >= 0:
        string = content[at:]
        while string.find("@") > -1:
            s=string[1:]
            x=s.find("@")
            try:
                if x > -1:
                    working = s[:x].split(' ')
                else:
                    working = s.split(' ')
                try:
                    working.remove('')
                except:
                    None
                working[1] = re.sub('[!.?,:)(]', '', working[1])
                try:
                    user = User.objects.filter(first_name=working[0], last_name=working[1])[0]
                    addition = "<a class='in-comment-link' target='_blank' href = '../dashboard/"+str(user.id)+"'>"+working[0]+" "+working[1]+"</a>"
                    final=final.replace("@"+working[0]+" "+working[1], addition)
                except Exception as e:
                    tests+="<br>Failed: "+str(e)
            except Exception as e:
                None
            string = s[x:]
    return final

def active_recent(user):
    use = user
    utc_month=datetime.datetime.utcnow().strftime("%m")
    utc_day=datetime.datetime.utcnow().strftime("%d")
    utc_h=datetime.datetime.utcnow().strftime("%H")
    utc_m=datetime.datetime.utcnow().strftime("%M")
    d_min = 60*int(utc_h) + int(utc_m)
    if use.profile.last_activity:
        usr=use.profile.last_activity
        u_min = 60*int(usr.strftime("%H")) + int(usr.strftime("%M"))
        close = int(d_min) - int(u_min) < 1
        active = usr.strftime("%d") == utc_day and usr.strftime("%m") == utc_month and close
    else:
        active = False
    return active


#@end
#@author:scott
# #@data:2017-02-27
def top_post(request):
    domain_name = request.META['HTTP_HOST']
    community_id = request.POST.get('community_id')
    pid = request.POST.get("post_id")
    post = CommunityPosts.objects.get(id=pid)
    top = request.POST.get('top')
    if top == 'True':
        post.top = 0
    else:
        post.top = 1
    post.save()
    return HttpResponse(json.dumps({"Success": "True"}), content_type='application/json')
#@end