from django.db import models
from django.contrib.auth.models import User
from student.models import District, State
from file_uploader.models import FileUploads


class CommunityCommunities(models.Model):
    class Meta:
        db_table = 'community_communities'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    motto = models.CharField(blank=False, max_length=255, db_index=True)
    logo = models.ForeignKey(FileUploads, on_delete=models.PROTECT, null=True, default=None, blank=True)
    hangout = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    private = models.BooleanField(blank=False, default=0)
    discussion_priority = models.BooleanField(blank=False, default=0)


class CommunityUsers(models.Model):
    class Meta:
        db_table = 'community_users'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    facilitator = models.BooleanField(blank=False, default=0)


class CommunityCourses(models.Model):
    class Meta:
        db_table = 'community_courses'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.CASCADE)
    course = models.CharField(blank=False, max_length=255)


class CommunityResources(models.Model):
    class Meta:
        db_table = 'community_resources'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=255, db_index=True)
    link = models.CharField(blank=False, max_length=255, db_index=True)
    logo = models.ForeignKey(FileUploads, on_delete=models.PROTECT, null=True, default=None, blank=True)


class CommunityDiscussions(models.Model):
    class Meta:
        db_table = 'community_discussions'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.CASCADE)
    subject = models.CharField(blank=False, max_length=255, db_index=True)
    post = models.TextField(blank=False, max_length=255, db_index=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=True, db_index=False)
    date_reply = models.DateTimeField(auto_now_add=True, db_index=False)
    attachment = models.ForeignKey(FileUploads, on_delete=models.PROTECT, null=True, default=None, blank=True)


class CommunityDiscussionReplies(models.Model):
    class Meta:
        db_table = 'community_discussion_replies'
    discussion = models.ForeignKey(CommunityDiscussions, on_delete=models.CASCADE)
    subject = models.CharField(blank=False, max_length=255, db_index=True)
    post = models.TextField(blank=False, max_length=255, db_index=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=True, db_index=False)
    attachment = models.ForeignKey(FileUploads, on_delete=models.PROTECT, null=True, default=None, blank=True)


class CommunityNotificationGroup(models.Model):
    class Meta:
        db_table = 'community_notification_group'
    name = models.CharField(blank=True, null=True, max_length=20, db_index=False)
    description = models.TextField(blank=False, max_length=255, db_index=False)


class CommunityNotificationType(models.Model):
    class Meta:
        db_table = 'community_notification_type'
    name = models.CharField(blank=True, null=True, max_length=20, db_index=False)
    description = models.TextField(blank=False, max_length=255, db_index=False)
    group = models.ForeignKey(CommunityNotificationGroup, on_delete=models.PROTECT)
    subject = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    body = models.TextField(blank=True, null=True, db_index=False)
    action = models.CharField(blank=True, null=True, max_length=255, db_index=False)


class CommunityNotificationConfig(models.Model):
    class Meta:
        db_table = 'community_notification_config'
    via_pepper = models.BooleanField(blank=False, default=0)
    via_email = models.BooleanField(blank=False, default=0)
    type = models.ForeignKey(CommunityNotificationType, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    frequency = models.CharField(max_length=20, db_index=False, default="")
    self_config = models.BooleanField(blank=False, default=0)


class CommunityNotificationAudit(models.Model):
    class Meta:
        db_table = 'community_notification_audit'
    subject = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    body = models.TextField(blank=False, db_index=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    create_date = models.DateTimeField(auto_now_add=False, db_index=False)
    send_date = models.DateTimeField(auto_now_add=False, db_index=False)
    sent = models.BooleanField(blank=False, default=0)


class CommunityPosts(models.Model):
    class Meta:
        db_table = 'community_posts'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(blank=False, max_length=255, db_index=False)
    date_create = models.DateTimeField(auto_now_add=True, db_index=False)
    date_update = models.DateTimeField(auto_now_add=True, db_index=False)
    # @author:scott
    # @date:2017-02-27
    top = models.BooleanField(blank=False, default=0)
    # @end

class CommunityPostsImages(models.Model):
    class Meta:
        db_table = 'community_posts_images'
    post = models.ForeignKey(CommunityPosts, on_delete=models.CASCADE)
    link = models.TextField(blank=False, max_length=1024, null=False)
    embed = models.BooleanField(blank=False, default=1)


class CommunityComments(models.Model):
    class Meta:
        db_table = 'community_posts_comments'
    post = models.ForeignKey(CommunityPosts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, max_length=255, db_index=False)
    sub_comment = models.ForeignKey("self", on_delete=models.CASCADE, default=None, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, db_index=False)


class CommunityLikes(models.Model):
    class Meta:
        db_table = 'community_posts_likes'
    post = models.ForeignKey(CommunityPosts, on_delete=models.CASCADE, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommunityComments, on_delete=models.CASCADE, null=True, blank=True, default=None)
    date_create = models.DateTimeField(auto_now_add=True, db_index=False)
