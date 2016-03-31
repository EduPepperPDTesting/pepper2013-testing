from .models import PermGroup


def check_user_perms(user, items='any', actions='any', exclude_superuser=False):
    """
    Check to see what level of permissions a user has (if any). If called with just a user, it'll check to see if the
    user has *any* permissions.
    :param user: User object.
    :param items: List of the items (or single item) on which the user wants to take action.
    :param actions: List of the actions (or a single action) we are checking for permissions.
    :param exclude_superuser: Set to True if you want to exclude the superuser override.
    :return: Boolean if this is a general check, list of available permissions or False, otherwise.
    """
    if user.is_authenticated():
        if not exclude_superuser and user.is_superuser:
            return True

        try:
            if items == 'any':
                permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                       permgrouppermission__permission__isnull=False)
            else:
                if type(items) is str:
                    items = [items]
                if actions == 'any':
                    permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                           permgrouppermission__permission__item__in=items)
                else:
                    if type(actions) is str:
                        actions = [actions]
                    permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                                           permgrouppermission__permission__item__in=items,
                                                           permgrouppermission__permission__action__in=actions)
            if permissions.count():
                return True
        except:
            return False

    return False
