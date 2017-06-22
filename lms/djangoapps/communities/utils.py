from .models import CommunityUsers, CommunityCommunities


def is_facilitator(user, community):
    try:
        CommunityUsers.objects.get(community=community, user=user, facilitator=True)
    except:
        return False
    return True


def is_member(user, community):
    try:
        CommunityUsers.objects.get(community=community, user=user)
    except:
        return False
    return True

def is_private(community):
    try:
        isPrivate = True if CommunityCommunities.objects.get(community=community).private == '1' else False
    except:
        return False
    return isPrivate