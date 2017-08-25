from mitxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
# from communities.models import CommunityUsers

@login_required
def getvideoframe(request, uname):
    space_pos = uname.find("_")
    first_name = uname[0:space_pos]
    last_name = uname[space_pos+1:]

    return render_to_response('webchat/webvideoframe.html', {"first_name": first_name, "last_name": last_name})

@login_required
def gettextframe(request, uname):
    space_pos = uname.find("_")
    first_name = uname[0:space_pos]
    last_name = uname[space_pos+1:]

    return render_to_response('webchat/webtextframe.html', {"first_name": first_name, "last_name": last_name})