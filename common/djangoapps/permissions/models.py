from django.db import models
from django.contrib.auth.models import User


class PermPermission(models.Model):
    class Meta:
        db_table = 'perm_permission'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    item = models.CharField(blank=False, max_length=255, db_index=True)
    action = models.CharField(blank=False, max_length=255, db_index=True)


class PermGroup(models.Model):
    class Meta:
        db_table = 'perm_group'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    type = models.CharField(max_length=10, null=False, default='System')


class PermGroupMember(models.Model):
    class Meta:
        db_table = 'perm_group_membership'
        unique_together = ('user', 'group')
    user = models.ForeignKey(User)
    group = models.ForeignKey(PermGroup)


class PermGroupPermission(models.Model):
    class Meta:
        db_table = 'perm_group_permission'
        unique_together = ('permission', 'group')
    permission = models.ForeignKey(PermPermission)
    group = models.ForeignKey(PermGroup)
