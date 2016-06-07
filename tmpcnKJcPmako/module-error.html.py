# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465231028.585305
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/module-error.html'
_template_uri = 'module-error.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        error = context.get('error', UNDEFINED)
        data = context.get('data', UNDEFINED)
        settings = context.get('settings', UNDEFINED)
        staff_access = context.get('staff_access', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<section class="outside-app">\n  <h1>')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(_("There has been an error on the <em>{platform_name}</em> servers").format(platform_name=settings.PLATFORM_NAME)))
        __M_writer(u'</h1>\n  <p>')
        # SOURCE LINE 5
        __M_writer(filters.decode.utf8(_("We're sorry, this module is temporarily unavailable. Our staff is working to fix it as soon as possible. Please email us at <a href=\"mailto:{tech_support_email}\">{tech_support_email}</a> to report any problems or downtime.").format(platform_name=settings.PLATFORM_NAME, tech_support_email=settings.TECH_SUPPORT_EMAIL)))
        __M_writer(u'</p>\n\n')
        # SOURCE LINE 7
        if staff_access:
            # SOURCE LINE 8
            __M_writer(u'<h1>')
            __M_writer(filters.decode.utf8(_("Details")))
            __M_writer(u'</h1>\n\n<p>')
            # SOURCE LINE 10
            __M_writer(filters.decode.utf8(_("Error:")))
            __M_writer(u'\n<pre>\n')
            # SOURCE LINE 12
            __M_writer(filters.html_escape(filters.decode.utf8(error )))
            __M_writer(u'\n</pre>\n</p>\n\n<p>')
            # SOURCE LINE 16
            __M_writer(filters.decode.utf8(_("Raw data:")))
            __M_writer(u'\n\n<pre>')
            # SOURCE LINE 18
            __M_writer(filters.html_escape(filters.decode.utf8(data )))
            __M_writer(u'</pre>\n</p>\n\n')
        # SOURCE LINE 22
        __M_writer(u'</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


