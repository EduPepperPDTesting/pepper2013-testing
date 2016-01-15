from .utils import has_admin_perm, has_any_perm
from django.utils.decorators import available_attrs
from functools import wraps
from django.http import HttpResponseForbidden


def user_has_perms(item, action='any'):
    """
    Decorator for checking permissions before allowing access to a view.
    :param item: The item the user is trying to access.
    :param action: The action which the user is trying to take.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if has_admin_perm(request.user, item, action):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden
        return _wrapped_view
    return decorator


def user_has_admin_perms():
    """
    Decorator for determining if a user has *any* admin perms.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if has_any_perm(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden
        return _wrapped_view
    return decorator
