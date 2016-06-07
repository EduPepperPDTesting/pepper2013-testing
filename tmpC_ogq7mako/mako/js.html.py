# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229152.425179
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/djangoapps/pipeline_mako/templates/mako/js.html'
_template_uri = 'mako/js.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        url = context.get('url', UNDEFINED)
        async = context.get('async', UNDEFINED)
        type = context.get('type', UNDEFINED)
        defer = context.get('defer', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<script ')
        # SOURCE LINE 2
        if async:
            # SOURCE LINE 3
            __M_writer(u'async ')
        # SOURCE LINE 5
        if defer:
            # SOURCE LINE 6
            __M_writer(u'defer ')
        # SOURCE LINE 8
        __M_writer(u'type="')
        __M_writer(filters.decode.utf8(type))
        __M_writer(u'" src="')
        __M_writer(filters.decode.utf8( url ))
        __M_writer(u'" charset="utf-8"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


