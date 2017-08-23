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
from student.models import UserTestGroup, CourseEnrollment, UserProfile, District, State, School
from xmodule.modulestore.django import modulestore
import pymongo
from django.db.models import Q
from django.conf import settings
from PIL import Image
import os
import os.path
import shutil
from student.feeding import dashboard_feeding_store
import csv
from courseware.courses import get_courses, get_course_about_section
from django.core.validators import validate_email

# -------------------------------------------------------------------main
def main(request):
    get_flag = request.GET.get("flag")
    post_flag = request.POST.get("flag")

    if(get_flag):
        if(get_flag == "organization_list"):
            return organization_list(request)

        elif(get_flag == "checkPost"):
            return organization_check(request)

        elif (get_flag == "organization_get"):
            return organization_get(request)

        elif (get_flag == "organization_main_get"):
            return organization_main_page_configuration_get(request)

        elif (get_flag == "organization_get_locations"):
            return organization_get_locations(request)

    elif(post_flag):
        if (post_flag == "organization_add"):
            return organization_add(request)

        elif (post_flag == "organization_delete"):
            return organization_delete(request)

        elif (post_flag == "organizational_save_base"):
            return organizational_save_base(request)

        elif (post_flag == "org_upload"):
            return org_upload(request)

        elif (post_flag == "organizational_save_main_base"):
            return organizational_save_main_base(request)

        elif (post_flag == "org_main_upload"):
            return org_main_upload(request)

        elif (post_flag == "org_dashboard_upload"):
            return org_dashboard_upload(request)

        elif (post_flag == "org_dashboard_upload_cms"):
            return org_dashboard_upload_cms(request)

        elif (post_flag == "org_option_cvs_upload"):
            return org_option_cvs_upload(request)

        elif (post_flag == "organization_check_Entity"):
            return org_check_Entity(request)

        elif (post_flag == "organization_remove_img"):
            return organization_remove_img(request)

        elif (post_flag == "organization_get_info"):
            return organization_get_info(request)

        elif (post_flag == "organization_course_list"):
            return organization_course_list(request)

        elif (post_flag == "organization_manage_user_info"):
            return organization_manage_user_info(request)

        elif (post_flag == "org_manage_user_cvs_upload"):
            return org_manage_user_cvs_upload(request)
    else:
        tmp = "organization/organization.html"
        return render_to_response(tmp)


# -------------------------------------------------------------------organization_manage_user_info
@login_required
def organization_manage_user_info(request):
    email = request.POST.get('email', "")
    data = {'Success': False}

    try:
        if email != "":
            user = User.objects.get(email=email)
            if user:
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
                data['email'] = user.email
                data['state'] = user.profile.district.state.name
                data['district'] = user.profile.district.name
                data['school'] = user.profile.school.name
            else:
                data['email_error'] = True

            data['Success'] = True

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_manage_user_cvs_upload
@login_required
def org_manage_user_cvs_upload(request):
    data = {'Success': False}
    import_file = request.FILES.get('organization_manage_user_cvs')
    r = csv.reader(import_file, dialect=csv.excel)
    rows = []
    rows.extend(r)

    back_rows = []
    for i, line in enumerate(rows):
        email = line[0]
        try:
            validate_email(email)
            user = User.objects.get(email=email)
            back_rows.append({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "state": user.profile.district.state.name,
                "district": user.profile.district.name,
                "school": user.profile.school.name
            })
        except Exception as e:
            pass
            # data = {'Success': False, 'Error': '{0}'.format(e)}

    data = {'Success': True, 'back_rows': back_rows}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_list
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


# -------------------------------------------------------------------organization_check
@login_required
def organization_check(request):
    valid = True
    error = ''
    name = request.GET.get('name')
    oid = request.GET.get('oid')

    qs = Q(OrganizationName=name)
    if(oid != "-1"):
        qs &= ~Q(id=oid)

    if (OrganizationMetadata.objects.filter(qs).count()):
        valid = False
        error = 'This name is already in use. '

    return HttpResponse(json.dumps({'success': valid, 'Error': error}), content_type="application/json")


# -------------------------------------------------------------------organization_add
@login_required
def organization_add(request):
    name = request.POST.get('organizational_name', False)
    copyfromid = request.POST.get('organizational_copy_from', False)
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

            # --------------OrganizationDataitems
            if oid == "-1":
                dataitems = '['
                dataitems = dataitems + '{"name":"Major Subject Area","required":"1","default":"1"},'
                dataitems = dataitems + '{"name":"Grade Level-Check all that apply","required":"1","default":"2"},'
                dataitems = dataitems + '{"name":"Number of Years in Education","required":"1","default":"3"},'
                dataitems = dataitems + '{"name":"My Learners\' Profile","required":"1","default":"4"},'
                dataitems = dataitems + '{"name":"About me","default":"5"}'
                dataitems = dataitems + ']'

                org_data = OrganizationDataitems()
                org_data.DataItem = dataitems
                org_data.organization = organization
                org_data.save()

            if copyfromid:
                organization_old = OrganizationMetadata.objects.get(id=copyfromid)

                path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/'
                if not os.path.exists(path):
                    os.mkdir(path)

                path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/cms/'
                if not os.path.exists(path):
                    os.mkdir(path)

                path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + str(organization.id) + '/'
                if not os.path.exists(path):
                    os.mkdir(path)

                path_cms = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/cms/' + str(organization.id) + '/'
                if not os.path.exists(path_cms):
                    os.mkdir(path_cms)

                # --------------OrganizationMenuitem
                for bean1 in OrganizationMenuitem.objects.filter(organization=organization_old, ParentID=0):
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

                    for bean2 in OrganizationMenuitem.objects.filter(organization=organization_old, ParentID=bean1.id):
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
                            shutil.copyfile(tmp_logo_src, path_cms + bean1.Icon)

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

                    if (bean1.itemType == "logo" or bean1.itemType == "Profile Logo" or bean1.itemType == "Profile Logo Curriculumn") and bean1.itemValue != "":
                        tmp_logo_src = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + str(organization_old.id) + '/' + bean1.itemValue
                        if os.path.exists(tmp_logo_src):
                            shutil.copyfile(tmp_logo_src, path + bean1.itemValue)

            data = {'Success': True}
        except Exception as e:
            data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_add
