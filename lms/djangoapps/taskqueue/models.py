from django.db import models


class Tasks(models.Model):
    class Meta:
        db_table = 'queue_task'
    data = models.TextField(blank=False, max_length=255)
    function = models.TextField(blank=False, max_length=255)
