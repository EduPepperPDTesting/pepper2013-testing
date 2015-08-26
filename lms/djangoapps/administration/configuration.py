from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response, render_to_string
from student.models import ResourceLibrary,StaticContent
from collections import deque
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from django.contrib.auth.models import User
from student.models import UserProfile,Registration,CourseEnrollmentAllowed
from django import db
import random
import json
import time
import logging

from django import db
from models import *
from StringIO import StringIO
from student.models import Transaction,District,Cohort,School,State
from mail import send_html_mail
import datetime
from pytz import UTC
import urllib
log = logging.getLogger("tracking")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
    from django.contrib.sessions.models import Session
    return render_to_response('administration/configuration.html', {})

##############################################
# Dropdown List
##############################################
def drop_association_type(request):  
    data=CertificateAssociationType.objects.all()
    data=data.order_by("name")        
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name})
  
    return HttpResponse(json.dumps(r))

def drop_association(request):
    asociationType = CertificateAssociationType.objects.filter(Q(id=request.GET.get('association_type')))[0]
    if asociationType.name=='Author':
       data = Author.objects.all()   
    elif asociationType.name=='District':
       data = District.objects.all()
    elif asociationType.name=='School':
       data = School.objects.all()
    data = data.order_by("name")  
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name})        
    return HttpResponse(json.dumps(r))

def drop_publish_association(request):
    asociationType = CertificateAssociationType.objects.filter(Q(id=request.GET.get('association_type')))[0]
    cdata = Certificate.objects.filter(Q(association_type=request.GET.get('association_type')))
    idarr = [x.association for x in cdata]
    if asociationType.name=='Author':
       data = Author.objects.filter(~Q(id__in=idarr)) 
    elif asociationType.name=='District':
       data = District.objects.filter(~Q(id__in=idarr))
    elif asociationType.name=='School':
       data = School.objects.filter(~Q(id__in=idarr))
    data = data.order_by("name")      
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name})        
    return HttpResponse(json.dumps(r))

def drop_states(request):
    data=State.objects.all()
    data=data.order_by("name")        
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name})        
    return HttpResponse(json.dumps(r))

def drop_districts(request):
    data=District.objects.all()
    if request.GET.get('state'):
        data=data.filter(state=request.GET.get('state'))
    data=data.order_by("name")        
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name,"code":item.code})        
    return HttpResponse(json.dumps(r))

def drop_schools(request):
    data=School.objects.all()
    if request.GET.get('district'):
        data=data.filter(district=request.GET.get('district'))
    elif request.GET.get('state'):
        data=data.filter(district__state=request.GET.get('state'))
    r=list()
    data=data.order_by("name")
    for item in data:
        r.append({"id":item.id,"name":item.name})        
    return HttpResponse(json.dumps(r))

def drop_cohorts(request):
    data=Cohort.objects.all()
    if request.GET.get('district'):
        data=data.filter(district=request.GET.get('district'))
    elif request.GET.get('state'):
        data=data.filter(district__state=request.GET.get('state'))
    r=list()
    for item in data:
        r.append({"id":item.id,"code":item.code})
    return HttpResponse(json.dumps(r))

from django.core.paginator import Paginator,InvalidPage, EmptyPage

def paging(all,size,page):
    try:
        page=int(page)
    except Exception:
        page=1
    try:
        size=int(size)
    except Exception:
        size=1
    paginator = Paginator(list(all), size)
    if page<1: page=1
    if page>paginator.num_pages: page=paginator.num_pages
    data=paginator.page(page)
    return data

