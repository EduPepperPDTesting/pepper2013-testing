from django.http import Http404
from mitxmako.shortcuts import render_to_response
from django.db import connection

from student.models import CourseEnrollment
from django.contrib.auth.models import User
import django_comment_client.utils as utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.contrib.auth.decorators import login_required
from xmodule.remindstore import remindstore, messagestore
import capa.xqueue_interface as xqueue_interface
from django.conf import settings
from datetime import datetime
from pytz import UTC
import json

@login_required
def notifications(request,user_id=None):
    if user_id:
        user=User.objects.get(id=user_id)
    else:
        user = request.user
    context={
        'curr_user':user
        }     

    return render_to_response("notifications.html",context)
    
def get_interactive_update(request):
    rs = remindstore()
    count = rs.items_count(str(request.user.id))
    info  = rs.return_items(str(request.user.id))
    return utils.JsonResponse({'results': info,'count': count})

def get_interactive_update_range(request):
    rs = remindstore()
    count = rs.get_total(str(request.user.id))
    info  = rs.return_items(str(request.user.id),int(request.POST.get('skip')),int(request.POST.get('limit')))
    return utils.JsonResponse({'results': info,'count': count})

def save_interactive_update(request):
    rs = remindstore()
    info = json.loads(request.POST.get('info'))
    info['date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    user_id = str(info['user_id']).split(',')
    if len(user_id)>1:
        for v in user_id:
            singleInfo = info.copy()
            singleInfo['user_id'] = v
            rs.insert_item(singleInfo)
    else:
        rs.insert_item(info)
    return utils.JsonResponse({'results':'true'})

def set_interactive_update(request):
    rs = remindstore()
    #info = rs.set_item(request.POST.get('_id'),request.POST.get('_name'),request.POST.get('_value'))
    info = rs.set_item(request.POST.get('_id'),request.POST.get('_name'),request.POST.get('_value'),request.POST.get('_user_id'),request.POST.get('_record_id'))
    return utils.JsonResponse({})

s3_interface = {
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
            'secret_access_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
            'storage_bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        }

def get_message(request):
    rs = messagestore()
    count = rs.get_total(str(request.user.id),str(request.POST.get('message_people')))
    info  = rs.return_items(str(request.user.id),str(request.POST.get('message_people')),int(request.POST.get('skip')),int(request.POST.get('limit')))
    return utils.JsonResponse({'results': info,'count': count})

def save_message(request):
    rs = messagestore()
    info = json.loads(request.POST.get('info'))
    info['date']=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    rs.insert_item(info)
    return utils.JsonResponse({'results':'true'})

def upload_image(request):
    success = True
    try:
        fd = request.FILES.get("image_file",None)
        index=fd.name.rfind(".")
        extensions_name=fd.name[index+1:] 
        main_name=fd.name[0:index] 
        #fname = fd.name.split(".")
        file_key = main_name +"_"+datetime.now(UTC).strftime(
            xqueue_interface.dateformat
        )+"."+extensions_name

        fd.seek(0)
        s3_public_url = upload_to_s3(
            fd, file_key, s3_interface
        )
    except Exception:
        success = False
    return utils.JsonResponse({'success':success,'file_info': s3_public_url})

def upload_to_s3(file_to_upload, keyname, s3_interface):

    conn = S3Connection(s3_interface['access_key'], s3_interface['secret_access_key'])
    bucketname = str(s3_interface['storage_bucket_name'])
    bucket = conn.create_bucket(bucketname.lower())

    k = Key(bucket)
    k.key = 'message_board/'+keyname
    k.set_metadata('filename', file_to_upload.name)
    k.set_contents_from_file(file_to_upload)

    k.set_acl("public-read")
    public_url = k.generate_url(60 * 60 * 24 * 1825) # URL timeout in seconds.

    return public_url