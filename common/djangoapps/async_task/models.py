from django.db import models
from student.models import User


class AsyncTask(models.Model):
    class Meta:
        db_table = 'async_task'
    # type: what mission the async task launched for
    type = models.CharField(max_length=25, db_index=False)
    title = models.CharField(max_length=255, db_index=False)
    last_message = models.CharField(max_length=255, db_index=False)
    # status: started, progress, finished, error
    status = models.CharField(max_length=25, db_index=True)
    create_user = models.ForeignKey(User, null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
