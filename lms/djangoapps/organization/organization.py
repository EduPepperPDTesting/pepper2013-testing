from mitxmako.shortcuts import render_to_response, render_to_string
from django.http import HttpResponse
import json
from models import *
from django import db
from datetime import datetime, timedelta, date
from pytz import UTC
from django.contrib.auth.models import User

import urllib2
from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from permissions.utils import check_access_level, check_user_perms
from StringIO import StringIO
import xlsxwriter
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School, CourseEnrollment
from xmodule.modulestore.django import modulestore
import pymongo
from django.db.models import Q
from django.conf import settings
from PIL import Image
import os
import os.path
import shutil

#-------------------------------------------------------------------main
def main(request):
    get_flag = request.GET.get("flag")
    post_flag = request.POST.get("flag")

    if(get_flag):
        if(get_flag == "organization_list"):
            return organization_list(request);

        elif(get_flag == "checkPost"):
            return organization_check(request);

        elif (get_flag == "organization_get"):
            return organization_get(request);

        elif (get_flag == "organization_main_get"):
            return organization_main_page_configuration_get(request);

    elif(post_flag):
        if (post_flag == "organization_add"):
            return organization_add(request);

        elif (post_flag == "organization_delete"):
            return organization_delete(request);

        elif (post_flag == "organizational_save_base"):
            return organizational_save_base(request);

        elif (post_flag == "org_upload"):
            return org_upload(request);

        elif (post_flag == "organizational_save_main_base"):
            return organizational_save_main_base(request);

        elif (post_flag == "org_main_upload"):
            return org_main_upload(request);

        elif (post_flag == "org_dashboard_upload"):
            return org_dashboard_upload(request);

        elif (post_flag == "org_dashboard_upload_cms"):
            return org_dashboard_upload_cms(request);

        elif (post_flag == "organization_check_Entity"):
            return org_check_Entity(request);

        elif (post_flag == "organization_remove_img"):
            return organization_remove_img(request);

        elif (post_flag == "organization_get_info"):
            return organization_get_info(request);

    else:
        tmp = "organization/organization.html";
        return render_to_response(tmp)

#-------------------------------------------------------------------organization_list
@login_required
def organization_list(request):
    oid = request.GET.get("oid")
    if (oid):
        list = OrganizationMetadata.objects.filter(id=oid)
    else:
        list = OrganizationMetadata.objects.prefetch_related().all()

    rows = []
    for org in list:
        rows.append({'id': org.id, 'OrganizationName': org.OrganizationName})

    return HttpResponse(json.dumps({'success': True, 'rows': rows}), content_type="application/json")

#-------------------------------------------------------------------organization_check
@login_required
def organization_check(request):
    valid = True
    error = ''
    name = request.GET.get('name')
    oid = request.GET.get('oid')

    qs = Q(OrganizationName=name);
    if(oid != "-1"):
        qs &= ~Q(id=oid)

    if (OrganizationMetadata.objects.filter(qs).count()):
        valid = False
        error = 'This name is already in use. '

    return HttpResponse(json.dumps({'success': valid, 'Error': error}), content_type="application/json")

