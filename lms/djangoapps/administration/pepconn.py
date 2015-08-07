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
import csv

import multiprocessing
from multiprocessing import Process,Queue,Pipe
from django.core.validators import validate_email, validate_slug, ValidationError

import gevent
from django import db
from models import *
from StringIO import StringIO
from student.models import Transaction,District,Cohort,School,State
from mail import send_html_mail
import datetime
from pytz import UTC

log = logging.getLogger("tracking")

from gevent import monkey

def postpone(function):
    def decorator(*args, **kwargs):
        p = Process(target = function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()
    return decorator

@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
    from django.contrib.sessions.models import Session
    return render_to_response('administration/pepconn.html', {})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user_submit(request):
    # monkey.patch_all(socket=False)
    
    if request.method == 'POST':
        district_id=request.POST.get("district")
        school_id=request.POST.get("school")

        # output_pipe,input_pipe=multiprocessing.Pipe()
        # request.session['task']=''

        #** readlines from csv
        file=request.FILES.get('file')
        r=csv.reader(file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        rl = []
        rl.extend(r)

        #** create task
        task=ImportTask()
        task.filename=file.name
        # task.total_lines=100
        task.total_lines=len(rl);
        task.save()
        db.transaction.commit()

        #** close connection before import
        # http://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
        from django.db import connection 
        connection.close()

        #** begin import
        do_import_user(task.id, rl, request)
        
        return HttpResponse(json.dumps({'success': True,'taskId':task.id}))
    else:
        return HttpResponse('')

USER_CSV_COLS=('email',)

def random_mark(length):
    assert(length>0)
    return "".join(random.sample('abcdefg&#%^*1234567890',length))

def task_status(request):
    task=ImportTask.objects.get(id=request.POST.get('taskId'))
    
    if task:
        j=json.dumps({'task':task.filename,'precent':'%.2f' % ((float(task.process_lines)/float(task.total_lines)) * 100)}) #output_pipe.recv()
    else:
        j=json.dumps({'task':'no'})
    return HttpResponse(j)

@postpone
def do_import_user(taskid,csv_lines,request):
    gevent.sleep(0)

    district_id=request.POST.get("district")
    school_id=request.POST.get("school")
    send_registration_email=request.POST.get('send_registration_email')=='true'
    task=ImportTask.objects.get(id=taskid);

    #** ==================== testing 
    # curr=""
    # process=0

    # while 1:
    #     now=time.strftime("%Y-%m-%d %X", time.localtime())
    #     if now!=curr:
    #         process=process+1

    #         task.filename=now
    #         task.process_lines=process
    #         task.save()
    #         db.transaction.commit()
            
    #         log.debug(now)
    #         curr=now
    
    #** ==================== importing
    count_success=0
 
    #** import into district
    district=District.objects.get(id=district_id)
    for i,line in enumerate(csv_lines):
        #** record csv lines process
        task.process_lines=i+1
        task.save()
        db.transaction.commit()

        tasklog=ImportTaskLog()

        email=line[USER_CSV_COLS.index('email')]

        #** generating origin username
        username=random_mark(20)
            
        tasklog.username=username
        tasklog.email=email
        tasklog.create_date=datetime.datetime.now(UTC)
        tasklog.district=district
        tasklog.line=i+1
        tasklog.import_task=task
              
        try:
            validate_user_cvs_line(line)

            #** user
            user = User(username=username, email=email, is_active=False)
            user.set_password(username)
            user.save()

            #** registration
            registration = Registration()
            registration.register(user)

            #** profile
            profile=UserProfile(user=user)
            profile.district=district
            profile.subscription_status="Imported"
            if school_id:
                profile.school=School.objects.get(id=school_id)
            profile.save()

            #** course enroll
            cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
            cea.is_active = True
            cea.auto_enroll = True
            cea.save()

            #** send activation email if required
            if send_registration_email:
                try:
                    reg = Registration.objects.get(user=user)
                    props = {'key': reg.activation_key, 'district': district.name}
                    subject = render_to_string('emails/activation_email_subject.txt', props)
                    subject = ''.join(subject.splitlines())
                    body = render_to_string('emails/activation_email.txt', props)
                    send_html_mail(subject, body, settings.SUPPORT_EMAIL, ['mailfcl@126.com','gingerj@education2000.com',request.user.email,email])
                except Exception as e:
                    raise Exception("Faild to send registration email")
                
            #** count success
            count_success=count_success+1
            task.success_lines=count_success
            task.save()

            tasklog.save()
                            
            db.transaction.commit()
        except Exception as e:
            db.transaction.rollback()

            tasklog.error="%s" % e
            tasklog.save()
            
            db.transaction.commit()
            
            log.debug("import error: %s" % e)

    #** post process
    tasklogs=ImportTaskLog.objects.filter(import_task=task)
    if len(tasklogs):
        FIELDS = ["line", "username", "email", "district", "create_date", "error"]
        TITLES = ["Line", "Username", "Email", "District", "Create Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row={"line":d.line,
                 "username":d.username,
                 "email":d.email,
                 "district":d.district.name,
                 "create_date":d.create_date,
                 "error":d.error
                 }
            writer.writerow(row)
        output.seek(0)
        attachs=[{'filename':'log.csv','minetype':'text/csv','data':output.read()}]
        send_html_mail("User Data Import Report",
                       "Report of importing %s, see attachment." % task.filename,
                       settings.SUPPORT_EMAIL, ['mailfcl@126.com','gingerj@education2000.com',request.user.email], attachs)
        output.close()

def validate_user_cvs_line(line):
    #** check field count
    n=0
    for item in line:
        if len(item.strip()):
            n=n+1
    if n != len(USER_CSV_COLS):
        raise Exception("Wrong fields count")

    #** email
    email=line[USER_CSV_COLS.index('email')]
    validate_email(email)

    #** check user exists
    if len(User.objects.filter(email=email)) > 0:
        raise Exception("An account with the Email '{email}' already exists".format(email=email))


##############################################
# Dropdown List
##############################################

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
    paginator = Paginator(all, size)
    if page<1: page=1
    if page>paginator.num_pages: page=paginator.num_pages
    data=paginator.page(page)
    return data

def registration_table(request):
    data=UserProfile.objects.all().select_related('User')

    if request.GET.get('state',None):
        data=data.filter(Q(district__state_id=request.GET.get('state')))
        
    if request.GET.get('district',None):
        data=data.filter(Q(district_id=request.GET.get('district')))
        
    if request.GET.get('school',None):
        data=data.filter(Q(school_id=request.GET.get('school')))

    if request.GET.get('sortField',None):
        if request.GET.get('sortOrder')=='desc':
            data=data.order_by("-"+request.GET.get('sortField'))
        else:
            data=data.order_by(request.GET.get('sortField'))
    
    page=request.GET.get('page')
    size=request.GET.get('size')
    data=paging(data,size,page)

    rows=[]
    pagingInfo={'page':data.number,'pages':data.paginator.num_pages}

    for p in data:
        date=p.activate_date.strftime('%b-%d-%y %H:%M:%S') if p.activate_date else ''

        rows.append({'id':p.user.id
                     ,'user__email':p.user.email
                     ,'user__first_name':p.user.first_name
                     ,'user__last_name':p.user.last_name
                     ,'district':p.district.name
                     ,'activate_date':date})

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
    

