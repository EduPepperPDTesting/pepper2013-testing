from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from student.models import ResourceLibrary,StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required

def import_user(request):
    return render_to_response('configuration/import_user.html', {})
