from .models import PermGroup, PermPermission


def has_any_perm(user):
    """
    Check to see if the user has *any* of the Admin Menu permissions.
    :param user: User object.
    :return:
    """
    if has_admin_perm(user):
        return True
    return False


def has_admin_perm(user, item='any', action='any'):
    """
    Check to see what level of permissions a user has (if any).
    :param user: User object.
    :param item: The item on which the user wants to take action.
    :param action: The action we are checking for permissions.
    :return: Boolean if this is a general check, list of available permissions or False, otherwise.
    """
    if user.is_authenticated():
        if user.is_superuser():
            return True

        try:
            if item == 'any':
                permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                       permgrouppermission__permission__isnull=False)
            else:
                if action == 'any':
                    permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                           permgrouppermission__permission__item=item)
                else:
                    permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                           permgrouppermission__permission__item=item,
                                                           permgrouppermission__permission__action=action)
        except:
            return False

        if permissions.count():
            return True
    return False