@login_required
def organization_delete(request):
    try:
        for oid in request.POST.get("ids", "").split(","):
            org = OrganizationMetadata.objects.filter(id=oid)

            OrganizationDataitems.objects.filter(organization=org).delete()
            OrganizationDistricts.objects.filter(organization=org).delete()
            OrganizationMenuitem.objects.filter(organization=org).delete()
            OrganizationMenu.objects.filter(organization=org).delete()
            OrganizationDashboard.objects.filter(organization=org).delete()

            org.delete()

        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_check_Entity
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
                    is_add = False
                    break

        data = {'Success': True, 'Add': is_add}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_remove_img
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
                    break
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
                                break
                            break
                    elif (column == "OrganizationLogo"):
                        for tmp1 in OrganizationMetadata.objects.filter(id=oid):
                            for tmp2 in OrganizationMenu.objects.filter(organization=tmp1, itemType="organization_logo"):
                                filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + "/" + tmp2.itemValue
                                tmp2.itemValue = ""
                                tmp2.save()

                                if os.path.isfile(filename):
                                    os.remove(filename)

                                data = {'Success': True}
                                break
                            break

                    elif (column == "LogoProfile"):
                        for tmp1 in OrganizationMetadata.objects.filter(id=oid):
                            for tmp2 in OrganizationDashboard.objects.filter(organization=tmp1, itemType="Profile Logo"):
                                filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + "/" + tmp2.itemValue
                                tmp2.itemValue = ""
                                tmp2.save()

                                if os.path.isfile(filename):
                                    os.remove(filename)

                                data = {'Success': True}
                                break
                            break

                    elif (column == "LogoProfileCurr"):
                        for tmp1 in OrganizationMetadata.objects.filter(id=oid):
                            for tmp2 in OrganizationDashboard.objects.filter(organization=tmp1, itemType="Profile Logo Curriculumn"):
                                filename = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + "/" + tmp2.itemValue
                                tmp2.itemValue = ""
                                tmp2.save()

                                if os.path.isfile(filename):
                                    os.remove(filename)

                                data = {'Success': True}
                                break
                            break

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_get
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

                    # --------------OrganizationMetadata
                    data['DistrictType'] = org.DistrictType
                    data['SchoolType'] = org.SchoolType

                    # --------------OrganizationDataitems
                    org_data_list = OrganizationDataitems.objects.filter(organization=organizations)
                    for tmp1 in org_data_list:
                        data['specific_items'] = tmp1.DataItem
                        break

                    # --------------OrganizationFooter
                    org_footer_list = OrganizationFooter.objects.filter(organization=organizations)
                    for tmp1 in org_footer_list:
                        data['Footer Content'] = tmp1.DataItem
                        break

                    # --------------OrganizationMoreText
                    org_announcement_list = OrganizationMoreText.objects.filter(organization=organizations, itemType="Announcement")
                    for tmp1 in org_announcement_list:
                        data['Announcement Content'] = tmp1.DataItem
                        break

                    # --------------OrganizationMoreText
                    for tmp1 in OrganizationMoreText.objects.filter(organization=organizations, itemType="menu_item_permission"):
                        data['menu_item_permission'] = tmp1.DataItem
                        break

                    # --------------Course Assignment
                    for tmp1 in OrganizationMoreText.objects.filter(organization=organizations, itemType="Course Assignment"):
                        data['Course Assignment'] = tmp1.DataItem
                        break

                    # --------------OrganizationDistricts
                    sid_did = ""
                    org_dir_list = OrganizationDistricts.objects.filter(organization=organizations)
                    for tmp1 in org_dir_list:
                        if(not sid_did == ""):
                            sid_did += ":"

                        tmp1_text = ""
                        if(tmp1.EntityType == "State"):
                            for tmp2 in State.objects.filter(id=tmp1.OrganizationEnity):
                                tmp1_text = tmp2.name
                                break
                        elif(tmp1.EntityType == "District"):
                            for tmp2 in District.objects.filter(id=tmp1.OrganizationEnity):
                                tmp1_text = tmp2.name
                                break
                        else:
                            for tmp2 in School.objects.filter(id=tmp1.OrganizationEnity):
                                tmp1_text = tmp2.name
                                break

                        sid_did += tmp1.EntityType + "," + str(tmp1.OrganizationEnity) + "," + tmp1_text + "," + str(tmp1.id)

                    data['sid_did'] = sid_did

                    # --------------OrganizationDashboard
                    for tmp1 in OrganizationDashboard.objects.filter(organization=organizations):
                        data[tmp1.itemType] = tmp1.itemValue

                    # --------------OrganizationMenu
                    for tmp1 in OrganizationMenu.objects.filter(organization=organizations):
                        data[tmp1.itemType] = tmp1.itemValue

                    # --------------OrganizationMenu
                    menu_items = ""
                    for tmp1 in OrganizationMenuitem.objects.filter(organization=organizations, ParentID=0):
                        if menu_items != "":
                            menu_items = menu_items + "=<="

                        menu_items_child = ""
                        for tmp2 in OrganizationMenuitem.objects.filter(organization=organizations, ParentID=tmp1.id):
                            if menu_items_child != "":
                                menu_items_child = menu_items_child + "_<_"

                            menu_items_child = menu_items_child + str(tmp2.rowNum) + "_>_" + tmp2.MenuItem + "_>_" + tmp2.Url + "_>_" + str(tmp2.isAdmin) + "_>_" + str(tmp2.id)

                        menu_items = menu_items + str(tmp1.rowNum) + "=>=" + tmp1.MenuItem + "=>=" + tmp1.Url + "=>=" + str(tmp1.isAdmin) + "=>=" + menu_items_child + "=>=" + tmp1.Icon + "=>=" + str(tmp1.id)

                    data["menu_items"] = menu_items

                    # --------------OrganizationCms
                    cms_items = ""
                    for tmp1 in OrganizationCmsitem.objects.filter(organization=organizations):
                        if cms_items != "":
                            cms_items = cms_items + "=<="

                        cms_items = cms_items + str(tmp1.rowNum) + "=>=" + tmp1.CmsItem + "=>=" + tmp1.Url + "=>=" + tmp1.Grade + "=>=" + tmp1.Icon

                    data["cms_items"] = cms_items

                    for tmp1 in OrganizationMoreText.objects.filter(organization=organizations, itemType="Cms Manage User"):
                        data["cms_manage_user"] = tmp1.DataItem
                        break

                    break
            else:
                data['find'] = False
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_get_locations
@login_required
def organization_get_locations(request):
    data = {}
    rows_state = []
    rows_district = []
    rows_school = []
    district_id = request.GET.get('district_id', "")
    school_id = request.GET.get('school_id', "")

    try:
        if district_id != "":
            for tmp1 in District.objects.filter(id=district_id):
                for tmp2 in School.objects.filter(district=tmp1).order_by("name"):
                    rows_school.append({'id': tmp2.id, 'name': tmp2.name, 'district_id': tmp2.district.id})
                break

        elif school_id != "":
            for tmp2 in School.objects.filter(id=school_id).order_by("name"):
                rows_school.append({'id': tmp2.id, 'name': tmp2.name, 'district_id': tmp2.district.id})

        else:
            for org in State.objects.all().order_by("name"):
                rows_state.append({'id': org.id, 'name': org.name})

            for org1 in District.objects.filter(state__isnull=False).order_by("name"):
                rows_district.append({'id': org1.id, 'name': org1.name, 'state_id': org1.state.id})

        data = {'Success': True, 'rows_state': rows_state, 'rows_district': rows_district, 'rows_school': rows_school}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organizational_save_base
