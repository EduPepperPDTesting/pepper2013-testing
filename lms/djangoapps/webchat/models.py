from django.db import models
from django.contrib.auth.models import User
from communities.models import CommunityCommunities

class CommunityWebchat (models.Model):
    class Meta:
        db_table = 'community_webchat'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)

class UserWebchat (models.Model):
    class Meta:
        db_table = 'auth_user_webchat'
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)