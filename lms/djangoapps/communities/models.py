from django.db import models
from django.contrib.auth.models import User


class CommunityCommunities(models.Model):
    class Meta:
        db_table = 'community_communities'
    community = models.CharField(blank=False, max_length=255, db_index=True, unique=True)
    name = models.CharField(blank=False, max_length=255, db_index=True)
    motto = models.CharField(blank=False, max_length=255, db_index=True)
    logo = models.CharField(blank=False, max_length=255, db_index=True)
    private = models.BooleanField(blank=False, default=0)


class CommunityUsers(models.Model):
    class Meta:
        db_table = 'community_users'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    facilitator = models.BooleanField(blank=False, default=0)


class CommunityCourses(models.Model):
    class Meta:
        db_table = 'community_courses'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.PROTECT)
    course = models.CharField(blank=False, max_length=255)


class CommunityResources(models.Model):
    class Meta:
        db_table = 'community_resources'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.PROTECT)
    name = models.CharField(blank=False, max_length=255, db_index=True)
    link = models.CharField(blank=False, max_length=255, db_index=True)
    logo = models.CharField(blank=False, max_length=255, db_index=True)


class CommunityDiscussions(models.Model):
    class Meta:
        db_table = 'community_discussions'
    community = models.ForeignKey(CommunityCommunities, on_delete=models.PROTECT)
    subject = models.CharField(blank=False, max_length=255, db_index=True)
    post = models.TextField(blank=False, max_length=255, db_index=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=False, db_index=False)
    link = models.CharField(blank=False, max_length=255, db_index=False)


class CommunityDiscussionReplies(models.Model):
    class Meta:
        db_table = 'community_discussion_replies'
    discussion = models.ForeignKey(CommunityDiscussions, on_delete=models.PROTECT)
    subject = models.CharField(blank=False, max_length=255, db_index=True)
    post = models.TextField(blank=False, max_length=255, db_index=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=False, db_index=False)
    link = models.CharField(blank=False, max_length=255, db_index=False)
