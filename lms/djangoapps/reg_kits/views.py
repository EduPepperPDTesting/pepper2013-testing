from django.core.mail import send_mail
from mitxmako.shortcuts import render_to_response, render_to_string
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django import db
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, Http404
import student.views
import branding
import courseware.views
from mitxmako.shortcuts import marketing_link
from util.cache import cache_if_anonymous
import json
from student.models import UserProfile,Registration,CourseEnrollmentAllowed
from student.models import Transaction,District,Cohort,School,State
from django import forms
import csv
from django.core.paginator import Paginator,InvalidPage, EmptyPage
from django.db.models import Q
from django.core.validators import validate_email, validate_slug, ValidationError
from pytz import UTC
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from courseware.courses import get_courses
from xmodule.modulestore.django import modulestore
import pymongo

def valid_pager(all,size,page):
    paginator = Paginator(all, size)
    try:
        page=int(page)
    except Exception:
        page=1
    if page<1: page=1
    if page>paginator.num_pages: page=paginator.num_pages
    data=paginator.page(page)
    return data

def pager_params(request):
    b=list()
    for (n,v) in request.GET.items():
        if n != 'page':
            b.append("%s=%s" % (n,v))
    return "&".join(b)

##############################################
# DISTRICT
##############################################
@login_required
@user_passes_test(lambda u: u.is_superuser)
def district(request):
    data=District.objects.all()
    if request.GET.get('state_id'):
        data=data.filter(state_id=request.GET.get('state_id'))
    data=valid_pager(data,20,request.GET.get('page'))
    return render_to_response('reg_kits/district.html', {"districts":data,"ui":"list","pager_params":pager_params(request)})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def district_create(request):
    return render_to_response('reg_kits/district.html', {"districts":District.objects.all(),"district_from":True})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def district_modify(request,district_id=''):
    district={}
    if district_id:
        c=District.objects.get(id=district_id)
        district['id']=c.id
        district['name']=c.name
    return render_to_response('reg_kits/district.html',
                              {"districts":District.objects.all(),
                               "district":district,
                               "ui":'form'})
@ensure_csrf_cookie
@cache_if_anonymous
def district_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    state_id = request.POST['state_id']
    try:
        if request.POST.get('id'):
            d=District(request.POST['id'])
        else:
            d=District()        
        d.code=request.POST['code']
        d.name=request.POST['name']
        d.state_id=request.POST['state_id']
        d.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def district_delete(request):
    ids=request.GET.get("ids").split(",")
    message={'success': True}
    try:
        District.objects.filter(id__in=ids).delete()
        db.transaction.commit()
    except Exception as e:
        db.transaction.rollback()
        message={'success': False,'error': "%s" % e}
    return HttpResponse(json.dumps(message))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def district_form(request,district_id=None):
   if district_id:
       c=District.objects.get(id=district_id)
   else:
       c=District()
   return render_to_response('reg_kits/district.html', {"ui":"form","district":c})

##############################################
# COHORT
##############################################
@login_required
@user_passes_test(lambda u: u.is_superuser)
def cohort(request):
    data=Cohort.objects.all()
    if request.GET.get('district_id'):
        data=data.filter(district_id=request.GET.get('district_id'))
    if request.GET.get('state_id'):
        data=data.filter(Q(district__state_id=request.GET.get('state_id')))    
    data=valid_pager(data,20,request.GET.get('page'))

    for item in data:
        item.licences_exist=UserProfile.objects.filter(~Q(subscription_status = "Inactive"),cohort_id=item.id).count()
        
    return render_to_response('reg_kits/cohort.html', {"cohorts":data,"ui":"list","pager_params":pager_params(request)})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cohort_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        if request.POST.get('id'):
            d=Cohort(request.POST['id'])
        else:
            d=Cohort()
        d.id==request.POST['id']
        d.code=request.POST['code']
        d.licences=request.POST['licences']
        d.term_months=request.POST['term_months']
        d.start_date=request.POST['start_date']
        d.district_id=request.POST['district_id']
        d.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cohort_delete(request):
    ids=request.GET.get("ids").split(",")
    message={'success': True}
    try:
        Cohort.objects.filter(id__in=ids).delete()
    except Exception as e:
        db.transaction.rollback()
        message={'success': False,'error':"%s" % e}
    return HttpResponse(json.dumps(message))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cohort_form(request,cohort_id=None):
   if cohort_id:
       c=Cohort.objects.get(id=cohort_id)
   else:
       c=Cohort()
       c.term_months=12
   return render_to_response('reg_kits/cohort.html', {"ui":"form", "cohort":c, "transactions":Transaction.objects.all()})

