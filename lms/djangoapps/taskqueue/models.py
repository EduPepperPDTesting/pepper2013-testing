from django.db import models


class Tasks(models.Model):
    class Meta:
        db_table = 'queue_task'
    data = models.TextField(blank=False, max_length=255)
    function = models.TextField(blank=False, max_length=255)
    job = models.ForeignKey(Job, on_delete=models.PROTECT)


class Job(models.Model):
    class Meta:
        db_table = 'queue_table'
    function = models.TextField(blank=False, max_length=255)
    completed = models.IntegerField(blank=False, default=0)
    total = models.IntegerField(blank=False, default=0)
