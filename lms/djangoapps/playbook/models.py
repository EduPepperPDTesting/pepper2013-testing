from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        db_table = 'playbook_category'
    
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Catalog(models.Model):
    class Meta:
        db_table = 'playbook_catalog'
    
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class PlaybookTags(models.Model):
    class Meta:
        db_table = 'playbook_playtags'

    name = models.CharField(max_length=100, unique=True, null=False ,blank=False)
    creator = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Play(models.Model):
    class Meta:
        db_table = 'playbook_play'

    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', related_name='category_play')
    duration = models.IntegerField(default=90)
    tip = models.TextField(null=True, blank=True)
    use_conditions = models.BooleanField(default=False)
    catalog = models.ManyToManyField('Catalog', null=True, related_name='catalog_play')
    creator = models.ForeignKey(User, related_name='created_plays')
    modifier = models.ForeignKey(User, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('PlaybookTags', null=True, related_name='playbooktags_play')
    modified_time = models.DateTimeField(auto_now=True)
