from django.db import models
from student.models import User
from django.conf import settings
import pymongo
import logging
log = logging.getLogger("tracking")


class Categories(models.Model):
    class Meta:
        db_table = 'reporting_categories'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    order = models.IntegerField(default=0)


class Reports(models.Model):
    class Meta:
        db_table = 'reporting_reports'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    category = models.ForeignKey(Categories, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)


class Views(models.Model):
    class Meta:
        db_table = 'reporting_views'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    collection = models.CharField(blank=False, max_length=255, db_index=True)


class ViewColumns(models.Model):
    class Meta:
        db_table = 'reporting_view_columns'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    column = models.CharField(blank=False, max_length=255, db_index=True)
    view = models.ForeignKey(Views, on_delete=models.CASCADE)


class ViewRelationships(models.Model):
    class Meta:
        db_table = 'reporting_view_relationships'
    left = models.ForeignKey(ViewColumns, on_delete=models.PROTECT, related_name='viewrelationships_left')
    right = models.ForeignKey(ViewColumns, on_delete=models.PROTECT, related_name='viewrelationships_right')


class ReportViews(models.Model):
    class Meta:
        db_table = 'reporting_report_views'
    view = models.ForeignKey(Views, on_delete=models.CASCADE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False, null=False, default=0)


class ReportViewColumns(models.Model):
    class Meta:
        db_table = 'reporting_report_view_columns'
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    column = models.ForeignKey(ViewColumns, on_delete=models.PROTECT)


class ReportFilters(models.Model):
    class Meta:
        db_table = 'reporting_report_filters'
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    conjunction = models.CharField(blank=True, null=True, max_length=3)
    column = models.ForeignKey(ViewColumns, on_delete=models.PROTECT)
    value = models.CharField(blank=False, max_length=255)
    operator = models.CharField(blank=False, max_length=2)
    order = models.IntegerField(blank=False, null=False, default=0)