##############################################
# SCHOOL
##############################################
def filter_school(request):
    data=School.objects.all()
    if request.GET.get('district_id'):
        data=data.filter(district_id=request.GET.get('district_id'))
    if request.GET.get('state_id'):
        data=data.filter(Q(district__state_id=request.GET.get('state_id')))
    return data

@login_required
@user_passes_test(lambda u: u.is_superuser)
def school(request):
    data=filter_school(request)
    data=valid_pager(data,20,request.GET.get('page'))
    return render_to_response('reg_kits/school.html', {"schools":data,"ui":"list","pager_params":pager_params(request)})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def school_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        if request.POST.get('id'):
            d=School(request.POST['id'])
        else:
            d=School()
        d.name=request.POST['name']
        d.code=request.POST['code']
        d.district_id=request.POST['district_id']
        d.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def school_delete(request):
    ids=request.GET.get("ids").split(",")
    message={'success': True}
    try:
        School.objects.filter(id__in=ids).delete()
        db.transaction.commit()
    except Exception as e:
        db.transaction.rollback()
        message={'success': False,'error':"%s" % e}
    return HttpResponse(json.dumps(message))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def school_form(request,school_id=None):
   if school_id:
       c=School.objects.get(id=school_id)
   else:
       c=School()
   return render_to_response('reg_kits/school.html', {"ui":"form","school":c})

