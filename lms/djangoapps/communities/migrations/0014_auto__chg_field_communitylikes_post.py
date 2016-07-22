# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CommunityLikes.post'
        db.alter_column('community_posts_likes', 'post_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityPosts'], null=True))

    def backwards(self, orm):

        # Changing field 'CommunityLikes.post'
        db.alter_column('community_posts_likes', 'post_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['communities.CommunityPosts']))

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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'communities.communitycommunities': {
            'Meta': {'object_name': 'CommunityCommunities', 'db_table': "'community_communities'"},
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
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['communities.CommunityComments']", 'null': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['communities.CommunityPosts']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'communities.communityposts': {
            'Meta': {'object_name': 'CommunityPosts', 'db_table': "'community_posts'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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