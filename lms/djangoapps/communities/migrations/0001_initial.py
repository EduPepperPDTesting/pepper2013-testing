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
            ('community', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('motto', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('logo', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityCommunities'])

        # Adding model 'CommunityUsers'
        db.create_table('community_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'], on_delete=models.PROTECT)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('facilitator', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('communities', ['CommunityUsers'])

        # Adding model 'CommunityCourses'
        db.create_table('community_courses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'], on_delete=models.PROTECT)),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('communities', ['CommunityCourses'])

        # Adding model 'CommunityResources'
        db.create_table('community_resources', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['communities.CommunityCommunities'], on_delete=models.PROTECT)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('logo', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('communities', ['CommunityResources'])


    def backwards(self, orm):
        # Deleting model 'CommunityCommunities'
        db.delete_table('community_communities')

        # Deleting model 'CommunityUsers'
        db.delete_table('community_users')

        # Deleting model 'CommunityCourses'
        db.delete_table('community_courses')

        # Deleting model 'CommunityResources'
        db.delete_table('community_resources')


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
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
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
        'communities.communityresources': {
            'Meta': {'object_name': 'CommunityResources', 'db_table': "'community_resources'"},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communities.CommunityCommunities']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
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
        }
    }

    complete_apps = ['communities']