from django.db import models
# from student.models import District, School, State
# from django.contrib.auth.models import User
# from student.models import UserProfile
# from django.conf import settings
# import pymongo
# import logging
# log = logging.getLogger("tracking")


class LDAPSettings(models.Model):
    class Meta:
        db_table = 'ldap_settings'
    name = models.CharField(blank=False, max_length=255, db_index=True, unique=True)
    user_dn = models.CharField(blank=False, max_length=255, db_index=False)
    base_dn = models.CharField(blank=False, max_length=255, db_index=False)
    server = models.CharField(blank=False, max_length=255, db_index=False)
    search_filter = models.CharField(blank=False, max_length=255, db_index=False)


class LDAPMappings(models.Model):
    class Meta:
        db_table = 'ldap_mappings'
    settings = models.ForeignKey(LDAPSettings)
    local_field = models.CharField(blank=False, max_length=255, db_index=False)
    ldap_field = models.CharField(blank=False, max_length=255, db_index=False)
