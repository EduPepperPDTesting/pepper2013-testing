from django.db import models
from django.contrib.auth.models import User
from communities.models import CommunityCommunities
from file_uploader.models import FileUploads

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

class MessageAlerts (models.Model):
    class Meta:
        db_table = 'webchat_alerts'
    to_user = models.ForeignKey (User, on_delete=models.CASCADE, related_name='messagealerts_to')
    from_user = models.ForeignKey (User, on_delete=models.CASCADE, related_name='messagealerts_from')

class ChatAttachment(models.Model):
    class Meta:
        db_table = 'pepptalk_attachments'
    user_from = models.CharField(blank=False, max_length=255)
    user_to = models.ForeignKey(User, on_delete=models.PROTECT)
    attachment = models.ForeignKey(FileUploads, on_delete=models.PROTECT, null=True, default=None, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, db_index=False)