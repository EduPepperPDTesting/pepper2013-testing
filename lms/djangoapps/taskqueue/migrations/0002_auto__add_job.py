# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table('queue_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('function', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('completed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('taskqueue', ['Job'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table('queue_job')


    models = {
        'taskqueue.job': {
            'Meta': {'object_name': 'Job', 'db_table': "'queue_job'"},
            'completed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'function': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'taskqueue.tasks': {
            'Meta': {'object_name': 'Tasks', 'db_table': "'queue_task'"},
            'data': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'function': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['taskqueue']