@login_required
def organizational_save_base(request):
    try:
        oid = request.POST.get("oid", "")
        for_district = request.POST.get("for_district", "")
        for_school = request.POST.get("for_school", "")
        specific_items = request.POST.get("specific_items", "")
        sid_did = request.POST.get("sid_did", "")
        course_assignment_content = request.POST.get("course_assignment_content", "")
        motto = request.POST.get("motto", "")
        motto_curr = request.POST.get("motto_curr", "")
        menu_items = request.POST.get("menu_items", "")
        cms_items = request.POST.get("cms_items", "")
        dashboard_option = request.POST.get("dashboard_option", "")
        is_icon = request.POST.get("is_icon", "")
        is_icon_width_text = request.POST.get("is_icon_width_text", "")
        new_show_left = request.POST.get("new_show_left", "")
        new_show_right = request.POST.get("new_show_right", "")
        new_show_left_curr = request.POST.get("new_show_left_curr", "")
        new_show_right_curr = request.POST.get("new_show_right_curr", "")
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
        remove_all_menu = request.POST.get("remove_all_menu", "")
        menu_color = request.POST.get("menu_color", "")
        is_new_menu = request.POST.get("is_new_menu", "")
        my_feed_show = request.POST.get("my_feed_show", "")
        my_activities_show = request.POST.get("my_activities_show", "")
        my_report_show = request.POST.get("my_report_show", "")
        my_featured_show = request.POST.get("my_featured_show", "")
        is_my_feed_default = request.POST.get("is_my_feed_default", "")
        my_feed_show_curr = request.POST.get("my_feed_show_curr", "")
        my_activities_show_curr = request.POST.get("my_activities_show_curr", "")
        my_report_show_curr = request.POST.get("my_report_show_curr", "")
        my_featured_show_curr = request.POST.get("my_featured_show_curr", "")
        is_my_feed_default_curr = request.POST.get("is_my_feed_default_curr", "")
        org_logo_url = request.POST.get("org_logo_url", "")
        org_profile_logo_url = request.POST.get("org_profile_logo_url", "")
        org_profile_logo_curr_url = request.POST.get("org_profile_logo_curr_url", "")
        logo_url = request.POST.get("logo_url", "")
        footer_flag = request.POST.get("footer_flag", "")
        footer_content = request.POST.get("footer_content", "")
        is_announcement = request.POST.get("is_Announcement", "")
        announcement_content = request.POST.get("announcement_content", "")
        feed_txt = request.POST.get("feed_txt", "")
        activities_txt = request.POST.get("activities_txt", "")
        progress_txt = request.POST.get("progress_txt", "")
        resources_txt = request.POST.get("resources_txt", "")
        feed_txt_curr = request.POST.get("feed_txt_curr", "")
        activities_txt_curr = request.POST.get("activities_txt_curr", "")
        progress_txt_curr = request.POST.get("progress_txt_curr", "")
        resources_txt_curr = request.POST.get("resources_txt_curr", "")
        back_sid_all = ""

        if(oid):
            # --------------OrganizationMetadata
            org_metadata = OrganizationMetadata()
            org_metadata_list = OrganizationMetadata.objects.filter(id=oid)
            for tmp1 in org_metadata_list:
                org_metadata = tmp1
                break

            org_metadata.DistrictType = for_district
            org_metadata.SchoolType = for_school
            org_metadata.save()

            # --------------OrganizationDataitems
            if(not specific_items):
                specific_items = ""
            org_data = OrganizationDataitems()
            org_data_list = OrganizationDataitems.objects.filter(organization=org_metadata)
            for tmp1 in org_data_list:
                org_data = tmp1
                break

            org_data.DataItem = specific_items
            org_data.organization = org_metadata
            org_data.save()

            # --------------OrganizationFooter
            org_footer = OrganizationFooter()
            org_data_list = OrganizationFooter.objects.filter(organization=org_metadata)
            for tmp1 in org_data_list:
                org_footer = tmp1
                break

            org_footer.DataItem = footer_content
            org_footer.organization = org_metadata
            org_footer.save()

            # --------------OrganizationMoreText
            org_announcement = OrganizationMoreText()
            org_announcement_list = OrganizationMoreText.objects.filter(organization=org_metadata, itemType="Announcement")
            for tmp1 in org_announcement_list:
                org_announcement = tmp1
                break

            org_announcement.DataItem = announcement_content
            org_announcement.organization = org_metadata
            org_announcement.itemType = "Announcement"
            org_announcement.save()

            receiver_ids = [0]
            expiration_date = "01/01/2200"
            expiration_date = datetime.strptime(expiration_date + " 23:59:59", "%m/%d/%Y %H:%M:%S")

            store = dashboard_feeding_store()
            store.remove({"user_id": request.user.id, "source": "organization", "organization_type": "Pepper", "organization_id": oid})
            store.create(type='announcement', organization_type='Pepper', user_id=request.user.id, content=announcement_content, attachment_file=None, receivers=receiver_ids, date=datetime.utcnow(), expiration_date=expiration_date, source='organization', organization_id=oid)

            # --------------OrganizationDistricts
            if(sid_did != ""):
                sid_did_list = sid_did.split(":")
                org_dir_list = OrganizationDistricts.objects.filter(organization=org_metadata)

                # Delete the deleted records
                for org_dir_list_c in org_dir_list:
                    is_delete = True

                    for sid_did_list_c in sid_did_list:
                        array1 = sid_did_list_c.split(",")
                        if str(org_dir_list_c.id) == str(array1[2]):
                            is_delete = False
                            break

                    if is_delete:
                        org_dir_list_c.delete()

                # Add all
                for sid_did_list_c in sid_did_list:
                    array1 = sid_did_list_c.split(",")
                    array1_did = array1[2]
                    org_dis = OrganizationDistricts()
                    is_new = True
                    if array1_did != "":
                        for org_dir_list_c in OrganizationDistricts.objects.filter(id=array1_did):
                            org_dis = org_dir_list_c
                            if str(org_dis.EntityType) != str(array1[1]) or str(org_dis.OrganizationEnity) != str(array1[0]):
                                org_dis.OtherFields = "{'date':'" + str(datetime.utcnow()) + "'}"
                            is_new = False
                            break

                    org_dis.EntityType = array1[1]
                    org_dis.OrganizationEnity = array1[0]
                    org_dis.organization = org_metadata
                    if is_new:
                        org_dis.OtherFields = "{'date':'" + str(datetime.utcnow()) + "'}"

                    org_dis.save()

                    if back_sid_all != "":
                        back_sid_all += ","

                    back_sid_all += str(org_dis.id)
            else:
                OrganizationDistricts.objects.filter(organization=org_metadata).delete()

            # --------------OrganizationDashboard
            if(motto != ""):
                org_dashboard_motto = OrganizationDashboard()
                for tmp1 in OrganizationDashboard.objects.filter(organization=org_metadata, itemType="Motto"):
                    org_dashboard_motto = tmp1
                    break

                org_dashboard_motto.organization = org_metadata
                org_dashboard_motto.itemType = "Motto"
                org_dashboard_motto.itemValue = motto
                org_dashboard_motto.save()

            if(motto_curr != ""):
                org_dashboard_motto_curr = OrganizationDashboard()
                for tmp1 in OrganizationDashboard.objects.filter(organization=org_metadata, itemType="Motto Curriculumn"):
                    org_dashboard_motto_curr = tmp1
                    break

                org_dashboard_motto_curr.organization = org_metadata
                org_dashboard_motto_curr.itemType = "Motto Curriculumn"
                org_dashboard_motto_curr.itemValue = motto_curr
                org_dashboard_motto_curr.save()

            # --------------OrganizationMenuitem
            if (menu_items):
                menu_items_list = menu_items.split("=<=")

                # Delete the deleted records
                for item_c in OrganizationMenuitem.objects.filter(organization=org_metadata, ParentID=0):
                    if item_c.rowNum > len(menu_items_list):
                        OrganizationMenuitem.objects.filter(organization=org_metadata, ParentID=item_c.id).delete()
                        item_c.delete()

                permission_content = ""
                for tmp1 in menu_items_list:
                    tmp2 = tmp1.split("=>=")

                    org_menu_item = OrganizationMenuitem()
                    for org_menu_item1 in OrganizationMenuitem.objects.filter(organization=org_metadata, ParentID=0, rowNum=int(tmp2[0])):
                        org_menu_item = org_menu_item1
                        break

                    org_menu_item.organization = org_metadata
                    org_menu_item.MenuItem = tmp2[1]
                    org_menu_item.Url = tmp2[2]
                    org_menu_item.Icon = tmp2[5]
                    if tmp2[3] == "1":
                        org_menu_item.isAdmin = True
                    else:
                        org_menu_item.isAdmin = False
                    org_menu_item.rowNum = tmp2[0]
                    org_menu_item.save()

                    if permission_content != "":
                        permission_content += ", "
                    permission_content += "'id_" + str(org_menu_item.id) + "':'" + tmp2[6] + "'"

                    if tmp2[4]:
                        sub_items_list = tmp2[4].split("_<_")

                        # Delete the deleted records
                        for item_c in OrganizationMenuitem.objects.filter(organization=org_metadata, ParentID=org_menu_item.id):
                            if item_c.rowNum > len(sub_items_list):
                                item_c.delete()

                        for tmp3 in sub_items_list:
                            tmp4 = tmp3.split("_>_")
                            org_menu_item1 = OrganizationMenuitem()
                            for org_menu_item1_1 in OrganizationMenuitem.objects.filter(organization=org_metadata, ParentID=org_menu_item.id, rowNum=int(tmp4[0])):
                                org_menu_item1 = org_menu_item1_1
                                break

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

                            if permission_content != "":
                                permission_content += ", "

                            permission_content += "'id_" + str(org_menu_item1.id) + "':'" + tmp4[4] + "'"

                # --------------OrganizationMoreText
                org_permission = OrganizationMoreText()
                for tmp1 in OrganizationMoreText.objects.filter(organization=org_metadata, itemType="menu_item_permission"):
                    org_permission = tmp1
                    break

                org_permission.DataItem = "{" + permission_content + "}"
                org_permission.organization = org_metadata
                org_permission.itemType = "menu_item_permission"
                org_permission.save()
            else:
                OrganizationMenuitem.objects.filter(organization=org_metadata).delete()

            # --------------course_assignment_content
            org_course_assignment = OrganizationMoreText()
            for tmp1 in OrganizationMoreText.objects.filter(organization=org_metadata, itemType="Course Assignment"):
                org_course_assignment = tmp1
                break

            org_course_assignment.DataItem = course_assignment_content
            org_course_assignment.organization = org_metadata
            org_course_assignment.itemType = "Course Assignment"
            org_course_assignment.save()

            # --------------OrganizationCmsitem
            if (cms_items):
                cms_items_list = cms_items.split("=<=")

                # Delete the deleted records
                for item_c in OrganizationCmsitem.objects.filter(organization=org_metadata):
                    if item_c.rowNum > len(cms_items_list):
                        item_c.delete()

                # Add all
                manage_user_content = ""
                for tmp1 in cms_items_list:
                    tmp2 = tmp1.split("=>=")
                    org_menu_item = OrganizationCmsitem()

                    for org_menu_item1 in OrganizationCmsitem.objects.filter(organization=org_metadata, rowNum=int(tmp2[0])):
                        org_menu_item = org_menu_item1
                        break

                    org_menu_item.organization = org_metadata
                    org_menu_item.rowNum = tmp2[0]
                    org_menu_item.CmsItem = tmp2[1]
                    org_menu_item.Url = tmp2[2]
                    org_menu_item.Grade = tmp2[3]
                    org_menu_item.Icon = tmp2[4]
                    org_menu_item.save()

                    if manage_user_content != "":
                        manage_user_content += ", "
                    manage_user_content += "{'rowNum':'" + tmp2[0] + "', 'content':'" + tmp2[5] + "'}"

                # --------------manage_user_content
                org_cmu = OrganizationMoreText()
                for tmp1 in OrganizationMoreText.objects.filter(organization=org_metadata, itemType="Cms Manage User"):
                    org_cmu = tmp1
                    break

                org_cmu.DataItem = "[" + manage_user_content + "]"
                org_cmu.organization = org_metadata
                org_cmu.itemType = "Cms Manage User"
                org_cmu.save()
            else:
                OrganizationCmsitem.objects.filter(organization=org_metadata).delete()

            org_organizationmenusave(org_metadata, "Menu Color", menu_color)
            org_organizationmenusave(org_metadata, "Is Icon", is_icon)
            org_organizationmenusave(org_metadata, "Is Icon With Text", is_icon_width_text)
            org_organizationmenusave(org_metadata, "Text Color", menu_text_color)
            org_organizationmenusave(org_metadata, "Text Font", menu_text_font)
            org_organizationmenusave(org_metadata, "Text Size", menu_text_size)
            org_organizationmenusave(org_metadata, "Text Color Icons", menu_text_color_icons)
            org_organizationmenusave(org_metadata, "Text Font Icons", menu_text_font_icons)
            org_organizationmenusave(org_metadata, "Text Size Icons", menu_text_size_icons)
            org_organizationmenusave(org_metadata, "Text Color Me", menu_text_color_me)
            org_organizationmenusave(org_metadata, "Text Font Me", menu_text_font_me)
            org_organizationmenusave(org_metadata, "Text Size Me", menu_text_size_me)
            org_organizationmenusave(org_metadata, "Space Betwwen Items", space_between_items)
            org_organizationmenusave(org_metadata, "Is New Menu", is_new_menu)
            org_organizationmenusave(org_metadata, "Organization Logo Url", org_logo_url)
            org_organizationmenusave(org_metadata, "Logo Url", logo_url)
            org_organizationmenusave(org_metadata, "Remove All Menu", remove_all_menu)
            org_organizationmenusave(org_metadata, "Footer Selected", footer_flag)
            org_organizationmenusave(org_metadata, "Initial Pepper Announcement", is_announcement)

            org_organizationdashboardsave(org_metadata, "Dashboard option etc", dashboard_option)
            org_organizationdashboardsave(org_metadata, "Profile Logo Url", org_profile_logo_url)
            org_organizationdashboardsave(org_metadata, "Profile Logo Url Curriculumn", org_profile_logo_curr_url)
            org_organizationdashboardsave(org_metadata, "My Feed Show", my_feed_show)
            org_organizationdashboardsave(org_metadata, "My Activities Show", my_activities_show)
            org_organizationdashboardsave(org_metadata, "My Report Show", my_report_show)
            org_organizationdashboardsave(org_metadata, "My Featured Show", my_featured_show)
            org_organizationdashboardsave(org_metadata, "Is My Feed Default", is_my_feed_default)
            org_organizationdashboardsave(org_metadata, "My Feed Show Curriculumn ", my_feed_show_curr)
            org_organizationdashboardsave(org_metadata, "My Activities Show Curriculumn", my_activities_show_curr)
            org_organizationdashboardsave(org_metadata, "My Report Show Curriculumn", my_report_show_curr)
            org_organizationdashboardsave(org_metadata, "My Featured Show Curriculumn", my_featured_show_curr)
            org_organizationdashboardsave(org_metadata, "Is My Feed Default Curriculumn", is_my_feed_default_curr)
            org_organizationdashboardsave(org_metadata, "Show Left DB", new_show_left)
            org_organizationdashboardsave(org_metadata, "Show Right DB", new_show_right)
            org_organizationdashboardsave(org_metadata, "Show Left DB Curriculumn", new_show_left_curr)
            org_organizationdashboardsave(org_metadata, "Show Right DB Curriculumn", new_show_right_curr)
            org_organizationdashboardsave(org_metadata, "Feed Title", feed_txt)
            org_organizationdashboardsave(org_metadata, "Activities Title", activities_txt)
            org_organizationdashboardsave(org_metadata, "Progress Title", progress_txt)
            org_organizationdashboardsave(org_metadata, "Resources Title", resources_txt)
            org_organizationdashboardsave(org_metadata, "Feed Title Curriculumn", feed_txt_curr)
            org_organizationdashboardsave(org_metadata, "Activities Title Curriculumn", activities_txt_curr)
            org_organizationdashboardsave(org_metadata, "Progress Title Curriculumn", progress_txt_curr)
            org_organizationdashboardsave(org_metadata, "Resources Title Curriculumn", resources_txt_curr)

        data = {'Success': True, 'back_sid_all': back_sid_all}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_organizationmenusave
