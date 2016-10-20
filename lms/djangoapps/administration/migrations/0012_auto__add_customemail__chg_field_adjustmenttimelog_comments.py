# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomEmail'
        db.create_table('admin_custom_emails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_content', self.gf('django.db.models.fields.TextField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.District'], null=True, on_delete=models.PROTECT)),
        ))
        db.send_create_signal('administration', ['CustomEmail'])


        # Changing field 'AdjustmentTimeLog.comments'
        db.alter_column('adjustment_time_log', 'comments', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

    def backwards(self, orm):
        # Deleting model 'CustomEmail'
        db.delete_table('admin_custom_emails')


        # Changing field 'AdjustmentTimeLog.comments'
        db.alter_column('adjustment_time_log', 'comments', self.gf('django.db.models.fields.CharField')(max_length=756, null=True))

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
        'administration.customemail': {
            'Meta': {'object_name': 'CustomEmail', 'db_table': "'admin_custom_emails'"},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['student.District']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
            'email_content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
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
        'administration.pepreginstructor': {
            'Meta': {'object_name': 'PepRegInstructor', 'db_table': "'pepreg_instructor'"},
            'date_create': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.PepRegTraining']"}),
            'user_create': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'administration.pepregstudent': {
            'Meta': {'object_name': 'PepRegStudent', 'db_table': "'pepreg_student'"},
            'date_create': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modify': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'student_credit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'student_status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.PepRegTraining']"}),
            'user_create': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'administration.pepregtraining': {
            'Meta': {'object_name': 'PepRegTraining', 'db_table': "'pepreg_training'"},
            'allow_attendance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_registration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_student_attendance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_validation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attendancel_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'classroom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'credits': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'date_create': ('django.db.models.fields.DateField', [], {}),
            'date_modify': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']"}),
            'geo_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'geo_props': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_registration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pepper_course': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'training_date': ('django.db.models.fields.DateField', [], {}),
            'training_time_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'training_time_start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_create': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
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