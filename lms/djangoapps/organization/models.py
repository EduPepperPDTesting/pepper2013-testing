from django.db import models
from student.models import District, State
from django.contrib.auth.models import User
from django.conf import settings
from student.feeding import MongoBaseStore
import logging

class Nologindesign(models.Model):
    class Meta:
        db_table = 'nologindesign'
    DesignName = models.CharField(blank=False, max_length=255, db_index=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
    DataItem = models.TextField(blank=False, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)


class OrganizationDistricts(models.Model):
    class Meta:
        db_table = 'organization_districts'
    EntityType = models.CharField(blank=False, max_length=20, db_index=False)
    OrganizationEnity = models.IntegerField(blank=False, default=0)
    OtherFields = models.TextField(blank=False, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)


class OrganizationAttributes(models.Model):
    class Meta:
        db_table = 'organization_attributes'
    LogoHome = models.CharField(blank=False, max_length=255, db_index=False)
    LogoProfile = models.CharField(blank=False, max_length=255, db_index=False)
    Motto = models.CharField(blank=False, max_length=255, db_index=False)
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

class OrganizationMenuitem(models.Model):
    class Meta:
        db_table = 'organization_menuitem'
    MenuItem = models.CharField(blank=False, max_length=255, db_index=False)
    Url = models.CharField(blank=False, max_length=255, db_index=False)
    Icon = models.CharField(blank=False, max_length=255, db_index=False)
    isAdmin = models.BooleanField(blank=False, default=0)
    rowNum = models.IntegerField(blank=False, default=0)
    ParentID = models.IntegerField(blank=False, default=0)
    organization = models.ForeignKey(OrganizationMetadata)

class DesignMenuitem(models.Model):
    class Meta:
        db_table = 'design_menuitem'
    MenuItem = models.CharField(blank=False, max_length=255, db_index=False)
    Url = models.CharField(blank=False, max_length=255, db_index=False)
    Icon = models.CharField(blank=False, max_length=255, db_index=False)
    rowNum = models.IntegerField(blank=False, default=0)
    ParentID = models.IntegerField(blank=False, default=0)
    design = models.ForeignKey(Nologindesign)


class OrganizationCmsitem(models.Model):
    class Meta:
        db_table = 'organization_cmsitem'
    CmsItem = models.CharField(blank=False, max_length=255, db_index=False)
    Url = models.CharField(blank=False, max_length=255, db_index=False)
    Icon = models.CharField(blank=False, max_length=255, db_index=False)
    Grade = models.CharField(blank=False, max_length=255, db_index=False)
    rowNum = models.IntegerField(blank=False, default=0)
    organization = models.ForeignKey(OrganizationMetadata)


class OrganizationMenu(models.Model):
    class Meta:
        db_table = 'organization_menu'
    itemType = models.CharField(blank=False, max_length=255, db_index=False)
    itemValue = models.CharField(blank=False, max_length=255, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)

class DesignMenu(models.Model):
    class Meta:
        db_table = 'design_menu'
    itemType = models.CharField(blank=False, max_length=255, db_index=False)
    itemValue = models.CharField(blank=False, max_length=255, db_index=False)
    design = models.ForeignKey(Nologindesign)

class OrganizationDashboard(models.Model):
    class Meta:
        db_table = 'organization_dashboard'
    itemType = models.CharField(blank=False, max_length=255, db_index=False)
    itemValue = models.CharField(blank=False, max_length=255, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)


class OrganizationFooter(models.Model):
    class Meta:
        db_table = 'organization_footer'
    DataItem = models.TextField(blank=False, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)

class DesignFooter(models.Model):
    class Meta:
        db_table = 'design_footer'
    DataItem = models.TextField(blank=False, db_index=False)
    design = models.ForeignKey(Nologindesign)

class OrganizationMoreText(models.Model):
    class Meta:
        db_table = 'organization_more_text'
    DataItem = models.TextField(blank=False, db_index=False)
    itemType = models.CharField(blank=False, max_length=255, db_index=False)
    organization = models.ForeignKey(OrganizationMetadata)


def course_assignment_store():
    options = {}
    options.update(settings.FEEDINGSTORE['OPTIONS'])
    return CourseAssignmentStore(**options)

class CourseAssignmentStore(MongoBaseStore):
    def __init__(self, host, db, port,
                 user=None, password=None, mongo_options=None, **kwargs):
        # super(MongoBaseStore, self).__init__(**kwargs)
        MongoBaseStore.__init__(self, host, db, collection="course_assignment_store", port=port, **kwargs)

    def create_course_record(self, user_id, course_assignment_id, date):
        data = {
            "type":"course_record",
            "user_id":user_id,
            "course_assignment_id":course_assignment_id,
            "date":date
        }
        return self.insert(data)

    def find_record(self, user_id, course_assignment_id):
        res = list(self.find({"user_id":user_id,"course_assignment_id":course_assignment_id}))
        if res:
            return True
        return False