##############################################
# USER
##############################################
def filter_user(request):
    data=UserProfile.objects.all() #.select_related('owner_object')

    filtered=[False]
    
    def q(k,none_as_empty=False):
        v=request.GET.get(k)
        if none_as_empty:
            empty=(v=='__NONE__')
        else:
            empty=(v=='')
        if (k in request.GET) and (not empty):
            filtered[0]=True
        if v=='__NONE__':
            v=None
        return v 
        
    if q('first_name'):
        data=data.filter(Q(user__first_name=q('first_name')))
    if q('last_name'):
        data=data.filter(Q(user__last_name=q('last_name')))
    if q('email'):
        data=data.filter(user__email=q('email'))
        
    if q('school_id',True):
        data=data.filter(school_id=q('school_id'))
    if q('district_id',True):
        data=data.filter(Q(district_id=q('district_id')))
    if q('state_id',True):
        data=data.filter(Q(district__state_id=q('state_id')))
    if q('cohort_id',True):
        data=data.filter(cohort_id=q('cohort_id'))
        
    if q('subscription_status'):
        data=data.filter(subscription_status=q('subscription_status'))
    if q('invite_days_min'):
        data=data.filter(invite_date__lte=datetime.datetime.now(UTC)-datetime.timedelta(int(q('invite_days_min'))))
    if q('invite_days_max'):
        data=data.filter(invite_date__gte=datetime.datetime.now(UTC)-datetime.timedelta(int(q('invite_days_max'))+1))
        
    # if request.GET.get('course_id'):
    #     data=data.filter(user__courseenrollment__course_id = request.GET.get('course_id'), user__courseenrollment__is_active = True)
    
    desc=""
    if request.GET.get("desc")=="yes":
        desc="-"
    if request.GET.get("sortby")=="user_id":
        data=data.order_by(desc+"user__id")
    if request.GET.get("sortby")=="active_link":
        data=data.order_by(desc+"user__registration__activation_key")           

    if request.GET.get("sortby")=="first_name":
        data=data.order_by(desc+"user__first_name")

    if request.GET.get("sortby")=="last_name":
        data=data.order_by(desc+"user__last_name")

    if request.GET.get("sortby")=="username":
        data=data.order_by(desc+"user__username")
        
    if request.GET.get("sortby")=="email":
        data=data.order_by(desc+"user__email")

    if request.GET.get("sortby")=="district":
        data=data.order_by(desc+"district__name")

    if request.GET.get("sortby")=="cohort":
        data=data.order_by(desc+"cohort__code")

    if request.GET.get("sortby")=="school":
        data=data.order_by(desc+"school__name")

    if request.GET.get("sortby")=="invite_date":
        data=data.order_by(desc+"invite_date")        
                    
    if request.GET.get("sortby")=="activate_date":
        data=data.order_by(desc+"activate_date")

    if request.GET.get("sortby")=="subscription_status":
        data=data.order_by(desc+"subscription_status")        

    return data,filtered[0]

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user(request):

    data,filtered=filter_user(request)
    invite_count=data.filter(subscription_status='Imported').count()

    size=request.GET.get('size')

    if size and size.isdigit():
        size=int(size)
    else:
        size=20
    
    data=valid_pager(data,size,request.GET.get('page'))

    for item in data:
        item.days_after_invite=''
        if(item.invite_date):
            item.days_after_invite=(datetime.datetime.now(UTC)-item.invite_date).days
            
    return render_to_response('reg_kits/user.html', {"invite_count":invite_count,
                                                     "users":data,
                                                     "ui":"list",
                                                     "pager_params":pager_params(request)})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_course_permission_csv(request):
    from StringIO import StringIO

    courses=filter_courses(request.GET.get('subject_id','all'),request.GET.get('author_id',''))

    FIELDS = ["district", "last_name", "first_name", "email"]
    TITLES = ["District", "Last Name", "First Name", "Email"]

    for c in courses:
        if not c.display_coursenumber:
            continue
        FIELDS.append(c.display_coursenumber)
        TITLES.append(c.display_coursenumber)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    
    writer.writerow(dict(zip(FIELDS, TITLES)))
    data,filtered=filter_user(request)

    if filtered:
      for d in data:
          row={
              "district":attstr(d,"district.name"),
              "last_name":attstr(d,"user.last_name"),
              "first_name":attstr(d,"user.first_name"),
              "email":attstr(d,"user.email"),       
              }
          for c in courses:
              if not c.display_coursenumber:
                  continue
              
              allow='Y' if CourseEnrollmentAllowed.objects.filter(email=d.user.email,course_id=c.id,is_active=True).exists() else 'N'
              row[c.display_coursenumber]=allow
              
          writer.writerow(row)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = datetime.datetime.now().strftime('attachment; filename=couse-permission-%Y-%m-%d-%H-%M-%S.csv')
    output.seek(0)
    response.write(output.read())
    output.close()
    return response

@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_course_permission_excel(request):
    from StringIO import StringIO
    import xlsxwriter

    courses=filter_courses(request.GET.get('subject_id','all'),request.GET.get('author_id',''))
    
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    
    FIELDS = ["district", "last_name", "first_name", "email"]
    TITLES = ["District", "Last Name", "First Name", "Email"]

    for c in courses:
        if not c.display_coursenumber:
            continue
        FIELDS.append(c.display_coursenumber)
        TITLES.append(c.display_coursenumber)

    for i,k in enumerate(TITLES):
        worksheet.write(0,i,k)
    row=1
    data,filtered=filter_user(request)
    
    if filtered:
      for d in data:
          for c in courses:
              if not c.display_coursenumber:
                  continue            
              allow='Y' if CourseEnrollmentAllowed.objects.filter(email=d.user.email,course_id=c.id,is_active=True).exists() else 'N'
              setattr(d,c.display_coursenumber,allow)
              
          d.first_name=attstr(d,"user.first_name")
          d.last_name=attstr(d,"user.last_name")
          d.district=attstr(d,"district.name")
          d.email=attstr(d,"user.email")
          
          for i,k in enumerate(FIELDS):
              worksheet.write(row,i,getattr(d,k))
      
          row=row+1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())    
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def course_permission_save(request):
    try:
        for email,one in json.loads(request.POST['data']).items():
            for course_id,allowed in one.items():
                cea,created=CourseEnrollmentAllowed.objects.get_or_create(email=email,course_id=course_id)
                cea.is_active=allowed
                cea.save()                
                #CourseEnrollmentAllowed.objects.filter(email=email,course_id=course_id).update(is_active=allowed)

    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    return HttpResponse(json.dumps({'success': True}))     

