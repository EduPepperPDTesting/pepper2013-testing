from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseForbidden
import json
from django.contrib.auth.decorators import login_required
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

@ensure_csrf_cookie
def get_user_login_info(request):
	user_log_info = []
	if request.POST.get('state') or request.POST.get('district') or request.POST.get('school'):
		data = UserProfile.objects.all()
		data = filter_user(request.POST, data)

		user_array = []
		for user in data:
			user_array.append(user.user_id)

		user_log_info = UserLoginInfo.objects.filter(user_id__in=user_array) # Django model QuerySet array. SQL:in operater
	else:
		user_log_info = UserLoginInfo.objects.filter()

	login_info_list = []
	for d in user_log_info:
		dict_tmp = {}
		try:
			obj_user = UserProfile.objects.get(user_id=d.user_id)
		except Exception as e:
			continue

		try:
			dict_tmp['district'] = str(obj_user.district.name)
			dict_tmp['state'] = str(obj_user.district.state.name)
		except Exception as e:
			dict_tmp['district'] = ''
			dict_tmp['state'] = ''

		try:
			dict_tmp['school'] = str(obj_user.school.name)
		except Exception as e:
			dict_tmp['school'] = ''

		dict_tmp['id'] = d.user_id
		dict_tmp['email'] = obj_user.user.email
		dict_tmp['username'] = obj_user.user.username
		dict_tmp['first_name'] = obj_user.user.first_name
		dict_tmp['last_name'] = obj_user.user.last_name
		dict_tmp['login_time'] = d.login_time

		dict_tmp['is_active'] = obj_user.user.is_active
		dict_tmp['is_staff'] = obj_user.user.is_staff
		dict_tmp['is_superuser'] = obj_user.user.is_superuser

		if not active_recent(obj_user) or d.logout_press:
			dict_tmp['logout_time'] = d.logout_time
			dict_tmp['last_session'] = study_time_format(d.last_session)
			dict_tmp['online_state'] = 'Off'
			dict_tmp['total_session'] = study_time_format(d.total_session)
		else:
			dict_tmp['logout_time'] = ''
			dict_tmp['last_session'] = ''
			dict_tmp['online_state'] = 'On'
			dict_tmp['total_session'] = study_time_format(d.total_session - 1800)

		login_info_list.append(dict_tmp)
	return HttpResponse(json.dumps({'rows': login_info_list}), content_type="application/json")

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
		psw_format_check = password_format_check(user_psw, user_psw_confirm)
		if psw_format_check['type'] != 200:
			context['value'] = psw_format_check
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
		user_psw_old = request.POST.get('user_post_old')

		# check the password and password_confirm format again
		psw_format_check = password_format_check(user_psw, user_psw_confirm)
		if psw_format_check['type'] != 200:
			context['value'] = psw_format_check
			return HttpResponse(json.dumps(context), content_type="application/json")

		'''
		verify the old password if old password in request
		'''
		if user_psw_old:
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

def password_format_check(psw1, psw2):
	error_info = [{"grouptype": "error1", "type": 200, "info": ""},
                  {"grouptype": "error1", "type": 1, "info": "Please fill in new password."},
                  {"grouptype": "error1", "type": 2, "info": "New password must contain A-Z, a-z, 0-9 and ~!@#$%^&* and must be 8-16 characters long."},
                  {"grouptype": "error1", "type": 3, "info": "New password must contain A-Z, a-z, 0-9 and ~!@#$%^&* and must be 8-16 characters long."},
                  {"grouptype": "error1", "type": 4, "info": "Confirm password is required."},
                  {"grouptype": "error1", "type": 5, "info": "Your new and confirm password are different. Please enter again."}]

	p1 = psw1.strip()
	p2 = psw2.strip()

	if not psw1:
		return error_info[1]

	if len(p1) < 8 or len(p1) > 16:
		return error_info[2]

	regexp = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~!@#$%^&*])[\da-zA-Z~!@#$%^&*]{8,16}$'
	match_str = re.findall(regexp, psw1)
	if not match_str:
		return error_info[3]

	if not psw2:
		return error_info[4]

	if psw1 != psw2:
		return error_info[5]

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


def usage_report_download_excel(request):
	if request.user.is_authenticated() and request.user.is_superuser:
		import xlsxwriter
		output = StringIO()
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		worksheet = workbook.add_worksheet()
		TITLES = ["State", "District", "School", "Email", "User Name", "First Name", "Last Name","Time Login", "Time Last Logout", "Last Session Time", "Total Session Time"]

		FIELDS = ["state", "district", "school", "email", "username", "first_name", "last_name","login_time", "logout_time", "last_session", "total_session"]

		for i, k in enumerate(TITLES):
			worksheet.write(0, i, k)
		row = 1
		down_result = get_download_info(request)
		for d in down_result:
			for k, v in enumerate(FIELDS):
				worksheet.write(row, k, d[v])
			row += 1
		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = datetime.datetime.now().strftime('attachment; filename=usage-report-%Y-%m-%d-%H-%M-%S.xlsx')
		workbook.close()
		response.write(output.getvalue())
		return response
	else:
		raise Http404

def get_download_info(request):
	user_log_info = []
	time_diff_m = request.POST.get('local_utc_diff_m')
	if request.POST.get('state') or request.POST.get('district') or request.POST.get('school'):
		data = UserProfile.objects.all()
		data = filter_user(request.POST, data)

		user_array = []
		for user in data:
			user_array.append(user.user_id)

		user_log_info = UserLoginInfo.objects.filter(user_id__in=user_array)
	else:
		user_log_info = UserLoginInfo.objects.filter()
	
	login_info_list = []
	for d in user_log_info:
		dict_tmp = {}
		try:
			obj_user = UserProfile.objects.get(user_id=d.user_id)
		except Exception as e:
			continue

		try:
			dict_tmp['district'] = str(obj_user.district.name)
			dict_tmp['state'] = str(obj_user.district.state.name)
		except Exception as e:
			dict_tmp['district'] = ''
			dict_tmp['state'] = ''

		try:
			dict_tmp['school'] = str(obj_user.school.name)
		except Exception as e:
			dict_tmp['school'] = ''

		dict_tmp['email'] = obj_user.user.email
		dict_tmp['username'] = obj_user.user.username
		dict_tmp['first_name'] = obj_user.user.first_name
		dict_tmp['last_name'] = obj_user.user.last_name
		dict_tmp['login_time'] = time_to_local(d.login_time,time_diff_m)

		if not active_recent(obj_user) or d.logout_press:
			dict_tmp['logout_time'] = time_to_local(d.logout_time,time_diff_m)
			dict_tmp['last_session'] = study_time_format(d.last_session)
			#dict_tmp['online_state'] = 'Off'
			dict_tmp['total_session'] = study_time_format(d.total_session)
		else:
			dict_tmp['logout_time'] = ''
			dict_tmp['last_session'] = ''
			#dict_tmp['online_state'] = 'On'
			dict_tmp['total_session'] = study_time_format(d.total_session - 1800)

		login_info_list.append(dict_tmp)
	return login_info_list

def filter_user(vars, data):
	if vars.get('state', None):
		data = data.filter(Q(district__state_id=vars.get('state')))
	if vars.get('district', None):
		data = data.filter(Q(district_id=vars.get('district')))
	if vars.get('school', None):
		data = data.filter(Q(school_id=vars.get('school')))
	data = data.filter(~Q(subscription_status='Imported'))
	return data

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