#-------------------------------------------------------------------organization_add
@login_required
def organization_add(request):
    name = request.POST.get('organizational_name', False)
    copyfromId = request.POST.get('organizational_copy_from', False)
    oid = request.POST.get('oid', False)
    data = {'Success': False}

    if name:
        if oid != "-1":
            organization = OrganizationMetadata.objects.get(id=oid)
        else:
            organization = OrganizationMetadata()

        try:
            organization.OrganizationName = name
            organization.save()

            if copyfromId:
                organization_old = OrganizationMetadata.objects.get(id=copyfromId) 

                path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + str(organization.id) + '/'
                if not os.path.exists(path):
                    os.mkdir(path)

                path_cms = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/cms/' + str(organization.id) + '/'
                if not os.path.exists(path):
                    os.mkdir(path)

                # --------------OrganizationMenuitem
                for bean1 in OrganizationMenuitem.objects.filter(organization=organization_old,ParentID=0):
                    org_menu_item = OrganizationMenuitem()
                    org_menu_item.MenuItem = bean1.MenuItem
                    org_menu_item.Url = bean1.Url
                    org_menu_item.Icon = bean1.Icon
                    org_menu_item.isAdmin = bean1.isAdmin                 
                    org_menu_item.rowNum = bean1.rowNum
                    org_menu_item.ParentID = 0
                    org_menu_item.organization = organization
                    org_menu_item.save()

                    if bean1.Icon != "":
                        tmp_logo_src = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + str(organization_old.id) + '/' + bean1.Icon
                        if os.path.exists(tmp_logo_src):
                            shutil.copyfile(tmp_logo_src, path + bean1.Icon)   

                    for bean2 in OrganizationMenuitem.objects.filter(organization=organization_old,ParentID=bean1.id):
                        org_menu_item2 = OrganizationMenuitem()
                        org_menu_item2.MenuItem = bean2.MenuItem
                        org_menu_item2.Url = bean2.Url
                        org_menu_item2.isAdmin = bean2.isAdmin                 
                        org_menu_item2.rowNum = bean2.rowNum
                        org_menu_item2.ParentID = org_menu_item.id
                        org_menu_item2.organization = organization
                        org_menu_item2.save()

                # --------------OrganizationCmsitem
                for bean1 in OrganizationCmsitem.objects.filter(organization=organization_old,):
                    org_cms_item = OrganizationCmsitem()
                    org_cms_item.CmsItem = bean1.CmsItem
                    org_cms_item.Url = bean1.Url
                    org_cms_item.Icon = bean1.Icon
                    org_cms_item.Grade = bean1.Grade                 
                    org_cms_item.rowNum = bean1.rowNum
                    org_cms_item.organization = organization
                    org_cms_item.save()

                    if bean1.Icon != "":
                        tmp_logo_src = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/cms/' + str(organization_old.id) + '/' + bean1.Icon
                        if os.path.exists(tmp_logo_src):
                            shutil.copyfile(tmp_logo_src, path + bean1.Icon)   

                # --------------OrganizationMenu
                for bean1 in OrganizationMenu.objects.filter(organization=organization_old):
                    org_menu = OrganizationMenu()
                    org_menu.itemType = bean1.itemType
                    org_menu.itemValue = bean1.itemValue
                    org_menu.organization = organization
                    org_menu.save()
                    
                    if (bean1.itemType == "logo" or bean1.itemType == "organization_logo") and bean1.itemValue != "":
                        tmp_logo_src = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + str(organization_old.id) + '/' + bean1.itemValue
                        if os.path.exists(tmp_logo_src):
                            shutil.copyfile(tmp_logo_src, path + bean1.itemValue)

                # --------------OrganizationDashboard
                for bean1 in OrganizationDashboard.objects.filter(organization=organization_old):
                    org_dashboard = OrganizationDashboard()
                    org_dashboard.itemType = bean1.itemType
                    org_dashboard.itemValue = bean1.itemValue
                    org_dashboard.organization = organization
                    org_dashboard.save()

            data = {'Success': True}
        except Exception as e:
            data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_add
@login_required
def organization_delete(request):
    try:
        for oid in request.POST.get("ids", "").split(","):
            org = OrganizationMetadata.objects.filter(id=oid)

            OrganizationDataitems.objects.filter(organization=org).delete()
            OrganizationDistricts.objects.filter(organization=org).delete()
            OrganizationAttributes.objects.filter(organization=org).delete()
            OrganizationMenuitem.objects.filter(organization=org).delete()
            OrganizationMenu.objects.filter(organization=org).delete()
            OrganizationDashboard.objects.filter(organization=org).delete()

            org.delete()

        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------org_check_Entity
@login_required
def org_check_Entity(request):
    try:
        oid = request.POST.get("oid", "")
        add_id = request.POST.get("add_id", "")
        add_type = request.POST.get("add_type", "")
        is_add = True

        if(oid and add_id and add_type):
            org_districts_list = OrganizationDistricts.objects.filter(EntityType=add_type, OrganizationEnity=add_id)
            for tmp1 in org_districts_list:
                if(tmp1.organization.id != oid):
                    is_add = False;
                    break;

        data = {'Success': True, 'Add': is_add}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_remove_img