def org_organizationmenusave(organization, itemtype, itemvalue):
    org_menu_tmp = OrganizationMenu()
    for tmp1 in OrganizationMenu.objects.filter(organization=organization, itemType=itemtype):
        org_menu_tmp = tmp1
        break

    org_menu_tmp.organization = organization
    org_menu_tmp.itemType = itemtype
    org_menu_tmp.itemValue = itemvalue
    org_menu_tmp.save()


# -------------------------------------------------------------------org_organizationdashboardsave
def org_organizationdashboardsave(organization, itemtype, itemvalue):
    org_menu_tmp = OrganizationDashboard()
    for tmp1 in OrganizationDashboard.objects.filter(organization=organization, itemType=itemtype):
        org_menu_tmp = tmp1
        break

    org_menu_tmp.organization = organization
    org_menu_tmp.itemType = itemtype
    org_menu_tmp.itemValue = itemvalue
    org_menu_tmp.save()


# -------------------------------------------------------------------organizational_save_base
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

            elif file_type == "profile_logo_curr":
                imgx = request.FILES.get("organizational_base_profile_logo_curr", None)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/'
            if not os.path.exists(path):
                os.mkdir(path)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + '/'
            if not os.path.exists(path):
                os.mkdir(path)

            if imgx:
                ext = os.path.splitext(imgx.name)[1]
                destination = open(path + file_type + ext, 'wb+')
                for chunk in imgx.chunks():
                    destination.write(chunk)
                destination.close()

                org_menu = OrganizationMenu()
                org_dashboard = OrganizationDashboard()

                if file_type == "home_logo":
                    for tmp1 in OrganizationMenu.objects.filter(organization=organization, itemType="logo"):
                        org_menu = tmp1
                        break

                    org_menu.organization = organization
                    org_menu.itemType = "logo"
                    org_menu.itemValue = file_type + ext
                    org_menu.save()

                elif file_type == "organization_logo":
                    for tmp1 in OrganizationMenu.objects.filter(organization=organization, itemType="organization_logo"):
                        org_menu = tmp1
                        break

                    org_menu.organization = organization
                    org_menu.itemType = "organization_logo"
                    org_menu.itemValue = file_type + ext
                    org_menu.save()

                elif file_type == "profile_logo":
                    for tmp1 in OrganizationDashboard.objects.filter(organization=organization, itemType="Profile Logo"):
                        org_dashboard = tmp1
                        break

                    org_dashboard.organization = organization
                    org_dashboard.itemType = "Profile Logo"
                    org_dashboard.itemValue = file_type + ext
                    org_dashboard.save()

                elif file_type == "profile_logo_curr":
                    for tmp1 in OrganizationDashboard.objects.filter(organization=organization, itemType="Profile Logo Curriculumn"):
                        org_dashboard = tmp1
                        break

                    org_dashboard.organization = organization
                    org_dashboard.itemType = "Profile Logo Curriculumn"
                    org_dashboard.itemValue = file_type + ext
                    org_dashboard.save()

                data = {'Success': True, 'name': file_type + ext}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_main_page_configuration_get
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
            break

        data['flag_new'] = flag_new
        data['Success'] = True

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organizational_save_main_base
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
            break

        org_main.SiteURL = site_url
        org_main.MainLogoText = logo_text
        org_main.MainPageButtonText = button_text
        org_main.MainPageButtonLink = button_link
        org_main.save()
        data = {'Success': True}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_main_upload
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

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/'
            if not os.path.exists(path):
                os.mkdir(path)

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
                    break

                data = {'Success': True, 'name': file_type + ext}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_dashboard_upload
