# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Categories'
        db.create_table('reporting_categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('reporting', ['Categories'])

        # Adding model 'Reports'
        db.create_table('reporting_reports', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.Categories'], null=True, on_delete=models.SET_NULL)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('reporting', ['Reports'])

        # Adding model 'Views'
        db.create_table('reporting_views', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('collection', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('reporting', ['Views'])

        # Adding model 'ViewColumns'
        db.create_table('reporting_view_columns', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('column', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.Views'])),
        ))
        db.send_create_signal('reporting', ['ViewColumns'])

        # Adding model 'ViewRelationships'
        db.create_table('reporting_view_relationships', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('left', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewrelationships_left', on_delete=models.PROTECT, to=orm['reporting.ViewColumns'])),
            ('right', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewrelationships_right', on_delete=models.PROTECT, to=orm['reporting.ViewColumns'])),
        ))
        db.send_create_signal('reporting', ['ViewRelationships'])

        # Adding model 'ReportViews'
        db.create_table('reporting_report_views', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.Views'])),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.Reports'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('reporting', ['ReportViews'])

        # Adding model 'ReportViewColumns'
        db.create_table('reporting_report_view_columns', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.Reports'])),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.ViewColumns'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('reporting', ['ReportViewColumns'])

        # Adding model 'ReportFilters'
        db.create_table('reporting_report_filters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reporting.Reports'])),
            ('conjunction', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('left', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reportfilters_left', on_delete=models.PROTECT, to=orm['reporting.ViewColumns'])),
            ('right', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reportfilters_right', on_delete=models.PROTECT, to=orm['reporting.ViewColumns'])),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('reporting', ['ReportFilters'])


    def backwards(self, orm):
        # Deleting model 'Categories'
        db.delete_table('reporting_categories')

        # Deleting model 'Reports'
        db.delete_table('reporting_reports')

        # Deleting model 'Views'
        db.delete_table('reporting_views')

        # Deleting model 'ViewColumns'
        db.delete_table('reporting_view_columns')

        # Deleting model 'ViewRelationships'
        db.delete_table('reporting_view_relationships')

        # Deleting model 'ReportViews'
        db.delete_table('reporting_report_views')

        # Deleting model 'ReportViewColumns'
        db.delete_table('reporting_report_view_columns')

        # Deleting model 'ReportFilters'
        db.delete_table('reporting_report_filters')


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
        'reporting.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'reporting.reportfilters': {
            'Meta': {'object_name': 'ReportFilters', 'db_table': "'reporting_report_filters'"},
            'conjunction': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reportfilters_left'", 'on_delete': 'models.PROTECT', 'to': "orm['reporting.ViewColumns']"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.Reports']"}),
            'right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reportfilters_right'", 'on_delete': 'models.PROTECT', 'to': "orm['reporting.ViewColumns']"})
        },
        'reporting.reports': {
            'Meta': {'object_name': 'Reports'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.Categories']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'reporting.reportviewcolumns': {
            'Meta': {'object_name': 'ReportViewColumns', 'db_table': "'reporting_report_view_columns'"},
            'column': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.ViewColumns']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.Reports']"})
        },
        'reporting.reportviews': {
            'Meta': {'object_name': 'ReportViews', 'db_table': "'reporting_report_views'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.Reports']"}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.Views']"})
        },
        'reporting.viewcolumns': {
            'Meta': {'object_name': 'ViewColumns', 'db_table': "'reporting_view_columns'"},
            'column': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reporting.Views']"})
        },
        'reporting.viewrelationships': {
            'Meta': {'object_name': 'ViewRelationships', 'db_table': "'reporting_view_relationships'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewrelationships_left'", 'on_delete': 'models.PROTECT', 'to': "orm['reporting.ViewColumns']"}),
            'right': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewrelationships_right'", 'on_delete': 'models.PROTECT', 'to': "orm['reporting.ViewColumns']"})
        },
        'reporting.views': {
            'Meta': {'object_name': 'Views'},
            'collection': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['reporting']