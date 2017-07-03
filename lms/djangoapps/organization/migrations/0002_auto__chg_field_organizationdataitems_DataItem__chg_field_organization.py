# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OrganizationDataitems.DataItem'
        db.alter_column('organization_dataitems', 'DataItem', self.gf('django.db.models.fields.TextField')())

        # Changing field 'OrganizationDashboard.itemValue'
        db.alter_column('organization_dashboard', 'itemValue', self.gf('django.db.models.fields.TextField')())

        # Changing field 'OrganizationMenu.itemValue'
        db.alter_column('organization_menu', 'itemValue', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'OrganizationDataitems.DataItem'
        db.alter_column('organization_dataitems', 'DataItem', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'OrganizationDashboard.itemValue'
        db.alter_column('organization_dashboard', 'itemValue', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'OrganizationMenu.itemValue'
        db.alter_column('organization_menu', 'itemValue', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'organization.mainpageconfiguration': {
            'BottomMainLogo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'MainLogoText': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'MainPageBottomImage': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'MainPageButtonLink': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'MainPageButtonText': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'MainPageConfiguration', 'db_table': "'main_page_configuration'"},
            'SiteURL': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'TopMainLogo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.organizationattributes': {
            'LogoHome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'LogoProfile': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'OrganizationAttributes', 'db_table': "'organization_attributes'"},
            'Motto': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationcmsitem': {
            'CmsItem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Grade': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'OrganizationCmsitem', 'db_table': "'organization_cmsitem'"},
            'Url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"}),
            'rowNum': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'organization.organizationdashboard': {
            'Meta': {'object_name': 'OrganizationDashboard', 'db_table': "'organization_dashboard'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itemValue': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationdataitems': {
            'DataItem': ('django.db.models.fields.TextField', [], {}),
            'Meta': {'object_name': 'OrganizationDataitems', 'db_table': "'organization_dataitems'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationdistricts': {
            'EntityType': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Meta': {'object_name': 'OrganizationDistricts', 'db_table': "'organization_districts'"},
            'OrganizationEnity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationmenu': {
            'Meta': {'object_name': 'OrganizationMenu', 'db_table': "'organization_menu'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itemValue': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationmenuitem': {
            'Icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'MenuItem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'OrganizationMenuitem', 'db_table': "'organization_menuitem'"},
            'ParentID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'Url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isAdmin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"}),
            'rowNum': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'organization.organizationmetadata': {
            'DistrictType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'OrganizationMetadata', 'db_table': "'organization_metadata'"},
            'OrganizationName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'SchoolType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['organization']