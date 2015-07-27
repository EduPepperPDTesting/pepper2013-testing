import datetime
from django.db import models
from student.models import District

class ImportTask(models.Model):
    class Meta:
        db_table = 'import_task'    
    filename = models.CharField(blank=False, max_length=255, db_index=True)
    total_lines = models.IntegerField(blank=False,default=0)
    process_lines = models.IntegerField(blank=False,default=0)
    success_lines = models.IntegerField(blank=False,default=0)

class ImportTaskLog(models.Model):
    class Meta:
        db_table = 'import_task_log'
    import_task = models.ForeignKey(ImportTask,on_delete=models.PROTECT)        
    line = models.IntegerField(blank=False,default=0)
    username = models.CharField(blank=False, max_length=30, db_index=True)
    email = models.CharField(blank=False, max_length=75, db_index=True)
    district = models.ForeignKey(District,on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now_add=True, db_index=False)
    error = models.CharField(blank=False, max_length=255, db_index=True)
