# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224883.371381
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/combinedopenended/openended/open_ended_rubric.html'
_template_uri = 'combinedopenended/openended/open_ended_rubric.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        len = context.get('len', UNDEFINED)
        range = context.get('range', UNDEFINED)
        id = context.get('id', UNDEFINED)
        categories = context.get('categories', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        # SOURCE LINE 2
        from random import randint 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['randint'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<form class="rubric-template" id="inputtype_')
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" xmlns="http://www.w3.org/1999/html">\n    <div class="visibility-control visibility-control-rubric">\n        <!--@begin:delete section-header-rubric-->\n        <!--@date:2013-11-02-->\n        <!--<div class="inner">\n        </div>\n        <span class="section-header section-header-rubric">')
        # SOURCE LINE 9
        __M_writer(filters.decode.utf8(_("Rubric")))
        __M_writer(u'</span>\n        -->\n        <!--@end-->\n    </div>\n    <!--@begin:delete info-->\n    <!--@date:2013-11-02-->\n    <!--<p>Select the criteria you feel best represents this submission in each category.</p>-->\n    <!--@end-->\n    <div class="rubric">\n')
        # SOURCE LINE 18
        for i in range(len(categories)):
            # SOURCE LINE 19
            __M_writer(u'        ')
            category = categories[i] 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['category'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n        ')
            # SOURCE LINE 20
            m = randint(0,1000) 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['m'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n            <span class="rubric-category">')
            # SOURCE LINE 21
            __M_writer(filters.decode.utf8(category['description']))
            __M_writer(u'</span>\n            <ul class="rubric-list">\n')
            # SOURCE LINE 23
            for j in range(len(category['options'])):
                # SOURCE LINE 24
                __M_writer(u'                ')
                option = category['options'][j] 
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['option'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\n')
                # SOURCE LINE 25
                if option['selected']:
                    # SOURCE LINE 26
                    __M_writer(u'                        <li class="selected-grade rubric-list-item">\n')
                    # SOURCE LINE 27
                else:
                    # SOURCE LINE 28
                    __M_writer(u'                        <li class="rubric-list-item">\n')
                # SOURCE LINE 30
                __M_writer(u'                    <label class="rubric-label" for="score-')
                __M_writer(filters.decode.utf8(i))
                __M_writer(u'-')
                __M_writer(filters.decode.utf8(j))
                __M_writer(u'-')
                __M_writer(filters.decode.utf8(m))
                __M_writer(u'">\n                        <span class="wrapper-score-selection"><input type="radio" class="score-selection" data-category="')
                # SOURCE LINE 31
                __M_writer(filters.decode.utf8(i))
                __M_writer(u'" name="score-selection-')
                __M_writer(filters.decode.utf8(i))
                __M_writer(u'" id="score-')
                __M_writer(filters.decode.utf8(i))
                __M_writer(u'-')
                __M_writer(filters.decode.utf8(j))
                __M_writer(u'-')
                __M_writer(filters.decode.utf8(m))
                __M_writer(u'" value="')
                __M_writer(filters.decode.utf8(option['points']))
                __M_writer(u'"/></span>\n                        <span class="wrappable">')
                # SOURCE LINE 32
                __M_writer(filters.decode.utf8(option['text']))
                __M_writer(u'</span>\n                    </label>\n                    </li>\n')
            # SOURCE LINE 36
            __M_writer(u'            </ul>\n')
        # SOURCE LINE 38
        __M_writer(u'    </div>\n</form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


