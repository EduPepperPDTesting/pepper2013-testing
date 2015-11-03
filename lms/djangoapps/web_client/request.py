# Imports
import json
import requests
import logging

AUDIT_LOG = logging.getLogger("audit")


class WebRequest:
    """
    Class for creating and carrying out requests to JSON REST services
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def do_request(self, endpoint, method, data):
        """
        Makes the request to specified endpoint. Returns parsed JSON object on success. Raises exceptions on error.
        """
        try:
            response = requests.request(method, self.base_url + endpoint, data=data, timeout=15)
            parsed = json.loads(response.text)
            if parsed.success == 'false':
                raise Exception(u"Unsuccessful request: {0}".format(parsed.message))
            return parsed
        except Exception as e:
            AUDIT_LOG.warning(u"There was a TNL connection error: {0}.".format(e))
            raise
