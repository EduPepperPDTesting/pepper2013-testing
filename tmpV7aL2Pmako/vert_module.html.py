# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224104.502667
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/vert_module.html'
_template_uri = 'vert_module.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        items = context.get('items', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<ol class="vert-mod">\n')
        # SOURCE LINE 2
        for idx, item in enumerate(items):
            # SOURCE LINE 3
            __M_writer(u'  <li id="vert-')
            __M_writer(filters.decode.utf8(idx))
            __M_writer(u'" data-id="')
            __M_writer(filters.decode.utf8(item['id']))
            __M_writer(u'">\n    ')
            # SOURCE LINE 4
            __M_writer(filters.decode.utf8(item['content']))
            __M_writer(u'\n  </li>\n')
        # SOURCE LINE 7
        __M_writer(u'</ol>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


