from .models import CommunityUsers


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
