# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465226521.216896
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/lib/capa/capa/templates/choicegroup.html'
_template_uri = 'choicegroup.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        status = context.get('status', UNDEFINED)
        basestring = context.get('basestring', UNDEFINED)
        isinstance = context.get('isinstance', UNDEFINED)
        int = context.get('int', UNDEFINED)
        input_type = context.get('input_type', UNDEFINED)
        value = context.get('value', UNDEFINED)
        choices = context.get('choices', UNDEFINED)
        submitted_message = context.get('submitted_message', UNDEFINED)
        msg = context.get('msg', UNDEFINED)
        show_correctness = context.get('show_correctness', UNDEFINED)
        answer_column_num = context.get('answer_column_num', UNDEFINED)
        name_array_suffix = context.get('name_array_suffix', UNDEFINED)
        id = context.get('id', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<form class="choicegroup capa_inputtype" id="inputtype_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'">\n    <div class="indicator_container">\n')
        # SOURCE LINE 3
        if input_type == 'checkbox' or not value:
            # SOURCE LINE 4
            if status == 'unsubmitted' or show_correctness == 'never':
                # SOURCE LINE 5
                __M_writer(u'        <span class="unanswered" style="display:inline-block;" id="status_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'"></span>\n')
                # SOURCE LINE 6
            elif status == 'correct':
                # SOURCE LINE 7
                __M_writer(u'        <span class="correct" id="status_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'"><span class="sr">Status: correct</span></span>\n')
                # SOURCE LINE 8
            elif status == 'incorrect':
                # SOURCE LINE 9
                __M_writer(u'        <span class="incorrect" id="status_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'"><span class="sr">Status: incorrect</span></span>\n')
                # SOURCE LINE 10
            elif status == 'incomplete':
                # SOURCE LINE 11
                __M_writer(u'        <span class="incorrect" id="status_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'"><span class="sr">Status: incomplete</span></span>\n')
        # SOURCE LINE 14
        __M_writer(u'    </div>\n    <fieldset>\n')
        # SOURCE LINE 16
        if answer_column_num is None:
            # SOURCE LINE 17
            for choice_id, choice_description, edu_show_me_id, index in choices:
                # SOURCE LINE 18
                __M_writer(u'            <label for="input_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'_')
                __M_writer(filters.decode.utf8(choice_id))
                __M_writer(u'" edu_show_me_id="')
                __M_writer(filters.decode.utf8(edu_show_me_id))
                __M_writer(u'"\n')
                # SOURCE LINE 20
                if input_type == 'radio' and ( (isinstance(value, basestring) and (choice_id == value))  or  (not isinstance(value, basestring) and choice_id in value) ):
                    # SOURCE LINE 21
                    __M_writer(u'                ')

                    if status == 'correct':
                        correctness = 'correct'
                    elif status == 'incorrect':
                        correctness = 'incorrect'
                    else:
                        correctness = None
                                    
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['correctness'] if __M_key in __M_locals_builtin_stored]))
                    # SOURCE LINE 28
                    __M_writer(u'\n')
                    # SOURCE LINE 29
                    if correctness and not show_correctness=='never':
                        # SOURCE LINE 30
                        __M_writer(u'                class="choicegroup_')
                        __M_writer(filters.decode.utf8(correctness))
                        __M_writer(u'"\n')
                # SOURCE LINE 33
                __M_writer(u'                >\n                <input type="')
                # SOURCE LINE 34
                __M_writer(filters.decode.utf8(input_type))
                __M_writer(u'" name="input_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(filters.decode.utf8(name_array_suffix))
                __M_writer(u'" id="input_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'_')
                __M_writer(filters.decode.utf8(choice_id))
                __M_writer(u'" aria-describedby="answer_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'" value="')
                __M_writer(filters.decode.utf8(choice_id))
                __M_writer(u'"\n')
                # SOURCE LINE 36
                if input_type == 'radio' and ( (isinstance(value, basestring) and (choice_id == value))  or  (not isinstance(value, basestring) and choice_id in value) ):
                    # SOURCE LINE 37
                    __M_writer(u'                checked="true"\n')
                    # SOURCE LINE 38
                elif input_type != 'radio' and choice_id in value:
                    # SOURCE LINE 39
                    __M_writer(u'                checked="true"\n')
                # SOURCE LINE 41
                __M_writer(u'\n                /> ')
                # SOURCE LINE 42
                __M_writer(filters.decode.utf8(choice_description))
                __M_writer(u'\n\n')
                # SOURCE LINE 44
                if input_type == 'radio' and ( (isinstance(value, basestring) and (choice_id == value))  or  (not isinstance(value, basestring) and choice_id in value) ):
                    # SOURCE LINE 45
                    __M_writer(u'                ')

                    if status == 'correct':
                        correctness = 'correct'
                    elif status == 'incorrect':
                        correctness = 'incorrect'
                    else:
                        correctness = None
                                    
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['correctness'] if __M_key in __M_locals_builtin_stored]))
                    # SOURCE LINE 52
                    __M_writer(u'\n')
                    # SOURCE LINE 53
                    if correctness and not show_correctness=='never':
                        # SOURCE LINE 54
                        __M_writer(u'                <span class="sr" aria-describedby="input_')
                        __M_writer(filters.decode.utf8(id))
                        __M_writer(u'_')
                        __M_writer(filters.decode.utf8(choice_id))
                        __M_writer(u'">Status: ')
                        __M_writer(filters.decode.utf8(correctness))
                        __M_writer(u'</span>\n')
                # SOURCE LINE 57
                __M_writer(u'            </label>\n')
            # SOURCE LINE 59
        else:
            # SOURCE LINE 60
            for choice_id, choice_description, edu_show_me_id, index in choices:
                # SOURCE LINE 61
                if index%int(answer_column_num)==0:
                    # SOURCE LINE 62
                    if index>0:
                        # SOURCE LINE 63
                        __M_writer(u'                    </div>\n')
                    # SOURCE LINE 65
                    __M_writer(u'                <div style="float:left;width:auto;margin:10px;">\n')
                # SOURCE LINE 67
                __M_writer(u'                <label for="input_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'_')
                __M_writer(filters.decode.utf8(choice_id))
                __M_writer(u'" edu_show_me_id="')
                __M_writer(filters.decode.utf8(edu_show_me_id))
                __M_writer(u'"\n')
                # SOURCE LINE 69
                if input_type == 'radio' and ( (isinstance(value, basestring) and (choice_id == value))  or  (not isinstance(value, basestring) and choice_id in value) ):
                    # SOURCE LINE 70
                    __M_writer(u'                ')

                    if status == 'correct':
                        correctness = 'correct'
                    elif status == 'incorrect':
                        correctness = 'incorrect'
                    else:
                        correctness = None
                                    
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['correctness'] if __M_key in __M_locals_builtin_stored]))
                    # SOURCE LINE 77
                    __M_writer(u'\n')
                    # SOURCE LINE 78
                    if correctness and not show_correctness=='never':
                        # SOURCE LINE 79
                        __M_writer(u'                class="choicegroup_')
                        __M_writer(filters.decode.utf8(correctness))
                        __M_writer(u'"\n')
                # SOURCE LINE 82
                __M_writer(u'                >\n                <input type="')
                # SOURCE LINE 83
                __M_writer(filters.decode.utf8(input_type))
                __M_writer(u'" name="input_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(filters.decode.utf8(name_array_suffix))
                __M_writer(u'" id="input_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'_')
                __M_writer(filters.decode.utf8(choice_id))
                __M_writer(u'" aria-describedby="answer_')
                __M_writer(filters.decode.utf8(id))
                __M_writer(u'" value="')
                __M_writer(filters.decode.utf8(choice_id))
                __M_writer(u'"\n')
                # SOURCE LINE 85
                if input_type == 'radio' and ( (isinstance(value, basestring) and (choice_id == value))  or  (not isinstance(value, basestring) and choice_id in value) ):
                    # SOURCE LINE 86
                    __M_writer(u'                checked="true"\n')
                    # SOURCE LINE 87
                elif input_type != 'radio' and choice_id in value:
                    # SOURCE LINE 88
                    __M_writer(u'                checked="true"\n')
                # SOURCE LINE 90
                __M_writer(u'\n                /> ')
                # SOURCE LINE 91
                __M_writer(filters.decode.utf8(choice_description))
                __M_writer(u'\n\n')
                # SOURCE LINE 93
                if input_type == 'radio' and ( (isinstance(value, basestring) and (choice_id == value))  or  (not isinstance(value, basestring) and choice_id in value) ):
                    # SOURCE LINE 94
                    __M_writer(u'                ')

                    if status == 'correct':
                        correctness = 'correct'
                    elif status == 'incorrect':
                        correctness = 'incorrect'
                    else:
                        correctness = None
                                    
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['correctness'] if __M_key in __M_locals_builtin_stored]))
                    # SOURCE LINE 101
                    __M_writer(u'\n')
                    # SOURCE LINE 102
                    if correctness and not show_correctness=='never':
                        # SOURCE LINE 103
                        __M_writer(u'                <span class="sr" aria-describedby="input_')
                        __M_writer(filters.decode.utf8(id))
                        __M_writer(u'_')
                        __M_writer(filters.decode.utf8(choice_id))
                        __M_writer(u'">Status: ')
                        __M_writer(filters.decode.utf8(correctness))
                        __M_writer(u'</span>\n')
                # SOURCE LINE 106
                __M_writer(u'                </label>               \n')
            # SOURCE LINE 108
            __M_writer(u'            </div>\n')
        # SOURCE LINE 110
        __M_writer(u'        <span id="answer_')
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"></span>\n    </fieldset>\n\n')
        # SOURCE LINE 113
        if show_correctness == "never" and (value or status not in ['unsubmitted']):
            # SOURCE LINE 114
            __M_writer(u'    <div class="capa_alert">')
            __M_writer(filters.decode.utf8(submitted_message))
            __M_writer(u'</div>\n')
        # SOURCE LINE 116
        __M_writer(u'    <!--@begin:Return the message of multiple choice-->\n    <!--@date:2013-11-02-->\n')
        # SOURCE LINE 118
        if msg:
            # SOURCE LINE 119
            __M_writer(u'      <span class="message">')
            __M_writer(msg)
            __M_writer(u'</span>\n')
        # SOURCE LINE 121
        __M_writer(u'    <!--@end-->\n</form>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


