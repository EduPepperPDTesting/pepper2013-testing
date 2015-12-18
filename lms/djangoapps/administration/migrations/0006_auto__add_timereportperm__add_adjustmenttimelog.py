# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TimeReportPerm'
        db.create_table('time_report_perm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User'])),
        ))
        db.send_create_signal('administration', ['TimeReportPerm'])

        # Adding model 'AdjustmentTimeLog'
        db.create_table('adjustment_time_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('user_email', self.gf('django.db.models.fields.CharField')(max_length=75, db_index=True)),
            ('admin_email', self.gf('django.db.models.fields.CharField')(max_length=75, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('adjustment_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('course_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, db_index=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, db_index=True)),
        ))
        db.send_create_signal('administration', ['AdjustmentTimeLog'])


    def backwards(self, orm):
        # Deleting model 'TimeReportPerm'
        db.delete_table('time_report_perm')

        # Deleting model 'AdjustmentTimeLog'
        db.delete_table('adjustment_time_log')


    models = {
        'administration.adjustmenttimelog': {
            'Meta': {'object_name': 'AdjustmentTimeLog', 'db_table': "'adjustment_time_log'"},
            'adjustment_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'admin_email': ('django.db.models.fields.CharField', [], {'max_length': '75', 'db_index': 'True'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'db_index': 'True'}),
            'course_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_index': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'user_email': ('django.db.models.fields.CharField', [], {'max_length': '75', 'db_index': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'max_length': '11'})
        },
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
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
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
        'administration.hangoutpermissions': {
            'Meta': {'object_name': 'HangoutPermissions', 'db_table': "'hangout_permissions'"},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'administration.importtask': {
            'Meta': {'object_name': 'ImportTask', 'db_table': "'admin_import_task'"},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process_lines': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'success_lines': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_lines': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
        },
        'administration.importtasklog': {
            'Meta': {'object_name': 'ImportTaskLog', 'db_table': "'admin_import_task_log'"},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_data': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.ImportTask']", 'on_delete': 'models.PROTECT'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'administration.timereportperm': {
            'Meta': {'object_name': 'TimeReportPerm', 'db_table': "'time_report_perm'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
        },
        'administration.timereporttask': {
            'Meta': {'object_name': 'TimeReportTask', 'db_table': "'admin_time_report_task'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'success_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
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
        }
    }

    complete_apps = ['administration']