from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link
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

from mako.template import Template
import mitxmako

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

    # send_html_mail("aaa",
    #                "bbb",
    #                settings.SUPPORT_EMAIL, ['mailfcl@126.com'])

    
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
        do_import_user(task, rl, request)
        
        return HttpResponse(json.dumps({'success': True,'taskId':task.id}))
    else:
        return HttpResponse('')

USER_CSV_COLS=('email','state_name','district_name',)

def random_mark(length):
    assert(length>0)
    return "".join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890@#$%^&*_+{};~',length))

def user_import_progress(request):
    try:
        task=ImportTask.objects.get(id=request.POST.get('taskId'))
        j=json.dumps({'task':task.filename,'percent':'%.2f' % ((float(task.process_lines)/float(task.total_lines)) * 100)})
    except Exception as e:
        j=json.dumps({'task':'no', 'percent':100})
    return HttpResponse(j, content_type="application/json")

def render_from_string(template_string, dictionary, context=None, namespace='main'):
    context_instance = Context(dictionary)
    # add dictionary to context_instance
    context_instance.update(dictionary or {})
    # collapse context_instance to a single dictionary for mako
    context_dictionary = {}
    context_instance['settings'] = settings
    context_instance['MITX_ROOT_URL'] = settings.MITX_ROOT_URL
    context_instance['marketing_link'] = marketing_link

    # In various testing contexts, there might not be a current request context.
    if mitxmako.middleware.requestcontext is not None:
        for d in mitxmako.middleware.requestcontext:
            context_dictionary.update(d)
    for d in context_instance:
        context_dictionary.update(d)
    if context:
        context_dictionary.update(context)
    # fetch and render template
    raw_template = Template(template_string)
    return raw_template.render_unicode(**context_dictionary)

@postpone
def do_import_user(task,csv_lines,request):
    gevent.sleep(0)

    # district_id=request.POST.get("district")
    # school_id=request.POST.get("school")

    #** import into district
    # district=District.objects.get(id=district_id)
    
    send_registration_email=request.POST.get('send_registration_email')=='true'

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
    
    for i,line in enumerate(csv_lines):
        #** record csv lines process
        task.process_lines=i+1
        task.save()
        db.transaction.commit()

        tasklog=ImportTaskLog()

        email=line[USER_CSV_COLS.index('email')]
        state_name=line[USER_CSV_COLS.index('state_name')]
        district_name=line[USER_CSV_COLS.index('district_name')]

        #** generating origin username
        username=random_mark(20)
            
        tasklog.username=username
        tasklog.email=email
        tasklog.create_date=datetime.datetime.now(UTC)
        tasklog.district_name=district_name
        tasklog.line=i+1
        tasklog.task=task
              
        try:
            validate_user_cvs_line(line)

            district=District.objects.get(state__name=state_name,name=district_name)

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
            # if school_id:
            #     profile.school=School.objects.get(id=school_id)
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

                    use_custom = request.POST.get("customize_email")
                    if use_custom == 'true':
                        custom_email = request.POST.get("custom_email")
                        custom_email_subject = request.POST.get("custom_email_subject")
                        subject = render_from_string(custom_email_subject, props)
                        body = render_from_string(custom_email, props)
                    else:
                        subject = render_to_string('emails/activation_email_subject.txt', props)
                        body = render_to_string('emails/activation_email.txt', props)

                    subject = ''.join(subject.splitlines())

                    send_html_mail(subject, body, settings.SUPPORT_EMAIL, ['mailfcl@126.com',request.user.email,email])
                except Exception as e:
                    raise Exception("Faild to send registration email %s" % e)
            
        except Exception as e:
            db.transaction.rollback()
            tasklog.error="%s" % e
            log.debug("import error: %s" % e)

        finally:
            count_success=count_success+1
            task.success_lines=count_success
            task.save()
            tasklog.save()
            db.transaction.commit()

    #** post process
    tasklogs=ImportTaskLog.objects.filter(task=task)
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
                 "district":d.district_name,
                 "create_date":d.create_date,
                 "error":d.error
                 }
            writer.writerow(row)
        output.seek(0)
        attachs=[{'filename':'log.csv','minetype':'text/csv','data':output.read()}]
        send_html_mail("User Data Import Report",
                       "Report of importing %s, see attachment." % task.filename,
                       settings.SUPPORT_EMAIL, ['mailfcl@126.com',request.user.email], attachs)
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
    r=list()
    data=State.objects.all()
    data=data.order_by("name")        
    for item in data:
        r.append({"id":item.id,"name":item.name})        
    return HttpResponse(json.dumps(r))

