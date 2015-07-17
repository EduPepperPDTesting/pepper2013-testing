from django.db import models

class ImportTask(models.Model):
    class Meta:
        db_table = 'import_task'    
    filename = models.CharField(blank=False, max_length=255, db_index=True)
    total_lines = models.IntegerField(blank=False,default=0)
    process_lines = models.IntegerField(blank=False,default=0)
    success_lines = models.IntegerField(blank=False,default=0)

class ImportTaskError(models.Model):
    class Meta:
        db_table = 'import_task_error'
    import_task = models.ForeignKey(ImportTask,on_delete=models.PROTECT)        
    error = models.CharField(blank=False, max_length=255, db_index=True)
    line = models.IntegerField(blank=False,default=0)
