from django.http import Http404
from mitxmako.shortcuts import render_to_response
from django.db import connection

from student.models import CourseEnrollment
from django.contrib.auth.models import User
import django_comment_client.utils as utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.contrib.auth.decorators import login_required
from xmodule.remindstore import chunksstore
import capa.xqueue_interface as xqueue_interface
from django.conf import settings
from datetime import datetime
from pytz import UTC
import json
from people.people_in_es import gen_people_search_query, search_people
@login_required
def mychunks(request,user_id=None):
    if user_id:
        user=User.objects.get(id=user_id)
    else:
        user = request.user
    context={
        'curr_user':user
        }     
    # template context    
    # searching
    cond=gen_people_search_query(
        sort={'last_login':'desc'},
        start=0,
        size=100,
        must_not={'_id':request.user.id,'is_superuser':1,'is_staff':1},
        must={
            'people_of':request.user.id,
            'is_active':1,
            'course':'',
            'email_lower':request.GET.get('email','').lower(),
            'username_lower':request.GET.get('username','').lower(),
            'first_name_lower':request.GET.get('first_name','').lower(),
            'last_name_lower':request.GET.get('last_name','').lower(),
            'state_id':request.GET.get('state_id',''),            
            'district_id':request.GET.get('district_id',''),
            'school_id':request.GET.get('school_id',''),
            'major_subject_area_id':request.GET.get('subject_area_id',''),
            'grade_level_id':request.GET.get('grade_level_id',''),
            'years_in_education_id':request.GET.get('years_in_education_id',''),
            'percent_lunch':request.GET.get('percent_lunch',''),
            'percent_iep':request.GET.get('percent_iep',''),
            'percent_eng_learner':request.GET.get('percent_eng_learner','')
            })

    profiles,total=search_people(cond)
    context['people_search_debug']=1
    context['profiles']=profiles
    return render_to_response("my_chunks.html",context)
    

s3_interface = {
            'access_key': getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
            'secret_access_key': getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
            'storage_bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        }

def get_mychunk(request):
    rs = chunksstore()
    info = json.loads(request.POST.get('info'))
    return_info = rs.return_vertical_item(str(request.user.id),info['vertical_id'])
    return utils.JsonResponse({'results': return_info})

def get_mychunks_range(request):
    rs = chunksstore()
    count = rs.get_total(str(request.user.id))
    info  = rs.return_items(str(request.user.id),int(request.POST.get('skip')),int(request.POST.get('limit')))
    return utils.JsonResponse({'results': info,'count': count})

def save_mychunk(request):
    rs = chunksstore()
    info = json.loads(request.POST.get('info'))
    info['user_id']=str(request.user.id)
    rs.save_item(info)
    return utils.JsonResponse({'results':'true'})

def del_mychunk(request):
    rs = chunksstore()
    info = json.loads(request.POST.get('info'))
    rs.delete_item(str(request.user.id),info['vertical_id'])
    return utils.JsonResponse({'results':'true'})

def set_rate(request):
    rs = chunksstore()
    info = json.loads(request.POST.get('info'))
    info['user_id']=str(request.user.id)
    rs.set_rate(info)
    return utils.JsonResponse({'results':'true'})

def get_integrate_rate(request):
    rs = chunksstore()
    info = json.loads(request.POST.get('info'))
    rate_results=rs.get_integrate_rate(info)
    return utils.JsonResponse(rate_results)
    
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