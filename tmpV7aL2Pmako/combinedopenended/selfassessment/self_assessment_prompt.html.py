# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224883.380355
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/combinedopenended/selfassessment/self_assessment_prompt.html'
_template_uri = 'combinedopenended/selfassessment/self_assessment_prompt.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        prompt = context.get('prompt', UNDEFINED)
        initial_rubric = context.get('initial_rubric', UNDEFINED)
        child_type = context.get('child_type', UNDEFINED)
        allow_reset = context.get('allow_reset', UNDEFINED)
        state = context.get('state', UNDEFINED)
        previous_answer = context.get('previous_answer', UNDEFINED)
        ajax_url = context.get('ajax_url', UNDEFINED)
        id = context.get('id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<section id="self_assessment_')
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" class="open-ended-child" data-ajax-url="')
        __M_writer(filters.decode.utf8(ajax_url))
        __M_writer(u'"\n         data-id="')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'" data-state="')
        __M_writer(filters.decode.utf8(state))
        __M_writer(u'" data-allow_reset="')
        __M_writer(filters.decode.utf8(allow_reset))
        __M_writer(u'" data-child-type="')
        __M_writer(filters.decode.utf8(child_type))
        __M_writer(u'">\n    <div class="error"></div>\n    <div class="prompt">\n    ')
        # SOURCE LINE 7
        __M_writer(filters.decode.utf8(prompt))
        __M_writer(u'\n    </div>\n    <div class="visibility-control visibility-control-response">\n        <div class="inner">\n        </div>\n        <span class="section-header section-header-response">')
        # SOURCE LINE 12
        __M_writer(filters.decode.utf8(_("Response")))
        __M_writer(u'</span>\n    </div>\n    <div>\n    <!--@begin:textarea editor-add style and class-->\n    <!--@date:2013-11-02-->\n    <textarea  class="answer short-form-response mceEditor" cols="70" mce_editable="true" style="height:200px;">')
        # SOURCE LINE 17
        __M_writer(previous_answer)
        __M_writer(u'</textarea>\n    <!--@end-->\n    <div class="message-wrapper"></div>\n    <div class="file-upload-list"></div>\n    <div class="grader-status"></div>\n\n    <div class="rubric-wrapper">')
        # SOURCE LINE 23
        __M_writer(filters.decode.utf8(initial_rubric))
        __M_writer(u'</div>\n    <!--@begin:ORA-add progress bar, change button names-->\n    <!--@date:2013-11-02-->\n    <div class="file-upload"></div><br/>\n    <div class="ora-loading"><img src="/static/images/ora-loading.gif" ></div><br/>\n    <!--<input type="button" value="')
        # SOURCE LINE 28
        __M_writer(filters.decode.utf8(_('Save without submitting')))
        __M_writer(u'" class="save-button" name="show"/>-->\n    <input type="button" value="')
        # SOURCE LINE 29
        __M_writer(filters.decode.utf8(_('Submit')))
        __M_writer(u'" class="submit-button" name="show"/>\n    <!--@end-->\n    <div class="open-ended-action"></div>\n    <span id="answer_')
        # SOURCE LINE 32
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"></span>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


