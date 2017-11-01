from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from operator import itemgetter
from django.contrib.auth.models import User
from communities.models import CommunityUsers, CommunityCommunities
from .models import CommunityWebchat, UserWebchat
from people.views import my_people
from django.contrib.auth.models import User
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import opentok

@login_required
def getvideoframe(request, uname):
    space_pos = uname.find("_")
    first_name = uname[0:space_pos]
    last_name = uname[space_pos+1:]

    return render_to_response('webchat/webvideoframe.html', {"first_name": first_name, "last_name": last_name})

@login_required
def gettextframe(request, uname):
    # user_name = []
    # get_name = uname
    # while(get_name.find("_")):
    #     space_pos = get_name.find("_")
    #     add_name = get_name[0:space_pos]
    #     user_name.extend([add_name])
    #     get_name = get_name[space_pos+1:]

    user_name = uname.replace("_", " ").replace("`", ", ")
    id_index = user_name.index(", ")
    user_id = user_name[id_index+2:]
    return render_to_response('webchat/webtextframe.html', {"user_name": user_name, "user_id": user_id})

# @login_required
# def get_all_users(request):
#     user = User.objects.get(id=request.user.id)
@login_required
def get_users_org(request):
    orgs_list = list()
    orgs_list.append('All Users')
    data = {'orgs_list': orgs_list}
    return render_to_response('webchat/listorgusers.html', data)

