"""
Models for Base Info
"""
import json

from django.conf import settings
from django.db import models
from django.db import connection

class Enum(models.Model):
    name = models.CharField(blank=False, max_length=30)
    value = models.IntegerField(blank=False) 
    content = models.CharField(blank=False, max_length=100)
    extend = models.TextField(blank=True, max_length=1024)
    odr = models.IntegerField(blank=False) 

    def getList(self,name):
        self.object.filter(name=name).order_by("odr")