def filter_courses(subject_id='all',author_id='all'):
    filterDic = {'_id.category':'course'}
    
    if subject_id!='all':
        filterDic['metadata.display_subject'] = subject_id

    if author_id!='all':
        filterDic['metadata.display_organization'] = author_id   

    items = modulestore().collection.find(filterDic).sort("metadata.display_coursenumber",pymongo.ASCENDING)
    courses = modulestore()._load_items(list(items), 0)
    return courses

@login_required
@user_passes_test(lambda u: u.is_superuser)
def course_permission(request):
    courses=filter_courses(request.GET.get('subject_id',''),request.GET.get('author_id','')) # pass 'all' for all

    data,filtered=filter_user(request)

    if not filtered:
        data=[]

    size=request.GET.get('size')

    if size and size.isdigit():
        size=int(size)
    else:
        size=20
    
    data=valid_pager(data,size,request.GET.get('page'))

    for item in data:
        item.days_after_invite=''
        if(item.invite_date):
            item.days_after_invite=(datetime.datetime.now(UTC)-item.invite_date).days
            
    return render_to_response('reg_kits/course_permission.html', {
                                                             "courses":courses,
                                                     "users":data,
                                                     "ui":"list",
                                                     "pager_params":pager_params(request)})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        if request.POST.get('id'):
            profile=UserProfile.objects.get(user_id=request.POST['id'])
            user=User.objects.get(id=request.POST['id'])
        else:
            profile=UserProfile()
            user=User()

        if request.POST['subscription_status']=='Registered':
            user.is_active=True
        else:
            user.is_active=False 
            
        user.email=request.POST['email']
        user.save()

        profile.user_id=user.id
        profile.school_id=request.POST['school_id']
        profile.cohort_id=request.POST['cohort_id']
        profile.district_id=request.POST['district_id']
        profile.subscription_status=request.POST['subscription_status']
        profile.save()

    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_modify_status(request):
    for id in request.POST.get("ids").split(","): 
        user=User.objects.get(id=id)
        profile=UserProfile.objects.get(user_id=id)
        try:
            if request.POST['subscription_status']=='Registered':
                user.is_active=True
            else:
                user.is_active=False
            user.save()
            profile.subscription_status=request.POST['subscription_status']
            profile.save()
        except Exception as e:
            db.transaction.rollback()
            return HttpResponse(json.dumps({'success': False,'error':'%s' % e}))
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request):
    ids=request.POST.get("ids").split(",")
    message={'success': True}
    try:
        User.objects.filter(id__in=ids).delete()
        UserProfile.objects.filter(user_id__in=ids).delete()
        db.transaction.commit()
    except Exception as e:
        db.transaction.rollback()
        message={'success': False,'error':'%s' % (e)}
    return HttpResponse(json.dumps(message))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_form(request,user_id=None):
    if user_id:
        c=UserProfile.objects.get(id=user_id)
    else:
        c=UserProfile()
    return render_to_response('reg_kits/user.html', {"ui":"form","profile":c})

USER_CSV_COL_EMAIL=0
USER_CSV_COUNT_COL=1

def validate_user_cvs_line(line):
    email=line[USER_CSV_COL_EMAIL]
    exist=False
    # check field count
    n=0
    for item in line:
        if len(item.strip()):
            n=n+1
    if n != USER_CSV_COUNT_COL:
        raise Exception("Wrong fields count")
    validate_email(email)
    
    if len(User.objects.filter(email=email)) > 0:
        raise Exception("An account with the Email '{email}' already exists".format(email=email))
        exist=True
    return exist

def attstr(obj,attr):
    r=obj
    try:
        for a in attr.split("."):
            r=getattr(r,a)
    except:
        r=""

    if r is None: r=""
    return r

