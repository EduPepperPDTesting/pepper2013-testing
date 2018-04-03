@@ -1,174 +0,0 @@
# sudo apt-get install libsasl2-dev libssl-dev libldap2-dev
# pip install python-ldap
import logging

import ldap
from django import db
from django.db import transaction
from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django_future.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.translation import ugettext as _


from mitxmako.shortcuts import render_to_response
from pepper_utilities.utils import render_json_response, random_mark
from student.models import Registration, UserProfile

log = logging.getLogger("mitx.student")
AUDIT_LOG = logging.getLogger("audit")


def ldap_exists(ldap_name):
    exists = True
    return exists


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


@ensure_csrf_cookie
def ldap_signin(request):
    """Assertion consume service (acs) of pepper"""
    ldap_process = LDAPSignIn(request)
    return ldap_process.auth()


class LDAPSignIn:
    request = {}
    ldap_settings = {}
    email = ''

    def __init__(self, request):
        self.request = request

    def auth(self):
        """AJAX request to log in the user via LDAP."""
        if 'email' not in self.request.POST or 'password' not in self.request.POST:
            response = {
                'success': False,
                'value': _('There was an error receiving your login information. Please email us if this issue continues.')
            }
            return render_json_response(response)

        self.ldap_settings = self.load_ldap_settings(self.request.REQUEST.get('name'))
        ldap_server = self.ldap_settings['server']
        self.email = self.request.REQUEST.get('email')
        password = self.request.REQUEST.get('password')
        # the following is the user_dn format provided by the ldap server
        user_dn = self.ldap_settings['user_dn'].format({'email': self.email})
        # adjust this to your base dn for searching
        base_dn = self.ldap_settings['base_dn']
        connect = ldap.open(ldap_server)
        search_filter = self.ldap_settings['search_filter'].format({'email': self.email})
        try:
            # if authentication successful, get the full user data
            connect.bind_s(user_dn, password)
            result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
            connect.unbind_s()
        except ldap.LDAPError as e:
            connect.unbind_s()
            # log the error, etc.
            log.error('There was an error authenticating user {0}: {1}'.format(self.email, e))
            response = {
                'success': False,
                'value': _("There was an error logging in to your system. Please email us if this issue continues.")
            }
            return render_json_response(response)
        else:
            # check to see if the user exists locally
            try:
                user = User.objects.get(email=self.email)
            except User.DoesNotExist:
                AUDIT_LOG.warning(u"Unknown user email: {0}. Creating new user.".format(self.email))

            else:
                pass

    def create_unknown_user(self):
        """Create the sso user who does not exist in pepper"""
        try:
            # Generate username
            username = random_mark(20)

            user = User(username=username, email=self.email, is_active=False)
            user.set_password(username)  # Set password the same with username
            user.save()

            registration = Registration()
            registration.register(user)

            user.profile = UserProfile(user=user)
            user.profile.subscription_status = "Imported"

            self.update_user()

            return redirect(reverse('register_sso_user', args=[registration.activation_key]))

        except Exception as e:
            db.transaction.rollback()
            log.error("Failed to create SSO user: {0}".format(e))
            raise e

    def update_user(self):
        # Save mapped attributes
        for k, v in self.parsed_data.items():
            if k == 'first_name':
                self.user.first_name = self.parsed_data['first_name']
            elif k == 'last_name':
                self.user.last_name = self.parsed_data['last_name']
            elif k == 'email':
                self.user.email = self.parsed_data['email']
            elif k == 'district':
                self.user.profile.district = District.objects.get(name=self.parsed_data['district'])
            elif k == 'school':
                self.user.profile.school = School.objects.get(name=self.parsed_data['school'])
            elif k == 'grade_level':
                ids = GradeLevel.objects.filter(name__in=self.parsed_data['grade_level'].split(',')).values_list(
                    'id', flat=True)
                self.user.profile.grade_level = ','.join(ids)
            elif k == 'major_subject_area':
                ids = SubjectArea.objects.filter(name__in=self.parsed_data['major_subject_area'].split(',')).values_list(
                    'id', flat=True)
                self.user.profile.major_subject_area = ','.join(ids)
            elif k == 'years_in_education':
                self.user.profile.years_in_education = YearsInEducation.objects.get(
                    name=self.parsed_data['years_in_education'])
            elif k == 'percent_lunch':
                self.user.profile.percent_lunch = Enum.objects.get(name='percent_lunch',
                                                                   content=self.parsed_data['percent_lunch'])
            elif k == 'percent_iep':
                self.user.profile.percent_iep = Enum.objects.get(name='percent_iep',
                                                                 content=self.parsed_data['percent_iep'])
            elif k == 'percent_eng_learner':
                self.user.profile.percent_eng_learner = Enum.objects.get(
                    name='percent_eng_learner', content=self.parsed_data['percent_eng_learner'])

            self.user.profile.sso_type = self.sso_type
            self.user.profile.sso_idp = self.idp_name
            self.user.profile.sso_user_id = self.parsed_data.get('idp_user_id')

            self.user.save()
            self.user.profile.save()

    def load_ldap_settings(self):
        settings = {}
        return settings
