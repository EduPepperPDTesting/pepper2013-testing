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
        isPrivate = CommunityCommunities.objects.get(community=community).private
        raise Exception(isPrivate)
    except:
        return False
    return isPrivate