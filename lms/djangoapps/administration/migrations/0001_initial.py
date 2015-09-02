# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImportTask'
        db.create_table('admin_import_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('total_lines', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('process_lines', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('success_lines', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('task_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('administration', ['ImportTask'])

        # Adding model 'ImportTaskLog'
        db.create_table('admin_import_task_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['administration.ImportTask'], on_delete=models.PROTECT)),
            ('line', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=75, db_index=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('administration', ['ImportTaskLog'])

        # Adding model 'EmailTask'
        db.create_table('admin_email_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_emails', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('process_emails', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('success_emails', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('task_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('administration', ['EmailTask'])

        # Adding model 'EmailTaskLog'
        db.create_table('admin_email_task_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('send_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['administration.EmailTask'], on_delete=models.PROTECT)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=75, db_index=True)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('administration', ['EmailTaskLog'])

        # Adding model 'FilterFavorite'
        db.create_table('admin_filter_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, db_index=True)),
            ('filter_json', self.gf('django.db.models.fields.CharField')(max_length=4096, db_index=True)),
        ))
        db.send_create_signal('administration', ['FilterFavorite'])

        # Adding model 'TaskExecutorLog'
        db.create_table('admin_task_executor_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=150, db_index=True)),
            ('execute_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('administration', ['TaskExecutorLog'])

        # Adding model 'Author'
        db.create_table('author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('administration', ['Author'])

        # Adding model 'CertificateAssociationType'
        db.create_table('certificate_association_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('administration', ['CertificateAssociationType'])

        # Adding model 'Certificate'
        db.create_table('certificate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('certificate_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('certificate_blob', self.gf('django.db.models.fields.TextField')(null=True)),
            ('readonly', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('association_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['administration.CertificateAssociationType'])),
            ('association', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('administration', ['Certificate'])


    def backwards(self, orm):
        # Deleting model 'ImportTask'
        db.delete_table('admin_import_task')

        # Deleting model 'ImportTaskLog'
        db.delete_table('admin_import_task_log')

        # Deleting model 'EmailTask'
        db.delete_table('admin_email_task')

        # Deleting model 'EmailTaskLog'
        db.delete_table('admin_email_task_log')

        # Deleting model 'FilterFavorite'
        db.delete_table('admin_filter_favorite')

        # Deleting model 'TaskExecutorLog'
        db.delete_table('admin_task_executor_log')

        # Deleting model 'Author'
        db.delete_table('author')

        # Deleting model 'CertificateAssociationType'
        db.delete_table('certificate_association_type')

        # Deleting model 'Certificate'
        db.delete_table('certificate')


    models = {
        'administration.author': {
            'Meta': {'object_name': 'Author', 'db_table': "'author'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'administration.certificate': {
            'Meta': {'object_name': 'Certificate', 'db_table': "'certificate'"},
            'association': ('django.db.models.fields.IntegerField', [], {}),
            'association_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.CertificateAssociationType']"}),
            'certificate_blob': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'certificate_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readonly': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'administration.certificateassociationtype': {
            'Meta': {'object_name': 'CertificateAssociationType', 'db_table': "'certificate_association_type'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'administration.emailtask': {
            'Meta': {'object_name': 'EmailTask', 'db_table': "'admin_email_task'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process_emails': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'success_emails': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_emails': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'administration.emailtasklog': {
            'Meta': {'object_name': 'EmailTaskLog', 'db_table': "'admin_email_task_log'"},
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '75', 'db_index': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.EmailTask']", 'on_delete': 'models.PROTECT'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'administration.filterfavorite': {
            'Meta': {'object_name': 'FilterFavorite', 'db_table': "'admin_filter_favorite'"},
            'filter_json': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'administration.importtask': {
            'Meta': {'object_name': 'ImportTask', 'db_table': "'admin_import_task'"},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process_lines': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'success_lines': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_lines': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'administration.importtasklog': {
            'Meta': {'object_name': 'ImportTaskLog', 'db_table': "'admin_import_task_log'"},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '75', 'db_index': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.ImportTask']", 'on_delete': 'models.PROTECT'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'administration.taskexecutorlog': {
            'Meta': {'object_name': 'TaskExecutorLog', 'db_table': "'admin_task_executor_log'"},
            'execute_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
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
        }
    }

    complete_apps = ['administration']