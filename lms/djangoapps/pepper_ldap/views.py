# sudo apt-get install libsasl2-dev libssl-dev libldap2-dev
# pip install python-ldap
import logging

import ldap
import re

from django import db
from django.db import transaction
from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django_future.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.translation import ugettext as _
from django.forms.models import model_to_dict

from mitxmako.shortcuts import render_to_response
from pepper_utilities.utils import render_json_response, random_mark, get_request_array
from permissions.decorators import user_has_perms
from student.models import Registration, UserProfile
from .models import LDAPSettings, LDAPMappings

log = logging.getLogger("mitx.student")
AUDIT_LOG = logging.getLogger("audit")


def ldap_exists(ldap_name):
    exists = True
    try:
        settings = LDAPSettings.objects.get(name=ldap_name)
    except:
        exists = False
    return exists


def load_ldap_settings(ldap_id):
    settings_instance = LDAPSettings.objects.get(id=ldap_id)
    settings = model_to_dict(settings_instance)
    mappings = list(LDAPMappings.objects.filter(settings=settings_instance).values())
    settings['mappings'] = mappings
    return settings


def check_input(ldap_settings):
    status = True
    message = ''
    if not ldap_settings.name:
        status = False
        message = 'You must include the name.'

    if re.match(' ', ldap_settings.name):
        status = False
        message = "There can't be any spaces in the name."

    if not re.match('\{email\}', ldap_settings.user_dn):
        status = False
        message = 'You must include {email} where it should be inserted in the User DN.'

    if not re.match('\{email\}', ldap_settings.search_filter):
        status = False
        message = 'You must include {email} where it should be inserted in the Search Filter.'

    if not ldap_settings.server:
        status = False
        message = 'You must include the server.'

    return status, message

@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
def ldap_configure(request):
    return render_to_response('ldap_config.html', {})


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
def ldap_settings_json(request):
    settings = []
    ldap_ids = LDAPSettings.objects.all().values('id')
    for i in ldap_ids:
        settings.append(load_ldap_settings(i['id']))
    return render_json_response(settings)


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
def ldap_save_config(request):
    response = {
        'success': True,
    }
    try:
        config_id = request.POST.get('config_id')
        if config_id:
            ldap_settings = LDAPSettings.objects.get(id=config_id)
            LDAPMappings.objects.get(settings=ldap_settings).delete()
        else:
            ldap_settings = LDAPSettings()

        ldap_settings.name = request.POST.get('ldap_name')
        ldap_settings.base_dn = request.POST.get('base_dn')
        ldap_settings.user_dn = request.POST.get('user_dn')
        ldap_settings.search_filter = request.POST.get('search_filter')
        ldap_settings.server = request.POST.get('server')

        status, message = check_input(ldap_settings)
        if status:
            ldap_settings.save()
        else:
            raise Exception(message)

        has_user_id = False
        local_fields = request.POST.getlist('local_field')
        ldap_fields = request.POST.getlist('ldap_field')
        for key, field in enumerate(local_fields):
            if field == 'idp_user_id':
                has_user_id = True
            ldap_mappings = LDAPMappings()
            ldap_mappings.settings = ldap_settings
            ldap_mappings.local_field = field
            ldap_mappings.ldap_field = ldap_fields[key]
            ldap_mappings.save()

        if not has_user_id:
            raise Exception('User ID is required. Please add one.')
    except Exception as e:
        response = {
            'success': False,
            'error': '{0}'.format(e)
        }
        transaction.rollback()
    else:
        transaction.commit()
    return render_json_response(response)


@ensure_csrf_cookie
@user_has_perms('sso', 'administer')
def ldap_remove_config(request):
    response = {
        'success': True,
    }
    try:
        LDAPSettings.objects.get(id=request.POST.get('config')).delete()
    except Exception as e:
        response = {
            'success': False,
            'error': '{0}'.format(e)
        }
    return render_json_response(response)


@ensure_csrf_cookie
def ldap_login(request, name):
    """
    This view will display the non-modal LDAP-based login form
    """
    if request.user.is_authenticated():
        return redirect(reverse('dashboard'))

    if not ldap_exists(name):
        error_context = {'window_title': 'Missing Configuration',
                         'error_title': 'Missing Configuration',
                         'error_message': 'This LDAP configuration does not exist. Please check the URL.'}
        return render_to_response('error.html', error_context)

    return render_to_response('ldap_login.html', {})


