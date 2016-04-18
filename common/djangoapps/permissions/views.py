from mitxmako.shortcuts import render_to_response
from .models import PermGroup, PermGroupMember, PermPermission, PermGroupPermission
import json
from django.http import HttpResponse
from django_future.csrf import ensure_csrf_cookie
from django.db import IntegrityError
from .decorators import user_has_perms
from .utils import check_user_perms
from student.models import User
from pepper_utilities.utils import get_request_array


@user_has_perms('permissions', 'administer')
def permissions_view(request):
    permissions = permissions_data()
    groups = group_data()
    admin_rights = check_user_perms(request.user, 'permissions', 'administer')
    assign_rights = check_user_perms(request.user, 'permissions', ['administer', 'assign'])
    data = {'permissions': permissions,
            'groups': groups,
            'admin_rights': admin_rights,
            'assign_rights': assign_rights}
    return render_to_response('permissions/permissions.html', data)


@user_has_perms('permissions', 'administer')
def group_check(request):
    valid = True
    error = ''
    if PermGroup.objects.filter(name=request.GET.get('name'), type=request.GET.get('type')).count():
        valid = False
        error = 'This name/type is already in use.'
    return HttpResponse(json.dumps({'Valid': valid, 'Error': error}), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_add(request):
    name = request.POST.get('name', False)
    group_id = request.POST.get('group_id', False)
    group_type = request.POST.get('group_type', None)
    if name:
        if group_id:
            group = PermGroup.objects.get(id=group_id)
        else:
            group = PermGroup()
        group.name = name
        group.type = group_type
        group.save()
        data = {'Success': True}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_delete(request):
    try:
        group_ids = get_request_array(request.POST, 'group_id')
        for group_id in group_ids:
            group = PermGroup.objects.get(id=group_id)
            group.delete()
        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': ''.format(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_permission_add(request):
    group_id = int(request.POST.get('group', False))
    group = PermGroup.objects.get(id=group_id)
    permission_id = int(request.POST.get('permission', False))
    permission = PermPermission.objects.get(id=permission_id)
    if permission and group:
        try:
            group_permission = PermGroupPermission()
            group_permission.group = group
            group_permission.permission = permission
            group_permission.save()
            data = {'Success': True}
        except IntegrityError as e:
            data = {'Success': False, 'Error': 'duplicate'}
        except Exception as e:
            data = {'Success': False, 'Error': ''.format(e)}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_permission_delete(request):
    try:
        group_permission_ids = get_request_array(request.POST, 'group_permission_id')
        for group_permission_id in group_permission_ids:
            group_permission = PermGroupPermission.objects.get(id=group_permission_id)
            group_permission.delete()
        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': ''.format(e)}
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
            try:
                group_member = PermGroupMember()
                group_member.group = group
                group_member.user = user
                group_member.save()
                data = {'Success': True}
            except IntegrityError as e:
                data = {'Success': False, 'Error': 'duplicate'}
            except Exception as e:
                data = {'Success': False, 'Error': ''.format(e)}
        elif state:
            if school:
                users = User.objects.filter(profile__school=school)
            elif district:
                users = User.objects.filter(profile__district=district)
            else:
                users = User.objects.filter(profile__district__state=state)
            errors = list()
            for user in users:
                try:
                    group_member = PermGroupMember()
                    group_member.group = group
                    group_member.user = user
                    group_member.save()
                except IntegrityError as e:
                    errors.append('duplicate')
                except Exception as e:
                    errors.append(''.format(e))
            if len(errors):
                data = {'Success': True, 'Errors': errors}
                if len(errors) == users.count():
                    data['Success'] = False
            else:
                data = {'Success': True}
        else:
            data = {'Success': False}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def group_member_delete(request):
    try:
        group_member_ids = get_request_array(request.POST, 'group_member_id')
        for group_member_id in group_member_ids:
            group_member = PermGroupMember.objects.get(id=group_member_id)
            group_member.delete()
        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': ''.format(e)}
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
        data.append({'id': group.id, 'name': group.name, 'type': group.type})
    return HttpResponse(json.dumps(data), content_type='application/json')


@user_has_perms('permissions', 'administer')
def group_member_list(request):
    group = PermGroup.objects.get(id=request.GET.get('group_id'))
    group_members = PermGroupMember.objects.prefetch_related().filter(group=group)
    member_list = list()
    for member in group_members:
        member_dict = dict()
        try:
            member_dict.update({'user_id': member.user.id})
        except:
            pass
        try:
            member_dict.update({'first_name': member.user.first_name})
        except:
            pass
        try:
            member_dict.update({'last_name': member.user.last_name})
        except:
            pass
        try:
            member_dict.update({'email': member.user.email})
        except:
            pass
        try:
            member_dict.update({'district': member.user.profile.district.name})
        except:
            pass
        try:
            member_dict.update({'state': member.user.profile.district.state.name})
        except:
            pass
        try:
            member_dict.update({'school': member.user.profile.school.name})
        except:
            pass
        member_list.append(member_dict)
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
    permission_id = request.POST.get('permission_id', False)
    if name and item and action:
        if permission_id:
            permission = PermPermission.objects.get(id=permission_id)
        else:
            permission = PermPermission()
        try:
            permission.name = name
            permission.item = item
            permission.action = action
            permission.save()
            data = {'Success': True}
        except Exception as e:
            data = {'Success': False, 'Error': ''.format(e)}
    else:
        data = {'Success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')


@ensure_csrf_cookie
@user_has_perms('permissions', 'administer')
def permission_delete(request):
    try:
        permission_ids = get_request_array(request.POST, 'permission_id')
        for permission_id in permission_ids:
            permission = PermPermission.objects.get(id=permission_id)
            permission.delete()
        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': ''.format(e)}
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
