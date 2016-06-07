# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465230191.444728
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/problem_ajax.html'
_template_uri = 'problem_ajax.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        ajax_url = context.get('ajax_url', UNDEFINED)
        progress_detail = context.get('progress_detail', UNDEFINED)
        element_id = context.get('element_id', UNDEFINED)
        id = context.get('id', UNDEFINED)
        progress_status = context.get('progress_status', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<section id="problem_')
        __M_writer(filters.decode.utf8(element_id))
        __M_writer(u'" class="problems-wrapper" data-problem-id="')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" data-url="')
        __M_writer(filters.decode.utf8(ajax_url))
        __M_writer(u'" data-progress_status="')
        __M_writer(filters.decode.utf8(progress_status))
        __M_writer(u'" data-progress_detail="')
        __M_writer(filters.decode.utf8(progress_detail))
        __M_writer(u'"></section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


