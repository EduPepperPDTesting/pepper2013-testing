import datetime
from django.db import models
from django.contrib.auth.models import User


class TNLCourses(models.Model):
    class Meta:
        db_table = 'tnl_courses'
    course = models.CharField(blank=False, max_length=255, db_index=True)
    tnl_id = models.CharField(blank=True, max_length=255, db_index=False)
    registered = models.BooleanField(blank=False, default=0)
    date_added = models.DateTimeField(auto_now_add=True, db_index=False)
    registration_date = models.DateTimeField(blank=True, db_index=False)


class TNLCompletionTrack(models.Model):
    class Meta:
        db_table = 'tnl_completion_track'
    user = models.ForeignKey(User, default=0)
    course = models.ForeignKey(TNLCourses)
    registered = models.BooleanField(blank=False, default=0)
    date_added = models.DateTimeField(auto_now_add=True, db_index=False)
    registration_date = models.DateTimeField(blank=True, db_index=False)
