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

@login_required
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

        elif (post_flag == "organization_check_Entity"):
            return org_check_Entity(request);

        elif (post_flag == "organization_remove_img"):
            return organization_remove_img(request);

    else:
        tmp = "organization/organization.html";
        return render_to_response(tmp)

#-------------------------------------------------------------------organization_list
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
def organization_add(request):
    name = request.POST.get('organizational_name', False)
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

            data = {'Success': True}
        except Exception as e:
            data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_add
def organization_delete(request):
    try:
        for oid in request.POST.get("ids", "").split(","):
            org = OrganizationMetadata.objects.filter(id=oid)

            OrganizationDataitems.objects.filter(organization=org).delete()
            OrganizationDistricts.objects.filter(organization=org).delete()
            OrganizationAttributes.objects.filter(organization=org).delete()

            org.delete()

        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------org_check_Entity
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
                    for tmp1 in OrganizationMetadata.objects.filter(id=oid):
                        for tmp2 in OrganizationAttributes.objects.filter(organization=tmp1):
                            if (column == "LogoHome"):
                                filename = tmp2.LogoHome
                                tmp2.LogoHome = ""
                            else:
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

                    break;
            else:
                data['find'] = False
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organizational_save_base
def organizational_save_base(request):
    try:
        oid = request.POST.get("oid", "")
        for_district = request.POST.get("for_district", "")
        for_school = request.POST.get("for_school", "")
        specific_items = request.POST.get("specific_items", "")
        sid_did = request.POST.get("sid_did", "")
        motto = request.POST.get("motto", "")

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
            if(specific_items):
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
            if (motto):
                org_attr = OrganizationAttributes();
                org_attr_list = OrganizationAttributes.objects.filter(organization=org_metadata)
                for tmp1 in org_attr_list:
                    org_attr = tmp1
                    break;

                org_attr.Motto = motto
                org_attr.organization = org_metadata

                org_attr.save();

        data = {'Success': True}
    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organizational_save_base
def org_upload(request):
    try:
        data = {'Success': False}

        file_type = request.POST.get("file_type", "")
        oid = request.POST.get("oid", "")

        if(file_type and oid):
            organization = OrganizationMetadata.objects.get(id=oid)

            if file_type == "home_logo":
                imgx = request.FILES.get("organizational_base_home_logo", None)

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
                if file_type == "home_logo":
                    org_attr.LogoHome = file_type + ext

                elif file_type == "profile_logo":
                    org_attr.LogoProfile = file_type + ext

                elif file_type == "top_main_logo":
                    org_attr.TopMainLogo = file_type + ext

                elif file_type == "bottom_main_logo":
                    org_attr.BottomMainLogo = file_type + ext

                elif file_type == "main_page_bottom_image":
                    org_attr.MainPageBottomImage = file_type + ext

                org_attr.save()

                data = {'Success': True, 'name': file_type + ext}

    except Exception as e:
        data = {'Success': False, 'Error': '{0}'.format(e)}

    return HttpResponse(json.dumps(data), content_type="application/json")

#-------------------------------------------------------------------organization_main_page_configuration_get
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