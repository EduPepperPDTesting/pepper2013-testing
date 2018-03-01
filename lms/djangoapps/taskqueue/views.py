from mitxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from util.json_request import JsonResponse
import json
import requests
from django.http import HttpResponse
from django.conf import settings
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def pop_queue ():
    return "Done."