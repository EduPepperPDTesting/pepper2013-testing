import urllib2


def get_request_array(params, name, max=None):
    """
    Gets array values from a POST or GET.
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
