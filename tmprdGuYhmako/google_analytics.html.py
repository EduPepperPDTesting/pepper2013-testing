# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218681.678537
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/google_analytics.html'
_template_uri = u'google_analytics.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<script type="text/javascript">\nvar _gaq = _gaq || [];\n_gaq.push([\'_setAccount\', \'UA-35248639-1\']);\n_gaq.push([\'_trackPageview\']);\n\n(function() {\n  var ga = document.createElement(\'script\'); ga.type = \'text/javascript\'; ga.async = true;\n  ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\n  var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\n})();\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


