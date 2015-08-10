import datetime
from django.db import models
from student.models import District
from django.contrib.auth.models import User

class ImportTask(models.Model):
    class Meta:
        db_table = 'admin_import_task'    
    filename = models.CharField(blank=False, max_length=255, db_index=True)
    total_lines = models.IntegerField(blank=False,default=0)
    process_lines = models.IntegerField(blank=False,default=0)
    success_lines = models.IntegerField(blank=False,default=0)

class ImportTaskLog(models.Model):
    class Meta:
        db_table = 'admin_import_task_log'
    task = models.ForeignKey(ImportTask,on_delete=models.PROTECT)        
    line = models.IntegerField(blank=False,default=0)
    username = models.CharField(blank=False, max_length=30, db_index=True)
    email = models.CharField(blank=False, max_length=75, db_index=True)
    district_name = models.CharField(blank=False, max_length=255, db_index=True)
    create_date = models.DateTimeField(auto_now_add=True, db_index=False)
    error = models.CharField(blank=False, max_length=255, db_index=True)

class EmailTask(models.Model):
    class Meta:
        db_table = 'admin_email_task'    
    total_emails = models.IntegerField(blank=False,default=0)
    process_emails = models.IntegerField(blank=False,default=0)
    success_emails = models.IntegerField(blank=False,default=0)

class EmailTaskLog(models.Model):
    class Meta:
        db_table = 'admin_email_task_log'
    send_date = models.DateTimeField(auto_now_add=True, db_index=False)        
    task = models.ForeignKey(EmailTask,on_delete=models.PROTECT)        
    username = models.CharField(blank=False, max_length=30, db_index=True)
    email = models.CharField(blank=False, max_length=75, db_index=True)
    district_name = models.CharField(blank=False, max_length=255, db_index=True)
    error = models.CharField(blank=False, max_length=255, db_index=True)

class FilterFavorite(models.Model):
    class Meta:
        db_table = 'admin_filter_favorite'
    
    user = models.ForeignKey(User)
    name = models.CharField(blank=False, max_length=150, db_index=True)
    filter_json = models.CharField(blank=False, max_length=4096, db_index=True)
    
    