def get_all_ptusers(request):
    user_community = CommunityUsers.objects.select_related().filter(user=request.user)
    rows = list()
    user_ids = request.POST.getlist("user_ids[]")
    term = request.POST.get("term")
    if term:
        ids = list()

        users_firstname = User.objects.filter(first_name__icontains=term, id__in=user_ids)

        for user_item in users_firstname:
            row = list()
            row.append(str(user_item.first_name) + " " + str(user_item.last_name))
            row.append(str(user_item.id))
            row.append(checkInCommunities(request.user, user_item))

            rows.append(row)
            ids.append(user_item.id)

        users_lastname = User.objects.exclude(id__in=ids).filter(last_name__icontains=term, id__in=user_ids)

        for user_item in users_lastname:
            row = list()
            row.append(str(user_item.first_name) + " " + str(user_item.last_name))
            row.append(str(user_item.id))
            row.append('https://image.flaticon.com/icons/svg/125/125702.svg')
            row.append(checkInCommunities(request.user, user_item))

            rows.append(row)

    else:
        for user_id in user_ids:
            row = list()
            user = User.objects.get(id=int(user_id))
            if user:
                row.append(str(user.first_name) + " " + str(user.last_name))
                row.append(str(user.id))
                row.append('https://image.flaticon.com/icons/svg/125/125702.svg')
                row.append(checkInCommunities(request.user, user))

                rows.append(row)

    if not rows:
        return HttpResponse(json.dumps({'success': 0}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': 1, 'rows': rows}), content_type="application/json")

@login_required
def get_network(request):
    orgs_list = list()
    orgs_list.append('My Network')
    data = {'orgs_list': orgs_list}
    return render_to_response('webchat/listorgusers.html', data)

def get_network_users(request):
    rows = list()

    user_ids = request.POST.getlist("user_ids[]")

    for user_id in user_ids:
        row = list()
        user = User.objects.get(id=int(user_id))
        if user:
            row.append(str(user.first_name) + " " + str(user.last_name))
            row.append(str(user.id))
            row.append('https://image.flaticon.com/icons/svg/125/125702.svg')
            row.append(checkInCommunities(request.user, user))

            rows.append(row)

    if not rows:
        return HttpResponse(json.dumps({'success': 0}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': 1, 'rows': rows}), content_type="application/json")

def checkInCommunities(user, otherUser):
    other_community_list = list()
    commIcon = ''

    if not otherUser.is_superuser:
        items = CommunityUsers.objects.select_related().filter(user=otherUser, community__private=True)
        for item in items:
            other_community_list.append(item.community.id)

    if other_community_list:
        community_list = list()

        items = CommunityUsers.objects.select_related().filter(user=user, community__private=True)
        for item in items:
            community_list.append(item.community.id)

        if community_list:
            for other_community in other_community_list:
                if other_community in community_list:
                    commIcon = 'https://image.flaticon.com/icons/svg/33/33965.svg'
                    break

    return commIcon

@login_required
def get_communities(request):
    """
    Returns the communities page.
    :param request: Request object.
    :return: The Communities page.
    """
    community_list = list() #
    filter_dict = dict()

    # If this is a regular user, we only want to show public communities and private communities to which they belong.
    if not request.user.is_superuser:
        # Filter the normal query to only show public communities.
        filter_dict.update({'private': False})

        # Do a separate filter to grab private communities this user belongs to.
        items = CommunityUsers.objects.select_related().filter(user=request.user, community__private=True)
        for item in items: #orgs_list.append({'id': item.community.id, 'name': item.community.name})
            community_list.append({'id': item.community.id, 'name': item.community.name})

    # Query for the communities this user is allowed to see.
    items = CommunityCommunities.objects.filter(**filter_dict)
    for item in items:
        community_name = item.name
        try:
            community_name = community_name.replace("'", "~")
        except:
            pass

        community_list.append({'id': item.id, 'name': community_name})

    # Set up the data to send to the communities template, with the communities sorted by name.
    #data = {'orgs': sorted(community_list, key=itemgetter('name'))}
    data = {'orgs_list': community_list}
    return render_to_response('webchat/listorgusers.html', data)

def get_session_token(request):
    session_id = request.POST.get("session")
    api_key = "45939862"        # Replace with your OpenTok API key.
    api_secret = "d69400f3e386d0fc35ebd51cf0aaefd6aa973214"  # Replace with your OpenTok API secret.
    sdk = opentok.OpenTok (api_key, api_secret)
    connectionMetadata = "username="+request.user.username+",userLevel=4"
    token = sdk.generate_token (session_id)
    return HttpResponse (json.dumps({'token':token}), content_type="application/json")

def get_community_session(request):
    community = CommunityWebchat.objects.filter(community__id=request.POST.get('community_id'))
    if not community:
        api_key = "45939862"        # Replace with your OpenTok API key.
        api_secret = "d69400f3e386d0fc35ebd51cf0aaefd6aa973214"  # Replace with your OpenTok API secret.
        opentok_sdk = opentok.OpenTok (api_key, api_secret)
        sid = opentok_sdk.create_session()
        comm = CommunityWebchat()
        ref = CommunityCommunities.objects.get (id=request.POST.get('community_id'))
        comm.community = ref
        comm.session_id = sid.session_id
        comm.save()
        return HttpResponse(json.dumps({'session': sid.session_id}), content_type="application/json")
    else:
        ref = CommunityCommunities.objects.get(id=request.POST.get('community_id'))
        comm = CommunityWebchat.objects.get(community=ref)
        return HttpResponse (json.dumps({'session': comm.session_id}), content_type="application/json")


def get_user_session(request):
    user = UserWebchat.objects.filter(user__id=request.POST.get('user_id'))
    if not user:
        api_key = "45939862"        # Replace with your OpenTok API key.
        api_secret = "d69400f3e386d0fc35ebd51cf0aaefd6aa973214"  # Replace with your OpenTok API secret.
        opentok_sdk = opentok.OpenTok (api_key, api_secret)
        sid = opentok_sdk.create_session()
        use = UserWebchat()
        ref = User.objects.get (id=request.POST.get('user_id'))
        use.user = ref
        use.session_id = sid.session_id
        use.save()
        return HttpResponse(json.dumps({'session': sid.session_id}), content_type="application/json")
    else:
        ref = User.objects.get(id=request.POST.get('user_id'))
        use = UserWebchat.objects.get(user=ref)
        return HttpResponse (json.dumps({'session': use.session_id}), content_type="application/json")


def get_community_user_rows(request):
    """
    Builds the rows for display in the community members in webchat widget.
    :param request: User request
    :return: Table rows for the community members
    """
    community_id = request.POST.get("community_id");
    users = CommunityUsers.objects.filter(community=community_id)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    # page = int(request.GET['page'])
    # size = int(request.GET['size'])
    # start = page * size
    # end = start + size

    # # Add the row data to the list of rows.
    rows = list()

    my_network = list()
    # getMyPeople = my_people(request, checkInNetwork = 1)
    # myPeople = json.loads(getMyPeople.read())
    # raise Exception(myPeople)
    # myPeopleList = getMyPeople.replace("[{", "[").replace("}]", "]").split("}, {")
    #
    # myPeopleDict = {}
    # for item in myPeopleList:
    #     i = item.split(': ')
    #     myPeopleDict[i[0]] = i[1]
    #
    # for networkUser in MyPeopleDict:
    #     my_network.append(networkUser.user_id)

    #for item in users[start:end]:
    for item in users:
        row = list()
        row.append(str(item.user.first_name) + " " + str(item.user.last_name))
        row.append(str(item.user.id))

        if item.user.id in my_network:
            row.append('https://image.flaticon.com/icons/svg/125/125702.svg')
        else:
            row.append('https://image.flaticon.com/icons/svg/125/125702.svg')

        row.append(checkInCommunities(request.user, item.user))
        rows.append(row)

    if not rows:
        return HttpResponse(json.dumps({'success': 0}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': 1, 'rows': rows}), content_type="application/json")

def webchat_search(request):
    user = list()
    user = get_network_users(request, 1)

