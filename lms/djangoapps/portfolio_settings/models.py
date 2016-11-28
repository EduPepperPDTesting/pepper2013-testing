from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import logging
log = logging.getLogger("tracking")


class ProtfolioPermissions(models.Model):
    class Meta:
        db_table = 'protfolio_permissions'
    user_id = models.IntegerField(blank=False, max_length=11)
    course_id = models.CharField(blank=False, max_length=255)
    permission_level = models.CharField(blank=False, null=True, max_length=50)