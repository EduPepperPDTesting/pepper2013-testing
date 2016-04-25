from django.db import models
from django.conf import settings
import pymongo
import logging
log = logging.getLogger("tracking")


class Reports(models.Model):
    class Meta:
        db_table = 'reporting_reports'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    private = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.SET_NULL)


class Categories(models.Model):
    class Meta:
        db_table = 'reporting_categories'
    name = models.CharField(blank=False, max_length=255, db_index=True)


class Views(models.Model):
    class Meta:
        db_table = 'reporting_views'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    collection = models.CharField(blank=False, max_length=255, db_index=True)


class ReportViews(models.Model):
    class Meta:
        db_table = 'reporting_report_views'
    view = models.ForeignKey(Views, on_delete=models.CASCADE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False, null=False, default=0)


class ViewColumns(models.Model):
    class Meta:
        db_table = 'reporting_view_columns'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    column = models.CharField(blank=False, max_length=255, db_index=True)
    view = models.ForeignKey(Views, on_delete=models.CASCADE)


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
    left = models.ForeignKey(ViewColumns, on_delete=models.PROTECT)
    right = models.ForeignKey(ViewColumns, on_delete=models.PROTECT)
    operator = models.CharField(blank=False, max_length=2)