@login_required
def organization_remove_img(request):
    data = {'Success': False}
    try:
        oid = request.POST.get("oid", "")
        column = request.POST.get("column", "")
        db = request.POST.get("db", "")

        if(column and db):
            if(db == "configuration"):
                for tmp1 in MainPageConfiguration.objects.all():
                    if(column == "TopMainLogo"):
                        filename = tmp1.TopMainLogo
                        tmp1.TopMainLogo = ""
                    elif(column == "BottomMainLogo"):
                        filename = tmp1.BottomMainLogo
                        tmp1.BottomMainLogo = ""
                    else:
                        filename = tmp1.MainPageBottomImage
                        tmp1.MainPageBottomImage = ""

                    filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/main_page/' + filename
                    if os.path.isfile(filename):
                        os.remove(filename)

                    tmp1.save()
                    data = {'Success': True}
                    break;
            else:
                if(oid):
                    if (column == "LogoHome"):
                        for tmp1 in OrganizationMetadata.objects.filter(id=oid):                           
                            for tmp2 in OrganizationMenu.objects.filter(organization=tmp1, itemType="logo"):                               
                                filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + "/" + tmp2.itemValue
                                tmp2.itemValue = ""
                                tmp2.save()

                                if os.path.isfile(filename):
                                    os.remove(filename)
                                
                                data = {'Success': True}
                                break;
                            break;
                    elif (column == "OrganizationLogo"):
                        for tmp1 in OrganizationMetadata.objects.filter(id=oid):                           
                            for tmp2 in OrganizationMenu.objects.filter(organization=tmp1, itemType="organization_logo"):
                                filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + "/" + tmp2.itemValue
                                tmp2.itemValue = ""
                                tmp2.save()

                                if os.path.isfile(filename):
                                    os.remove(filename)
                                
                                data = {'Success': True}
                                break;
                            break;

                    elif (column == "LogoProfile"):
                        for tmp1 in OrganizationMetadata.objects.filter(id=oid):
                            for tmp2 in OrganizationAttributes.objects.filter(organization=tmp1):
                                if (column == "LogoProfile"):
                                    filename = tmp2.LogoProfile
                                    tmp2.LogoProfile = ""

                                filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + "/" + filename
                                if os.path.isfile(filename):
                                    os.remove(filename)

                                tmp2.save()
                            data = {'Success': True}
                            break;

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_get
@login_required
def organization_get(request):
    oid = request.GET.get('oid', False)
    data = {}
    try:
        if oid:
            data = {'Success': True}
            organizations = OrganizationMetadata.objects.filter(id=oid)
            if(len(organizations) > 0):
                data['find'] = True
                for tmp in organizations:
                    org = tmp
                    data['New'] = True

                    # --------------OrganizationMetadata
                    data['DistrictType'] = org.DistrictType
                    data['SchoolType'] = org.SchoolType

                    if (org.DistrictType != ""):
                        data['New'] = False

                    # --------------OrganizationDataitems
                    org_data_list = OrganizationDataitems.objects.filter(organization=organizations)
                    for tmp1 in org_data_list:
                        data['specific_items'] = tmp1.DataItem
                        data['New'] = False
                        break;

                    # --------------OrganizationDistricts
                    sid_did = "";
                    org_dir_list = OrganizationDistricts.objects.filter(organization=organizations)
                    for tmp1 in org_dir_list:
                        if(not sid_did == ""):
                            sid_did += ":"

                        tmp1_text = "";
                        if(tmp1.EntityType == "State"):
                            for tmp2 in State.objects.filter(id=tmp1.OrganizationEnity):
                                tmp1_text = tmp2.name
                                break;
                        elif(tmp1.EntityType == "District"):
                            for tmp2 in District.objects.filter(id=tmp1.OrganizationEnity):
                                tmp1_text = tmp2.name
                                break;
                        else:
                            for tmp2 in School.objects.filter(id=tmp1.OrganizationEnity):
                                tmp1_text = tmp2.name
                                break;

                        sid_did += tmp1.EntityType + "," + str(tmp1.OrganizationEnity) + "," + tmp1_text

                        if(data['New']):
                            data['New'] = False

                    data['sid_did'] = sid_did

                    # --------------OrganizationAttributes
                    org_attr_list = OrganizationAttributes.objects.filter(organization=organizations)
                    for tmp1 in org_attr_list:
                        data['home_logo'] = tmp1.LogoHome
                        data['profile_logo'] = tmp1.LogoProfile
                        data['motto'] = tmp1.Motto
                        data['New'] = False
                        break;
                    
                    # --------------OrganizationDashboard
                    for tmp1 in OrganizationDashboard.objects.filter(organization=organizations):
                        data[tmp1.itemType] = tmp1.itemValue

                    # --------------OrganizationMenu
                    for tmp1 in OrganizationMenu.objects.filter(organization=organizations):
                        data[tmp1.itemType] = tmp1.itemValue

                    # --------------OrganizationMenu
                    menu_items = ""
                    for tmp1 in OrganizationMenuitem.objects.filter(organization=organizations,ParentID=0):
                        if menu_items != "":
                            menu_items = menu_items + "=<="

                        menu_items_child = ""
                        for tmp2 in OrganizationMenuitem.objects.filter(organization=organizations,ParentID=tmp1.id):
                            if menu_items_child != "":
                                menu_items_child = menu_items_child + "_<_"
                            
                            menu_items_child = menu_items_child + str(tmp2.rowNum) + "_>_" + tmp2.MenuItem + "_>_" + tmp2.Url + "_>_" + str(tmp2.isAdmin)

                        menu_items = menu_items + str(tmp1.rowNum) + "=>=" + tmp1.MenuItem + "=>=" + tmp1.Url + "=>=" + str(tmp1.isAdmin) + "=>=" + menu_items_child + "=>=" + tmp1.Icon
                    
                    data["menu_items"] = menu_items

                    # --------------OrganizationCms
                    cms_items = ""
                    for tmp1 in OrganizationCmsitem.objects.filter(organization=organizations):
                        if cms_items != "":
                            cms_items = cms_items + "=<="

                        cms_items = cms_items + str(tmp1.rowNum) + "=>=" + tmp1.CmsItem + "=>=" + tmp1.Url + "=>=" + tmp1.Grade + "=>=" + tmp1.Icon
                    
                    data["cms_items"] = cms_items

                    break;
            else:
                data['find'] = False
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organizational_save_base
@login_required
def organizational_save_base(request):
    try:
        oid = request.POST.get("oid", "")
        for_district = request.POST.get("for_district", "")
        for_school = request.POST.get("for_school", "")
        specific_items = request.POST.get("specific_items", "")
        sid_did = request.POST.get("sid_did", "")
        motto = request.POST.get("motto", "")
        menu_items = request.POST.get("menu_items", "")
        cms_items = request.POST.get("cms_items", "")
        dashboard_option = request.POST.get("dashboard_option", "")
        is_icon = request.POST.get("is_icon", "")
        is_icon_width_text = request.POST.get("is_icon_width_text", "")
        new_show_left = request.POST.get("new_show_left", "")
        new_show_right = request.POST.get("new_show_right", "")
        menu_text_color = request.POST.get("menu_text_color", "")
        menu_text_font = request.POST.get("menu_text_font", "")
        menu_text_size = request.POST.get("menu_text_size", "")
        menu_text_color_icons = request.POST.get("menu_text_color_icons", "")
        menu_text_font_icons = request.POST.get("menu_text_font_icons", "")
        menu_text_size_icons = request.POST.get("menu_text_size_icons", "")
        space_between_items = request.POST.get("space_between_items", "")
        menu_text_color_me = request.POST.get("menu_text_color_me", "")
        menu_text_font_me = request.POST.get("menu_text_font_me", "")
        menu_text_size_me = request.POST.get("menu_text_size_me", "")
        menu_color = request.POST.get("menu_color", "")
        is_new_menu = request.POST.get("is_new_menu", "")
        my_feed_show = request.POST.get("my_feed_show", "")
        my_activities_show = request.POST.get("my_activities_show", "")
        my_report_show = request.POST.get("my_report_show", "")
        my_featured_show = request.POST.get("my_featured_show", "")
        is_my_feed_default = request.POST.get("is_my_feed_default", "")        
        org_logo_url = request.POST.get("org_logo_url", "")
        logo_url = request.POST.get("logo_url", "")

        if(oid):
            # --------------OrganizationMetadata
            org_metadata = OrganizationMetadata();
            org_metadata_list = OrganizationMetadata.objects.filter(id=oid)
            for tmp1 in org_metadata_list:
                org_metadata = tmp1
                break;

            org_metadata.DistrictType = for_district
            org_metadata.SchoolType = for_school

            org_metadata.save();

            #--------------OrganizationDataitems
            if(not specific_items):
                specific_items = "";
            org_data = OrganizationDataitems();
            org_data_list = OrganizationDataitems.objects.filter(organization=org_metadata)
            for tmp1 in org_data_list:
                org_data = tmp1
                break;

            org_data.DataItem = specific_items
            org_data.organization = org_metadata

            org_data.save();

            # --------------OrganizationDistricts
            OrganizationDistricts.objects.filter(organization=org_metadata).delete()
            if(sid_did and sid_did != ""):
                for tmp1 in sid_did.split(":"):
                    tmp2 = tmp1.split(",")
                    org_dis = OrganizationDistricts()
                    org_dis.EntityType = tmp2[1]
                    org_dis.OrganizationEnity = tmp2[0]
                    org_dis.organization = org_metadata
                    org_dis.save();

            # --------------OrganizationAttributes            
            org_attr = OrganizationAttributes();
            org_attr_list = OrganizationAttributes.objects.filter(organization=org_metadata)
            for tmp1 in org_attr_list:
                org_attr = tmp1
                break;

            org_attr.Motto = motto
            org_attr.organization = org_metadata

            org_attr.save();
 
            # --------------OrganizationMenuitem
            OrganizationMenuitem.objects.filter(organization=org_metadata).delete()
            if (menu_items):                
                for tmp1 in menu_items.split("=<="):
                    tmp2 = tmp1.split("=>=")

                    org_menu_item = OrganizationMenuitem()
                    org_menu_item.organization = org_metadata
                    org_menu_item.MenuItem = tmp2[1]
                    org_menu_item.Url = tmp2[2]
                    if tmp2[5] != "":
                        org_menu_item.Icon = tmp2[5]
                            
                    if tmp2[3] == "1":
                        org_menu_item.isAdmin = True
                    else:
                        org_menu_item.isAdmin = False
                    org_menu_item.rowNum = tmp2[0]
                    org_menu_item.save()
                    if tmp2[4]:
                        for tmp3 in tmp2[4].split("_<_"):
                            tmp4 = tmp3.split("_>_")
                            org_menu_item1 = OrganizationMenuitem()
                            org_menu_item1.organization = org_metadata
                            org_menu_item1.MenuItem = tmp4[1]
                            org_menu_item1.Url = tmp4[2]
                            if tmp4[3] == "1":
                                org_menu_item1.isAdmin = True
                            else:
                                org_menu_item1.isAdmin = False
                            org_menu_item1.rowNum = tmp4[0]
                            org_menu_item1.ParentID = org_menu_item.id
                            org_menu_item1.save() 

            # --------------OrganizationCmsitem
            OrganizationCmsitem.objects.filter(organization=org_metadata).delete()
            if (cms_items):                
                for tmp1 in cms_items.split("=<="):
                    tmp2 = tmp1.split("=>=")

                    org_menu_item = OrganizationCmsitem()
                    org_menu_item.organization = org_metadata
                    org_menu_item.CmsItem = tmp2[1]
                    org_menu_item.Url = tmp2[2]
                    org_menu_item.Grade = tmp2[3]
                    if tmp2[4] != "":
                        org_menu_item.Icon = tmp2[4]
                    
                    org_menu_item.rowNum = tmp2[0]
                    org_menu_item.save()

            # --------------OrganizationMenu Menu color
            org_OrganizationMenuSave(org_metadata, "Menu Color", menu_color)             

            # --------------OrganizationMenu Is Icon
            org_OrganizationMenuSave(org_metadata, "Is Icon", is_icon)       

            # --------------OrganizationMenu Is Icon with Text         
            org_OrganizationMenuSave(org_metadata, "Is Icon With Text", is_icon_width_text) 

            # --------------OrganizationMenu Is Icon with Text         
            org_OrganizationMenuSave(org_metadata, "Show Left DB", new_show_left) 

            # --------------OrganizationMenu Is Icon with Text         
            org_OrganizationMenuSave(org_metadata, "Show Right DB", new_show_right) 

            # --------------OrganizationMenu Text Color
            org_OrganizationMenuSave(org_metadata, "Text Color", menu_text_color) 

            # --------------OrganizationMenu Text Font
            org_OrganizationMenuSave(org_metadata, "Text Font", menu_text_font) 

            # --------------OrganizationMenu Text Size
            org_OrganizationMenuSave(org_metadata, "Text Size", menu_text_size)   

            # --------------OrganizationMenu Text Color Icons
            org_OrganizationMenuSave(org_metadata, "Text Color Icons", menu_text_color_icons) 

            # --------------OrganizationMenu Text Font Icons
            org_OrganizationMenuSave(org_metadata, "Text Font Icons", menu_text_font_icons) 

            # --------------OrganizationMenu Text Size Icons
            org_OrganizationMenuSave(org_metadata, "Text Size Icons", menu_text_size_icons)    

            # --------------OrganizationMenu Text Color Me
            org_OrganizationMenuSave(org_metadata, "Text Color Me", menu_text_color_me) 

            # --------------OrganizationMenu Text Font Me
            org_OrganizationMenuSave(org_metadata, "Text Font Me", menu_text_font_me) 

            # --------------OrganizationMenu Text Size Me
            org_OrganizationMenuSave(org_metadata, "Text Size Me", menu_text_size_me)   

            # --------------OrganizationMenu Space Betwwen Items
            org_OrganizationMenuSave(org_metadata, "Space Betwwen Items", space_between_items)

            # --------------OrganizationMenu Is New Menu
            org_OrganizationMenuSave(org_metadata, "Is New Menu", is_new_menu)

            # --------------OrganizationMenu My Feed Show
            org_OrganizationMenuSave(org_metadata, "My Feed Show", my_feed_show)

            # --------------OrganizationMenu My Activities Show
            org_OrganizationMenuSave(org_metadata, "My Activities Show", my_activities_show)

            # --------------OrganizationMenu My Report Show
            org_OrganizationMenuSave(org_metadata, "My Report Show", my_report_show)

            # --------------OrganizationMenu My Featured Show
            org_OrganizationMenuSave(org_metadata, "My Featured Show", my_featured_show)

            # --------------OrganizationMenu Is My Feed Default
            org_OrganizationMenuSave(org_metadata, "Is My Feed Default", is_my_feed_default)

            # --------------OrganizationMenu Organization Logo Url
            org_OrganizationMenuSave(org_metadata, "Organization Logo Url", org_logo_url)

            # --------------OrganizationMenu Logo Url
            org_OrganizationMenuSave(org_metadata, "Logo Url", logo_url)

            # --------------organizationDashboard
            if(dashboard_option):
                org_dashboard = OrganizationDashboard()
                for tmp1 in OrganizationDashboard.objects.filter(organization=org_metadata, itemType="Dashboard option etc"):
                    org_dashboard = tmp1
                    break;

                org_dashboard.organization = org_metadata               
                org_dashboard.itemType = "Dashboard option etc"
                org_dashboard.itemValue = dashboard_option
                org_dashboard.save()

        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------org_OrganizationMenuSave
