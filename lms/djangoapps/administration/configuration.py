from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

import json
import logging

from django import db
from models import *
from student.models import District, Cohort, School, State, UserProfile
import urllib
from django.core.paginator import Paginator

from permissions.decorators import user_has_perms
from study_time.models import record_time_store
from reporting.models import reporting_store
from threading import Thread
import gevent
import time
from pytz import UTC
from datetime import datetime
from reporting.school_year import school_year_collection
from administration.models import PepRegStudent,PepRegInstructor,PepRegTraining,PepRegTraining_Backup,PepRegInstructor_Backup,PepRegStudent_Backup
log = logging.getLogger("tracking")


@user_has_perms('certificate')
def main(request):
    return render_to_response('administration/configuration.html', {})


##############################################
# Dropdown List
##############################################
def drop_association_type(request):  
    data = CertificateAssociationType.objects.all()
    data = data.order_by("name")
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name})
  
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_association(request):
    asociationType = CertificateAssociationType.objects.filter(Q(id=request.GET.get('association_type')))[0]
    if asociationType.name == 'Author':
        data = Author.objects.all()
    elif asociationType.name == 'District':
        data = District.objects.all()
    elif asociationType.name == 'School':
        data = School.objects.all()
    data = data.order_by("name")  
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_publish_association(request):
    asociationType = CertificateAssociationType.objects.filter(Q(id=request.GET.get('association_type')))[0]
    cdata = Certificate.objects.filter(Q(association_type=request.GET.get('association_type')))
    idarr = [x.association for x in cdata]
    if asociationType.name == 'Author':
        data = Author.objects.filter(~Q(id__in=idarr))
    elif asociationType.name == 'District':
        data = District.objects.filter(~Q(id__in=idarr))
    elif asociationType.name == 'School':
        data = School.objects.filter(~Q(id__in=idarr))
    data = data.order_by("name")      
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_states(request):
    data=State.objects.all()
    data=data.order_by("name")        
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_districts(request):
    data = District.objects.all()
    if request.GET.get('state'):
        data = data.filter(state=request.GET.get('state'))
    data=data.order_by("name")        
    r = list()
    for item in data:
        r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_schools(request):
    data = School.objects.all()
    if request.GET.get('district'):
        data = data.filter(district=request.GET.get('district'))
    elif request.GET.get('state'):
        data = data.filter(district__state=request.GET.get('state'))
    r = list()
    data = data.order_by("name")
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_cohorts(request):
    data = Cohort.objects.all()
    if request.GET.get('district'):
        data = data.filter(district=request.GET.get('district'))
    elif request.GET.get('state'):
        data = data.filter(district__state=request.GET.get('state'))
    r=list()
    for item in data:
        r.append({"id": item.id, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def paging(all, size, page):
    try:
        page = int(page)
    except Exception:
        page = 1
    try:
        size = int(size)
    except Exception:
        size = 1
    paginator = Paginator(list(all), size)
    if page < 1:
        page = 1
    if page > paginator.num_pages:
        page = paginator.num_pages
    data = paginator.page(page)
    return data


@user_has_perms('certificate', 'view')
def certificate_table(request):
    data = Certificate.objects.all()
    if request.GET.get('association_type', None):
        data = data.filter(Q(association_type=request.GET.get('association_type')))
    if request.GET.get('certificate_name', None):
        data = data.filter(Q(certificate_name=request.GET.get('certificate_name')))
    if request.GET.get('association', None):
        data = data.filter(Q(association=request.GET.get('association')))
    
    page = request.GET.get('page')
    size = request.GET.get('size')
    data = paging(data, size, page)

    rows = []
    pagingInfo = {'page': data.number, 'pages': data.paginator.num_pages}

    for p in data:

        if p.association_type_id != 0:
            if p.association_type.name == "Author":
                association = Author.objects.filter(Q(id=p.association))
            elif p.association_type.name == "District":
                association = District.objects.filter(Q(id=p.association))
            elif p.association_type.name == "School":
                association = School.objects.filter(Q(id=p.association))
            association_type_name = p.association_type.name
            association_name = association[0].name     
        else:
            association_type_name = ""
            association_name = ""
        rows.append({'certificate_name': p.certificate_name,
                     'association_type': association_type_name,
                     'association': association_name,
                     'id': p.id})
    return HttpResponse(json.dumps({'rows': rows, 'paging': pagingInfo}), content_type="application/json")


@user_has_perms('certificate', 'view')
def favorite_filter_load(request):
    favs = []

    for ff in FilterFavorite.objects.filter(user=request.user).order_by('name'):
        favs.append({'id': ff.id,
                     'name': ff.name,
                     'filter': ff.filter_json
                     })
    
    return HttpResponse(json.dumps(favs), content_type="application/json")


@user_has_perms('certificate', 'view')
def favorite_filter_save(request):
    ff = FilterFavorite()
    ff.user = request.user
    ff.name = request.GET.get('name')
    ff.filter_json = request.GET.get('filter')
    ff.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@user_has_perms('certificate', 'view')
def favorite_filter_delete(request):
    FilterFavorite.objects.filter(id=request.GET.get('id')).delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def send_registration_email(request):
#     return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@user_has_perms('certificate', 'delete')
def certificate_delete(request):
    ids= request.POST.get('ids').split(',')
    for id in ids:
        Certificate.objects.filter(id=id).delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@user_has_perms('certificate', 'edit')
def certificate_save(request):
    cid = request.POST.get('id')
    readonly = request.POST.get('readonly') == 'true'
    content = urllib.quote(request.POST.get('content').decode('utf8').encode('utf8'))
    c = Certificate.objects.filter(id=cid)
    try:
        if len(c) == 0:
            cdata = Certificate.objects.create(certificate_name=request.POST.get('name'),
                                               association_type_id=request.POST.get('association_type'),
                                               association=request.POST.get('association'),
                                               certificate_blob=content,
                                               readonly=readonly)
            returnID = cdata.id
        else:
            uc = Certificate.objects.get(id=cid)
            uc.certificate_name = request.POST.get('name')
            uc.association_type_id = request.POST.get('association_type')
            uc.association = request.POST.get('association')
            uc.certificate_blob = request.POST.get('content')
            uc.readonly = readonly
            uc.save()
            returnID = uc.id
        info = {'success': True, 'msg': 'Save complete.', 'id': returnID}
    except db.utils.IntegrityError:
        info = {'success': False, 'msg': 'Certificate name already exists.'}
    return HttpResponse(json.dumps(info), content_type="application/json")


@user_has_perms('certificate', 'view')
def certificate_loadData(request):
    c = Certificate.objects.filter(id=request.POST.get('id'))[0]
    try:
        content = urllib.unquote(c.certificate_blob.decode('utf8').encode('utf8'))
    except:
        content = ""
    data = {'certificate_name': c.certificate_name,
            'association_type': c.association_type_id,
            'association': c.association,
            'content': content,
            'readonly': c.readonly,
            'id': c.id
            }
    return HttpResponse(json.dumps(data), content_type="application/json")


# TODO: This should be removed, and replaced with the new permissions system.
def has_hangout_perms(user):
    try:
        user_profile = UserProfile.objects.get(user=user.id)
        permissions = HangoutPermissions.objects.get(district=user_profile.district_id)
        permission = permissions.permission
    except HangoutPermissions.DoesNotExist:
        permission = 1
        
    return permission


@login_required
def get_user_info(request):
    json_return = {'first_name': request.user.first_name,
                   'last_name': request.user.last_name,
                   'email': request.user.email,
                   'secret': 'La2aiphaab2gaeB'
                   }
    return HttpResponse(json.dumps(json_return), content_type="application/json")


# -------------------------------------#
#    End of Year Roll Over             #
# -------------------------------------#

def postpone(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@user_has_perms('end_of_year_roll_over', ['administer'], exclude_superuser=True)
def roll_over(request):
    task = ImportTask()
    task.filename = 'School Year'
    task.total_lines = len(school_year_collection)
    task.user = request.user
    task.save()
    db.transaction.commit()

    from django.db import connection
    connection.close()
    save_school_year(task, request)
    return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")


@postpone
def save_school_year(task, request):
    gevent.sleep(0)
    count_success = 0
    rs = reporting_store()
    try:
        year = time.strftime('%Y', time.localtime(time.time()))
        year = str(int(year) - 1) + '-' + year
        i = 0
        backup_training(year)
        backup_training_student(year)
        backup_training_instructor(year)
        for collection in school_year_collection:
            rs.set_collection(collection)
            rs.collection.update({'school_year': 'current'}, {'$set': {"school_year": year}}, multi=True)
            i += 1
            task.process_lines = i
        remove_time()
        remove_pepreg_training()
    except Exception as e:
            db.transaction.rollback()
            log.debug("import error %s" % e)

    finally:
        count_success += 1
        task.success_lines = count_success
        task.update_time = datetime.now(UTC)
        task.save()
        db.transaction.commit()


def remove_time():
    rts = record_time_store()
    rts.collection.remove()
    rts.collection_page.remove()
    rts.collection_discussion.remove()
    rts.collection_portfolio.remove()
    rts.collection_external.remove()
    rts.collection_adjustment.remove()
    rts.collection_aggregate.remove()


def remove_pepreg_training():
    PepRegTraining.objects.all().delete()
    PepRegInstructor.objects.all().delete()
    PepRegStudent.objects.all().delete()

def backup_training(year):
    trainings = PepRegTraining.objects.all()
    for train in trainings:
        training_backup = PepRegTraining_Backup()
        training_backup.id = train.id
        training_backup.school_year = year
        training_backup.district =train.district
        training_backup.description=train.description
        training_backup.subject=train.subject
        training_backup.name=train.name
        training_backup.pepper_course=train.pepper_course
        training_backup.training_date=train.training_date
        training_backup.training_time_start=train.training_time_start
        training_backup.training_time_end=train.training_time_end
        training_backup.geo_location=train.geo_location
        training_backup.geo_props=train.geo_props
        training_backup.classroom=train.classroom
        training_backup.credits=train.credits
        training_backup.attendancel_id=train.attendancel_id
        training_backup.allow_registration=train.allow_registration
        training_backup.max_registration=train.max_registration
        training_backup.allow_attendance=train.allow_attendance
        training_backup.allow_student_attendance=train.allow_student_attendance
        training_backup.allow_validation=train.allow_validation
        training_backup.user_create=train.user_create
        training_backup.date_create=train.date_create
        training_backup.user_modify=train.user_modify
        training_backup.date_modify=train.date_modify
        training_backup.last_date=train.last_date
        training_backup.school_id=train.school_id
        training_backup.save()

def backup_training_student(year):
    trainings = PepRegStudent.objects.all()
    for train in trainings:
        training_backup = PepRegStudent_Backup()
        training_backup.school_year = year
        training_backup.training =train.training
        training_backup.student=train.student
        training_backup.student_status=train.student_status
        training_backup.student_credit=train.student_credit
        training_backup.user_create=train.user_create
        training_backup.date_create=train.date_create
        training_backup.user_modify=train.user_modify
        training_backup.date_modify=train.date_modify
        training_backup.save()

def backup_training_instructor(year):
    trainings = PepRegInstructor.objects.all()
    for train in trainings:
        training_backup = PepRegInstructor_Backup()
        training_backup.school_year = year
        training_backup.training =train.training
        training_backup.instructor=train.instructor
        training_backup.user_create=train.user_create
        training_backup.date_create=train.date_create
        training_backup.all_edit=train.all_edit
        training_backup.all_delete=train.all_delete
        training_backup.save()
