from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseForbidden
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django_future.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from student.models import District, Cohort, School, State
from django.db.models import Q
from student.models import UserProfile
from StringIO import StringIO
import datetime
# from django.utils.translation import ugettext as _
from ratelimitbackend.exceptions import RateLimitException
from student.models import CmsLoginInfo
from django.contrib.auth import logout, authenticate, login

import re
import urllib2
from datetime import timedelta
from models import UserLoginInfo

import logging
log = logging.getLogger("tracking")

@login_required
def main(request):
	if request.user.is_superuser:
		return render_to_response('administration/usage_report.html', {})
	else:
		error_context = {'window_title': '403 Error - Access Denied',
		 				 'error_title': '403 Error - Access Denied',
		 				 'error_message': 'You do not have access to this are of the site. If you feel this is\
                                           in error, please contact the site administrator for assistance.'}
        return HttpResponseForbidden(render_to_response('error.html', error_context))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_user_login_info(request):
	columns = {0: ['district__state__name', '__iexact'],
			   1: ['district__name', '__iexact'],
			   2: ['school__name', '__iexact'],
			   3: ['user__email', '__icontains'],
			   4: ['user__username', '__icontains'],
			   5: ['user__first_name', '__icontains'],
			   6: ['user__last_name', '__icontains'],
			   7: ['loginfo__login_time', ''],
			   8: ['loginfo__logout_time', ''],
			   9: ['loginfo__last_session', ''],
			   10: ['loginfo__total_session', '']}

	# Parse the sort data passed in.
	sorts = get_post_array(request.GET, 'col')
	# Parse the filter data passed in.
	filters = get_post_array(request.GET, 'fcol', 12)
	# Get the page number and number of rows per page, and calculate the start and end of the query.
	page = int(request.GET['page'])
	size = int(request.GET['size'])
	start = page * size
	end = start + size

	order = build_sorts(columns, sorts)
	if len(filters):
		kwargs = build_filter(columns, filters)
		user_data = UserProfile.objects.filter(**kwargs).order_by(*order)
	else:
		user_data = UserProfile.objects.all().order_by(*order)

	total_rows_count = user_data.count()
	login_info_list = list()
	for d in user_data[start:end]:
		dict_tmp = {}
		try:
			dict_tmp['district'] = str(d.district.name)
			dict_tmp['state'] = str(d.district.state.name)
		except Exception as e:
			dict_tmp['district'] = ''
			dict_tmp['state'] = ''

		try:
			dict_tmp['school'] = str(d.school.name)
		except Exception as e:
			dict_tmp['school'] = ''

		dict_tmp['id'] = d.user_id
		dict_tmp['email'] = d.user.email
		dict_tmp['username'] = d.user.username
		dict_tmp['first_name'] = d.user.first_name
		dict_tmp['last_name'] = d.user.last_name

		dict_tmp['is_staff'] = d.user.is_staff
		dict_tmp['is_active'] = d.user.is_active
		dict_tmp['is_superuser'] = d.user.is_superuser

		try:
			user_login_data = d.loginfo.all()[0]
			if not active_recent(d) or user_login_data.logout_press:
				dict_tmp['logout_time'] = user_login_data.logout_time
				dict_tmp['last_session'] = study_time_format(user_login_data.last_session)
				dict_tmp['online_state'] = 'Off'
				dict_tmp['total_session'] = study_time_format(user_login_data.total_session)
			else:
				dict_tmp['logout_time'] = ''
				dict_tmp['last_session'] = ''
				dict_tmp['online_state'] = 'On'
				dict_tmp['total_session'] = study_time_format(user_login_data.total_session - 1800)
		except:
			dict_tmp['login_time'] = ''
			dict_tmp['logout_time'] = ''
			dict_tmp['last_session'] = ''
			dict_tmp['online_state'] = ''
			dict_tmp['total_session'] = ''

		login_info_list.append(dict_tmp)
	return HttpResponse(json.dumps({'rows': login_info_list, 'rows_count': total_rows_count}), content_type="application/json")

def get_post_array(post, name, max=None):
    """
    Gets array values from a POST.
    """
    output = dict()
    for key in post.keys():
        value = urllib2.unquote(post.get(key))
        if key.startswith(name + '[') and not value == 'undefined':
            start = key.find('[')
            i = key[start + 1:-1]
            if max and int(i) > max:
                i = 'all'
            output.update({i: value})
    return output

def build_filter(columns, filters):
	filter_result = dict()
	for k in filters:
		if int(k) > 6:
			continue
		else:
			filter_result[columns[int(k)][0] + columns[int(k)][1]] = filters[k]
	return filter_result


def build_sorts(columns, sorts):
	order_result = list()
	for k in sorts:
		if int(k) > 10:
			break
		else:
			if sorts[k] == '0':
				order_result.append(columns[int(k)][0])
			else:
				order_result.append('-' + columns[int(k)][0])
	return order_result


