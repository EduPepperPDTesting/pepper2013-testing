# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LDAPSettings'
        db.create_table('ldap_settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('user_dn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('base_dn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('server', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('search_filter', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('pepper_ldap', ['LDAPSettings'])

        # Adding model 'LDAPMappings'
        db.create_table('ldap_mappings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pepper_ldap.LDAPSettings'])),
            ('local_field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ldap_field', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('pepper_ldap', ['LDAPMappings'])


    def backwards(self, orm):
        # Deleting model 'LDAPSettings'
        db.delete_table('ldap_settings')

        # Deleting model 'LDAPMappings'
        db.delete_table('ldap_mappings')


    models = {
        'pepper_ldap.ldapmappings': {
            'Meta': {'object_name': 'LDAPMappings', 'db_table': "'ldap_mappings'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ldap_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'local_field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pepper_ldap.LDAPSettings']"})
        },
        'pepper_ldap.ldapsettings': {
            'Meta': {'object_name': 'LDAPSettings', 'db_table': "'ldap_settings'"},
            'base_dn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'search_filter': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_dn': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['pepper_ldap']