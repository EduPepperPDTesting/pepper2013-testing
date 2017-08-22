from mitxmako.shortcuts import render_to_string
from organization.models import OrganizationMetadata, OrganizationDistricts, OrganizationMenu, OrganizationFooter
from pepper_utilities.utils import render_json_response
from lxml.html.clean import Cleaner


def check_org(user):
    org_enabled = False
    org_menu = {}
    org_object = {}
    if user.is_authenticated():
        try:
            state_id = user.profile.district.state.id
        except:
            state_id = -1
        try:
            district_id = user.profile.district.id
        except:
            district_id = -1
        try:
            school_id = user.profile.school.id
        except:
            school_id = -1

        if school_id != -1:
            org = OrganizationDistricts.objects.get(OrganizationEnity=school_id, EntityType="School")
            if org:
                org_object = org.organization
                org_enabled = True

        if (not org_enabled) and district_id != -1:
            org = OrganizationDistricts.objects.get(OrganizationEnity=district_id, EntityType="District")
            if org:
                org_object = org.organization
                org_enabled = True

        if (not org_enabled) and state_id != -1:
            org = OrganizationDistricts.objects.get(OrganizationEnity=state_id, EntityType="State")
            if org:
                org_object = org.organization
                org_enabled = True

        if org_enabled:
            org_menu["org_id"] = org_object.id
            for om in OrganizationMenu.objects.filter(organization=org_object):
                org_menu[om.itemType] = om.itemValue

    return org_enabled, org_object, org_menu


def header_return(request):
    org_enabled, org_object, org_menu = check_org(request.user)
    if org_enabled and org_menu["Is New Menu"] == "1":
        html = render_to_string("navigation_new.html", {})
    else:
        html = render_to_string("navigation.html", {})
    # <link rel="stylesheet" href="/static/css/admin_ui_controls.css" type="text/css" media="screen" />
    # <script type="text/javascript" src="/static/js/admin_ui_controls.js"></script>
    return render_json_response({'html': html, 'css': [], 'js': []})


def footer_return(request):
    org_enabled, org_object, org_menu = check_org(request.user)

    html = render_to_string('footer.html', {})
    if org_enabled:
        footer_selected = OrganizationMenu.objects.get(organization=org_object, itemType="Footer Selected")
        if footer_selected and footer_selected.itemValue == "1":
            footer = OrganizationFooter.objects.filter(organization=org_object)
            if footer:
                html = footer.DataItem

    return render_json_response({'html': html, 'css': [], 'js': []})