def org_OrganizationMenuSave(organization, itemType, itemValue):
    #if(itemValue):
    org_menu_tmp = OrganizationMenu()
    for tmp1 in OrganizationMenu.objects.filter(organization=organization, itemType=itemType):
        org_menu_tmp = tmp1
        break;

    org_menu_tmp.organization = organization               
    org_menu_tmp.itemType = itemType
    org_menu_tmp.itemValue = itemValue
    org_menu_tmp.save()

#-------------------------------------------------------------------organizational_save_base
@login_required
def org_upload(request):
    try:
        data = {'Success': False}

        file_type = request.POST.get("file_type", "")
        oid = request.POST.get("oid", "")

        if(file_type and oid):
            organization = OrganizationMetadata.objects.get(id=oid)

            if file_type == "home_logo":
                imgx = request.FILES.get("organizational_base_home_logo", None)
            
            elif file_type == "organization_logo":
                imgx = request.FILES.get("organizational_base_organization_logo", None)

            elif file_type == "profile_logo":
                imgx = request.FILES.get("organizational_base_profile_logo", None)

            elif file_type == "top_main_logo":
                imgx = request.FILES.get("organizational_base_top_main_logo", None)

            elif file_type == "bottom_main_logo":
                imgx = request.FILES.get("organizational_base_bottom_main_logo", None)

            elif file_type == "main_page_bottom_image":
                imgx = request.FILES.get("organizational_base_main_page_bottom_image", None)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + '/'
            if not os.path.exists(path):
                os.mkdir(path)

            if imgx:
                ext = os.path.splitext(imgx.name)[1]
                destination = open(path + file_type + ext, 'wb+')
                for chunk in imgx.chunks():
                    destination.write(chunk)
                destination.close()

                org_attr = OrganizationAttributes()
                for tmp1 in OrganizationAttributes.objects.filter(organization=organization):
                    org_attr = tmp1
                    break;                

                org_attr.organization = organization
                
                org_menu = OrganizationMenu()
                if file_type == "home_logo":
                    for tmp1 in OrganizationMenu.objects.filter(organization=organization, itemType="logo"):
                        org_menu = tmp1
                        break;

                    org_menu.organization = organization
                    org_menu.itemType = "logo"
                    org_menu.itemValue = file_type + ext
                    org_menu.save()

                elif file_type == "organization_logo":
                    for tmp1 in OrganizationMenu.objects.filter(organization=organization, itemType="organization_logo"):
                        org_menu = tmp1
                        break;

                    org_menu.organization = organization
                    org_menu.itemType = "organization_logo"
                    org_menu.itemValue = file_type + ext
                    org_menu.save()

                elif file_type == "profile_logo":
                    org_attr.LogoProfile = file_type + ext
                    org_attr.save()

                elif file_type == "top_main_logo":
                    org_attr.TopMainLogo = file_type + ext
                    org_attr.save()

                elif file_type == "bottom_main_logo":
                    org_attr.BottomMainLogo = file_type + ext
                    org_attr.save()

                elif file_type == "main_page_bottom_image":
                    org_attr.MainPageBottomImage = file_type + ext
                    org_attr.save()                

                data = {'Success': True, 'name': file_type + ext}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_main_page_configuration_get
