from django.conf import settings
from BeautifulSoup import BeautifulSoup
from mitxmako.shortcuts import render_to_string
from organization.models import OrganizationDistricts, OrganizationMenu, OrganizationFooter
from pepper_utilities.utils import render_jsonp_response
from staticfiles.storage import staticfiles_storage
from pipeline_mako import compressed_css


def check_org(user):
    """
    Gets information about the org that a user might belong to.

    :param user: django user object
    :return:
        org_enabled: Whether this user has a customized org.
        org_object: The org data from the DB.
        org_menu: all of the org metadata.
    """
    org_enabled = False
    org_menu = {}
    org_object = {}

    # Don't even bother with this if the user isn't logged in.
    if user.is_authenticated():
        # Get any state, district and school data associated with the user.
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

        # Look up the org data for each of those.
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

        # If there is an org customization associated with the user's orgs, parse all of the data.
        if org_enabled:
            org_menu["org_id"] = org_object.id
            for om in OrganizationMenu.objects.filter(organization=org_object):
                org_menu[om.itemType] = om.itemValue

    return org_enabled, org_object, org_menu


def html_parse(html):
    """
    Parses the HTML to clean off script and style tags

    :param html: The HTML string to clean
    :return: The cleaned HTML
    """
    soup = BeautifulSoup(html)  # create a new bs4 object from the html data loaded
    for script in soup(["script", "style", "link"]):  # remove all javascript and stylesheet code
        script.extract()

    return soup.prettify()


def get_css(request, group):
    """
    Gets the CSS files based on whether this is a local dev version or a regular server.

    :param request: The django request object.
    :param group: The group to get the CSS for (as defined in PIPELINE_CSS).
    :return: The list of CSS files.
    """
    css = []
    if settings.MITX_FEATURES['USE_DJANGO_PIPELINE']:
        compressed_css(group)
    else:
        for filename in settings.PIPELINE_CSS[group]['source_filenames']:
            css.append(request.build_absolute_uri(staticfiles_storage.url(filename.replace('.scss', '.css'))))

    return css


def header_return(request):
    """
    View that returns the header for the current user.

    :param request: The django request object.
    :return: Rendered JSON.
    """

    callback = request.GET.get('callback')

    # Get some information on whether the user belongs to an org with customizations.
    org_enabled, org_object, org_menu = check_org(request.user)

    # This JS is used on both templates.
    js = []
    # This CSS id used in both templates.
    css = get_css(request, 'header')

    # If there is a customized org, render the new-style header.
    if org_enabled and org_menu["Is New Menu"] == "1":
        # Get the parsed HTML.
        html = html_parse(render_to_string("navigation_new.html", {
            "show_extended": True,
            "organization_obj": org_object,
            "org_data": org_menu,
            "is_external": True
        }))
        # Add the template-specific JS.
        js.append(request.build_absolute_uri('/static/js/navigation_new.js'))
    # Otherwise use the regular template.
    else:
        # Get the parsed HTML.
        html = html_parse(render_to_string("navigation.html", {
            "show_extended": True,
            "is_external": True
        }))
        # Add the template-specific JS
        js.append(request.build_absolute_uri('/static/js/navigation.js'))

    data = {'html': html, 'css': css, 'js': js}
    return render_jsonp_response(callback, data)


def footer_return(request):
    """
    View that returns the footer for the current user.

    :param request: The django request object.
    :return: Rendered JSON.
    """
    callback = request.GET.get('callback')

    # Get some information on whether the user belongs to an org with customizations.
    org_enabled, org_object, org_menu = check_org(request.user)

    # Default to the normal footer.
    html = render_to_string('footer.html', {'alt_footer': False, 'is_external': True})

    # If there is a customized org, get the footer layout from the DB.
    if org_enabled:
        # If the footer is customized, get the footer layout and use that instead.
        footer_selected = OrganizationMenu.objects.get(organization=org_object, itemType="Footer Selected")
        if footer_selected and footer_selected.itemValue == "1":
            footer = OrganizationFooter.objects.get(organization=org_object)
            if footer:
                html = footer.DataItem

    data = {'html': html, 'css': get_css(request, 'footer'), 'js': []}
    return render_jsonp_response(callback, data)
