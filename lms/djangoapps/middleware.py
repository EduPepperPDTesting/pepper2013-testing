from django.conf import settings
from django.utils import timezone
from student.models import UserProfile

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
