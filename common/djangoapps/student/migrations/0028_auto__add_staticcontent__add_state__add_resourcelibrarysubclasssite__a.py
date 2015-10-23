# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StaticContent'
        db.create_table('student_staticcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('student', ['StaticContent'])

        # Adding model 'State'
        db.create_table('state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['State'])

        # Adding model 'ResourceLibrarySubclassSite'
        db.create_table('student_resourcelibrarysubclasssite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibrarySubclassSite'])

        # Adding model 'Transaction'
        db.create_table('transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Cohort'], on_delete=models.PROTECT, db_column='owner_id')),
            ('code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('term_months', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['Transaction'])

        # Adding model 'GradeLevel'
        db.create_table('grade_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['GradeLevel'])

        # Adding model 'Cohort'
        db.create_table('cohort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.District'], on_delete=models.PROTECT)),
            ('code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('licences', self.gf('django.db.models.fields.IntegerField')()),
            ('term_months', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('student', ['Cohort'])

        # Adding model 'YearsInEducation'
        db.create_table('years_in_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['YearsInEducation'])

        # Adding model 'CmsLoginInfo'
        db.create_table('cms_login_info', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('log_type_login', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('login_or_logout_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('student', ['CmsLoginInfo'])

        # Adding model 'District'
        db.create_table('district', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.State'], on_delete=models.PROTECT)),
            ('code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('student', ['District'])

        # Adding model 'ResourceLibrary'
        db.create_table('student_resourcelibrary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.ResourceLibraryCategory'])),
            ('subclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.ResourceLibrarySubclass'], null=True, blank=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibrary'])

        # Adding model 'StudentModule'
        db.create_table('courseware_studentmodule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module_type', self.gf('django.db.models.fields.CharField')(default='problem', max_length=32, db_index=True)),
            ('module_state_key', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='module_id', db_index=True)),
            ('student_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('state', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('max_grade', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('done', self.gf('django.db.models.fields.CharField')(default='na', max_length=8, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('module_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('student', ['StudentModule'])

        # Adding model 'SubjectArea'
        db.create_table('subject_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['SubjectArea'])

        # Adding model 'School'
        db.create_table('school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.District'], on_delete=models.PROTECT)),
            ('code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('student', ['School'])

        # Adding model 'ResourceLibraryCategory'
        db.create_table('student_resourcelibrarycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibraryCategory'])

        # Adding model 'ResourceLibrarySubclass'
        db.create_table('student_resourcelibrarysubclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibrarySubclass'])

        # Adding M2M table for field sites on 'ResourceLibrarySubclass'
        m2m_table_name = db.shorten_name('student_resourcelibrarysubclass_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resourcelibrarysubclass', models.ForeignKey(orm['student.resourcelibrarysubclass'], null=False)),
            ('resourcelibrarysubclasssite', models.ForeignKey(orm['student.resourcelibrarysubclasssite'], null=False))
        ))
        db.create_unique(m2m_table_name, ['resourcelibrarysubclass_id', 'resourcelibrarysubclasssite_id'])

        # Adding model 'People'
        db.create_table('student_people', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_id', to=orm['auth.User'])),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(related_name='people_id', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('student', ['People'])

        # Adding field 'CourseEnrollmentAllowed.is_active'
        db.add_column('student_courseenrollmentallowed', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.school'
        db.add_column('auth_userprofile', 'school',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.School'], on_delete=models.PROTECT),
                      keep_default=False)

        # Adding field 'UserProfile.cohort'
        db.add_column('auth_userprofile', 'cohort',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['student.Cohort'], on_delete=models.PROTECT),
                      keep_default=False)

        # Adding field 'UserProfile.district'
        db.add_column('auth_userprofile', 'district',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.District'], on_delete=models.PROTECT),
                      keep_default=False)

        # Adding field 'UserProfile.years_in_education'
        db.add_column('auth_userprofile', 'years_in_education',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.YearsInEducation'], on_delete=models.PROTECT),
                      keep_default=False)

        # Adding field 'UserProfile.major_subject_area'
        db.add_column('auth_userprofile', 'major_subject_area',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.SubjectArea'], on_delete=models.PROTECT),
                      keep_default=False)

        # Adding field 'UserProfile.grade_level_id'
        db.add_column('auth_userprofile', 'grade_level_id',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255, db_index=True),
                      keep_default=False)

        # Adding field 'UserProfile.bio'
        db.add_column('auth_userprofile', 'bio',
                      self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.subscription_status'
        db.add_column('auth_userprofile', 'subscription_status',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=20),
                      keep_default=False)

        # Adding field 'UserProfile.invite_date'
        db.add_column('auth_userprofile', 'invite_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=None),
                      keep_default=False)

        # Adding field 'UserProfile.activate_date'
        db.add_column('auth_userprofile', 'activate_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=None),
                      keep_default=False)

        # Adding field 'UserProfile.people_of'
        db.add_column('auth_userprofile', 'people_of',
                      self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=2048, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.percent_lunch'
        db.add_column('auth_userprofile', 'percent_lunch',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserProfile.percent_iep'
        db.add_column('auth_userprofile', 'percent_iep',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserProfile.percent_eng_learner'
        db.add_column('auth_userprofile', 'percent_eng_learner',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserProfile.sso_type'
        db.add_column('auth_userprofile', 'sso_type',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.sso_idp'
        db.add_column('auth_userprofile', 'sso_idp',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PendingNameChange.new_first_name'
        db.add_column('student_pendingnamechange', 'new_first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'PendingNameChange.new_last_name'
        db.add_column('student_pendingnamechange', 'new_last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'StaticContent'
        db.delete_table('student_staticcontent')

        # Deleting model 'State'
        db.delete_table('state')

        # Deleting model 'ResourceLibrarySubclassSite'
        db.delete_table('student_resourcelibrarysubclasssite')

        # Deleting model 'Transaction'
        db.delete_table('transaction')

        # Deleting model 'GradeLevel'
        db.delete_table('grade_level')

        # Deleting model 'Cohort'
        db.delete_table('cohort')

        # Deleting model 'YearsInEducation'
        db.delete_table('years_in_education')

        # Deleting model 'CmsLoginInfo'
        db.delete_table('cms_login_info')

        # Deleting model 'District'
        db.delete_table('district')

        # Deleting model 'ResourceLibrary'
        db.delete_table('student_resourcelibrary')

        # Deleting model 'StudentModule'
        db.delete_table('courseware_studentmodule')

        # Deleting model 'SubjectArea'
        db.delete_table('subject_area')

        # Deleting model 'School'
        db.delete_table('school')

        # Deleting model 'ResourceLibraryCategory'
        db.delete_table('student_resourcelibrarycategory')

        # Deleting model 'ResourceLibrarySubclass'
        db.delete_table('student_resourcelibrarysubclass')

        # Removing M2M table for field sites on 'ResourceLibrarySubclass'
        db.delete_table(db.shorten_name('student_resourcelibrarysubclass_sites'))

        # Deleting model 'People'
        db.delete_table('student_people')

        # Deleting field 'CourseEnrollmentAllowed.is_active'
        db.delete_column('student_courseenrollmentallowed', 'is_active')

        # Deleting field 'UserProfile.school'
        db.delete_column('auth_userprofile', 'school_id')

        # Deleting field 'UserProfile.cohort'
        db.delete_column('auth_userprofile', 'cohort_id')

        # Deleting field 'UserProfile.district'
        db.delete_column('auth_userprofile', 'district_id')

        # Deleting field 'UserProfile.years_in_education'
        db.delete_column('auth_userprofile', 'years_in_education_id')

        # Deleting field 'UserProfile.major_subject_area'
        db.delete_column('auth_userprofile', 'major_subject_area_id')

        # Deleting field 'UserProfile.grade_level_id'
        db.delete_column('auth_userprofile', 'grade_level_id')

        # Deleting field 'UserProfile.bio'
        db.delete_column('auth_userprofile', 'bio')

        # Deleting field 'UserProfile.subscription_status'
        db.delete_column('auth_userprofile', 'subscription_status')

        # Deleting field 'UserProfile.invite_date'
        db.delete_column('auth_userprofile', 'invite_date')

        # Deleting field 'UserProfile.activate_date'
        db.delete_column('auth_userprofile', 'activate_date')

        # Deleting field 'UserProfile.people_of'
        db.delete_column('auth_userprofile', 'people_of')

        # Deleting field 'UserProfile.percent_lunch'
        db.delete_column('auth_userprofile', 'percent_lunch')

        # Deleting field 'UserProfile.percent_iep'
        db.delete_column('auth_userprofile', 'percent_iep')

        # Deleting field 'UserProfile.percent_eng_learner'
        db.delete_column('auth_userprofile', 'percent_eng_learner')

        # Deleting field 'UserProfile.sso_type'
        db.delete_column('auth_userprofile', 'sso_type')

        # Deleting field 'UserProfile.sso_idp'
        db.delete_column('auth_userprofile', 'sso_idp')

        # Deleting field 'PendingNameChange.new_first_name'
        db.delete_column('student_pendingnamechange', 'new_first_name')

        # Deleting field 'PendingNameChange.new_last_name'
        db.delete_column('student_pendingnamechange', 'new_last_name')


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
        'student.cmslogininfo': {
            'Meta': {'object_name': 'CmsLoginInfo', 'db_table': "'cms_login_info'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'log_type_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'login_or_logout_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'student.cohort': {
            'Meta': {'object_name': 'Cohort', 'db_table': "'cohort'"},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licences': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'term_months': ('django.db.models.fields.IntegerField', [], {})
        },
        'student.courseenrollment': {
            'Meta': {'ordering': "('user', 'course_id')", 'unique_together': "(('user', 'course_id'),)", 'object_name': 'CourseEnrollment'},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'honor'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'student.courseenrollmentallowed': {
            'Meta': {'unique_together': "(('email', 'course_id'),)", 'object_name': 'CourseEnrollmentAllowed'},
            'auto_enroll': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'student.district': {
            'Meta': {'object_name': 'District', 'db_table': "'district'"},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.State']", 'on_delete': 'models.PROTECT'})
        },
        'student.gradelevel': {
            'Meta': {'object_name': 'GradeLevel', 'db_table': "'grade_level'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'so': ('django.db.models.fields.IntegerField', [], {})
        },
        'student.pendingemailchange': {
            'Meta': {'object_name': 'PendingEmailChange'},
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_email': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'student.pendingnamechange': {
            'Meta': {'object_name': 'PendingNameChange'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'new_last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rationale': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'student.people': {
            'Meta': {'object_name': 'People'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'people': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'people_id'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_id'", 'to': "orm['auth.User']"})
        },
        'student.registration': {
            'Meta': {'object_name': 'Registration', 'db_table': "'auth_registration'"},
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'student.resourcelibrary': {
            'Meta': {'object_name': 'ResourceLibrary'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.ResourceLibraryCategory']"}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'subclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.ResourceLibrarySubclass']", 'null': 'True', 'blank': 'True'})
        },
        'student.resourcelibrarycategory': {
            'Meta': {'object_name': 'ResourceLibraryCategory'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'student.resourcelibrarysubclass': {
            'Meta': {'object_name': 'ResourceLibrarySubclass'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['student.ResourceLibrarySubclassSite']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'student.resourcelibrarysubclasssite': {
            'Meta': {'object_name': 'ResourceLibrarySubclassSite'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'max_length': '255'})
        },
        'student.school': {
            'Meta': {'object_name': 'School', 'db_table': "'school'"},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'student.state': {
            'Meta': {'object_name': 'State', 'db_table': "'state'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'so': ('django.db.models.fields.IntegerField', [], {})
        },
        'student.staticcontent': {
            'Meta': {'object_name': 'StaticContent'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'student.studentmodule': {
            'Meta': {'object_name': 'StudentModule', 'db_table': "'courseware_studentmodule'"},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'done': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '8', 'db_index': 'True'}),
            'grade': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_grade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'module_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'module_state_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'module_id'", 'db_index': 'True'}),
            'module_type': ('django.db.models.fields.CharField', [], {'default': "'problem'", 'max_length': '32', 'db_index': 'True'}),
            'state': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'student.subjectarea': {
            'Meta': {'object_name': 'SubjectArea', 'db_table': "'subject_area'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'so': ('django.db.models.fields.IntegerField', [], {})
        },
        'student.testcenterregistration': {
            'Meta': {'object_name': 'TestCenterRegistration'},
            'accommodation_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'accommodation_request': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'authorization_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'client_authorization_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'confirmed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'eligibility_appointment_date_first': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'eligibility_appointment_date_last': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'exam_series_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'testcenter_user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['student.TestCenterUser']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'upload_error_message': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'upload_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'user_updated_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'student.testcenteruser': {
            'Meta': {'object_name': 'TestCenterUser'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'address_3': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'candidate_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'client_candidate_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'confirmed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '8', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'fax_country_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'phone_country_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'processed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'salutation': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'upload_error_message': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'upload_status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'unique': 'True'}),
            'user_updated_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'student.transaction': {
            'Meta': {'object_name': 'Transaction', 'db_table': "'transaction'"},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Cohort']", 'on_delete': 'models.PROTECT', 'db_column': "'owner_id'"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'subscription_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'term_months': ('django.db.models.fields.IntegerField', [], {})
        },
        'student.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'auth_userprofile'"},
            'activate_date': ('django.db.models.fields.DateTimeField', [], {}),
            'allow_certificate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bio': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'cohort': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['student.Cohort']", 'on_delete': 'models.PROTECT'}),
            'courseware': ('django.db.models.fields.CharField', [], {'default': "'course.xml'", 'max_length': '255', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']", 'on_delete': 'models.PROTECT'}),
            'gender': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'goals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grade_level_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_date': ('django.db.models.fields.DateTimeField', [], {}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'level_of_education': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'major_subject_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.SubjectArea']", 'on_delete': 'models.PROTECT'}),
            'meta': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'people_of': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'blank': 'True'}),
            'percent_eng_learner': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percent_iep': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'percent_lunch': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.School']", 'on_delete': 'models.PROTECT'}),
            'sso_idp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sso_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subscription_status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'year_of_birth': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'years_in_education': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.YearsInEducation']", 'on_delete': 'models.PROTECT'})
        },
        'student.usertestgroup': {
            'Meta': {'object_name': 'UserTestGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'db_index': 'True', 'symmetrical': 'False'})
        },
        'student.yearsineducation': {
            'Meta': {'object_name': 'YearsInEducation', 'db_table': "'years_in_education'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'so': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['student']
