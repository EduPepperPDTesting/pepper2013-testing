from .models import PermGroup


def has_any_perm(user):
    """
    Check to see if the user has *any* of the Admin Menu permissions.
    :param user: User object.
    :return:
    """
    if has_admin_perm(user):
        return True
    return False


def has_admin_perm(user, item='any', action='read'):
    """
    Check to see what level of permissions a user has (if any).
    :param user: User object.
    :param item: The item on which the user wants to take action.
    :param action: The action we are checking for permissions.
    :return:
    """
    try:
        if item == 'any':
            permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                   permgrouppermission__permission__isnull=False)
        else:
            permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                   permgrouppermission__permission__item=item,
                                                   permgrouppermission__permission__action=action)
    except:
        return False

    permissions_return = []
    if permissions.count():
        if item == 'any':
            return True
        else:
            for permission in permissions:
                permissions_return.append(permission.action)
            return permissions_return
    return False
