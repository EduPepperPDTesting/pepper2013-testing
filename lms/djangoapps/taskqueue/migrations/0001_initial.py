# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tasks'
        db.create_table('queue_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('function', self.gf('django.db.models.fields.TextField')(max_length=255)),
        ))
        db.send_create_signal('taskqueue', ['Tasks'])


    def backwards(self, orm):
        # Deleting model 'Tasks'
        db.delete_table('queue_task')


    models = {
        'taskqueue.tasks': {
            'Meta': {'object_name': 'Tasks', 'db_table': "'queue_task'"},
            'data': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'function': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['taskqueue']