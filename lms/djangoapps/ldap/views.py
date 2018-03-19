# sudo apt-get install libsasl2-dev libssl-dev libldap2-dev
# pip install python-ldap
import ldap


def load_ldap_settings(config):
    settings = {}
    return settings


def ldap_auth(request):
    ldap_settings = load_ldap_settings(request.REQUEST.get('config'))
    ldap_server = ldap_settings['server']
    username = request.REQUEST.get('user')
    password = request.REQUEST.get('password')
    # the following is the user_dn format provided by the ldap server
    user_dn = ldap_settings['user_dn'].format({'username': username})
    # adjust this to your base dn for searching
    base_dn = ldap_settings['base_dn']
    connect = ldap.open(ldap_server)
    search_filter = ldap_settings['search_filter'].format({'username': username})
    try:
        # if authentication successful, get the full user data
        connect.bind_s(user_dn, password)
        result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        # return all user data results
        connect.unbind_s()
    except ldap.LDAPError as e:
        connect.unbind_s()
        # log the error, etc.
    else:
        # Do sso stuff
        pass
