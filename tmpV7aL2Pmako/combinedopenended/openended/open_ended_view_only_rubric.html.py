# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224883.360318
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/combinedopenended/openended/open_ended_view_only_rubric.html'
_template_uri = 'combinedopenended/openended/open_ended_view_only_rubric.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        range = context.get('range', UNDEFINED)
        len = context.get('len', UNDEFINED)
        categories = context.get('categories', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<div class="rubric">\n')
        # SOURCE LINE 2
        for i in range(len(categories)):
            # SOURCE LINE 3
            __M_writer(u'    ')
            category = categories[i] 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['category'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            # SOURCE LINE 4
            for j in range(len(category['options'])):
                # SOURCE LINE 5
                __M_writer(u'            ')
                option = category['options'][j] 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['option'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\n')
                # SOURCE LINE 6
                if option['selected']:
                    # SOURCE LINE 7
                    __M_writer(u'               ')
                    __M_writer(filters.decode.utf8(category['description']))
                    __M_writer(u' : ')
                    __M_writer(filters.decode.utf8(option['points']))
                    __M_writer(u' |\n')
        # SOURCE LINE 11
        __M_writer(u'</div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


