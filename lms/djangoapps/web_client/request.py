# Imports
import json
import requests
import logging
import httplib

AUDIT_LOG = logging.getLogger("audit")


def patch_send():
    """
    Monkey-patches the httplib send to output the raw HTTP request as an exception.
    """
    def new_send(self, data):
        raise Exception(data)
    httplib.HTTPConnection.send = new_send


class WebRequest:
    """
    Class for creating and carrying out requests to JSON REST services
    """
    def __init__(self,
                 base_url,
                 success_attribute=None,
                 success_value=None,
                 error_message=None,
                 content_type=None,
                 debug=False
                 ):
        self.base_url = base_url
        self.success_attribute = success_attribute
        self.success_value = success_value
        self.error_message = error_message
        self.debug = debug
        if content_type:
            self.content_type = content_type
        else:
            self.content_type = 'text/plain'

    def do_request(self, endpoint, method, data):
        """
        Makes the request to specified endpoint. Returns parsed JSON object on success. Raises exceptions on error.
        """
        try:
            # Make the request to the given URL/endpoint with the given data
            kwargs = {'method': method,
                      'url': self.base_url + endpoint,
                      'timeout': 15,
                      'headers': {'Content-Type': self.content_type}
                      }
            if method == 'post':
                kwargs.update({'data': data})
            else:
                kwargs.update({'params': data})
            # Patch the httplib send for debugging purposes.
            if self.debug:
                patch_send()
            response = requests.request(**kwargs)

            # Make sure the request was successful first by checking the HTTP status, then check any specified JSON
            # attributes, if there are any.
            if response.status_code == 200:
                # Parse the JSON returned.
                parsed = json.loads(response.text)
                # If a JSON attribute was specified, check to see if it matches the supplied value.
                if self.success_attribute and not parsed[self.success_attribute] == self.success_value:
                    raise Exception(u"Unsuccessful request: {0}".format(parsed[self.error_message]))
                return parsed
            else:
                # Raise an exception if the code was anything other than a 200.
                raise Exception(u"URL {0} returned HTTP code: {1}".format(response.url, response.status_code))
        except Exception as e:
            # Log any exceptions before raising them.
            AUDIT_LOG.warning(u"There was a WebRequest connection error: {0}.".format(e))
            raise e
