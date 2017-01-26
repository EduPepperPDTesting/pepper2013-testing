from django.db import models
from student.models import District, State
from django.contrib.auth.models import User
from django.conf import settings
import logging


class OrganizationMetadata(models.Model):
    class Meta:
        db_table = 'organization_metadata'
    OrganizationName = models.CharField(blank=False, max_length=255, db_index=False)
    DistrictType = models.CharField(blank=False, max_length=255, db_index=False)
    SchoolType = models.CharField(blank=False, max_length=255, db_index=False)
    url = models.CharField(blank=False, max_length=100, db_index=False)

class OrganizationDataitems(models.Model):
    class Meta:
        db_table = 'organization_dataitems'
    DataItem = models.CharField(blank=False, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)

class OrganizationDistricts(models.Model):
    class Meta:
        db_table = 'organization_districts'
    EntityType = models.CharField(blank=False, max_length=20, db_index=False)
    OrganizationEnity = models.IntegerField(blank=False, default=0)
    organization = models.ForeignKey(OrganizationMetadata)

class OrganizationAttributes(models.Model):
    class Meta:
        db_table = 'organization_attributes'
    LogoHome = models.CharField(blank=False, max_length=255, db_index=False)
    LogoProfile = models.CharField(blank=False, max_length=255, db_index=False)
    Motto = models.CharField(blank=False, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)

class MainPageConfiguration(models.Model):
    class Meta:
        db_table = 'main_page_configuration'
    SiteURL = models.CharField(blank=False, max_length=255, db_index=False)
    TopMainLogo = models.CharField(blank=False, max_length=255, db_index=False)
    MainLogoText = models.CharField(blank=False, max_length=255, db_index=False)
    BottomMainLogo = models.CharField(blank=False, max_length=255, db_index=False)
    MainPageBottomImage = models.CharField(blank=False, max_length=255, db_index=False)
    MainPageButtonText = models.CharField(blank=False, max_length=255, db_index=False)
    MainPageButtonLink = models.CharField(blank=False, max_length=255, db_index=False)