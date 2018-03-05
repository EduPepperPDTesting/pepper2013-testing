from django.db import models


class Job(models.Model):
    class Meta:
        db_table = 'queue_job'
    function = models.TextField(blank=False, max_length=255)
    completed = models.IntegerField(blank=False, default=0)
    total = models.IntegerField(blank=False, default=0)


class Tasks(models.Model):
    class Meta:
        db_table = 'queue_task'
    data = models.TextField(blank=False, max_length=255)
    function = models.TextField(blank=False, max_length=255)


