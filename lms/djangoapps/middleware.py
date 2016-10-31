from django.conf import settings
from django.utils import timezone
from student.models import UserProfile

import datetime
from datetime import timedelta
from administration.models import UserLoginInfo

class SessionExpiry(object):
    """ Set the session expiry according to settings """
    def process_request(self, request):
        if getattr(settings, 'PEPPER_SESSION_EXPIRY', None):
            request.session.set_expiry(settings.PEPPER_SESSION_EXPIRY)
        return None


class UpdateLastActivityMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            UserProfile.objects.filter(user__id=request.user.id) \
                           .update(last_activity=timezone.now())


class UserLastActiveSaveMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        if request.user.is_authenticated():
            utc_time = datetime.datetime.utcnow()
            user_log_info = UserLoginInfo.objects.filter(user_id=request.user.id)
            if user_log_info:
                time_diff = utc_time - datetime.datetime.strptime(user_log_info[0].temp_time, '%Y-%m-%d %H:%M:%S')
                time_diff_seconds = time_diff.seconds

                if time_diff_seconds > 120:
                    utc_time_str = utc_time.strftime('%Y-%m-%d %H:%M:%S')

                    user_log_info[0].temp_time = utc_time_str
                    utc_time_30m_str = (utc_time + timedelta(seconds=30*60)).strftime('%Y-%m-%d %H:%M:%S')
                    user_log_info[0].logout_time = utc_time_30m_str
                    db_login_time = datetime.datetime.strptime(user_log_info[0].login_time, '%Y-%m-%d %H:%M:%S')
                    last_session = datetime.datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S') - db_login_time
                    user_log_info[0].last_session = last_session.seconds + 1800
                    user_log_info[0].total_session = user_log_info[0].total_session + time_diff_seconds
                    user_log_info[0].save()
