from django.db import models


def file_upload_location(instance, filename):
    path = instance.type
    if instance.sub_type:
        path += '/{0}'.format(instance.sub_type)
    path += '/{0}'.format(filename)
    return path


class FileUploads(models.Model):
    class Meta:
        db_table = 'file_uploads'
    upload = models.FileField(upload_to=file_upload_location)

    type = None
    sub_type = None
