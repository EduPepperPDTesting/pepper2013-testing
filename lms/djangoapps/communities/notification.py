from django.contrib.auth.models import User
from django import db
import json
from mitxmako.shortcuts import render_to_response, render_to_string
from django.contrib.auth.decorators import login_required
from models import NotificationConfig, NotificationGroup, NotificationType, NotificationAudit
from django.http import HttpResponse

from .models import CommunityCommunities, CommunityUsers


@login_required
def configuration(request):
    facilitators = CommunityUsers.objects.select_related().filter(facilitator=True, user=request.user)
    
    return render_to_response('communities/notification.html', {'facilitators': facilitators})


def groups(request):
    al = NotificationGroup.objects.all()
    json_out = [al.count()]
    rows = list()

    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size
    
    for item in al[start:end]:
        row = [
            item.name,
            item.description,
            "<input type=hidden name=id value=%s>" % item.id
            ]
    
        rows.append(row)
    json_out.append(rows)
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def all_groups(request):
    al = NotificationGroup.objects.all()
  
    rows = list()

    for item in al:
        row = {
            "id": item.id,
            "name": item.name
            }
    
        rows.append(row)

    return HttpResponse(json.dumps(rows), content_type="application/json")


def save_group(request):
    try:
        id = request.POST.get("id")
        if id:
            group = NotificationGroup.objects.get(id=id)
        else:
            group = NotificationGroup()
        group.name = request.POST.get("name")
        group.description = request.POST.get("description")
        group.save()
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def types(request):
    al = NotificationType.objects.all()
    json_out = [al.count()]
    rows = list()

    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size
    
    for item in al[start:end]:
        row = [
            item.name,
            item.description,
            "<input type=hidden name=id value=%s>" % item.id
            ]
    
        rows.append(row)
    json_out.append(rows)
    return HttpResponse(json.dumps(json_out), content_type="application/json")

    
def save_type(request):
    try:
        id = request.POST.get("id")
        if id:
            type = NotificationType.objects.get(id=id)
        else:
            type = NotificationType()
        type.name = request.POST.get("name")
        type.group_id = request.POST.get("group")
        type.description = request.POST.get("description")
        type.subject = request.POST.get("subject")
        type.body = request.POST.get("body")
        type.action = request.POST.get("action")
        
        type.save()
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def edit_group(request):
    id = request.POST.get("id")
    group = NotificationGroup.objects.get(id=id)
    json_out = {'id': group.id, 'name': group.name, 'description': group.description}
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def edit_type(request):
    id = request.POST.get("id")
    type = NotificationType.objects.get(id=id)
    json_out = {'id': type.id,
                'name': type.name,
                'description': type.description,
                'group': type.group_id,
                'subject': type.subject,
                'body': type.body,
                'action': type.action
                }
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def config(request):
    al = NotificationType.objects.all()
    json_out = [al.count()]
    rows = list()

    page = int(request.GET.get('page'))
    size = int(request.GET.get('size'))
    start = page * size
    end = start + size
    
    for item in al[start:end]:
        try:
            config = NotificationConfig.objects.get(type=item, user=request.user)
        except:
            config = NotificationConfig()
  
        row = [
            "<input type=hidden name=type_id value=%s>%s" % (item.id, item.action),
            config.via_pepper,
            config.via_email,
            config.frequency,
            ]
    
        rows.append(row)
    json_out.append(rows)
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def config_other(request):
    al = NotificationType.objects.all()
    json_out = [al.count()]
    rows = list()

    page = int(request.GET.get('page'))
    size = int(request.GET.get('size'))
    start = page * size
    end = start + size
    
    for item in al[start:end]:
        row = [
            "<input type=hidden name=type_id value=%s>%s" % (item.id, item.action),
            False,
            False,
            ""]
        rows.append(row)
    json_out.append(rows)
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def save_other_config(request):
    data = json.loads(request.POST.get("data"))
    filter = json.loads(request.POST.get("filter"))

    users = User.objects.all()
    if filter.get("state_id"):
        users = users.filter(district__state_id=filter.get("state_id"))

    if filter.get("district_id"):
        users = users.filter(district_id=filter.get("district_id"))

    if filter.get("cohort_id"):
        users = users.filter(cohort_id=filter.get("cohort_id"))

    if filter.get("community_id"):
        facilitator_ids = CommunityUsers.objects.filter(community_id=filter.get("community_id"), facilitator=True).values_list('user_id', flat=True)
        users = users.filter(id__in=facilitator_ids)
    
    try:
        for d in data:
            for u in users:
                config, created = NotificationConfig.objects.get_or_create(type_id=d["type_id"], user=u)
                if created or (not config.self_config):
                    config.type_id = d["type_id"]
                    config.via_pepper = d["via_pepper"]
                    config.via_email = d["via_email"]
                    config.frequency = d["frequency"]
                    config.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def save_config(request):
    data = json.loads(request.POST.get("data"))

    try:
        for d in data:
            config, created = NotificationConfig.objects.get_or_create(type_id=d["type_id"], user=request.user)
            config.type_id = d["type_id"]
            config.via_pepper = d["via_pepper"]
            config.via_email = d["via_email"]
            config.frequency = d["frequency"]
            config.self_config = True
            config.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_group(request):
    ids = request.POST.getlist("ids[]")
    try:
        for id in ids:
            NotificationGroup.objects.get(id=id).delete()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_type(request):
    ids = request.POST.getlist("ids[]")
    try:
        for id in ids:
            NotificationType.objects.get(id=id).delete()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

