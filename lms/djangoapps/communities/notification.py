from django.conf import settings
from mail import send_html_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import db
import json
from mitxmako.shortcuts import render_to_response, render_to_string
from django.contrib.auth.decorators import login_required
from models import CommunityNotificationConfig, CommunityNotificationGroup, CommunityNotificationType, CommunityNotificationAudit
from django.http import HttpResponse
import re
from .models import CommunityCommunities, CommunityUsers
from notifications.views import save_interactive_info
from datetime import datetime, timedelta
import sys
import logging
from xmodule.course_module import CourseDescriptor

log = logging.getLogger("tracking")

@login_required
def configuration(request):
    facilitators = CommunityUsers.objects.select_related().filter(facilitator=True, user=request.user)
    
    return render_to_response('communities/notification.html', {'facilitators': facilitators})


def groups(request):
    al = CommunityNotificationGroup.objects.all()
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
    al = CommunityNotificationGroup.objects.all()
  
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
            group = CommunityNotificationGroup.objects.get(id=id)
        else:
            group = CommunityNotificationGroup()
        group.name = request.POST.get("name")
        group.description = request.POST.get("description")
        group.save()
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def types(request):
    al = CommunityNotificationType.objects.all()
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
            type = CommunityNotificationType.objects.get(id=id)
        else:
            type = CommunityNotificationType()
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
    group = CommunityNotificationGroup.objects.get(id=id)
    json_out = {'id': group.id, 'name': group.name, 'description': group.description}
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def edit_type(request):
    id = request.POST.get("id")
    type = CommunityNotificationType.objects.get(id=id)
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
    al = CommunityNotificationType.objects.all()
    json_out = [al.count()]
    rows = list()

    page = int(request.GET.get('page'))
    size = int(request.GET.get('size'))
    start = page * size
    end = start + size
    
    for item in al[start:end]:
        try:
            config = CommunityNotificationConfig.objects.get(type=item, user=request.user)
        except:
            config = CommunityNotificationConfig()
  
        row = [
            "<input type=hidden name=type_id value=%s>%s" % (item.id, item.name),
            config.via_pepper,
            config.via_email,
            config.frequency,
            ]
    
        rows.append(row)
    json_out.append(rows)
    return HttpResponse(json.dumps(json_out), content_type="application/json")


