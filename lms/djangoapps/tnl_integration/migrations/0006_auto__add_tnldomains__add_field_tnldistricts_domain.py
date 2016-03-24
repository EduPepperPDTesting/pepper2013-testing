# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TNLDomains'
        db.create_table('tnl_domains', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.State'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('grades', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('base_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('admin_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('provider_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('edagancy_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('credit_value_type_id', self.gf('django.db.models.fields.IntegerField')()),
            ('credit_area_id', self.gf('django.db.models.fields.IntegerField')()),
            ('credit_value', self.gf('django.db.models.fields.IntegerField')()),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('tnl_integration', ['TNLDomains'])

        # Adding field 'TNLDistricts.domain'
        db.add_column('tnl_districts', 'domain',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['tnl_integration.TNLDomains']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'TNLDomains'
        db.delete_table('tnl_domains')

        # Deleting field 'TNLDistricts.domain'
        db.delete_column('tnl_districts', 'domain_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student.district': {
            'Meta': {'object_name': 'District', 'db_table': "'district'"},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.State']", 'on_delete': 'models.PROTECT'})
        },
        'student.state': {
            'Meta': {'object_name': 'State', 'db_table': "'state'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'so': ('django.db.models.fields.IntegerField', [], {})
        },
        'tnl_integration.tnlcompletiontrack': {
            'Meta': {'object_name': 'TNLCompletionTrack', 'db_table': "'tnl_completion_track'"},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tnl_integration.TNLCourses']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
        },
        'tnl_integration.tnlcourses': {
            'Meta': {'object_name': 'TNLCourses', 'db_table': "'tnl_courses'"},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'section_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'tnl_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'tnl_integration.tnldistricts': {
            'Meta': {'object_name': 'TNLDistricts', 'db_table': "'tnl_districts'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['student.District']"}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['tnl_integration.TNLDomains']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tnl_integration.tnldomains': {
            'Meta': {'object_name': 'TNLDomains', 'db_table': "'tnl_domains'"},
            'admin_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'base_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'credit_area_id': ('django.db.models.fields.IntegerField', [], {}),
            'credit_value': ('django.db.models.fields.IntegerField', [], {}),
            'credit_value_type_id': ('django.db.models.fields.IntegerField', [], {}),
            'edagancy_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'grades': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.State']"})
        }
    }

    complete_apps = ['tnl_integration']