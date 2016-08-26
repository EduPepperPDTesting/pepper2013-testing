from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta

from models import UserLoginInfo

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