# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrganizationMetadata'
        db.create_table('organization_metadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('OrganizationName', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('DistrictType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('SchoolType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('organization', ['OrganizationMetadata'])

        # Adding model 'OrganizationDataitems'
        db.create_table('organization_dataitems', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('DataItem', self.gf('django.db.models.fields.TextField')),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationDataitems'])

        # Adding model 'OrganizationDistricts'
        db.create_table('organization_districts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('EntityType', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('OrganizationEnity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationDistricts'])

        # Adding model 'OrganizationAttributes'
        db.create_table('organization_attributes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('LogoHome', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('LogoProfile', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Motto', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationAttributes'])

        # Adding model 'MainPageConfiguration'
        db.create_table('main_page_configuration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SiteURL', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('TopMainLogo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('MainLogoText', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('BottomMainLogo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('MainPageBottomImage', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('MainPageButtonText', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('MainPageButtonLink', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('organization', ['MainPageConfiguration'])

        # Adding model 'OrganizationMenuitem'
        db.create_table('organization_menuitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('MenuItem', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Icon', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('isAdmin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rowNum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ParentID', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationMenuitem'])

        # Adding model 'OrganizationMenu'
        db.create_table('organization_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('itemType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('itemValue', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationMenu'])

        # Adding model 'OrganizationDashboard'
        db.create_table('organization_dashboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('itemType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('itemValue', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationDashboard'])

        # Adding model 'OrganizationCmsitem'
        db.create_table('organization_cmsitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('CmsItem', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Icon', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rowNum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('Grade', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organization.OrganizationMetadata'])),
        ))
        db.send_create_signal('organization', ['OrganizationCmsitem'])


    def backwards(self, orm):
        # Deleting model 'OrganizationMetadata'
        db.delete_table('organization_metadata')

        # Deleting model 'OrganizationDataitems'
        db.delete_table('organization_dataitems')

        # Deleting model 'OrganizationDistricts'
        db.delete_table('organization_districts')

        # Deleting model 'OrganizationAttributes'
        db.delete_table('organization_attributes')

        # Deleting model 'MainPageConfiguration'
        db.delete_table('main_page_configuration')

        # Deleting model 'OrganizationMenuitem'
        db.delete_table('organization_menuitem')

        # Deleting model 'OrganizationMenu'
        db.delete_table('organization_menu')

        # Deleting model 'OrganizationDashboard'
        db.delete_table('organization_dashboard')

        # Deleting model 'OrganizationMenuitem'
        db.delete_table('organization_menuitem')



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
        'organization.organizationdashboard': {
            'Meta': {'object_name': 'OrganizationDashboard', 'db_table': "'organization_dashboard'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itemValue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"})
        },
        'organization.organizationdataitems': {
            'DataItem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'itemValue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        },
        'organization.organizationcmsitem': {
            'Icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'CmsItem': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'OrganizationCmsitem', 'db_table': "'organization_cmsitem'"},
            'Grade': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),            
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organization.OrganizationMetadata']"}),
            'rowNum': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['organization']