from saml2 import BINDING_HTTP_REDIRECT
from saml2 import BINDING_HTTP_POST

from django.http import HttpResponse, HttpResponseRedirect


def saml_django_response(binding, http_args):
    if binding == BINDING_HTTP_POST:
        resp = "\n".join(http_args["data"])
        resp = resp.replace("<body>", "<body style='display:none'>")
        return HttpResponse("%s" % resp)
    elif binding == BINDING_HTTP_REDIRECT:
        return HttpResponseRedirect(http_args["headers"][0][1])
