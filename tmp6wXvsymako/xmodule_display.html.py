# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223005.372657
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/templates/xmodule_display.html'
_template_uri = 'xmodule_display.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        ajax_url = context.get('ajax_url', UNDEFINED)
        class_ = context.get('class_', UNDEFINED)
        content = context.get('content', UNDEFINED)
        module_name = context.get('module_name', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<section class="xmodule_display xmodule_')
        __M_writer(filters.decode.utf8(class_))
        __M_writer(u'" data-type="')
        __M_writer(filters.decode.utf8(module_name))
        __M_writer(u'" data-url="')
        __M_writer(filters.decode.utf8(ajax_url))
        __M_writer(u'">\n    ')
        # SOURCE LINE 2
        __M_writer(filters.decode.utf8(content))
        __M_writer(u'\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


