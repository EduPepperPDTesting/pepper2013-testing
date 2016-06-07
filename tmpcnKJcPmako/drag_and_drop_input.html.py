# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465230191.429102
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/lib/capa/capa/templates/drag_and_drop_input.html'
_template_uri = 'drag_and_drop_input.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        status = context.get('status', UNDEFINED)
        msg = context.get('msg', UNDEFINED)
        id = context.get('id', UNDEFINED)
        value = context.get('value', UNDEFINED)
        drag_and_drop_json = context.get('drag_and_drop_json', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<section id="inputtype_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" class="capa_inputtype" >\n    <div class="drag_and_drop_problem_div" id="drag_and_drop_div_')
        # SOURCE LINE 2
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"\n     data-plain-id="')
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'">\n    </div>\n\n    <div class="drag_and_drop_problem_json" id="drag_and_drop_json_')
        # SOURCE LINE 6
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"\n        style="display:none;">')
        # SOURCE LINE 7
        __M_writer(filters.decode.utf8(drag_and_drop_json))
        __M_writer(u'</div>\n\n    <div class="script_placeholder" data-src="/static/js/capa/drag_and_drop.js"></div>\n\n')
        # SOURCE LINE 11
        if status == 'unsubmitted':
            # SOURCE LINE 12
            __M_writer(u'        <div class="unanswered" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'">\n')
            # SOURCE LINE 13
        elif status == 'correct':
            # SOURCE LINE 14
            __M_writer(u'        <div class="correct" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'">\n')
            # SOURCE LINE 15
        elif status == 'incorrect':
            # SOURCE LINE 16
            __M_writer(u'        <div class="incorrect" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'">\n')
            # SOURCE LINE 17
        elif status == 'incomplete':
            # SOURCE LINE 18
            __M_writer(u'        <div class="incorrect" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'">\n')
        # SOURCE LINE 20
        __M_writer(u'\n\n    <input type="text" name="input_')
        # SOURCE LINE 22
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" id="input_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" aria-describedby="answer_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" value="')
        __M_writer(filters.html_escape(filters.decode.utf8(value)))
        __M_writer(u'"\n    style="display:none;"/>\n\n    <p class="status" aria-describedby="input_')
        # SOURCE LINE 25
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'">\n')
        # SOURCE LINE 26
        if status == 'unsubmitted':
            # SOURCE LINE 27
            __M_writer(u'        unanswered\n')
            # SOURCE LINE 28
        elif status == 'correct':
            # SOURCE LINE 29
            __M_writer(u'        correct\n')
            # SOURCE LINE 30
        elif status == 'incorrect':
            # SOURCE LINE 31
            __M_writer(u'        incorrect\n')
            # SOURCE LINE 32
        elif status == 'incomplete':
            # SOURCE LINE 33
            __M_writer(u'        incomplete\n')
        # SOURCE LINE 35
        __M_writer(u'    </p>\n\n    <p id="answer_')
        # SOURCE LINE 37
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" class="answer"></p>\n\n')
        # SOURCE LINE 39
        if msg:
            # SOURCE LINE 40
            __M_writer(u'        <span class="message">')
            __M_writer(msg)
            __M_writer(u'</span>\n')
        # SOURCE LINE 42
        __M_writer(u'\n')
        # SOURCE LINE 43
        if status in ['unsubmitted', 'correct', 'incorrect', 'incomplete']:
            # SOURCE LINE 44
            __M_writer(u'        </div>\n')
        # SOURCE LINE 46
        __M_writer(u'</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


