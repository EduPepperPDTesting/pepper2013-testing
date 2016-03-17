from mitxmako.shortcuts import render_to_response, render_to_string, reverse
from .models import PermGroup, PermGroupMember, PermPermission, PermGroupPermission
import json
from django.http import HttpResponse, HttpResponseForbidden
from .decorators import user_has_perms


@user_has_perms('permissions', 'administer')
def permissions_view(request):
    permissions = permissions_data()
    groups = group_data()
    data = {'permissions': permissions,
            'groups': groups}
    return render_to_response('permissions/permissions.html', data)


def group_data(group_id=False):
    if group_id:
        groups = [PermGroup.objects.get(id=group_id)]
    else:
        groups = list(PermGroup.objects.all())
    return groups


@user_has_perms('permissions', 'administer')
def group_list(request):
    groups = group_data(request.GET.get('group_id', False))
    return HttpResponse(json.dumps(groups), content_type='application/json')


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
                            'district': member.user.userprofile.district.name,
                            'state': member.user.userprofile.district.state.name,
                            'school': member.user.userprofile.school.name})
    return HttpResponse(json.dumps(member_list), content_type='application/json')


@user_has_perms('permissions', 'administer')
def group_permissions_list(request):
    group = PermGroup.objects.get(id=request.GET.get('group_id'))
    permissions = PermGroupPermission.objects.filter(group=group)
    permission_list = list()
    for permission in permissions:
        permission_list.append({'permission_id': permission.permission.id,
                                'name': permission.permission.name})
    return HttpResponse(json.dumps(permission_list), content_type='application/json')


def permissions_data(permission_id=False):
    if permission_id:
        permissions = [PermPermission.objects.get(id=permission_id)]
    else:
        permissions = list(PermPermission.objects.all())
    return permissions


@user_has_perms('permissions', 'administer')
def permissions_list(request):
    permissions = permissions_data(request.GET.get('permission_id'))
    return HttpResponse(json.dumps(permissions), content_type='application/json')
