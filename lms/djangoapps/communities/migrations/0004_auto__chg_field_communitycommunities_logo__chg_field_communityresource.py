# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'CommunityCommunities.logo' to match new field type.
        db.rename_column('community_communities', 'logo', 'logo_id')
        # Changing field 'CommunityCommunities.logo'
        db.alter_column('community_communities', 'logo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['file_uploader.FileUploads'], null=True, on_delete=models.PROTECT))

        # Renaming column for 'CommunityResources.logo' to match new field type.
        db.rename_column('community_resources', 'logo', 'logo_id')
        # Changing field 'CommunityResources.logo'
        db.alter_column('community_resources', 'logo_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['file_uploader.FileUploads'], null=True, on_delete=models.PROTECT))

    def backwards(self, orm):

        # Renaming column for 'CommunityCommunities.logo' to match new field type.
        db.rename_column('community_communities', 'logo_id', 'logo')
        # Changing field 'CommunityCommunities.logo'
        db.alter_column('community_communities', 'logo', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Renaming column for 'CommunityResources.logo' to match new field type.
        db.rename_column('community_resources', 'logo_id', 'logo')
        # Changing field 'CommunityResources.logo'
        db.alter_column('community_resources', 'logo', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

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
        'communities.communitycommunities': {
            'Meta': {'object_name': 'CommunityCommunities', 'db_table': "'community_communities'"},
            'community': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['file_uploader.FileUploads']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'communities.communitycourses': {
            'Meta': {'object_name': 'CommunityCourses', 'db_table': "'community_courses'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']", 'on_delete': 'models.PROTECT'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'communities.communitydiscussionreplies': {
            'Meta': {'object_name': 'CommunityDiscussionReplies', 'db_table': "'community_discussion_replies'"},
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityDiscussions']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
        },
        'communities.communitydiscussions': {
            'Meta': {'object_name': 'CommunityDiscussions', 'db_table': "'community_discussions'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']", 'on_delete': 'models.PROTECT'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'on_delete': 'models.PROTECT'})
        },
        'communities.communityresources': {
            'Meta': {'object_name': 'CommunityResources', 'db_table': "'community_resources'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['file_uploader.FileUploads']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'communities.communityusers': {
            'Meta': {'object_name': 'CommunityUsers', 'db_table': "'community_users'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']", 'on_delete': 'models.PROTECT'}),
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
        }
    }

    complete_apps = ['communities']