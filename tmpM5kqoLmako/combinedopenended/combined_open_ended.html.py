# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223123.116711
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/combinedopenended/combined_open_ended.html'
_template_uri = 'combinedopenended/combined_open_ended.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        status = context.get('status', UNDEFINED)
        task_number = context.get('task_number', UNDEFINED)
        display_name = context.get('display_name', UNDEFINED)
        weight = context.get('weight', UNDEFINED)
        accept_file_upload = context.get('accept_file_upload', UNDEFINED)
        items = context.get('items', UNDEFINED)
        allow_reset = context.get('allow_reset', UNDEFINED)
        state = context.get('state', UNDEFINED)
        score = context.get('score', UNDEFINED)
        location = context.get('location', UNDEFINED)
        ajax_url = context.get('ajax_url', UNDEFINED)
        task_count = context.get('task_count', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<section id="combined-open-ended" class="combined-open-ended" data-location="')
        # SOURCE LINE 2
        __M_writer(filters.decode.utf8(location))
        __M_writer(u'" data-ajax-url="')
        __M_writer(filters.decode.utf8(ajax_url))
        __M_writer(u'" data-allow_reset="')
        __M_writer(filters.decode.utf8(allow_reset))
        __M_writer(u'" data-state="')
        __M_writer(filters.decode.utf8(state))
        __M_writer(u'" data-task-count="')
        __M_writer(filters.decode.utf8(task_count))
        __M_writer(u'" data-task-number="')
        __M_writer(filters.decode.utf8(task_number))
        __M_writer(u'" data-accept-file-upload = "')
        __M_writer(filters.decode.utf8(accept_file_upload))
        __M_writer(u'" data-score="')
        __M_writer(filters.decode.utf8(score))
        __M_writer(u'" data-weight="')
        __M_writer(filters.decode.utf8(weight))
        __M_writer(u'">\n    <div class="name">\n        <!--@begin:delete display_name-->\n        <!--@date:2013-11-02-->\n        <!--<h2>')
        # SOURCE LINE 6
        __M_writer(filters.decode.utf8(display_name))
        __M_writer(u'</h2>-->\n        <!--@end-->\n        <div class="progress-container">\n        </div>\n    </div>\n    <div class="problemwrapper">\n        <div class="status-bar">\n            <table class="statustable">\n                <tr>\n                    <td class="problemtype-container">\n                        <!--@begin:add display_name-->\n                        <!--@date:2013-11-02-->\n                         <div class="problemtype" style="width:100%;word-wrap:break-word;overflow:hidden;">\n                            ')
        # SOURCE LINE 19
        __M_writer(filters.decode.utf8(display_name))
        __M_writer(u'\n                        </div>\n                        <!--@end-->\n\n                    </td>\n                    <td class="assessments-container">\n                        <!--@begin:delete Assessments-->\n                        <!--@date:2013-11-02-->\n                        <!--\n                        <div class="assessment-text">\n                            ')
        # SOURCE LINE 29
        __M_writer(filters.decode.utf8(_("Assessments:")))
        __M_writer(u'\n                        </div>\n                        <div class="status-container">\n                            ')
        # SOURCE LINE 32
        __M_writer(status)
        __M_writer(u'\n                        </div>\n                        -->\n                        <!--@end-->\n                    </td>\n                </tr>\n            </table>\n        </div>\n\n        <div class="item-container">\n            <div class="visibility-control visibility-control-prompt">\n                <!--@begin:delete Prompt-->\n                <!--@date:2013-11-02-->\n                <!--\n                <div class="inner">\n                </div>\n                <a href="" class="section-header section-header-prompt question-header">')
        # SOURCE LINE 48
        __M_writer(filters.decode.utf8(_("Hide Prompt")))
        __M_writer(u'</a>-->\n                <!--@end-->\n                <a href="" class="section-header section-header-prompt question-header"></a>\n            </div>\n            <div class="problem-container">\n')
        # SOURCE LINE 53
        for item in items:
            # SOURCE LINE 54
            __M_writer(u'                <div class="item">')
            __M_writer(item['content'] )
            __M_writer(u'</div>\n')
        # SOURCE LINE 56
        __M_writer(u'            </div>\n            <div class="oe-tools response-tools">\n                <span class="oe-tools-label"></span>\n                <!--@begin:Modify Text-->\n                <!--@date:2013-11-02-->\n                <input type="button" value="')
        # SOURCE LINE 61
        __M_writer(filters.decode.utf8(_('Edit')))
        __M_writer(u'" class="reset-button" name="reset"/>\n                <!--@end-->\n            </div>\n        </div>\n\n        <div class="combined-rubric-container">\n        </div>\n        <div class="oe-tools problem-tools">\n                <!--<span class="oe-tools-label">Once you have completed this form of assessment, you may continue.  </span>-->\n                <input type="button" value="')
        # SOURCE LINE 70
        __M_writer(filters.decode.utf8(_('Next Step')))
        __M_writer(u'" class="next-step-button" name="reset"/>\n        </div>\n\n        <section class="legend-container">\n        </section>\n\n        <div class="result-container">\n        </div>\n    </div>\n\n</section>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


