# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TrainingUsers.training'
        db.alter_column('training_users', 'training_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['administration.PepRegTraining']))

    def backwards(self, orm):

        # Changing field 'TrainingUsers.training'
        db.alter_column('training_users', 'training_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['training.TrainingTrainings']))

    models = {
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
            'last_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'max_registration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pepper_course': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'school_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'training_date': ('django.db.models.fields.DateField', [], {}),
            'training_time_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'training_time_start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_create': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
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
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
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
        'training.trainingtrainings': {
            'Meta': {'object_name': 'TrainingTrainings', 'db_table': "'training_trainings'"},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.State']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'training.trainingusers': {
            'Meta': {'object_name': 'TrainingUsers', 'db_table': "'training_users'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'training': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['administration.PepRegTraining']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
        }
    }

    complete_apps = ['training']