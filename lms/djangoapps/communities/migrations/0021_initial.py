# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CommunityCommunities'
        db.create_table('community_communities', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('motto', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('logo', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['file_uploader.FileUploads'], null=True, on_delete=models.PROTECT, blank=True)),
            ('hangout', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.State'], null=True, on_delete=models.PROTECT, blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.District'], null=True, on_delete=models.PROTECT, blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discussion_priority', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityCommunities'])

        # Adding model 'CommunityUsers'
        db.create_table('community_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('facilitator', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityUsers'])

        # Adding model 'CommunityCourses'
        db.create_table('community_courses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'])),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('communities', ['CommunityCourses'])

        # Adding model 'CommunityResources'
        db.create_table('community_resources', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('logo', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['file_uploader.FileUploads'], null=True, on_delete=models.PROTECT, blank=True)),
        ))
        db.send_create_signal('communities', ['CommunityResources'])

        # Adding model 'CommunityDiscussions'
        db.create_table('community_discussions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('post', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_reply', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['file_uploader.FileUploads'], null=True, on_delete=models.PROTECT, blank=True)),
        ))
        db.send_create_signal('communities', ['CommunityDiscussions'])

        # Adding model 'CommunityDiscussionReplies'
        db.create_table('community_discussion_replies', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityDiscussions'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('post', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['file_uploader.FileUploads'], null=True, on_delete=models.PROTECT, blank=True)),
        ))
        db.send_create_signal('communities', ['CommunityDiscussionReplies'])

        # Adding model 'CommunityNotificationGroup'
        db.create_table('community_notification_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255)),
        ))
        db.send_create_signal('communities', ['CommunityNotificationGroup'])

        # Adding model 'CommunityNotificationType'
        db.create_table('community_notification_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityNotificationGroup'], on_delete=models.PROTECT)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('communities', ['CommunityNotificationType'])

        # Adding model 'CommunityNotificationConfig'
        db.create_table('community_notification_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('via_pepper', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('via_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityNotificationType'], on_delete=models.PROTECT)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('frequency', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('self_config', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityNotificationConfig'])

        # Adding model 'CommunityNotificationAudit'
        db.create_table('community_notification_audit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', on_delete=models.PROTECT, to=orm['auth.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('send_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityNotificationAudit'])

        # Adding model 'CommunityPosts'
        db.create_table('community_posts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('top', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityPosts'])

        # Adding model 'CommunityPostsImages'
        db.create_table('community_posts_images', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityPosts'])),
            ('link', self.gf('django.db.models.fields.TextField')(max_length=1024)),
            ('embed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('communities', ['CommunityPostsImages'])

        # Adding model 'CommunityComments'
        db.create_table('community_posts_comments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityPosts'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('sub_comment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['communities.CommunityComments'], null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('communities', ['CommunityComments'])

        # Adding model 'CommunityLikes'
        db.create_table('community_posts_likes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['communities.CommunityPosts'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['communities.CommunityComments'], null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('communities', ['CommunityLikes'])


    def backwards(self, orm):
        # Deleting model 'CommunityCommunities'
        db.delete_table('community_communities')

        # Deleting model 'CommunityUsers'
        db.delete_table('community_users')

        # Deleting model 'CommunityCourses'
        db.delete_table('community_courses')

        # Deleting model 'CommunityResources'
        db.delete_table('community_resources')

        # Deleting model 'CommunityDiscussions'
        db.delete_table('community_discussions')

        # Deleting model 'CommunityDiscussionReplies'
        db.delete_table('community_discussion_replies')

        # Deleting model 'CommunityNotificationGroup'
        db.delete_table('community_notification_group')

        # Deleting model 'CommunityNotificationType'
        db.delete_table('community_notification_type')

        # Deleting model 'CommunityNotificationConfig'
        db.delete_table('community_notification_config')

        # Deleting model 'CommunityNotificationAudit'
        db.delete_table('community_notification_audit')

        # Deleting model 'CommunityPosts'
        db.delete_table('community_posts')

        # Deleting model 'CommunityPostsImages'
        db.delete_table('community_posts_images')

        # Deleting model 'CommunityComments'
        db.delete_table('community_posts_comments')

        # Deleting model 'CommunityLikes'
        db.delete_table('community_posts_likes')


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
        'communities.communitycomments': {
            'Meta': {'object_name': 'CommunityComments', 'db_table': "'community_posts_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityPosts']"}),
            'sub_comment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['communities.CommunityComments']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'communities.communitycommunities': {
            'Meta': {'object_name': 'CommunityCommunities', 'db_table': "'community_communities'"},
            'discussion_priority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.District']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'hangout': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['file_uploader.FileUploads']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.State']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'communities.communitycourses': {
            'Meta': {'object_name': 'CommunityCourses', 'db_table': "'community_courses'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']"}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'communities.communitydiscussionreplies': {
            'Meta': {'object_name': 'CommunityDiscussionReplies', 'db_table': "'community_discussion_replies'"},
            'attachment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['file_uploader.FileUploads']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityDiscussions']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
        },
        'communities.communitydiscussions': {
            'Meta': {'object_name': 'CommunityDiscussions', 'db_table': "'community_discussions'"},
            'attachment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['file_uploader.FileUploads']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_reply': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
        },
        'communities.communitylikes': {
            'Meta': {'object_name': 'CommunityLikes', 'db_table': "'community_posts_likes'"},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['communities.CommunityComments']", 'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['communities.CommunityPosts']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'communities.communitynotificationaudit': {
            'Meta': {'object_name': 'CommunityNotificationAudit', 'db_table': "'community_notification_audit'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'on_delete': 'models.PROTECT', 'to': "orm['auth.User']"}),
            'send_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'communities.communitynotificationconfig': {
            'Meta': {'object_name': 'CommunityNotificationConfig', 'db_table': "'community_notification_config'"},
            'frequency': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'self_config': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityNotificationType']", 'on_delete': 'models.PROTECT'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'}),
            'via_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'via_pepper': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'communities.communitynotificationgroup': {
            'Meta': {'object_name': 'CommunityNotificationGroup', 'db_table': "'community_notification_group'"},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'communities.communitynotificationtype': {
            'Meta': {'object_name': 'CommunityNotificationType', 'db_table': "'community_notification_type'"},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityNotificationGroup']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'communities.communityposts': {
            'Meta': {'object_name': 'CommunityPosts', 'db_table': "'community_posts'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'communities.communitypostsimages': {
            'Meta': {'object_name': 'CommunityPostsImages', 'db_table': "'community_posts_images'"},
            'embed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityPosts']"})
        },
        'communities.communityresources': {
            'Meta': {'object_name': 'CommunityResources', 'db_table': "'community_resources'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['file_uploader.FileUploads']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'communities.communityusers': {
            'Meta': {'object_name': 'CommunityUsers', 'db_table': "'community_users'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']"}),
            'facilitator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'file_uploader.fileuploads': {
            'Meta': {'object_name': 'FileUploads', 'db_table': "'file_uploads'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
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
        }
    }

    complete_apps = ['communities']