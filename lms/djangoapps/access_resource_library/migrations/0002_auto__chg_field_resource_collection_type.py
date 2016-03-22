# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Resource.collection_type'
        db.alter_column('resource_library_resource', 'collection_type', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Resource.collection_type'
        db.alter_column('resource_library_resource', 'collection_type', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'access_resource_library.genericresource': {
            'Meta': {'object_name': 'GenericResource', 'db_table': "'resource_library_generic_resource'"},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['access_resource_library.Resource']", 'on_delete': 'models.PROTECT'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'access_resource_library.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'resource_library_resource'"},
            'collection': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'collection_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['access_resource_library']