# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223109.956205
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/discussion/_js_body_dependencies.html'
_template_uri = u'courseware/../discussion/_js_body_dependencies.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django_comment_client.helpers import include_mustache_templates 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        runtime._include_file(context, u'/mathjax_include.html', _template_uri)
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(include_mustache_templates()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