@login_required
def organization_main_page_configuration_get(request):
    data = {}
    try:
        flag_new = True
        for org_main in MainPageConfiguration.objects.prefetch_related().all():
            flag_new = False
            data['SiteURL'] = org_main.SiteURL
            data['TopMainLogo'] = org_main.TopMainLogo
            data['MainLogoText'] = org_main.MainLogoText
            data['BottomMainLogo'] = org_main.BottomMainLogo
            data['MainPageBottomImage'] = org_main.MainPageBottomImage
            data['MainPageButtonText'] = org_main.MainPageButtonText
            data['MainPageButtonLink'] = org_main.MainPageButtonLink
            data['mid'] = org_main.id
            break;

        data['flag_new'] = flag_new
        data['Success'] = True

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organizational_save_main_base
@login_required
def organizational_save_main_base(request):
    try:
        site_url = request.POST.get("site_url", "")
        logo_text = request.POST.get("logo_text", "")
        button_text = request.POST.get("button_text", "")
        button_link = request.POST.get("button_link", "")

        org_main = MainPageConfiguration()
        for tmp1 in MainPageConfiguration.objects.prefetch_related().all():
            org_main = tmp1
            break;

        org_main.SiteURL = site_url
        org_main.MainLogoText = logo_text
        org_main.MainPageButtonText = button_text
        org_main.MainPageButtonLink = button_link
        org_main.save();
        data = {'Success': True}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------org_main_upload