def config_other(request):
    al = CommunityNotificationType.objects.all()
    json_out = [al.count()]
    rows = list()

    page = int(request.GET.get('page'))
    size = int(request.GET.get('size'))
    start = page * size
    end = start + size
    
    for item in al[start:end]:
        row = [
            "<input type=hidden name=type_id value=%s>%s" % (item.id, item.name),
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
        users = users.filter(profile__district__state_id=filter.get("state_id"))

    if filter.get("district_id"):
        users = users.filter(profile__district_id=filter.get("district_id"))

    if filter.get("cohort_id"):
        users = users.filter(profile__cohort_id=filter.get("cohort_id"))

    if filter.get("community_id"):
        # facilitator=True
        facilitator_ids = CommunityUsers.objects.filter(community_id=filter.get("community_id")).values_list('user_id', flat=True)
        users = users.filter(id__in=facilitator_ids)
    
    try:
        for d in data:
            for u in users:
                config, created = CommunityNotificationConfig.objects.get_or_create(type_id=d["type_id"], user=u)
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
            config, created = CommunityNotificationConfig.objects.get_or_create(type_id=d["type_id"], user=request.user)
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
            CommunityNotificationGroup.objects.get(id=id).delete()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_type(request):
    ids = request.POST.getlist("ids[]")
    try:
        for id in ids:
            CommunityNotificationType.objects.get(id=id).delete()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def send_notification(action_user, community_id, courses_add=[], courses_del=[], resources_add=[],
                      resources_del=[], members_add=[], members_del=[], discussions_new=[],
                      discussions_reply=[], discussions_delete=[], replies_delete=[], domain_name='',
                      posts_new=[], posts_reply=[], posts_delete=[], posts_reply_delete=[]):

    community = CommunityCommunities.objects.get(id=community_id)

    def replace_values(body, values):
        return re.sub("{([\w ]*?)}", lambda x: values.get(x.group(1)), body)

    def get_class_attrs(obj, cls, attr_names):
        attrs = {}
        if obj.__class__.__name__ == cls:
            for n, k in attr_names.items():
                attrs[n] = getattr(obj, k, '')
        return attrs
    
    def process(user, type_name, list):
        if not len(list):
            return

        try:
            type = CommunityNotificationType.objects.get(name=type_name)

            for item in list:
                config = CommunityNotificationConfig.objects.filter(user=user, type=type)

                if config.exists():
                    config = config[0]

                values = {
                    "Community Name": community.name,
                    "Sender First Name": action_user.first_name,
                    "Sender Last Name": action_user.last_name,
                    "Receiver First Name": user.first_name,
                    "Receiver Last Name": user.last_name}

                if domain_name:
                    community_url = "https://" + domain_name + "/community/" + str(community.id)
                    values["Community URL"] = "<a href=\"" + community_url + "\" target=\"_blank\">" + community_url + "</a>"

                if type_name == "Delete Course" or type_name == "Add Course":
                    values["Course Name"] = item.display_name
                    values["Course Number"] = item.display_coursenumber

                if type_name == "Delete Resource" or type_name == "Add Resource":
                    values["Resource Title"] = item.name

                if type_name == "Delete Member" or type_name == "Add Member":
                    values["Member List"] = item

                if type_name in ["New Discussion", "Reply Discussion", "Delete Discussion", "Delete Reply"]:
                    values["Subject"] = item.subject
                    values["Posted By"] = "%s %s" % (item.user.first_name, item.user.last_name)
                    if domain_name:
                        if type_name == "New Discussion":
                            discussion_topic_url = "https://" + domain_name + "/community/discussion/" + str(item.id)
                            values["Discussion Topic URL"] = "<a href=\"" + discussion_topic_url + "\" target=\"_blank\">" + discussion_topic_url + "</a>"
                        elif type_name in ["Reply Discussion", "Delete Reply"]:
                            discussion_topic_url = "https://" + domain_name + "/community/discussion/" + str(item.discussion_id)
                            values["Discussion Topic URL"] = "<a href=\"" + discussion_topic_url + "\" target=\"_blank\">" + discussion_topic_url + "</a>"

                # Send the notification
                body = replace_values(type.body or "", values)
                subject = replace_values(type.subject or "", values)

                if config and config.via_pepper:
                    save_interactive_info({
                        "user_id": str(user.id),
                        "interviewer_id": action_user.id,
                        "interviewer_name": action_user.username,
                        "interviewer_fullname": "%s %s" % (action_user.first_name, action_user.last_name),
                        "type": type.name,
                        "body": body,
                        "subject": subject,
                        "location": reverse("community_view", args=[community_id])
                        })

                # Save none instant notification to audit
                if config and config.via_email:
                    days = {"Daily": 0, "Weekly": 7}
                    if config.frequency != 'Instant':
                        audit = CommunityNotificationAudit()
                        audit.subject = subject
                        audit.body = body
                        audit.receiver = user
                        audit.creator = action_user
                        audit.create_date = datetime.utcnow()
                        audit.send_date = audit.create_date + timedelta(days=days[config.frequency])
                        audit.save()
                    else:
                        send_html_mail(subject, body, settings.SUPPORT_EMAIL, [user.email])
        except Exception as e:
            log.error("Send %s notification failed to user %s (%s)" % (type_name, user.id, e))

    for member in CommunityUsers.objects.filter(community=community_id):
        if member.user.id != action_user.id:
            process(member.user, "Delete Course", courses_del)
            process(member.user, "Add Course", courses_add)
            process(member.user, "Delete Resource", resources_del)
            process(member.user, "Add Resource", resources_add)
            if len(members_del):
                process(member.user, "Delete Member", [",".join(map(lambda x: x.first_name + " " + x.last_name, members_del))])
            if len(members_add):
                process(member.user, "Add Member", [",".join(map(lambda x: x.first_name + " " + x.last_name, members_add))])
            process(member.user, "New Discussion", discussions_new)
            process(member.user, "Reply Discussion", discussions_reply)
            process(member.user, "Delete Discussion", discussions_delete)
            process(member.user, "Delete Reply", replies_delete)
            process(member.user, "New Post", posts_new)
            process(member.user, "Reply Post", posts_reply)
            process(member.user, "Delete Post", posts_delete)
            process(member.user, "Delete Reply Post", posts_reply_delete)

    if len(members_del):
        for member in members_del:
            if member.id != action_user.id:
                process(member, "Delete Member", [",".join(map(lambda x: x.first_name + " " + x.last_name, members_del))])