def drop_districts(request):
    r=list()
    if request.GET.get('state'):
        data=District.objects.all()
        data=data.filter(state=request.GET.get('state'))
        data=data.order_by("name")        
        for item in data:
            r.append({"id":item.id,"name":item.name,"code":item.code})        
    return HttpResponse(json.dumps(r))

def drop_schools(request):
    r=list()
    if request.GET.get('district'):
        data=School.objects.all()
        data=data.filter(district=request.GET.get('district'))
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
    pagingInfo={'page':data.number,'pages':data.paginator.num_pages,'total':data.paginator.count}

    for p in data:
        date=p.activate_date.strftime('%b-%d-%y %H:%M:%S') if p.activate_date else ''

        rows.append({'id':p.user.id
                     ,'user__email':p.user.email
                     ,'user__first_name':p.user.first_name
                     ,'user__last_name':p.user.last_name
                     ,'district':p.district.name
                     ,'activate_date':date
                     ,"subscription_status":p.subscription_status})

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
def registration_send_email(request):
    ids=[]
    if request.POST.get('ids'):
        ids=[int(s) for s in request.POST.get('ids').split(',') if s.isdigit()]
    else:
        data=UserProfile.objects.all()
        if request.POST.get('state',None):
            data=data.filter(district__state_id=request.POST.get('state'))

        if request.POST.get('district',None):
            data=data.filter(district_id=request.POST.get('district'))

        if request.POST.get('school',None):
            data=data.filter(school_id=request.POST.get('school'))            
        
        ids=data.values_list('user_id',flat=True)

    task=EmailTask()
    task.total_emails=len(ids)
    task.save()
    
    do_send_registration_email(task,ids,request)
    return HttpResponse(json.dumps({'success': True,'taskId':task.id}),content_type="application/json")    

@postpone
def do_send_registration_email(task,user_ids,request):
    gevent.sleep(0)

    count_success=0
    for user_id in user_ids:
        tasklog=EmailTaskLog()
        tasklog.task=task
        tasklog.send_date=datetime.datetime.now(UTC)
        try:
            user=User.objects.get(id=user_id)
            tasklog.username=user.username
            tasklog.email=user.email
            tasklog.district_name=user.profile.district.name
            
            reg = Registration.objects.get(user=user)
            props = {'key': reg.activation_key, 'district': user.profile.district.name}

            use_custom = request.POST.get("customize_email")
            if use_custom == 'true':
                custom_email = request.POST.get("custom_email")
                custom_email_subject = request.POST.get("custom_email_subject")
                subject = render_from_string(custom_email_subject, props)
                body = render_from_string(custom_email, props)
            else:
                subject = render_to_string('emails/activation_email_subject.txt', props)
                body = render_to_string('emails/activation_email.txt', props)
            
            subject = ''.join(subject.splitlines())
            
            send_html_mail(subject, body, settings.SUPPORT_EMAIL, ['mailfcl@126.com',user.email])
        except Exception as e:
            db.transaction.rollback()
            tasklog.error="%s" % e
        finally:
            count_success=count_success+1
            task.success_emails=count_success
            task.save()
            tasklog.save()
            db.transaction.commit()

    #** post process
    tasklogs=EmailTaskLog.objects.filter(task=task)
    if len(tasklogs):
        FIELDS = ["username", "email", "district", "send_date", "error"]
        TITLES = ["Username", "Email", "District", "Send Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row={
                 "username":d.username,
                 "email":d.email,
                 "district":d.district_name,
                 "send_date":d.send_date,
                 "error":d.error
                 }
            writer.writerow(row)
        output.seek(0)
        attachs=[{'filename':'log.csv','minetype':'text/csv','data':output.read()}]
        send_html_mail("Sending Registration Email Report",
                       "Report of sending registration email, see attachment.",
                       settings.SUPPORT_EMAIL, ['mailfcl@126.com',request.user.email], attachs)
        output.close()

def registration_email_progress(request):
    try:
        task=EmailTask.objects.get(id=request.POST.get('taskId'))
        j=json.dumps({'percent':'%.2f' % ((float(task.process_lines)/float(task.total_lines)) * 100)})
    except Exception as e:
        j=json.dumps({'percent':100})
    return HttpResponse(j, content_type="application/json")    

def registration_invite_count(request):
    data=UserProfile.objects.all().select_related('User')

    if request.POST.get('state',None):
        data=data.filter(Q(district__state_id=request.POST.get('state')))
        
    if request.POST.get('district',None):
        data=data.filter(Q(district_id=request.POST.get('district')))
        
    if request.POST.get('school',None):
        data=data.filter(Q(school_id=request.POST.get('school')))
            
    count=data.filter(subscription_status='Imported').count()
    return HttpResponse(json.dumps({'success': True,'count':count}), content_type="application/json")    