@login_required
def org_main_upload(request):
    try:
        data = {'Success': False}
        file_type = request.POST.get("file_type", "")

        if(file_type):
            if file_type == "top_main_logo":
                imgx = request.FILES.get("organizational_base_top_main_logo", None)

            elif file_type == "bottom_main_logo":
                imgx = request.FILES.get("organizational_base_bottom_main_logo", None)

            elif file_type == "main_page_bottom_image":
                imgx = request.FILES.get("organizational_base_main_page_bottom_image", None)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/main_page/'
            if not os.path.exists(path):
                os.mkdir(path)

            if imgx:
                ext = os.path.splitext(imgx.name)[1]
                destination = open(path + file_type + ext, 'wb+')
                for chunk in imgx.chunks():
                    destination.write(chunk)
                destination.close()

                for mainpage in MainPageConfiguration.objects.prefetch_related().all():
                    if file_type == "top_main_logo":
                        mainpage.TopMainLogo = file_type + ext

                    elif file_type == "bottom_main_logo":
                        mainpage.BottomMainLogo = file_type + ext

                    elif file_type == "main_page_bottom_image":
                        mainpage.MainPageBottomImage = file_type + ext

                    mainpage.save()
                    break;

                data = {'Success': True, 'name': file_type + ext}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------org_dashboard_upload
