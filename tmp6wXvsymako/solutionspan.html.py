# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223005.511093
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/lib/capa/capa/templates/solutionspan.html'
_template_uri = 'solutionspan.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        id = context.get('id', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<section class="solution-span">\n <span id="solution_')
        # SOURCE LINE 2
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"></span>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