@login_required
def org_dashboard_upload(request):
    try:
        data = {'Success': False}

        rownum = request.POST.get("rowNum", "")
        oid = request.POST.get("oid", "")
        fileelementid = request.POST.get("fileelementid", "")

        if(rownum and oid):
            rownum = str(rownum)
            organization = OrganizationMetadata.objects.get(id=oid)
            imgx = request.FILES.get("menu_items_icon_" + rownum, None)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/'
            if not os.path.exists(path):
                os.mkdir(path)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/' + oid + '/'

            if not os.path.exists(path):
                os.mkdir(path)

            if imgx:
                destination = open(path + imgx.name, 'wb+')
                for chunk in imgx.chunks():
                    destination.write(chunk)
                destination.close()

                for org_menu_item in OrganizationMenuitem.objects.filter(organization=organization, rowNum=int(rownum), ParentID=0):
                    org_menu_item.Icon = imgx.name
                    org_menu_item.save()
                    break

                data = {'Success': True, 'name': imgx.name}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_dashboard_upload_cms
@login_required
def org_dashboard_upload_cms(request):
    try:
        data = {'Success': False}

        rownum = request.POST.get("rowNum", "")
        oid = request.POST.get("oid", "")
        fileelementid = request.POST.get("fileelementid", "")

        if(rownum and oid):
            rownum = str(rownum)
            organization = OrganizationMetadata.objects.get(id=oid)
            imgx = request.FILES.get("cms_items_icon_" + rownum, None)

            path = settings.PROJECT_ROOT.dirname().dirname() + '/uploads/organization/'
            if not os.path.exists(path):
                os.mkdir(path)

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

                for org_menu_item in OrganizationCmsitem.objects.filter(organization=organization, rowNum=int(rownum)):
                    org_menu_item.Icon = imgx.name
                    org_menu_item.save()
                    break

                data = {'Success': True, 'name': imgx.name}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------org_option_cvs_upload
