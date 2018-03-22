# sudo apt-get install libsasl2-dev libssl-dev libldap2-dev
# pip install python-ldap
import logging

import ldap
from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django_future.csrf import ensure_csrf_cookie
from django.utils.translation import ugettext as _


from mitxmako.shortcuts import render_to_response
from pepper_utilities.utils import render_json_response

log = logging.getLogger("mitx.student")
AUDIT_LOG = logging.getLogger("audit")


def load_ldap_settings(config):
    settings = {}
    return settings


def ldap_exists(ldap_name):
    exists = True
    return exists


def ldap_auth(request):
    """AJAX request to log in the user via LDAP."""
    if 'email' not in request.POST or 'password' not in request.POST:
        return render_json_response({'success': False,
                                     'value': _('There was an error receiving your login information. Please email us.')})

    ldap_settings = load_ldap_settings(request.REQUEST.get('name'))
    ldap_server = ldap_settings['server']
    email = request.REQUEST.get('email')
    password = request.REQUEST.get('password')
    # the following is the user_dn format provided by the ldap server
    user_dn = ldap_settings['user_dn'].format({'email': email})
    # adjust this to your base dn for searching
    base_dn = ldap_settings['base_dn']
    connect = ldap.open(ldap_server)
    search_filter = ldap_settings['search_filter'].format({'email': email})
    try:
        # if authentication successful, get the full user data
        connect.bind_s(user_dn, password)
        result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        # check to see if the user exists locally
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            AUDIT_LOG.warning(u"Login failed - Unknown user email: {0}".format(email))
            user = None
        else:
            pass
        connect.unbind_s()
    except ldap.LDAPError as e:
        connect.unbind_s()
        # log the error, etc.
    else:
        # Do sso stuff
        pass


@ensure_csrf_cookie
def ldap_login(request):
    """
    This view will display the non-modal LDAP-based login form
    """
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))

    ldap_name = request.GET.get('name', '')

    if not ldap_exists(ldap_name):
        error_context = {'window_title': 'Missing Configuration',
                         'error_title': 'Missing Configuration',
                         'error_message': 'This LDAP configuration does not exist. Please check the URL.'}
        return render_to_response('error.html', error_context)

    return render_to_response('ldap_login.html', {})