@login_required
@ensure_csrf_cookie
def save_user_status(request):
	'''
	20170830 add for save user 3 status in usage_report.
	'''
	user_request = User.objects.filter(id=request.user.id)
	if user_request:
		if not user_request[0].is_superuser:
			return
	else:
		return

	context = {'success': False}
	user_id = int(request.POST.get('user_id'))
	user_changed = User.objects.filter(id=user_id)
	if user_changed:
		user = user_changed[0]
		is_active = int(request.POST.get('is_active'))
		is_staff = int(request.POST.get('is_staff'))
		is_superuser = int(request.POST.get('is_superuser'))

		user.is_active = is_active
		user.is_staff = is_staff
		user.is_superuser = is_superuser
		user.save()
		context['success'] = True
	return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
@ensure_csrf_cookie
def save_user_password(request):
	'''
	20170907 add for save user password in usage_report.
	Save user password without check old password.
	grouptype:
	error0: Save password failure, Please try later or contact administrator.
	error1: New password format or confirm password error.
	error2: Old password error.
	error3: New password equals to the old one error'
	'''
	user_request = User.objects.filter(id=request.user.id)
	if user_request:
		if not user_request[0].is_superuser:
			return
	else:
		return

	user_id = int(request.POST.get('user_id'))
	context = {'success': False, 'value': {}}

	user_login = User.objects.filter(id=user_id)
	if user_login:
		user = user_login[0]
		user_psw = request.POST.get('user_post_1')
		user_psw_confirm = request.POST.get('user_post_2')

		# check the password and password_confirm format again
		psw_format_check = password_format_check(user_psw, psw2=user_psw_confirm)
		if psw_format_check['type'] != 200:
			context['value'] = psw_format_check
			return HttpResponse(json.dumps(context), content_type="application/json")

		# verify whether the new password equals to the old one
		user_newpws = authenticate(username=user.username, password=user_psw, request=request)
		if user_newpws:
			context['value'] = {"grouptype": "error3", "type": 1, "info": "The password needs to be different from the previous one."}
			return HttpResponse(json.dumps(context), content_type="application/json")
		
		# save user password
		user.set_password(user_psw)
		user.save()
		
		# save user password_change_date
		user_log_info = UserLoginInfo.objects.filter(user_id=user_id)
		if user_log_info:
			utctime_str = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
			user_log_info[0].password_change_date = utctime_str
			user_log_info[0].save()

		context['success'] = True
	return HttpResponse(json.dumps(context), content_type="application/json")

@ensure_csrf_cookie
def save_user_password_checkold(request):
	'''
	Save password for no login user with check old password.
	'''
	user_id = int(request.POST.get('user_id'))
	context = {'success': False, 'value': {}}

	user_login = User.objects.filter(id=user_id)
	if user_login:
		user = user_login[0]
		user_psw = request.POST.get('user_post_1')
		user_psw_confirm = request.POST.get('user_post_2')
		user_psw_old = request.POST.get('user_post_0')
		if not user_psw_old:
			user_psw_old = ''

		# check the password and password_confirm format again
		psw_format_check = password_format_check(user_psw, psw2=user_psw_confirm)
		if psw_format_check['type'] != 200:
			context['value'] = psw_format_check
			return HttpResponse(json.dumps(context), content_type="application/json")

		# verify old password of the user
		oldpsw_check = user_authenticate(username=user.username, password=user_psw_old, request=request)
		if oldpsw_check['type'] != 200:
			context['value'] = oldpsw_check
			return HttpResponse(json.dumps(context), content_type="application/json")

		# verify whether the new password equals to the old one
		user_newpws = authenticate(username=user.username, password=user_psw, request=request)
		if user_newpws:
			context['value'] = {"grouptype":"error3","type":1,"info":"The password needs to be different from the previous one."}
			return HttpResponse(json.dumps(context), content_type="application/json")
		
		# save user password
		user.set_password(user_psw)
		user.save()
		
		# save user password_change_date
		user_log_info = UserLoginInfo.objects.filter(user_id=user_id)
		if user_log_info:
			utctime_str = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
			user_log_info[0].password_change_date = utctime_str
			user_log_info[0].save()

		context['success'] = True
	return HttpResponse(json.dumps(context), content_type="application/json")

def password_format_check(psw1, **psw2):
	error_info = [{"grouptype": "error1", "type": 200, "info": ""},
                  {"grouptype": "error1", "type": 1, "info": "Please fill in new password."},
                  {"grouptype": "error1", "type": 2, "info": "New password must contain A-Z, a-z, 0-9 and ~!@#$%^&* and must be 8-16 characters long."},
                  {"grouptype": "error1", "type": 3, "info": "New password must contain A-Z, a-z, 0-9 and ~!@#$%^&* and must be 8-16 characters long."},
                  {"grouptype": "error1", "type": 4, "info": "Confirm password is required."},
                  {"grouptype": "error1", "type": 5, "info": "Your new and confirm password are different. Please enter again."}]

	p1 = psw1.strip()
	if not p1:
		return error_info[1]

	if len(p1) < 8 or len(p1) > 16:
		return error_info[2]

	regexp = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~!@#$%^&*])[\da-zA-Z~!@#$%^&*]{8,16}$'
	match_str = re.findall(regexp, p1)
	if not match_str:
		return error_info[3]

	for p in psw2:
		p2 = psw2[p].strip()
		if not p2:
			return error_info[4]

		if p1 != p2:
			return error_info[5]
		break
	return error_info[0]