@login_required
def org_option_cvs_upload(request):
    try:
        data = {'Success': False}
        import_file = request.FILES.get('organizational_option_cvs')
        r = csv.reader(import_file, dialect=csv.excel)
        rows = []
        rows.extend(r)
        data = {'Success': True, 'rows': rows}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_get_info
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
            break

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
                        break

                if (not(data['OrganizationOK']) and district):
                    for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=district, EntityType="District"):
                        data['OrganizationOK'] = True
                        organization_obj = tmp1.organization
                        break

                if(not(data['OrganizationOK']) and state):
                    for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=state, EntityType="State"):
                        data['OrganizationOK'] = True
                        organization_obj = tmp1.organization
                        break

                if(data['OrganizationOK']):
                    data['DistrictType'] = organization_obj.DistrictType
                    data['SchoolType'] = organization_obj.SchoolType
                    data['OrganizationName'] = organization_obj.OrganizationName

                    for tmp2 in OrganizationDataitems.objects.filter(organization=organization_obj):
                        data['org_rg_data_items'] = tmp2.DataItem

                data['Success'] = True

            elif(source == "navigation"):
                if request.user.is_authenticated():
                    try:
                        state = request.user.profile.district.state.id
                    except:
                        state = -1
                    try:
                        district = request.user.profile.district.id
                    except:
                        district = -1
                    try:
                        school = request.user.profile.school.id
                    except:
                        school = -1

                    data['OrganizationOK'] = False

                    if (school != -1):
                        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=school,
                                                                         EntityType="School"):
                            data['OrganizationOK'] = True
                            organization_obj = tmp1.organization
                            break

                    if (not (data['OrganizationOK']) and district != -1):
                        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=district,
                                                                         EntityType="District"):
                            data['OrganizationOK'] = True
                            organization_obj = tmp1.organization
                            break

                    if (not (data['OrganizationOK']) and state != -1):
                        for tmp1 in OrganizationDistricts.objects.filter(OrganizationEnity=state, EntityType="State"):
                            data['OrganizationOK'] = True
                            organization_obj = tmp1.organization
                            break

                    if (data['OrganizationOK']):
                        data['OrganizationName'] = organization_obj.OrganizationName
                        data['OrganizationId'] = organization_obj.id
                        data['DistrictType'] = organization_obj.DistrictType
                        data['SchoolType'] = organization_obj.SchoolType

                        for tmp2 in OrganizationMenu.objects.filter(organization=organization_obj, itemType="Remove All Menu"):
                            data[tmp2.itemType] = tmp2.itemValue

                        for tmp2 in OrganizationMenu.objects.filter(organization=organization_obj, itemType="Footer Selected"):
                            data[tmp2.itemType] = tmp2.itemValue
                            if tmp2.itemValue == "1":
                                for tmp3 in OrganizationFooter.objects.filter(organization=organization_obj):
                                    data['footer_content'] = tmp3.DataItem

                        if (flag_main == "dashboard"):
                            for tmp2 in OrganizationDashboard.objects.filter(organization=organization_obj):
                                data[tmp2.itemType] = tmp2.itemValue

                    data['Success'] = True

    except Exception as e:
        data = {'SiteURL_OK': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------organization_course_list
@login_required
def organization_course_list(request):
    subject_id = request.POST.get('subject_id', 'all')
    grade_id = request.POST.get('grade_id', 'all')
    author_id = request.POST.get('author_id', 'all')
    district = request.POST.get('district', '')
    state = request.POST.get('state', '')
    collection = request.POST.get('collection', '')
    credit = request.POST.get('credit', '')
    is_new = request.POST.get('is_new', '')
    district_id = request.POST.get('district', '')
    state_id = request.POST.get('state', '')
    all_courses = get_courses(request.user, request.META.get('HTTP_HOST'))
    is_member = {'state': False, 'district': False}

    filter_dic = {'_id.category': 'course'}
    if subject_id != 'all':
        filter_dic['metadata.display_subject'] = subject_id

    if grade_id != 'all':
        if grade_id == '6-8' or grade_id == '9-12':
            filter_dic['metadata.display_grades'] = {'$in': [grade_id, '6-12']}
        else:
            filter_dic['metadata.display_grades'] = grade_id

    if author_id != 'all':
        filter_dic['metadata.display_organization'] = author_id

    if district_id != '' and district_id != '__NONE__':
        if district in all_district:
            is_member['district'] = True
            filter_dic['metadata.display_district'] = {'$in': [district, 'All']}
        else:
            filter_dic['metadata.display_district'] = district
    elif state_id != '' and state_id != '__NONE__':
        if state in all_state:
            is_member['state'] = True
            filter_dic['metadata.display_state'] = {'$in': [state, 'All']}
        else:
            filter_dic['metadata.display_state'] = state

    if collection != '':
        filter_dic['metadata.content_collections'] = {'$in': [collection, 'All']}

    if credit != '':
        filter_dic['metadata.display_credit'] = True

    items = modulestore().collection.find(filter_dic).sort("metadata.display_subject.0", pymongo.ASCENDING)
    courses = modulestore()._load_items(list(items), 0)

    subject_index = [-1, -1, -1, -1, -1]
    curr_subject = ["", "", "", "", ""]
    g_courses = [[], [], [], [], []]
    # end

    more_subjects_courses = [[], [], [], [], []]

    for course in courses:
        if is_new == '' or course.is_newish:
            course_filter(course, subject_index, curr_subject, g_courses, grade_id, more_subjects_courses)

    if subject_id == 'all':
        for i in range(0, len(more_subjects_courses)):
            if len(more_subjects_courses[i]) > 0:
                g_courses[i].append(more_subjects_courses[i])
    else:
        for i in range(0, len(more_subjects_courses)):
            if len(more_subjects_courses[i]) > 0:
                if len(g_courses[i]) > 0:
                    for n in range(0, len(more_subjects_courses[i])):
                        g_courses[i][0].append(more_subjects_courses[i][n])

    for gc in g_courses:
        for sc in gc:
            sc.sort(key=lambda x: x.display_coursenumber)

    rows_course = []
    for course in g_courses[4]:
        for c in course:
            if not c.close_course or c.close_course and c.keep_in_directory:
                rows_course.append({'id': c.id, 'title': get_course_about_section(c, 'title'), 'course_number': c.display_number_with_default})
    for course in g_courses[0]:
        for c in course:
            if not c.close_course or c.close_course and c.keep_in_directory:
                rows_course.append({'id': c.id, 'title': get_course_about_section(c, 'title'), 'course_number': c.display_number_with_default})
    for course in g_courses[1]:
        for c in course:
            if not c.close_course or c.close_course and c.keep_in_directory:
                rows_course.append({'id': c.id, 'title': get_course_about_section(c, 'title'), 'course_number': c.display_number_with_default})
    for course in g_courses[2]:
        for c in course:
            if not c.close_course or c.close_course and c.keep_in_directory:
                rows_course.append({'id': c.id, 'title': get_course_about_section(c, 'title'), 'course_number': c.display_number_with_default})
    for course in g_courses[3]:
        for c in course:
            if not c.close_course or c.close_course and c.keep_in_directory:
                rows_course.append({'id': c.id, 'title': get_course_about_section(c, 'title'), 'course_number': c.display_number_with_default})

    data = {'Success': True, "courses": rows_course, "subject_id": subject_id}

    return HttpResponse(json.dumps(data), content_type="application/json")


# -------------------------------------------------------------------course_filter
def course_filter(course, subject_index, currSubject, g_courses, currGrades, more_subjects_courses):
    if not course.close_course or course.close_course and course.keep_in_directory:
        if course.display_grades == 'K-5':
            if len(course.display_subject) > 1:
                more_subjects_courses[0].append(course)
            else:
                if course.display_subject != currSubject[0]:
                    currSubject[0] = course.display_subject
                    subject_index[0] += 1
                    g_courses[0].append([])
                g_courses[0][subject_index[0]].append(course)
        if (course.display_grades == '6-8' or course.display_grades == '6-12') and currGrades != '9-12':
            if len(course.display_subject) > 1:
                more_subjects_courses[1].append(course)
            else:
                if course.display_subject != currSubject[1]:
                    currSubject[1] = course.display_subject
                    subject_index[1] += 1
                    g_courses[1].append([])
                g_courses[1][subject_index[1]].append(course)
        if (course.display_grades == '9-12' or course.display_grades == '6-12') and currGrades != '6-8':
            if len(course.display_subject) > 1:
                more_subjects_courses[2].append(course)
            else:
                if course.display_subject != currSubject[2]:
                    currSubject[2] = course.display_subject
                    subject_index[2] += 1
                    g_courses[2].append([])
                g_courses[2][subject_index[2]].append(course)
        if course.display_grades == 'K-12':
            if len(course.display_subject) > 1:
                more_subjects_courses[3].append(course)
            else:
                if course.display_subject != currSubject[3]:
                    currSubject[3] = course.display_subject
                    subject_index[3] += 1
                    g_courses[3].append([])
                g_courses[3][subject_index[3]].append(course)
        # end

        # 20160322 add "Add new grade 'PreK-3'"
        # begin
        if course.display_grades == 'PreK-3':
            if len(course.display_subject) > 1:
                more_subjects_courses[4].append(course)
            else:
                if course.display_subject != currSubject[4]:
                    currSubject[4] = course.display_subject
                    subject_index[4] += 1
                    g_courses[4].append([])
                g_courses[4][subject_index[4]].append(course)
