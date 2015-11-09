import datetime
from django.db import models
from django.contrib.auth.models import User
from student.models import District


class TNLCourses(models.Model):
    class Meta:
        db_table = 'tnl_courses'
    course = models.CharField(max_length=255, db_index=True)
    tnl_id = models.CharField(null=False, max_length=255, db_index=True)
    section_id = models.CharField(null=False, max_length=255, db_index=True)
    registered = models.BooleanField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, db_index=False)
    registration_date = models.DateTimeField(null=True, db_index=False)


class TNLDistricts(models.Model):
    class Meta:
        db_table = 'tnl_districts'
    district = models.ForeignKey(District, default=0)
    date_added = models.DateTimeField(auto_now_add=True, db_index=False)


class TNLCompletionTrack(models.Model):
    class Meta:
        db_table = 'tnl_completion_track'
    user = models.ForeignKey(User, default=0)
    course = models.ForeignKey(TNLCourses)
    registered = models.BooleanField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, db_index=False)
    registration_date = models.DateTimeField(null=True, db_index=False)
