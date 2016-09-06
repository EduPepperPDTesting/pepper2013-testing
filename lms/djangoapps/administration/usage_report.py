from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django_future.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from student.models import District, Cohort, School, State
from django.http import HttpResponseForbidden
from django.db.models import Q
from student.models import UserProfile

import datetime
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

def filter_user(vars, data):
	if vars.get('state', None):
		data = data.filter(Q(district__state_id=vars.get('state')))
	if vars.get('district', None):
		data = data.filter(Q(district_id=vars.get('district')))
	if vars.get('school', None):
		data = data.filter(Q(school_id=vars.get('school')))
	data = data.filter(~Q(subscription_status='Imported'))
	return data

@ensure_csrf_cookie
def get_user_login_info(request):
	user_log_info = []
	if request.POST.get('state') or request.POST.get('district') or request.POST.get('school'):
		data = UserProfile.objects.all()
		data = filter_user(request.POST, data)

		user_array = []
		for user in data:
			user_array.append(user.user_id)

		user_log_info = UserLoginInfo.objects.filter(user_id__in=user_array) #Django model QuerySet array. SQL:in operater
	else:
		user_log_info = UserLoginInfo.objects.filter()
	
	login_info_list = []
	for d in user_log_info:
		dict_tmp = {}
		obj_user = User.objects.get(id=d.user_id)
		
		try:
			if obj_user.profile.district.state.id:
				dict_tmp['state'] = State.objects.get(id=obj_user.profile.district.state.id).name
		except Exception as e:
			dict_tmp['state'] = ''

		try:
			if obj_user.profile.district.id:
				dict_tmp['district'] = District.objects.get(id=obj_user.profile.district.id).name
		except Exception as e:
			dict_tmp['district'] = ''

		try:
			if obj_user.profile.school.id:
				dict_tmp['school'] = School.objects.get(id=obj_user.profile.school.id).name
		except Exception as e:
			dict_tmp['school'] = ''

		dict_tmp['email'] = obj_user.email
		dict_tmp['username'] = obj_user.username
		dict_tmp['first_name'] = obj_user.first_name
		dict_tmp['last_name'] = obj_user.last_name
		dict_tmp['login_time'] = d.login_time

		if active_recent(obj_user):
			dict_tmp['logout_time'] = ''
			dict_tmp['last_session'] = ''
			dict_tmp['online_state'] = 'On'
		else:
			dict_tmp['logout_time'] = d.logout_time
			dict_tmp['last_session'] = study_time_format(d.last_session)
			dict_tmp['online_state'] = 'Off'

		dict_tmp['total_session'] = study_time_format(d.total_session)

		login_info_list.append(dict_tmp)
	return HttpResponse(json.dumps({'rows': login_info_list}), content_type="application/json")

@ensure_csrf_cookie
@login_required
def user_lastactive_save(request):
	utc_time = datetime.datetime.utcnow()
	try:
		time_diff = utc_time - request.session['record_time']
	except Exception as e:
		request.session['record_time'] = utc_time
		time_diff = utc_time - request.session['record_time']
			
	time_diff_seconds = time_diff.seconds
	if time_diff_seconds > 120:
		request.session['record_time'] = utc_time
		user_log_info = UserLoginInfo.objects.filter(user_id=request.user.id)
		if user_log_info:
			utc_time_30m_str = (utc_time + timedelta(seconds=30*60)).strftime('%Y-%m-%d %H:%M:%S')
			user_log_info[0].logout_time = utc_time_30m_str

			db_login_time = datetime.datetime.strptime(user_log_info[0].login_time, '%Y-%m-%d %H:%M:%S')
			utc_time_str = utc_time.strftime('%Y-%m-%d %H:%M:%S')
			last_session = datetime.datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S') - db_login_time
			user_log_info[0].last_session = last_session.seconds + 1800
			user_log_info[0].total_session = user_log_info[0].total_session + time_diff_seconds
			user_log_info[0].save()
	return HttpResponse(json.dumps({}), content_type="application/json")

'''
def time_to_local(user_time,time_diff_m):
	user_time_time = datetime.datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S')
	plus_sub = 1
	time_diff_m_int = int(time_diff_m)
	if time_diff_m_int >= 0:
		plus_sub = 1
	else:
		plus_sub = -1
	
	user_time_str = (user_time_time + timedelta(seconds=abs(time_diff_m_int)*60)*plus_sub).strftime('%Y-%m-%d %H:%M:%S')
	return user_time_str
'''

def active_recent(user):
	user_now = user
	utc_month = datetime.datetime.utcnow().strftime("%m")
	utc_day = datetime.datetime.utcnow().strftime("%d")
	utc_h = datetime.datetime.utcnow().strftime("%H")
	utc_m = datetime.datetime.utcnow().strftime("%M")
	d_min = 60*int(utc_h) + int(utc_m)
	if user_now.profile.last_activity:
		user_last_activity = user_now.profile.last_activity
		u_min = 60*int(user_last_activity.strftime("%H")) + int(user_last_activity.strftime("%M"))
		close = int(d_min) - int(u_min) < 1
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
	return ('{0}{1} {2} {3}').format(sign, hour_full, minute, minute_unit)

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
	return
	'''
	if request.user.is_authenticated() and request.user.is_superuser:
		import xlsxwriter
		output = StringIO()
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		worksheet = workbook.add_worksheet()
		FIELDS = ["user_first_name", "user_last_name", "user_email", "district", "school", "total_time", "collaboration_time",
              "discussion_time", "portfolio_time", "external_time", "course_time", "complete_course_num", "current_course_num"]

        TITLES = ["state", "district", "school", "email", "username", "first_name", "last_name",
              "login_time", "logout_time", "last_session", "total_session", "online_state"]
        for i, k in enumerate(TITLES):
        	worksheet.write(0, i, k)
        row = 1

        
        results = get_download_info(request)

        for p in results:
        	for i, k in enumerate(FIELDS):
        		worksheet.write(row, i, p[k])
        	row += 1
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = datetime.now().strftime('attachment; filename=users-time-report-%Y-%m-%d-%H-%M-%S.xlsx')
        workbook.close()
        response.write(output.getvalue())
        return response
    else:
    	raise Http404
    '''

'''
def get_download_info(request):
	user_log_info = []
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
		obj_user = User.objects.get(id=d.user_id)
		
		try:
			if obj_user.profile.district.state.id:
				dict_tmp['state'] = State.objects.get(id=obj_user.profile.district.state.id).name
		except Exception as e:
			dict_tmp['state'] = ''

		try:
			if obj_user.profile.district.id:
				dict_tmp['district'] = District.objects.get(id=obj_user.profile.district.id).name
		except Exception as e:
			dict_tmp['district'] = ''

		try:
			if obj_user.profile.school.id:
				dict_tmp['school'] = School.objects.get(id=obj_user.profile.school.id).name
		except Exception as e:
			dict_tmp['school'] = ''

		dict_tmp['email'] = obj_user.email
		dict_tmp['username'] = obj_user.username
		dict_tmp['first_name'] = obj_user.first_name
		dict_tmp['last_name'] = obj_user.last_name
		dict_tmp['login_time'] = d.login_time

		if active_recent(obj_user):
			dict_tmp['logout_time'] = ''
			dict_tmp['last_session'] = ''
			dict_tmp['online_state'] = 'On'
		else:
			dict_tmp['logout_time'] = d.logout_time
			dict_tmp['last_session'] = study_time_format(d.last_session)
			dict_tmp['online_state'] = 'Off'

		dict_tmp['total_session'] = study_time_format(d.total_session)

		login_info_list.append(dict_tmp)
	return login_info_list
'''