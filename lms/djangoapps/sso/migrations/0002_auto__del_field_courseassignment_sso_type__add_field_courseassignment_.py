# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CourseAssignment.sso_type'
        db.delete_column('sso_course_assignments', 'sso_type')

        # Adding field 'CourseAssignment.sso_name'
        db.add_column('sso_course_assignments', 'sso_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'CourseAssignment.sso_type'
        db.add_column('sso_course_assignments', 'sso_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True),
                      keep_default=False)

        # Deleting field 'CourseAssignment.sso_name'
        db.delete_column('sso_course_assignments', 'sso_name')


    models = {
        'sso.courseassignment': {
            'Meta': {'object_name': 'CourseAssignment', 'db_table': "'sso_course_assignments'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sso_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'sso.courseassignmentcourse': {
            'Meta': {'object_name': 'CourseAssignmentCourse', 'db_table': "'sso_course_assignment_courses'"},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sso.CourseAssignment']"}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['sso']