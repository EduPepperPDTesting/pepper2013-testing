# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tasks.job'
        db.add_column('queue_task', 'job',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['taskqueue.Job'], on_delete=models.PROTECT),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tasks.job'
        db.delete_column('queue_task', 'job_id')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taskqueue.Job']", 'on_delete': 'models.PROTECT'})
        }
    }

    complete_apps = ['taskqueue']