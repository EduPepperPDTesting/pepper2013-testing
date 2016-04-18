from .utils import check_user_perms
from django.utils.decorators import available_attrs
import urlparse
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseForbidden
from mitxmako.shortcuts import render_to_response


def user_has_perms(item, action='any', access_level='any', exclude_superuser=False):
    """
    Decorator for checking permissions before allowing access to a view. Only usable on views with a request object. If
    called without any parameters, it will check if a user has *any* admin permissions.
    :param item: The item the user is trying to access.
    :param action: The action which the user is trying to take.
    :param access_level: The level of this access.
    :param exclude_superuser: Set to True if you want to exclude the superuser override.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if check_user_perms(request.user, item, action, access_level, exclude_superuser):
                return view_func(request, *args, **kwargs)
            if request.user.is_anonymous():
                path = request.build_absolute_uri()
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse.urlparse(settings.LOGIN_URL)[:2]
                current_scheme, current_netloc = urlparse.urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme) and
                        (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(path, None, REDIRECT_FIELD_NAME)
            else:
                error_context = {'window_title': '403 Error - Access Denied',
                                 'error_title': '403 Error - Access Denied',
                                 'error_message': 'You do not have access to this are of the site. If you feel this is\
                                                   in error, please contact the site administrator for assistance.'}
                return HttpResponseForbidden(render_to_response('error.html', error_context))
        return _wrapped_view
    return decorator