@login_required
def org_dashboard_upload(request):
    try:
        data = {'Success': False}

        rowNum = request.POST.get("rowNum", "")
        oid = request.POST.get("oid", "")
        fileElementId = request.POST.get("fileElementId", "")

        if(rowNum and oid):
            rowNum = str(rowNum)
            organization = OrganizationMetadata.objects.get(id=oid)            
            imgx = request.FILES.get("menu_items_icon_" + rowNum, None)
            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + '/'
           
            if not os.path.exists(path):
                os.mkdir(path)

            if imgx:
                destination = open(path + imgx.name, 'wb+')
                for chunk in imgx.chunks():
                    destination.write(chunk)
                destination.close()
                
                for org_menu_item in OrganizationMenuitem.objects.filter(organization=organization,rowNum=int(rowNum),ParentID=0):
                    org_menu_item.Icon = imgx.name
                    org_menu_item.save()
                    break;              

                data = {'Success': True, 'name': imgx.name}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------org_dashboard_upload_cms
@login_required
def org_dashboard_upload_cms(request):
    try:
        data = {'Success': False}

        rowNum = request.POST.get("rowNum", "")
        oid = request.POST.get("oid", "")
        fileElementId = request.POST.get("fileElementId", "")

        if(rowNum and oid):
            rowNum = str(rowNum)
            organization = OrganizationMetadata.objects.get(id=oid)            
            imgx = request.FILES.get("cms_items_icon_" + rowNum, None)
            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/cms/'
            if not os.path.exists(path):
                os.mkdir(path)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/cms/' + oid + '/'
            if not os.path.exists(path):
                os.mkdir(path)

            if imgx:
                destination = open(path + imgx.name, 'wb+')
                for chunk in imgx.chunks():
                    destination.write(chunk)
                destination.close()
                
                for org_menu_item in OrganizationCmsitem.objects.filter(organization=organization,rowNum=int(rowNum)):
                    org_menu_item.Icon = imgx.name
                    org_menu_item.save()
                    break;              

                data = {'Success': True, 'name': imgx.name}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_get_info