@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_school_csv(request):
    from StringIO import StringIO
    FIELDS = ['id',"name","district"]
    TITLES = ["School ID","School Name", "District"]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    writer.writerow(dict(zip(FIELDS, TITLES)))
    data=filter_school(request)
    for d in data:
        writer.writerow({
            "id":d.id,
            "name":d.name,
            "district":"%s - %s" % (attstr(d,"district.name"), attstr(d,"district.code"))
            })

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = today=datetime.datetime.now().strftime('attachment; filename=schools-%Y-%m-%d-%H-%M-%S.csv')
    output.seek(0)
    response.write(output.read())
    output.close()
    return response

@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_school_excel(request):
    from StringIO import StringIO
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    FIELDS = ['id',"name","_district"]
    TITLES = ["School ID","School Name", "District"]    
    
    for i,k in enumerate(TITLES): worksheet.write(0,i,k)
    
    row=1
    data=filter_school(request)
    for d in data:
        d._district="%s - %s" % (attstr(d,"district.name"), attstr(d,"district.code"))
        for i,k in enumerate(FIELDS):
            worksheet.write(row,i,getattr(d,k))
        row=row+1

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.datetime.now().strftime('attachment; filename=schools-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())    
    return response

@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_user_csv(request):
    from StringIO import StringIO
    FIELDS = ['user_id',"activate_link","first_name","last_name","username","email",
              "district","cohort","school","invite_date","activate_date","subscription_status"]
    
    TITLES = ["User ID" ,"Activate Link" ,"First Name" ,"Last Name" ,
              "Username" ,"Email" ,"District" ,"Cohort" ,"School" ,"Invite Date" ,"Activate Date" ,"Status"]

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    
    writer.writerow(dict(zip(FIELDS, TITLES)))
    data,filtered=filter_user(request)

    domain="http://"+request.META['HTTP_HOST']

    for d in data:
        key,link="",""
        if Registration.objects.filter(user_id=d.user_id).count():
            key=Registration.objects.get(user_id=d.user_id).activation_key

        if key: link=domain+reverse('register_user',args=[key])

        writer.writerow({
            "user_id":attstr(d,"user_id"),
            "activate_link":link,
            "first_name":attstr(d,"user.first_name"),
            "last_name":attstr(d,"user.last_name"),
            "username":attstr(d,"user.username"),
            "email":attstr(d,"user.email"),       
            "district":attstr(d,"district.name"),
            "cohort":attstr(d,"cohort.code"),
            "school":attstr(d,"school.name"),
            "invite_date":attstr(d,"invite_date"),
            "activate_date":attstr(d,"activate_date"),
            "subscription_status":attstr(d,"subscription_status")
                })

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = datetime.datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.csv')
    output.seek(0)
    response.write(output.read())
    output.close()
    return response

@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_user_excel(request):
    from StringIO import StringIO
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    
    FIELDS = ['user_id',"activate_link","first_name","last_name","username","email",
              "_district","_cohort","_school","_invite_date","_activate_date","subscription_status"]
    
    TITLES = ["User ID" ,"Activate Link" ,"First Name" ,"Last Name" ,
              "Username" ,"Email" ,"District" ,"Cohort" ,"School" ,"Invite Date" ,"Activate Date" ,"Status"]
    
    for i,k in enumerate(TITLES):
        worksheet.write(0,i,k)
    row=1
    data,filtered=filter_user(request)
    domain="http://"+request.META['HTTP_HOST'] 
    for d in data:
        if Registration.objects.filter(user_id=d.user_id).count():
            key=Registration.objects.get(user_id=d.user_id).activation_key
        else:
            key=None
        d.activate_link=""
        d.username=attstr(d,"user.username")
        d.first_name=attstr(d,"user.first_name")
        d.last_name=attstr(d,"user.last_name")
        d._school=attstr(d,"school.name")
        d._cohort=attstr(d,"cohort.code")
        d._district=attstr(d,"district.name")
        d.email=attstr(d,"user.email")
        d._invite_date="%s" % attstr(d,"invite_date")
        d._activate_date="%s" % attstr(d,"activate_date")
        
        for i,k in enumerate(FIELDS):
            if k=="activate_link" and key:
                d.activate_link=domain+reverse('register_user',args=[key])
                worksheet.write_url(row,i,getattr(d,k),None,key)
            else:
                worksheet.write(row,i,getattr(d,k))

        row=row+1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())    
    return response

