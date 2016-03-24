from mitxmako.shortcuts import render_to_response
from .models import PermGroup, PermGroupMember, PermPermission, PermGroupPermission
import json
from django.http import HttpResponse
from django_future.csrf import ensure_csrf_cookie
from .decorators import user_has_perms
from student.models import User


@user_has_perms('permissions', 'administer')
def permissions_view(request):
    permissions = permissions_data()
    groups = group_data()
    data = {'permissions': permissions,
            'groups': groups}
    return render_to_response('permissions/permissions.html', data)


@user_has_perms('permissions', 'administer')
def group_check(request):
    valid = True
    error = ''
    if PermGroup.objects.filter(name=request.GET.get('name')).count():
        valid = False
        error = 'This name is already in use.'
    return HttpResponse(json.dumps({'Valid': valid, 'Error': error}), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_add(request):
    name = request.POST.get('name', False)
    if name:
        group = PermGroup()
        group.name = name
        group.save()
        data = {'Success': True}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_permission_add(request):
    group_id = int(request.POST.get('group', False))
    group = PermGroup.objects.get(id=group_id)
    permission_id = int(request.POST.get('permission', False))
    permission = PermPermission.objects.get(id=permission_id)
    if permission and group:
        group_permission = PermGroupPermission()
        group_permission.group = group
        group_permission.permission = permission
        group_permission.save()
        data = {'Success': True}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_member_add(request):
    group_id = request.POST.get('group', False)
    try:
        group = PermGroup.objects.get(id=group_id)
    except:
        group = False
    member = request.POST.get('member', False)
    state = request.POST.get('state', False)
    district = request.POST.get('district', False)
    school = request.POST.get('school', False)

    if group:
        if member:
            user = User.objects.get(email=member)
            group_member = PermGroupMember()
            group_member.group = group
            group_member.user = user
            group_member.save()
            data = {'Success': True}
        elif state:
            if school:
                users = User.objects.filter(profile__school=school)
            elif district:
                users = User.objects.filter(profile__district=district)
            else:
                users = User.objects.filter(profile__district__state=state)
            for user in users:
                group_member = PermGroupMember()
                group_member.group = group
                group_member.user = user
                group_member.save()
            data = {'Success': True}
        else:
            data = {'Success': False}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


def group_data(group_id=False):
    if group_id:
        groups = [PermGroup.objects.get(id=group_id)]
    else:
        groups = list(PermGroup.objects.all())
    return groups


@user_has_perms('permissions', 'administer')
def group_list(request):
    groups = group_data(request.GET.get('group_id', False))
    data = list()
    for group in groups:
        data.append({'id': group.id, 'name': group.name})
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_has_perms('permissions', 'administer')
def group_member_list(request):
    group = PermGroup.objects.get(id=request.GET.get('group_id'))
    group_members = PermGroupMember.objects.prefetch_related().filter(group=group)
    member_list = list()
    for member in group_members:
        member_list.append({'user_id': member.user.id,
                            'first_name': member.user.first_name,
                            'last_name': member.user.last_name,
                            'email': member.user.email,
                            'district': member.user.profile.district.name,
                            'state': member.user.profile.district.state.name,
                            'school': member.user.profile.school.name})
    return HttpResponse(json.dumps(member_list), content_type='application/json')


@user_has_perms('permissions', 'administer')
def group_permissions_list(request):
    group = PermGroup.objects.get(id=request.GET.get('group_id'))
    permissions = PermGroupPermission.objects.filter(group=group)
    permission_list = list()
    for permission in permissions:
        permission_list.append({'id': permission.permission.id,
                                'name': permission.permission.name,
                                'item': permission.permission.item,
                                'action': permission.permission.action})
    return HttpResponse(json.dumps(permission_list), content_type='application/json')


@user_has_perms('permissions', 'administer')
def permission_check(request):
    valid = True
    error = ''
    if PermPermission.objects.filter(name=request.GET.get('name')).count():
        valid = False
        error = 'This name is already in use. '
    if PermPermission.objects.filter(item=request.GET.get('target'), action=request.GET.get('action')).count():
        valid = False
        error += 'This target/action combination is already in use.'
    return HttpResponse(json.dumps({'Valid': valid, 'Error': error}), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def permission_add(request):
    name = request.POST.get('name', False)
    item = request.POST.get('target', False)
    action = request.POST.get('action', False)
    if name and item and action:
        permission = PermPermission()
        permission.name = name
        permission.item = item
        permission.action = action
        permission.save()
        data = {'Success': True}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


def permissions_data(permission_id=False):
    if permission_id:
        permissions = [PermPermission.objects.get(id=permission_id)]
    else:
        permissions = list(PermPermission.objects.all())
    return permissions


@user_has_perms('permissions', 'administer')
def permissions_list(request):
    permissions = permissions_data(request.GET.get('permission_id', False))
    data = list()
    for permission in permissions:
        data.append({'id': permission.id,
                     'name': permission.name,
                     'item': permission.item,
                     'action': permission.action})
    return HttpResponse(json.dumps(data), content_type='application/json')