def organization_get_info(request):
    source = request.POST.get('source', False)
    flag_main = request.POST.get('flag_main', False)
    data = {'Success': False, 'SiteURL_OK': False, 'flag_main': flag_main}

    try:
        data['url'] = request.get_host()
        for org_main in MainPageConfiguration.objects.prefetch_related().all():
            if (org_main.SiteURL == data['url']):
                data['SiteURL_OK'] = True

                if(flag_main == "index"):
                    data['TopMainLogo'] = org_main.TopMainLogo
                    data['MainLogoText'] = org_main.MainLogoText
                    data['BottomMainLogo'] = org_main.BottomMainLogo
                    data['MainPageBottomImage'] = org_main.MainPageBottomImage
                    data['MainPageButtonText'] = org_main.MainPageButtonText
                    data['MainPageButtonLink'] = org_main.MainPageButtonLink
            else:
                data['SiteURL_OK'] = False
            break;

        if(data['SiteURL_OK']):
            if (source == "register"):
                district = request.POST.get('district', False)
                state = request.POST.get('state', False)
                school = request.POST.get('school', False)

                data['OrganizationOK'] = False

                if (school):
                    for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=school, EntityType="School"):
                        data['OrganizationOK'] = True
                        organization_obj = tmp1.organization
                        break;

                if (not(data['OrganizationOK']) and district):
                    for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=district, EntityType="District"):
                        data['OrganizationOK'] = True
                        organization_obj = tmp1.organization
                        break;

                if(not(data['OrganizationOK']) and state):
                    for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=state, EntityType="State"):
                        data['OrganizationOK'] = True
                        organization_obj = tmp1.organization
                        break;

                if(data['OrganizationOK']):
                    data['DistrictType'] = organization_obj.DistrictType
                    data['SchoolType'] = organization_obj.SchoolType
                    data['OrganizationName'] = organization_obj.OrganizationName

                    for tmp2 in OrganizationDataitems.objects.filter(organization=organization_obj):
                        data['org_rg_major_subject'] = tmp2.DataItem.find("org_rg_major_subject")
                        data['org_rg_grade_level'] = tmp2.DataItem.find("org_rg_grade_level")
                        data['org_rg_number_of'] = tmp2.DataItem.find("org_rg_number_of")
                        data['org_rg_my_learners'] = tmp2.DataItem.find("org_rg_my_learners")
                        data['org_rg_about_me'] = tmp2.DataItem.find("org_rg_about_me")
                        break;


                data['Success'] = True

            elif(source == "navigation"):
                if request.user.is_authenticated():
                    try:
                        state = request.user.profile.district.state.id
                        district = request.user.profile.district.id
                        school = request.user.profile.school.id
                    except:
                        state = -1
                        district = -1
                        school = -1
                    
                    data['OrganizationOK'] = False

                    if (school != -1):
                        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=school,
                                                                         EntityType="School"):
                            data['OrganizationOK'] = True
                            organization_obj = tmp1.organization
                            break;

                    if (not (data['OrganizationOK']) and district != -1):
                        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=district,
                                                                         EntityType="District"):
                            data['OrganizationOK'] = True
                            organization_obj = tmp1.organization
                            break;

                    if (not (data['OrganizationOK']) and state != -1):
                        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=state, EntityType="State"):
                            data['OrganizationOK'] = True
                            organization_obj = tmp1.organization
                            break;

                    if (data['OrganizationOK']):
                        data['OrganizationName'] = organization_obj.OrganizationName
                        data['OrganizationId'] = organization_obj.id
                        data['DistrictType'] = organization_obj.DistrictType
                        data['SchoolType'] = organization_obj.SchoolType

                        for tmp2 in OrganizationDataitems.objects.filter(organization=organization_obj):
                            data['org_tm_course_workshop_obj'] = tmp2.DataItem.find("org_tm_course_workshop")
                            data['org_tm_communities_obj'] = tmp2.DataItem.find("org_tm_communities")
                            data['org_tm_my_chunks_obj'] = tmp2.DataItem.find("org_tm_my_chunks")
                            data['org_tm_resources_obj'] = tmp2.DataItem.find("org_tm_resources")
                            data['org_tm_people_obj'] = tmp2.DataItem.find("org_tm_people")
                            data['org_tm_notifications_obj'] = tmp2.DataItem.find("org_tm_notifications")

                            data['org_tsm_configuration_obj'] = tmp2.DataItem.find("org_tsm_configuration")
                            data['org_tsm_pepper_pd_planner_obj'] = tmp2.DataItem.find("org_tsm_pepper_pd_planner")
                            data['org_tsm_pepconn_obj'] = tmp2.DataItem.find("org_tsm_pepconn")
                            data['org_tsm_roles_permissions_obj'] = tmp2.DataItem.find("org_tsm_roles_permissions")
                            data['org_tsm_time_report_obj'] = tmp2.DataItem.find("org_tsm_time_report")
                            data['org_tsm_reporting_obj'] = tmp2.DataItem.find("org_tsm_reporting")
                            data['org_tsm_sso_metadata_obj'] = tmp2.DataItem.find("org_tsm_sso_metadata")
                            data['org_tsm_tnl_configuration_obj'] = tmp2.DataItem.find("org_tsm_tnl_configuration")
                            data['org_tsm_studio_obj'] = tmp2.DataItem.find("org_tsm_studio")
                            data['org_tsm_alert_obj'] = tmp2.DataItem.find("org_tsm_alert")
                            data['org_tsm_notifications_obj'] = tmp2.DataItem.find("org_tsm_notifications")
                            data['org_tsm_usage_report_obj'] = tmp2.DataItem.find("org_tsm_usage_report")
                            data['org_tsm_portfolio_settings_obj'] = tmp2.DataItem.find("org_tsm_portfolio_settings")
                            break;


                        for tmp2 in OrganizationAttributes.objects.filter(organization=organization_obj):
                            data['LogoHome'] = tmp2.LogoHome
                            if (flag_main == "dashboard"):
                                data['LogoProfile'] = tmp2.LogoProfile
                                data['Motto'] = tmp2.Motto
                            break;

                    data['Success'] = True

    except Exception as e:
        data = {'SiteURL_OK': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")