@ensure_csrf_cookie
def ldap_signin(request):
    """Assertion consume service (acs) of pepper"""
    try:
        ldap_process = LDAPSignIn(request)
        return ldap_process.auth()
    except Exception as e:
        log.error('There was an error starting LDAP auth: {0}'.format(e))
        response = {
            'success': False,
            'value': _('There was an error with your login information. Please email us if this issue continues.')
        }
        return render_json_response(response)


class LDAPSignIn:
    request = {}
    ldap_id = 0
    ldap_settings = {}
    email = ''
    ldap_user_info = {}
    user = {}

    def __init__(self, request):
        try:
            self.request = request
            self.ldap_id = self.request.REQUEST.get('name')

            self.ldap_settings = load_ldap_settings(self.ldap_id)
            self.email = self.request.REQUEST.get('email')
        except Exception as e:
            raise e

    def auth(self):
        """AJAX request to log in the user via LDAP."""
        if 'email' not in self.request.POST or 'password' not in self.request.POST:
            response = {
                'success': False,
                'value': _('There was an error with your login information. Please email us if this issue continues.')
            }
            return render_json_response(response)

        password = self.request.REQUEST.get('password')
        # the following is the user_dn format provided by the ldap server
        user_dn = self.ldap_settings['user_dn'].format({'email': self.email})
        # adjust this to your base dn for searching
        base_dn = self.ldap_settings['base_dn']
        connect = ldap.open(self.ldap_settings['server'])
        search_filter = self.ldap_settings['search_filter'].format({'email': self.email})
        try:
            # if authentication successful, get the full user data
            connect.bind_s(user_dn, password)
            self.ldap_user_info = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
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
                self.user = User.objects.get(email=self.email)
            except User.DoesNotExist:
                AUDIT_LOG.warning(u"Unknown user email: {0}. Creating new user.".format(self.email))
                try:
                    self.create_unknown_user()
                except Exception as e:
                    log.error("Failed to create LDAP user: {0}".format(e))
                    response = {
                        'success': False,
                        'value': _("There was an error creating your user. Please email us if this issue continues.")
                    }
                    return render_json_response(response)
            else:
                self.update_user()
        return render_json_response({'success': True})

    def create_unknown_user(self):
        """Create the sso user who does not exist in pepper"""
        try:
            # Generate username
            username = random_mark(20)

            self.user = User(username=username, email=self.email, is_active=False)
            self.user.set_password(username)  # Set password the same with username
            self.user.save()

            registration = Registration()
            registration.register(self.user)

            self.user.profile = UserProfile(user=self.user)
            self.user.profile.subscription_status = "Imported"
            self.user.profile.save()

            self.update_user()

            return redirect(reverse('register_sso_user', args=[registration.activation_key]))

        except Exception as e:
            db.transaction.rollback()
            raise e

    def update_user(self):
        # Save mapped attributes
        for local_field, ldap_field in self.ldap_settings['mappings']:
            value = self.ldap_user_info[ldap_field]
            if local_field == 'first_name':
                self.user.first_name = value
            elif local_field == 'last_name':
                self.user.last_name = value
            elif local_field == 'email':
                self.user.email = value
            elif local_field == 'district':
                self.user.profile.district = value
            elif local_field == 'school':
                self.user.profile.school = value
            elif local_field == 'idp_user_id':
                self.user.profile.sso_user_id = value
            # elif local_field == 'grade_level':
            #     ids = GradeLevel.objects.filter(name__in=self.parsed_data['grade_level'].split(',')).values_list(
            #         'id', flat=True)
            #     self.user.profile.grade_level = ','.join(ids)
            # elif local_field == 'major_subject_area':
            #     ids = SubjectArea.objects.filter(name__in=self.parsed_data['major_subject_area'].split(',')).values_list(
            #         'id', flat=True)
            #     self.user.profile.major_subject_area = ','.join(ids)
            # elif local_field == 'years_in_education':
            #     self.user.profile.years_in_education = YearsInEducation.objects.get(
            #         name=self.parsed_data['years_in_education'])
            # elif local_field == 'percent_lunch':
            #     self.user.profile.percent_lunch = Enum.objects.get(name='percent_lunch',
            #                                                        content=self.parsed_data['percent_lunch'])
            # elif local_field == 'percent_iep':
            #     self.user.profile.percent_iep = Enum.objects.get(name='percent_iep',
            #                                                      content=self.parsed_data['percent_iep'])
            # elif local_field == 'percent_eng_learner':
            #     self.user.profile.percent_eng_learner = Enum.objects.get(
            #         name='percent_eng_learner', content=self.parsed_data['percent_eng_learner'])

        self.user.profile.sso_type = 'LDAP'
        self.user.profile.sso_idp = self.ldap_settings['name']

        self.user.save()
        self.user.profile.save()