def random_mark(length):
    assert(length>0)
    return "".join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890@#$%^&*_+{};~',length))

@login_required
@user_passes_test(lambda u: u.is_superuser)
@ensure_csrf_cookie
@cache_if_anonymous  
def import_user_submit(request):  
    message={}
    if request.method == 'POST':
        f=request.FILES['file']
        try:
            count_success=0
            # --- THIS FAILS ON SING COLUMN CVS ---
            # dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
            # f.seek(0)
            # r=csv.reader(f,dialect)
            r=csv.reader(f,delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            rl = []
            rl.extend(r)
            cohort_id=request.POST.get("cohort_id")
            cohort=Cohort.objects.get(id=cohort_id)
            if cohort.licences < UserProfile.objects.filter(~Q(subscription_status = "Inactive"),cohort_id=cohort_id).count() + len(rl):
                raise Exception("Licences limit exceeded")
            for line in rl:
                exist=validate_user_cvs_line(line)
                # if(exist):
                #     raise Exception("An user already exists, or duplicate lines.")
                email=line[USER_CSV_COL_EMAIL]
                import random
                username=random_mark(20)
                user = User(username=username, email=email, is_active=False)
                user.set_password(username)
                user.save()
                registration = Registration()
                registration.register(user)
                profile=UserProfile(user=user)
                # profile.transaction_id=transaction_id
                # profile.email=email
                # profile.username=username
                profile.cohort_id=cohort_id
                profile.subscription_status="Imported"
                profile.save()

                cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG/PEP101x/2014_Spring', email=email)
                cea.is_active = True
                cea.auto_enroll = True
                cea.save()

                count_success=count_success+1

                # reg = Registration.objects.get(user=user)
                # d = {'name': profile.name, 'key': reg.activation_key}
                # subject = render_to_string('emails/activation_email_subject.txt', d)
                # subject = ''.join(subject.splitlines())
                # message = render_to_string('emails/activation_emailh.txt', d)
            db.transaction.commit()
            message={"success": True,
                "message":"Success! %s users imported." % (count_success),
                "count_success":count_success,
            }            
        except Exception as e:
            db.transaction.rollback()
            message={'success': False,'error':'Import error: %s. At cvs line: %s, Nobody imported.' % (e,count_success+1)}
    return HttpResponse(json.dumps(message))

from mail import send_html_mail

@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_invite_email(request):
    try:
        data,filtered=filter_user(request)
        data=data.filter(subscription_status='Imported')
        remain=request.GET.get('remain')
        count=request.GET.get('count')
        wait=data[:int(count)]
        for item in wait:
            reg = Registration.objects.get(user_id=item.user_id)
            d = {'name': "%s %s" % (item.user.first_name,item.user.last_name), 'key': reg.activation_key,'district': item.district.name}
            subject = render_to_string('emails/activation_email_subject.txt', d)
            subject = ''.join(subject.splitlines())
            message = render_to_string('emails/activation_email.txt', d)
            try:
                send_html_mail(subject, message, settings.SUPPORT_EMAIL, [item.user.email])
            except Exception as e:
                # log.warning('unable to send reactivation email', exc_info=true)
                raise Exception('unable to send reactivation email: %s' % e)
            item.subscription_status='Unregistered'
            item.invite_date=datetime.datetime.now(UTC)
            item.save()
            db.transaction.commit()
        ret={"success":True,"sent":len(wait),"remain":data.count()}
    except Exception as e:
       ret={"success":False,"error":"%s" % e}
    return HttpResponse(json.dumps(ret))

##############################################
# transaction
##############################################
@login_required
@user_passes_test(lambda u: u.is_superuser)
def transaction_form(request,transaction_id=None):
    if transaction_id:
        t=Transaction.objects.get(id=transaction_id)
        c=Cohort.objects.get(id=t.owner_id)
    else:
        t=Transaction()
        c=None
    return render_to_response('reg_kits/transaction.html',
                              {"district":District.objects.all(), "transaction":t,"cohort":c, "ui":"form"})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def transaction(request):
    sql="select  a.*,c.code as district_code from transaction a \
    inner join cohort b on a.owner_id=b.id and a.subscription_type='cohort' \
    inner join district c on b.district_id=c.id"
    if request.GET.get('district_id'):
        sql=sql+" where b.district_id="+request.GET.get('district_id')
    elif request.GET.get('state_id'):
        sql=sql+" where c.state_id="+request.GET.get('state_id')
    data=Transaction.objects.raw(sql)
    data=valid_pager(list(data),20,request.GET.get('page'))
    return render_to_response('reg_kits/transaction.html', {"transactions":data, "ui":"list","pager_params":pager_params(request)})

@login_required
@user_passes_test(lambda u: u.is_superuser)
@ensure_csrf_cookie
@cache_if_anonymous
def transaction_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        if request.POST.get('id'):
            d=Transaction(request.POST['id'])
        else:
            d=Transaction()
        d.code=request.POST['code']
        d.owner_id=request.POST['cohort_id']
        d.start_date=request.POST['start_date']
        d.term_months=request.POST['term_months']
        # from django.contrib.contenttypes.models import ContentType
        # user_type = ContentType.objects.get(app_label="student", model="cohort")
        d.subscription_type=request.POST['subscription_type']
        d.status='ALLOW'
        d.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False,'error':"%s" % e}))
    return HttpResponse(json.dumps({'success': True}))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def transaction_delete(request):
    ids=request.GET.get("ids").split(",")
    message={'success': True}
    try:
        Transaction.objects.filter(id__in=ids).delete()
    except Exception as e:
        db.transaction.rollback()
        message={'success': False,'error':"%" % e}
    return HttpResponse(json.dumps(message))

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
    if request.GET.get('state_id'):
        data=data.filter(state_id=request.GET.get('state_id'))
    data=data.order_by("name")        
    r=list()
    for item in data:
        r.append({"id":item.id,"name":item.name,"code":item.code})        
    return HttpResponse(json.dumps(r))

