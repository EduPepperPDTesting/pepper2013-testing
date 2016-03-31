from django.db import models


class Resource(models.Model):
    class Meta:
        db_table = 'resource_library_resource'
    collection_type = models.CharField(blank=False, max_length=50, db_index=True)
    collection = models.CharField(blank=False, max_length=255, db_index=False)
    logo = models.CharField(blank=False, max_length=255, db_index=False)
    title = models.CharField(blank=False, max_length=255, db_index=True)
    color = models.CharField(blank=True, max_length=6, db_index=False)


class GenericResource(models.Model):
    class Meta:
        db_table = 'resource_library_generic_resource'
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    logo = models.CharField(blank=False, max_length=255, db_index=False)
    title = models.CharField(blank=False, max_length=255, db_index=True)
    color = models.CharField(blank=True, max_length=6, db_index=False)
    link = models.CharField(blank=False, max_length=255, db_index=False)

