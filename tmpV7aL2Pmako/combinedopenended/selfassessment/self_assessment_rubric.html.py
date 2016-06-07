# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224883.375893
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/combinedopenended/selfassessment/self_assessment_rubric.html'
_template_uri = 'combinedopenended/selfassessment/self_assessment_rubric.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        rubric = context.get('rubric', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<div class="assessment-container">\n    <div class="rubric">\n    ')
        # SOURCE LINE 3
        __M_writer(rubric )
        __M_writer(u'\n    </div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


