from .models import PermGroup


def check_user_perms(user, items='any', actions='any', access_level='any', exclude_superuser=False):
    """
    Check to see what level of permissions a user has (if any). If called with just a user, it'll check to see if the
    user has *any* permissions.
    :param user: User object.
    :param items: List of the items (or single item) on which the user wants to take action.
    :param actions: List of the actions (or a single action) we are checking for permissions.
    :param access_level: The level of this access.
    :param exclude_superuser: Set to True if you want to exclude the superuser override.
    :return: Boolean if this is a general check, list of available permissions or False, otherwise.
    """
    if user.is_authenticated():
        if not exclude_superuser and user.is_superuser:
            return True

        try:
            kwargs = {'permgroupmember__user': user}
            if items == 'any':
                kwargs.update({'permgrouppermission__permission__isnull': False})
            else:
                if type(items) is str:
                    items = [items]
                kwargs.update({'permgrouppermission__permission__item__in': items})
                if actions != 'any':
                    if type(actions) is str:
                        actions = [actions]
                    kwargs.update({'permgrouppermission__permission__action__in': actions})
                if access_level != 'any':
                    if type(access_level) is str:
                        access_level = [access_level]
                    kwargs.update({'permgrouppermission__permission__access_level__in': access_level})
            permissions = PermGroup.objects.filter(**kwargs).count()
            if permissions:
                return True
        except:
            return False

    return False


def check_access_level(user, items, actions):
    """
    Check to see what level of access a user has. This will return the highest level of access assigned to the user if
    they have multiple levels.
    :param user: User object.
    :param items: List of the items (or single item) on which the user wants to take action.
    :param actions: List of the actions (or a single action) we are checking for permissions.
    :return: False if the don't have access, the name of the highest access level otherwise.
    """

    if user.is_superuser:
        return 'System'

    if type(items) is str:
        items = [items]
    if type(actions) is str:
        actions = [actions]
    try:
        permissions = PermGroup.objects.filter(permgroupmember__user=user,
                                               permgrouppermission__permission__item__in=items,
                                               permgrouppermission__permission__action__in=actions)
        count = permissions.count()
    except:
        return False

    if count == 1:
        return permissions[0].access_level

    levels = {'System': 0, 'State': 1, 'District': 2, 'School': 3}
    level = 3
    level_name = 'School'
    for permission in permissions:
        if levels[permission.access_level] < level:
            level = levels[permission.access_level]
            level_name = permission.access_level
    return level_name
