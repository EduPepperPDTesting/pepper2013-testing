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
        CommunityUsers.objects.get(community=community, community__private=True)
    except:
        return False
    return True