def user_authenticate(username, password, request):
	error_info = [{"grouptype": "error2", "type": 200, "info": ""},
                  {"grouptype": "error2", "type": 1, "info": "Too many failed login attempts. Try again later."},
                  {"grouptype": "error2", "type": 2, "info": "Please verify that the old password is correct."}]

	try:
		user = authenticate(username=username, password=password, request=request)

		ip_address = request.META.get('HTTP_X_FORWARDED_FOR', 'not get')
		login_info = CmsLoginInfo(ip_address=ip_address, user_name=username, log_type_login=True, login_or_logout_time=datetime.datetime.utcnow())
		login_info.save()
    # this occurs when there are too many attempts from the same IP address
	except RateLimitException:
		return error_info[1]

	if user is None:
		# if we didn't find this username earlier, the account for this email
		# doesn't exist, and doesn't have a corresponding password
		return error_info[2]

	return error_info[0]

# -------------- Dropdown Lists -------------
def drop_states(request):
    r = list()
    if request.user.is_superuser is False:
        data = State.objects.get(id=request.user.profile.district.state.id)
        r.append({"id": data.id, "name": data.name})
    else:
        data = State.objects.all()
        data = data.order_by("name")
        for item in data:
            if item.id == request.user.profile.district.state.id:
                r.append({"id": item.id, "name": item.name, 'curr': item.id})
            else:
                r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")

def drop_districts(request):
    r = list()
    if request.user.is_superuser is False:
        data = District.objects.get(id=request.user.profile.district.id)
        r.append({"id": data.id, "name": data.name})
    else:
        if request.GET.get('state'):
            data = District.objects.filter(state=request.GET.get('state'))
        else:
            data = District.objects.filter(state=request.user.profile.district.state.id)
        data = data.order_by("name")
        for item in data:
            if item.id == request.user.profile.district.id:
                r.append({"id": item.id, "name": item.name, "code": item.code, 'curr': item.id})
            else:
                r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")

def drop_schools(request):
    r = list()
    if request.user.is_superuser is False:
        district = UserProfile.objects.get(user_id=request.user.id).district
        data = School.objects.filter(district=district.id)
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name})
    else:
        if request.GET.get('district'):
            data = School.objects.filter(district=request.GET.get('district'))
        else:
            data = School.objects.filter(district=request.user.profile.district.id)
        data = data.order_by("name")
        for item in data:
            if item.id == request.user.profile.school.id:
                r.append({"id": item.id, "name": item.name, 'curr': item.id})
            else:
                r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")

def time_to_local(user_time,time_diff_m):
	'''
	Just use for usage_report_download_excel
	'''
	user_time_time = datetime.datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S')
	plus_sub = 1
	time_diff_m_int = int(time_diff_m)
	if time_diff_m_int >= 0:
		plus_sub = 1
	else:
		plus_sub = -1
	
	user_time_str = (user_time_time + timedelta(seconds=abs(time_diff_m_int)*60)*plus_sub).strftime('%m-%d-%Y %I:%M:%S %p')
	return user_time_str

def active_recent(user_profile):
	'''
	Parameter is UserProfile object, not User project.
	'''
	user_profile = user_profile
	utc_month = datetime.datetime.utcnow().strftime("%m")
	utc_day = datetime.datetime.utcnow().strftime("%d")
	utc_h = datetime.datetime.utcnow().strftime("%H")
	utc_m = datetime.datetime.utcnow().strftime("%M")
	d_min = 60*int(utc_h) + int(utc_m)
	if user_profile.last_activity:
		user_last_activity = user_profile.last_activity
		u_min = 60*int(user_last_activity.strftime("%H")) + int(user_last_activity.strftime("%M"))
		close = int(d_min) - int(u_min) <= 30   
		active = user_last_activity.strftime("%d") == utc_day and user_last_activity.strftime("%m") == utc_month and close
	else:
		active = False
	return active

def study_time_format(t, is_sign=False):
	sign = ''
	if t < 0 and is_sign:
		sign = '-'
		t = abs(t)
	hour_unit = ' Hour, '
	minute_unit = ' Minute'
	hour = int(t / 60 / 60)
	minute = int(t / 60 % 60)
	if hour != 1:
		hour_unit = ' Hours, '
	if minute != 1:
		minute_unit = 'Minutes'
	if hour > 0:
		hour_full = str(hour) + hour_unit
	else:
		hour_full = ''
	return (('{0}{1} {2} {3}').format(sign, hour_full, minute, minute_unit)).strip()