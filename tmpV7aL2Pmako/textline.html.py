# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465227908.254754
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/lib/capa/capa/templates/textline.html'
_template_uri = 'textline.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        status = context.get('status', UNDEFINED)
        value = context.get('value', UNDEFINED)
        edu_show_me_id = context.get('edu_show_me_id', UNDEFINED)
        trailing_text = context.get('trailing_text', UNDEFINED)
        preprocessor = context.get('preprocessor', UNDEFINED)
        msg = context.get('msg', UNDEFINED)
        inline = context.get('inline', UNDEFINED)
        hidden = context.get('hidden', UNDEFINED)
        size = context.get('size', UNDEFINED)
        id = context.get('id', UNDEFINED)
        do_math = context.get('do_math', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        doinline = "inline" if inline else "" 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['doinline'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n<section id="inputtype_')
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" class="')
        __M_writer(filters.decode.utf8('text-input-dynamath' if do_math else ''))
        __M_writer(u' capa_inputtype ')
        __M_writer(filters.decode.utf8(doinline))
        __M_writer(u' textline" >\n\n')
        # SOURCE LINE 5
        if preprocessor is not None:
            # SOURCE LINE 6
            __M_writer(u'    <div class="text-input-dynamath_data" data-preprocessor="')
            __M_writer(filters.decode.utf8(preprocessor['class_name']))
            __M_writer(u'"/>\n    <div class="script_placeholder" data-src="')
            # SOURCE LINE 7
            __M_writer(filters.decode.utf8(preprocessor['script_src']))
            __M_writer(u'"/>\n')
        # SOURCE LINE 9
        __M_writer(u'\n')
        # SOURCE LINE 10
        if status == 'unsubmitted':
            # SOURCE LINE 11
            __M_writer(u'    <div class="unanswered ')
            __M_writer(filters.decode.utf8(doinline))
            __M_writer(u'" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'" edu_show_me_id="')
            __M_writer(filters.decode.utf8(edu_show_me_id))
            __M_writer(u'">\n')
            # SOURCE LINE 12
        elif status == 'correct':
            # SOURCE LINE 13
            __M_writer(u'    <div class="correct ')
            __M_writer(filters.decode.utf8(doinline))
            __M_writer(u'" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'" edu_show_me_id="')
            __M_writer(filters.decode.utf8(edu_show_me_id))
            __M_writer(u'">\n')
            # SOURCE LINE 14
        elif status == 'incorrect':
            # SOURCE LINE 15
            __M_writer(u'    <div class="incorrect ')
            __M_writer(filters.decode.utf8(doinline))
            __M_writer(u'" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'" edu_show_me_id="')
            __M_writer(filters.decode.utf8(edu_show_me_id))
            __M_writer(u'">\n')
            # SOURCE LINE 16
        elif status == 'incomplete':
            # SOURCE LINE 17
            __M_writer(u'    <div class="incorrect ')
            __M_writer(filters.decode.utf8(doinline))
            __M_writer(u'" id="status_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'" edu_show_me_id="')
            __M_writer(filters.decode.utf8(edu_show_me_id))
            __M_writer(u'">\n')
        # SOURCE LINE 19
        if hidden:
            # SOURCE LINE 20
            __M_writer(u'      <div style="display:none;" name="')
            __M_writer(filters.decode.utf8(hidden))
            __M_writer(u'" inputid="input_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'" edu_show_me_id="')
            __M_writer(filters.decode.utf8(edu_show_me_id))
            __M_writer(u'" />\n')
        # SOURCE LINE 22
        __M_writer(u'\n  <input type="text" name="input_')
        # SOURCE LINE 23
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" id="input_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" aria-describedby="answer_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" value="')
        __M_writer(filters.html_escape(filters.decode.utf8(value)))
        __M_writer(u'"\n')
        # SOURCE LINE 24
        if do_math:
            # SOURCE LINE 25
            __M_writer(u'            class="math"\n')
        # SOURCE LINE 27
        if size:
            # SOURCE LINE 28
            __M_writer(u'            size="')
            __M_writer(filters.decode.utf8(size))
            __M_writer(u'"\n')
        # SOURCE LINE 30
        if hidden:
            # SOURCE LINE 31
            __M_writer(u'            style="display:none;"\n')
        # SOURCE LINE 33
        __M_writer(u'   />\n   ')
        # SOURCE LINE 34
        __M_writer(filters.html_escape(filters.decode.utf8(trailing_text )))
        __M_writer(u'\n\n      <p class="status" aria-describedby="input_')
        # SOURCE LINE 36
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'">\n')
        # SOURCE LINE 37
        if status == 'unsubmitted':
            # SOURCE LINE 38
            __M_writer(u'        unanswered\n')
            # SOURCE LINE 39
        elif status == 'correct':
            # SOURCE LINE 40
            __M_writer(u'        correct\n')
            # SOURCE LINE 41
        elif status == 'incorrect':
            # SOURCE LINE 42
            __M_writer(u'        incorrect\n')
            # SOURCE LINE 43
        elif status == 'incomplete':
            # SOURCE LINE 44
            __M_writer(u'        incomplete\n')
        # SOURCE LINE 46
        __M_writer(u'      </p>\n\n      <p id="answer_')
        # SOURCE LINE 48
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" class="answer"></p>\n\n')
        # SOURCE LINE 50
        if do_math:
            # SOURCE LINE 51
            __M_writer(u'      <div id="display_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'" class="equation">`{::}`</div>\n      <textarea style="display:none" id="input_')
            # SOURCE LINE 52
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'_dynamath" name="input_')
            __M_writer(filters.decode.utf8(id))
            __M_writer(u'_dynamath">\n      </textarea>\n\n')
        # SOURCE LINE 56
        __M_writer(u'\n')
        # SOURCE LINE 57
        if status in ['unsubmitted', 'correct', 'incorrect', 'incomplete']:
            # SOURCE LINE 58
            __M_writer(u'</div>\n')
        # SOURCE LINE 60
        __M_writer(u'\n')
        # SOURCE LINE 61
        if msg:
            # SOURCE LINE 62
            __M_writer(u'      <span class="message">')
            __M_writer(msg)
            __M_writer(u'</span>\n')
        # SOURCE LINE 64
        __M_writer(u'\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