def drop_schools(request):
    data=School.objects.all()
    if request.GET.get('district_id'):
        data=data.filter(district_id=request.GET.get('district_id'))
    elif request.GET.get('state_id'):
        data=data.filter(district__state_id=request.GET.get('state_id'))
    r=list()
    data=data.order_by("name")
    for item in data:
        r.append({"id":item.id,"name":item.name})        
    return HttpResponse(json.dumps(r))

def drop_cohorts(request):
    data=Cohort.objects.all()
    if request.GET.get('district_id'):
        data=data.filter(district_id=request.GET.get('district_id'))
    elif request.GET.get('state_id'):
        data=data.filter(district__state_id=request.GET.get('state_id'))
    r=list()
    for item in data:
        r.append({"id":item.id,"code":item.code})
    return HttpResponse(json.dumps(r))

##############################################
# Import Cohort 
##############################################
COHORT_CSV_COLS=5

COHORT_CSV_COL_DISTRICT_CODE=0
COHORT_CSV_COL_CODE=1
COHORT_CSV_COL_LICENSES=2
COHORT_CSV_COL_TERM_MONTHS=3
COHORT_CSV_COL_START_DATE=4

def validate_cohort_cvs_line(line):
    exist=False
    # check field count
    n=0
    for item in line:
        if len(item.strip()):
            n=n+1

    if n != COHORT_CSV_COLS:
        raise Exception("Wrong column count %s" % n)

    code=line[COHORT_CSV_COL_CODE]
    
    if len(Cohort.objects.filter(code=code)) > 0:
        raise Exception("A cohort '{code}' already exists".format(code=code))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_cohort_submit(request):
    message={"success": True}

    if request.method == 'POST':
        f=request.FILES['file']
        count_success=0
        try:
            r=csv.reader(f,delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i,line in enumerate(r):
                district_code=line[COHORT_CSV_COL_DISTRICT_CODE]
                district_id=District.objects.get(code=district_code).id

                validate_cohort_cvs_line(line)
                cohort=Cohort()
                cohort.code=line[COHORT_CSV_COL_CODE]
                cohort.district_id=district_id
                cohort.licences=int(line[COHORT_CSV_COL_LICENSES])
                cohort.term_months=int(line[COHORT_CSV_COL_TERM_MONTHS])
                cohort.start_date=line[COHORT_CSV_COL_START_DATE]
                cohort.save()
                count_success=count_success+1
                
            db.transaction.commit()
            message={"success": True,
                "message":"Success! %s cohort(s) imported." % (count_success),
                "count_success":count_success
                }     
        except Exception as e:
            
            db.transaction.rollback()
            message={'success': False,'error':'Import error: %s. At cvs line: %s, Nothing impored.' % (e,count_success+1)}
    
    return HttpResponse(json.dumps(message))

##############################################
# Import District 
##############################################
DISTRICT_CSV_COLS=3

DISTRICT_CSV_COL_STATE_NAME=0
DISTRICT_CSV_COL_NAME=1
DISTRICT_CSV_COL_CODE=2

def validate_district_cvs_line(line):
    exist=False
    # check field count
    n=0
    for item in line:
        if len(item.strip()):
            n=n+1
    if n != DISTRICT_CSV_COLS:
        raise Exception("Wrong column count %s" % n)

    name=line[DISTRICT_CSV_COL_NAME]
    code=line[DISTRICT_CSV_COL_CODE]
    
    if len(District.objects.filter(name=name,code=code)) > 0:
        raise Exception("A district named '{name}' already exists".format(name=name))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_district_submit(request):
    message={"success": True}

    if request.method == 'POST':
        f=request.FILES['file']
        count_success=0
        try:
            r=csv.reader(f,delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i,line in enumerate(r):
                state_name=line[DISTRICT_CSV_COL_STATE_NAME]
                state_id=State.objects.get(name=state_name).id
                
                validate_district_cvs_line(line)
                district=District()
                district.code=line[DISTRICT_CSV_COL_CODE]
                district.name=line[DISTRICT_CSV_COL_NAME]
                district.state_id=state_id
                district.save()
                count_success=count_success+1
                
            db.transaction.commit()
            message={"success": True,
                "message":"Success! %s district(s) imported." % (count_success),
                "count_success":count_success
                }     
        except Exception as e:
            
            db.transaction.rollback()
            message={'success': False,'error':'Import error: %s. At cvs line: %s, Nothing impored.' % (e,count_success+1)}
    
    return HttpResponse(json.dumps(message))
##############################################
# Import School 
##############################################
SCHOOL_CSV_COLS=2

SCHOOL_CSV_COL_NAME=0
SCHOOL_CSV_COL_CODE=1

def validate_school_cvs_line(line,district_id):
    name=line[SCHOOL_CSV_COL_NAME]
    exist=False
    # check field count
    n=0
    for item in line:
        if len(item.strip()):
            n=n+1
    if n != SCHOOL_CSV_COLS:
        raise Exception("Wrong column count")
    if len(School.objects.filter(name=name,district_id=district_id)) > 0:
        raise Exception("A school named '{name}' already exists in the district".format(name=name))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_school_submit(request):
    if request.method == 'POST':
        f=request.FILES['file']
        district_id=request.POST.get('district_id')
        count_success=0
        try:
            # --- THIS FAILS ON SING COLUMN CVS ---
            # dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";,\t",quotechar='\n')
            # f.seek(0)
            # r=csv.reader(f,dialect)
            r=csv.reader(f,delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i,line in enumerate(r):
                exist=validate_school_cvs_line(line,district_id)
                school_name=line[SCHOOL_CSV_COL_NAME]
                school_code=line[SCHOOL_CSV_COL_CODE]
                school = School()
                school.name=school_name
                school.code=school_code
                school.district_id=district_id
                school.save()
                count_success=count_success+1
            # commit when all lines imported
            db.transaction.commit()
            # success information
            message={"success": True,
                "message":"Success! %s school(s) imported." % (count_success),
                "count_success":count_success
                }    
        except Exception as e:
            db.transaction.rollback()
            # failure information
            message={'success': False,'error':'Import error: %s. At cvs line: %s, Nothing impored.' % (e,count_success+1)}
    return HttpResponse(json.dumps(message))
