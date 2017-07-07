from functools import wraps
from django.http import HttpResponse


def ajax_login_required(redirect=None):
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                print request.user.is_authenticated
                return func(request, *args, **kwargs)
            else:
                return HttpResponse('Unauthorized', status=401)
        return returned_wrapper
    return decorator
