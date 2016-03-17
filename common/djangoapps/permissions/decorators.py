from .utils import check_user_perms
from django.utils.decorators import available_attrs
from functools import wraps
from django.http import HttpResponseForbidden


def user_has_perms(item, action='any'):
    """
    Decorator for checking permissions before allowing access to a view. Only usable on views with a request object. If
    called without any parameters, it will check if a user has *any* admin permissions.
    :param item: The item the user is trying to access.
    :param action: The action which the user is trying to take.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if check_user_perms(request.user, item, action):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden
        return _wrapped_view
    return decorator
