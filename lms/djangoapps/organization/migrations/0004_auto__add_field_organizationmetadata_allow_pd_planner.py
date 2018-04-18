# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OrganizationMetadata.allow_pd_planner'
        db.add_column('organization_metadata', 'allow_pd_planner',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OrganizationMetadata.allow_pd_planner'
        db.delete_column('organization_metadata', 'allow_pd_planner')


    models = {
        'organization.designfooter': {
            'DataItem': ('django.db.models.fields.TextField', [], {}),
            'Meta': {'object_name': 'DesignFooter', 'db_table': "'design_footer'"},
            'design': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Nologindesign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'organization.designmenu': {
            'Meta': {'object_name': 'DesignMenu', 'db_table': "'design_menu'"},
            'design': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Nologindesign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itemValue': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'organization.designmenuitem': {
            'Icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'MenuItem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'DesignMenuitem', 'db_table': "'design_menuitem'"},
            'ParentID': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'Url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'design': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.Nologindesign']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rowNum': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
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
        'organization.nologindesign': {
            'DesignName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'Nologindesign', 'db_table': "'nologindesign'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'itemValue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'OtherFields': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationfooter': {
            'DataItem': ('django.db.models.fields.TextField', [], {}),
            'Meta': {'object_name': 'OrganizationFooter', 'db_table': "'organization_footer'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationmenu': {
            'Meta': {'object_name': 'OrganizationMenu', 'db_table': "'organization_menu'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itemValue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationmenuitem': {
            'Icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Location': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '255'}),
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
            'allow_pd_planner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'organization.organizationmoretext': {
            'DataItem': ('django.db.models.fields.TextField', [], {}),
            'Meta': {'object_name': 'OrganizationMoreText', 'db_table': "'organization_more_text'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        }
    }

    complete_apps = ['organization']