def certificate_table(request):
    data = Certificate.objects.all()
    #data = Certificate.objects.raw('select certificate.id,certificate.certificate_name,certificate.association_type_id,certificate.association,certificate.certificate_blob,certificate.readonly, concat(author.name,district.name,school.name) as association_name from certificate left join author ON certificate.association=author.id left join district ON certificate.association=district.id left join school ON certificate.association=school.id')
    #data = Certificate.objects.raw('select certificate.id,certificate.certificate_name,certificate.association_type_id,certificate.association,certificate.certificate_blob,certificate.readonly,certificate_association_type.name as association_type_name,t.name as association_name from certificate left join certificate_association_type on certificate.association_type_id=certificate_association_type.id left join(select 1 as ktype,id,name from author union all select 2 as ktype,id,name from district union all select 3 as ktype,id,name from school) t on certificate.association_type_id=t.ktype and certificate.association=t.id')
    if request.GET.get('association_type',None):
        data=data.filter(Q(association_type=request.GET.get('association_type')))
    if request.GET.get('certificate_name',None):
        data=data.filter(Q(certificate_name=request.GET.get('certificate_name')))
    if request.GET.get('association',None):
        data=data.filter(Q(association=request.GET.get('association')))
    
    page = request.GET.get('page')
    size = request.GET.get('size')
    data = paging(data,size,page)

    rows = []
    pagingInfo={'page':data.number,'pages':data.paginator.num_pages}

    for p in data:

        if p.association_type_id!=0:
            if p.association_type.name=="Author":
                association = Author.objects.filter(Q(id=p.association))
            elif p.association_type.name=="District":
                association = District.objects.filter(Q(id=p.association))
            elif p.association_type.name=="School":
                association = School.objects.filter(Q(id=p.association))
            association_type_name = p.association_type.name
            association_name = association[0].name     
        else:
            association_type_name = ""
            association_name = ""
        rows.append({'certificate_name':p.certificate_name
                     ,'association_type':association_type_name
                     ,'association':association_name
                     ,'id':p.id})
    return HttpResponse(json.dumps({'rows':rows,'paging':pagingInfo}))

@login_required
@user_passes_test(lambda u: u.is_superuser)    
def favorite_filter_load(request):
    favs=[]
    
    # favs=[{'id':1,'name':'Alabama','filter':{'state':1,'district':34,'school':1406}}]

    for ff in FilterFavorite.objects.filter(user=request.user).order_by('name'):
        favs.append({
            'id':ff.id
            ,'name':ff.name
            ,'filter':ff.filter_json
            })
    
    return HttpResponse(json.dumps(favs))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def favorite_filter_save(request):
    ff=FilterFavorite()
    ff.user=request.user
    ff.name=request.GET.get('name')
    ff.filter_json=request.GET.get('filter')
    ff.save()
    return HttpResponse(json.dumps({'success': True}))    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def favorite_filter_delete(request):
    FilterFavorite.objects.filter(id=request.GET.get('id')).delete()
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_registration_email(request):
    return HttpResponse(json.dumps({'success': True}))    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def certificate_delete(request):
    ids= request.POST.get('ids').split(',')
    for id in ids:
        Certificate.objects.filter(id=id).delete()
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def certificate_save(request):    
    cid = request.POST.get('id')
    readonly = request.POST.get('readonly')=='true'
    info = {'success': True,'msg':'Save complete.'}
    content = urllib.quote(request.POST.get('content').decode('utf8').encode('utf8'))
    c = Certificate.objects.filter(id=cid)
    try:
        if len(c) == 0:
            Certificate.objects.create(certificate_name=request.POST.get('name'),association_type_id=request.POST.get('association_type'),association=request.POST.get('association'),certificate_blob=content,readonly=readonly)
        else:
            uc = Certificate.objects.get(id=cid)
            uc.certificate_name = request.POST.get('name')
            uc.association_type_id = request.POST.get('association_type')
            uc.association = request.POST.get('association')
            uc.certificate_blob = request.POST.get('content')
            uc.readonly = readonly
            uc.save()
    except db.utils.IntegrityError:
        info = {'success': False,'msg':'Certificate name already exists.'}
    return HttpResponse(json.dumps(info))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def certificate_loadData(request):
    c = Certificate.objects.filter(id=request.POST.get('id'))[0]
    try:
        content = urllib.unquote(c.certificate_blob.decode('utf8').encode('utf8'))
    except:
        content = ""
    data={'certificate_name':c.certificate_name
                     ,'association_type':c.association_type_id
                     ,'association':c.association
                     ,'content':content
                     ,'readonly':c.readonly
                     ,'id':c.id
                     }
    return HttpResponse(json.dumps(data))


