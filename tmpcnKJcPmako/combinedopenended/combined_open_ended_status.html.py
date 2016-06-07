# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229959.671521
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/combinedopenended/combined_open_ended_status.html'
_template_uri = 'combinedopenended/combined_open_ended_status.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        xrange = context.get('xrange', UNDEFINED)
        len = context.get('len', UNDEFINED)
        status_list = context.get('status_list', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<div class="status-elements">\n    <section id="combined-open-ended-status" class="combined-open-ended-status">\n')
        # SOURCE LINE 4
        for i in xrange(0,len(status_list)):
            # SOURCE LINE 5
            __M_writer(u'            ')
            status=status_list[i]
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['status'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            # SOURCE LINE 6
            if status['current']:
                # SOURCE LINE 7
                __M_writer(u'                <div class="statusitem statusitem-current" data-status-number="')
                __M_writer(filters.decode.utf8(i))
                __M_writer(u'">\n')
                # SOURCE LINE 8
            else:
                # SOURCE LINE 9
                __M_writer(u'                <div class="statusitem" data-status-number="')
                __M_writer(filters.decode.utf8(i))
                __M_writer(u'">\n')
            # SOURCE LINE 11
            __M_writer(u'           \t')
            __M_writer(filters.decode.utf8(status['human_task']))
            __M_writer(u'\n            </div>\n')
        # SOURCE LINE 14
        __M_writer(u'    </section>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


