# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseAssignment'
        db.create_table('sso_course_assignments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sso_type', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('sso', ['CourseAssignment'])

        # Adding model 'CourseAssignmentCourse'
        db.create_table('sso_course_assignment_courses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sso.CourseAssignment'])),
        ))
        db.send_create_signal('sso', ['CourseAssignmentCourse'])


    def backwards(self, orm):
        # Deleting model 'CourseAssignment'
        db.delete_table('sso_course_assignments')

        # Deleting model 'CourseAssignmentCourse'
        db.delete_table('sso_course_assignment_courses')


    models = {
        'sso.courseassignment': {
            'Meta': {'object_name': 'CourseAssignment', 'db_table': "'sso_course_assignments'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sso_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'sso.courseassignmentcourse': {
            'Meta': {'object_name': 'CourseAssignmentCourse', 'db_table': "'sso_course_assignment_courses'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sso.CourseAssignment']"}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['sso']