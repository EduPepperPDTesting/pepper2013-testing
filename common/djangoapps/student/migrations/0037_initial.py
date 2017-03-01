# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CmsLoginInfo'
        db.create_table('cms_login_info', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('log_type_login', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('login_or_logout_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('student', ['CmsLoginInfo'])

        # Adding model 'ResourceLibrarySubclassSite'
        db.create_table('student_resourcelibrarysubclasssite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibrarySubclassSite'])

        # Adding model 'ResourceLibrarySubclass'
        db.create_table('student_resourcelibrarysubclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibrarySubclass'])

        # Adding M2M table for field sites on 'ResourceLibrarySubclass'
        db.create_table('student_resourcelibrarysubclass_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resourcelibrarysubclass', models.ForeignKey(orm['student.resourcelibrarysubclass'], null=False)),
            ('resourcelibrarysubclasssite', models.ForeignKey(orm['student.resourcelibrarysubclasssite'], null=False))
        ))
        db.create_unique('student_resourcelibrarysubclass_sites', ['resourcelibrarysubclass_id', 'resourcelibrarysubclasssite_id'])

        # Adding model 'ResourceLibraryCategory'
        db.create_table('student_resourcelibrarycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['ResourceLibraryCategory'])

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

        # Adding model 'StaticContent'
        db.create_table('student_staticcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('student', ['StaticContent'])

        # Adding model 'YearsInEducation'
        db.create_table('years_in_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['YearsInEducation'])

        # Adding model 'GradeLevel'
        db.create_table('grade_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['GradeLevel'])

        # Adding model 'SubjectArea'
        db.create_table('subject_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['SubjectArea'])

        # Adding model 'State'
        db.create_table('state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('so', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('student', ['State'])

        # Adding model 'District'
        db.create_table('district', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.State'], on_delete=models.PROTECT)),
            ('code', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('student', ['District'])

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

        # Adding model 'School'
        db.create_table('school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.District'], on_delete=models.PROTECT)),
            ('code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('student', ['School'])

        # Adding model 'People'
        db.create_table('student_people', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_id', to=orm['auth.User'])),
            ('people', self.gf('django.db.models.fields.related.ForeignKey')(related_name='people_id', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('student', ['People'])

        # Adding model 'UserProfile'
        db.create_table('auth_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.School'], on_delete=models.PROTECT)),
            ('cohort', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['student.Cohort'], on_delete=models.PROTECT)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.District'], on_delete=models.PROTECT)),
            ('years_in_education', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.YearsInEducation'], on_delete=models.PROTECT)),
            ('major_subject_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.SubjectArea'], on_delete=models.PROTECT)),
            ('grade_level_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('subscription_status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('invite_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('activate_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('meta', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('courseware', self.gf('django.db.models.fields.CharField')(default='course.xml', max_length=255, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('people_of', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, blank=True)),
            ('year_of_birth', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=6, null=True, blank=True)),
            ('percent_lunch', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('percent_iep', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('percent_eng_learner', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sso_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('sso_idp', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sso_user_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('skype_username', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_activity', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('level_of_education', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=6, null=True, blank=True)),
            ('mailing_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('goals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('allow_certificate', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('student', ['UserProfile'])

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

        # Adding model 'TestCenterUser'
        db.create_table('student_testcenteruser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], unique=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('user_updated_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('client_candidate_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('salutation', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('address_3', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=16, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('extension', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=8, blank=True)),
            ('phone_country_code', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('fax_country_code', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('processed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('upload_status', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, blank=True)),
            ('upload_error_message', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('candidate_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('confirmed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
        ))
        db.send_create_signal('student', ['TestCenterUser'])

        # Adding model 'TestCenterRegistration'
        db.create_table('student_testcenterregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testcenter_user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.TestCenterUser'])),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('user_updated_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('client_authorization_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_index=True)),
            ('exam_series_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('eligibility_appointment_date_first', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('eligibility_appointment_date_last', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('accommodation_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('accommodation_request', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('processed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('upload_status', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, blank=True)),
            ('upload_error_message', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('authorization_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('confirmed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
        ))
        db.send_create_signal('student', ['TestCenterRegistration'])

        # Adding model 'UserTestGroup'
        db.create_table('student_usertestgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('student', ['UserTestGroup'])

        # Adding M2M table for field users on 'UserTestGroup'
        db.create_table('student_usertestgroup_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usertestgroup', models.ForeignKey(orm['student.usertestgroup'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('student_usertestgroup_users', ['usertestgroup_id', 'user_id'])

        # Adding model 'Registration'
        db.create_table('auth_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, db_index=True)),
        ))
        db.send_create_signal('student', ['Registration'])

        # Adding model 'PendingNameChange'
        db.create_table('student_pendingnamechange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('new_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('new_first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('new_last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('rationale', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal('student', ['PendingNameChange'])

        # Adding model 'PendingEmailChange'
        db.create_table('student_pendingemailchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('new_email', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, blank=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, db_index=True)),
        ))
        db.send_create_signal('student', ['PendingEmailChange'])

        # Adding model 'CourseEnrollment'
        db.create_table('student_courseenrollment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_index=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(default='honor', max_length=100)),
        ))
        db.send_create_signal('student', ['CourseEnrollment'])

        # Adding unique constraint on 'CourseEnrollment', fields ['user', 'course_id']
        db.create_unique('student_courseenrollment', ['user_id', 'course_id'])

        # Adding model 'CourseEnrollmentAllowed'
        db.create_table('student_courseenrollmentallowed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('auto_enroll', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('student', ['CourseEnrollmentAllowed'])

        # Adding unique constraint on 'CourseEnrollmentAllowed', fields ['email', 'course_id']
        db.create_unique('student_courseenrollmentallowed', ['email', 'course_id'])

        # Adding model 'DashboardPosts'
        db.create_table('dashboard_posts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dashboardposts_master', to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dashboardposts_user', to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('top', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('student', ['DashboardPosts'])

        # Adding model 'DashboardPostsImages'
        db.create_table('dashboard_posts_images', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.DashboardPosts'])),
            ('link', self.gf('django.db.models.fields.TextField')(max_length=1024)),
            ('embed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('student', ['DashboardPostsImages'])

        # Adding model 'DashboardComments'
        db.create_table('dashboard_posts_comments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.DashboardPosts'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('sub_comment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.DashboardComments'], null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('student', ['DashboardComments'])

        # Adding model 'DashboardLikes'
        db.create_table('dashboard_posts_likes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.DashboardPosts'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.DashboardComments'], null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('student', ['DashboardLikes'])

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


    def backwards(self, orm):
        # Removing unique constraint on 'CourseEnrollmentAllowed', fields ['email', 'course_id']
        db.delete_unique('student_courseenrollmentallowed', ['email', 'course_id'])

        # Removing unique constraint on 'CourseEnrollment', fields ['user', 'course_id']
        db.delete_unique('student_courseenrollment', ['user_id', 'course_id'])

        # Deleting model 'CmsLoginInfo'
        db.delete_table('cms_login_info')

        # Deleting model 'ResourceLibrarySubclassSite'
        db.delete_table('student_resourcelibrarysubclasssite')

        # Deleting model 'ResourceLibrarySubclass'
        db.delete_table('student_resourcelibrarysubclass')

        # Removing M2M table for field sites on 'ResourceLibrarySubclass'
        db.delete_table('student_resourcelibrarysubclass_sites')

        # Deleting model 'ResourceLibraryCategory'
        db.delete_table('student_resourcelibrarycategory')

        # Deleting model 'ResourceLibrary'
        db.delete_table('student_resourcelibrary')

        # Deleting model 'StaticContent'
        db.delete_table('student_staticcontent')

        # Deleting model 'YearsInEducation'
        db.delete_table('years_in_education')

        # Deleting model 'GradeLevel'
        db.delete_table('grade_level')

        # Deleting model 'SubjectArea'
        db.delete_table('subject_area')

        # Deleting model 'State'
        db.delete_table('state')

        # Deleting model 'District'
        db.delete_table('district')

        # Deleting model 'Cohort'
        db.delete_table('cohort')

        # Deleting model 'School'
        db.delete_table('school')

        # Deleting model 'People'
        db.delete_table('student_people')

        # Deleting model 'UserProfile'
        db.delete_table('auth_userprofile')

        # Deleting model 'Transaction'
        db.delete_table('transaction')

        # Deleting model 'TestCenterUser'
        db.delete_table('student_testcenteruser')

        # Deleting model 'TestCenterRegistration'
        db.delete_table('student_testcenterregistration')

        # Deleting model 'UserTestGroup'
        db.delete_table('student_usertestgroup')

        # Removing M2M table for field users on 'UserTestGroup'
        db.delete_table('student_usertestgroup_users')

        # Deleting model 'Registration'
        db.delete_table('auth_registration')

        # Deleting model 'PendingNameChange'
        db.delete_table('student_pendingnamechange')

        # Deleting model 'PendingEmailChange'
        db.delete_table('student_pendingemailchange')

        # Deleting model 'CourseEnrollment'
        db.delete_table('student_courseenrollment')

        # Deleting model 'CourseEnrollmentAllowed'
        db.delete_table('student_courseenrollmentallowed')

        # Deleting model 'DashboardPosts'
        db.delete_table('dashboard_posts')

        # Deleting model 'DashboardPostsImages'
        db.delete_table('dashboard_posts_images')

        # Deleting model 'DashboardComments'
        db.delete_table('dashboard_posts_comments')

        # Deleting model 'DashboardLikes'
        db.delete_table('dashboard_posts_likes')

        # Deleting model 'StudentModule'
        db.delete_table('courseware_studentmodule')


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
        'student.dashboardcomments': {
            'Meta': {'object_name': 'DashboardComments', 'db_table': "'dashboard_posts_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.DashboardPosts']"}),
            'sub_comment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['student.DashboardComments']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'student.dashboardlikes': {
            'Meta': {'object_name': 'DashboardLikes', 'db_table': "'dashboard_posts_likes'"},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['student.DashboardComments']", 'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['student.DashboardPosts']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'student.dashboardposts': {
            'Meta': {'object_name': 'DashboardPosts', 'db_table': "'dashboard_posts'"},
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dashboardposts_master'", 'to': "orm['auth.User']"}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dashboardposts_user'", 'to': "orm['auth.User']"})
        },
        'student.dashboardpostsimages': {
            'Meta': {'object_name': 'DashboardPostsImages', 'db_table': "'dashboard_posts_images'"},
            'embed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.DashboardPosts']"})
        },
        'student.district': {
            'Meta': {'object_name': 'District', 'db_table': "'district'"},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
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
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
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
            'skype_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sso_idp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sso_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sso_user_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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