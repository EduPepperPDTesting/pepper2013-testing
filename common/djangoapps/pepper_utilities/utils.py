import urllib2
from django.http import HttpResponse
import json
import random


def get_request_array(params, name, max=None):
    """
    Gets array values from a POST or GET.
    :param params: The array to pull data from (usually request.POST or request.GET).
    :param name: The name of the array (e.g. - 'name' in 'name[0]').
    :param max: Special case needed for tablesorter handling.
    :return: dict of indexes and values.
    """
    output = dict()
    for key in params.keys():
        value = urllib2.unquote(params.get(key))
        if key.startswith(name + '[') and not value == 'undefined':
            start = key.find('[')
            i = key[start + 1:-1]
            if max and int(i) > max:
                i = 'all'
            output.update({i: value})
    return output


def render_json_response(data):
    """
    Shortcut to return JSON responses.
    :param data: The data to convert to JSON (list or dict).
    :return: HttpResponse with the converted data and correct content type.
    """
    return HttpResponse(json.dumps(data), content_type='application/json')


def render_jsonp_response(callback, data):
    """
    Shortcut to return JSON responses.
    :param data: The data to convert to JSON (list or dict).
    :return: HttpResponse with the converted data and correct content type.
    """
    return HttpResponse('{0}({1})'.format(callback, json.dumps(data)), content_type='text/javascript')


def random_mark(length):
    """
    Generates a random string of the given length.
    :param length: The length of the random string.
    :return: The random string.
    """
    return "".join(
        random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz1234567890@#$%^&*_+{};~') for _ in range(length))
