# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FileUploads'
        db.create_table('file_uploads', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upload', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('file_uploader', ['FileUploads'])


    def backwards(self, orm):
        # Deleting model 'FileUploads'
        db.delete_table('file_uploads')


    models = {
        'file_uploader.fileuploads': {
            'Meta': {'object_name': 'FileUploads', 'db_table': "'file_uploads'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['file_uploader']