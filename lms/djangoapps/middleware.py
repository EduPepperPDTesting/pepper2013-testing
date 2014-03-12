from django.conf import settings

class SessionExpiry(object):
    """ Set the session expiry according to settings """
    def process_request(self, request):
        if getattr(settings, 'SESSION_EXPIRY', None):
            request.session.set_expiry(settings.SESSION_EXPIRY)
        return None


    
