# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Resource.color'
        db.add_column('resource_library_resource', 'color',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True),
                      keep_default=False)

        # Removing index on 'Resource', fields ['logo']
        db.delete_index('resource_library_resource', ['logo'])

        # Removing index on 'Resource', fields ['collection']
        db.delete_index('resource_library_resource', ['collection'])

        # Removing index on 'GenericResource', fields ['color']
        db.delete_index('resource_library_generic_resource', ['color'])

        # Removing index on 'GenericResource', fields ['link']
        db.delete_index('resource_library_generic_resource', ['link'])

        # Removing index on 'GenericResource', fields ['logo']
        db.delete_index('resource_library_generic_resource', ['logo'])


    def backwards(self, orm):
        # Adding index on 'GenericResource', fields ['logo']
        db.create_index('resource_library_generic_resource', ['logo'])

        # Adding index on 'GenericResource', fields ['link']
        db.create_index('resource_library_generic_resource', ['link'])

        # Adding index on 'GenericResource', fields ['color']
        db.create_index('resource_library_generic_resource', ['color'])

        # Adding index on 'Resource', fields ['collection']
        db.create_index('resource_library_resource', ['collection'])

        # Adding index on 'Resource', fields ['logo']
        db.create_index('resource_library_resource', ['logo'])

        # Deleting field 'Resource.color'
        db.delete_column('resource_library_resource', 'color')


    models = {
        'access_resource_library.genericresource': {
            'Meta': {'object_name': 'GenericResource', 'db_table': "'resource_library_generic_resource'"},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['access_resource_library.Resource']", 'on_delete': 'models.PROTECT'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'access_resource_library.resource': {
            'Meta': {'object_name': 'Resource', 'db_table': "'resource_library_resource'"},
            'collection': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'collection_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['access_resource_library']