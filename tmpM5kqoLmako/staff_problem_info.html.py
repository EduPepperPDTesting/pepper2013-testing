# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223123.015945
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/staff_problem_info.html'
_template_uri = 'staff_problem_info.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        category = context.get('category', UNDEFINED)
        settings = context.get('settings', UNDEFINED)
        xqa_key = context.get('xqa_key', UNDEFINED)
        histogram = context.get('histogram', UNDEFINED)
        is_released = context.get('is_released', UNDEFINED)
        xml_attributes = context.get('xml_attributes', UNDEFINED)
        location = context.get('location', UNDEFINED)
        fields = context.get('fields', UNDEFINED)
        module_content = context.get('module_content', UNDEFINED)
        element_id = context.get('element_id', UNDEFINED)
        render_histogram = context.get('render_histogram', UNDEFINED)
        edit_link = context.get('edit_link', UNDEFINED)
        user = context.get('user', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(module_content))
        __M_writer(u'\n')
        # SOURCE LINE 5
        if location.category in ['problem','video','html','combinedopenended','graphical_slider_tool']:
            # SOURCE LINE 6
            if edit_link:
                # SOURCE LINE 7
                __M_writer(u'<div>\n    <a href="')
                # SOURCE LINE 8
                __M_writer(filters.decode.utf8(edit_link))
                __M_writer(u'">Edit</a>\n')
                # SOURCE LINE 9
                if xqa_key:
                    # SOURCE LINE 10
                    __M_writer(u'        / <a href="#')
                    __M_writer(filters.decode.utf8(element_id))
                    __M_writer(u'_xqa-modal" onclick="javascript:getlog(\'')
                    __M_writer(filters.decode.utf8(element_id))
                    __M_writer(u"', {\n        'location': '")
                    # SOURCE LINE 11
                    __M_writer(filters.decode.utf8(location))
                    __M_writer(u"',\n        'xqa_key': '")
                    # SOURCE LINE 12
                    __M_writer(filters.decode.utf8(xqa_key))
                    __M_writer(u"',\n        'category': '")
                    # SOURCE LINE 13
                    __M_writer(filters.decode.utf8(category))
                    __M_writer(u"',\n        'user': '")
                    # SOURCE LINE 14
                    __M_writer(filters.decode.utf8(user))
                    __M_writer(u'\'\n     })" id="')
                    # SOURCE LINE 15
                    __M_writer(filters.decode.utf8(element_id))
                    __M_writer(u'_xqa_log">QA</a>\n')
                # SOURCE LINE 17
                __M_writer(u'</div>\n')
            # SOURCE LINE 19
            __M_writer(u'<div><a href="#')
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_debug" id="')
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_trig">')
            __M_writer(filters.decode.utf8(_("Staff Debug Info")))
            __M_writer(u'</a></div>\n\n')
            # SOURCE LINE 21
            if settings.MITX_FEATURES.get('ENABLE_STUDENT_HISTORY_VIEW') and \
      location.category == 'problem':
                # SOURCE LINE 23
                __M_writer(u'<div><a href="#')
                __M_writer(filters.decode.utf8(element_id))
                __M_writer(u'_history" id="')
                __M_writer(filters.decode.utf8(element_id))
                __M_writer(u'_history_trig">')
                __M_writer(filters.decode.utf8(_("Submission history")))
                __M_writer(u'</a></div>\n')
            # SOURCE LINE 25
            __M_writer(u'\n<section id="')
            # SOURCE LINE 26
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_xqa-modal" class="modal xqa-modal" style="width:80%; left:20%; height:80%; overflow:auto" >\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
            # SOURCE LINE 29
            __M_writer(filters.decode.utf8(_("{platform_name} Content Quality Assessment").format(platform_name=settings.PLATFORM_NAME)))
            __M_writer(u'</h2>\n    </header>\n\n    <form id="')
            # SOURCE LINE 32
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_xqa_form" class="xqa_form">\n      <label>')
            # SOURCE LINE 33
            __M_writer(filters.decode.utf8(_("Comment")))
            __M_writer(u'</label>\n      <input id="')
            # SOURCE LINE 34
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_xqa_entry" type="text" placeholder="')
            __M_writer(filters.decode.utf8(_('comment')))
            __M_writer(u'">\n      <label>')
            # SOURCE LINE 35
            __M_writer(filters.decode.utf8(_("Tag")))
            __M_writer(u'</label>\n      <span style="color:black;vertical-align: -10pt">')
            # SOURCE LINE 36
            __M_writer(filters.decode.utf8(_('Optional tag (eg "done" or "broken"):&nbsp; ')))
            __M_writer(u'      </span>\n      <input id="')
            # SOURCE LINE 37
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_xqa_tag" type="text" placeholder="')
            __M_writer(filters.decode.utf8(_('tag')))
            __M_writer(u'" style="width:80px;display:inline">\n      <div class="submit">\n        <button name="submit" type="submit">')
            # SOURCE LINE 39
            __M_writer(filters.decode.utf8(_('Add comment')))
            __M_writer(u'</button>\n      </div>\n      <hr>\n      <div id="')
            # SOURCE LINE 42
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_xqa_log_data"></div>\n    </form>\n\n  </div>\n</section>\n\n<section class="modal staff-modal" id="')
            # SOURCE LINE 48
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_debug" style="width:80%; left:20%; height:80%; overflow:auto;" >\n  <div class="inner-wrapper" style="color:black">\n    <header>\n      <h2>')
            # SOURCE LINE 51
            __M_writer(filters.decode.utf8(_('Staff Debug')))
            __M_writer(u'</h2>\n    </header>\n    <div class="staff_info" style="display:block">\nis_released = ')
            # SOURCE LINE 54
            __M_writer(filters.decode.utf8(is_released))
            __M_writer(u'\nlocation = ')
            # SOURCE LINE 55
            __M_writer(filters.html_escape(filters.decode.utf8(location )))
            __M_writer(u'\n<table>\n  <tr><th>')
            # SOURCE LINE 57
            __M_writer(filters.decode.utf8(_('Module Fields')))
            __M_writer(u'</th></tr>\n')
            # SOURCE LINE 58
            for name, field in fields:
                # SOURCE LINE 59
                __M_writer(u'  <tr><td>')
                __M_writer(filters.decode.utf8(name))
                __M_writer(u'</td><td><pre style="display:inline-block; margin: 0;">')
                __M_writer(filters.html_escape(filters.decode.utf8(field )))
                __M_writer(u'</pre></td></tr>\n')
            # SOURCE LINE 61
            __M_writer(u'</table>\n<table>\n  <tr><th>')
            # SOURCE LINE 63
            __M_writer(filters.decode.utf8(_('XML attributes')))
            __M_writer(u'</th></tr>\n')
            # SOURCE LINE 64
            for name, field in xml_attributes.items():
                # SOURCE LINE 65
                __M_writer(u'  <tr><td>')
                __M_writer(filters.decode.utf8(name))
                __M_writer(u'</td><td><pre style="display:inline-block; margin: 0;">')
                __M_writer(filters.html_escape(filters.decode.utf8(field )))
                __M_writer(u'</pre></td></tr>\n')
            # SOURCE LINE 67
            __M_writer(u'</table>\ncategory = ')
            # SOURCE LINE 68
            __M_writer(filters.html_escape(filters.decode.utf8(category )))
            __M_writer(u'\n    </div>\n')
            # SOURCE LINE 70
            if render_histogram:
                # SOURCE LINE 71
                __M_writer(u'    <div id="histogram_')
                __M_writer(filters.decode.utf8(element_id))
                __M_writer(u'" class="histogram" data-histogram="')
                __M_writer(filters.decode.utf8(histogram))
                __M_writer(u'"></div>\n')
            # SOURCE LINE 73
            __M_writer(u'  </div>\n</section>\n\n<section class="modal history-modal" id="')
            # SOURCE LINE 76
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_history" style="width:80%; left:20%; height:80%; overflow:auto;" >\n  <div class="inner-wrapper" style="color:black">\n    <header>\n      <h2>')
            # SOURCE LINE 79
            __M_writer(filters.decode.utf8(_("Submission History Viewer")))
            __M_writer(u'</h2>\n    </header>\n    <form id="')
            # SOURCE LINE 81
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_history_form">\n      <label for="')
            # SOURCE LINE 82
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_history_student_username">')
            __M_writer(filters.decode.utf8(_("User:")))
            __M_writer(u'</label>\n      <input id="')
            # SOURCE LINE 83
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_history_student_username" type="text" placeholder=""/>\n      <input type="hidden" id="')
            # SOURCE LINE 84
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_history_location" value="')
            __M_writer(filters.decode.utf8(location))
            __M_writer(u'"/>\n      <div class="submit">\n        <button name="submit" type="submit">')
            # SOURCE LINE 86
            __M_writer(filters.decode.utf8(_("View History")))
            __M_writer(u'</button>\n      </div>\n    </form>\n\n    <div id="')
            # SOURCE LINE 90
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_history_text" class="staff_info" style="display:block">\n    </div>\n  </div>\n</section>\n\n<div id="')
            # SOURCE LINE 95
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u'_setup"></div>\n\n<script type="text/javascript">\n// assumes courseware.html\'s loaded this method.\n$(function () {\n    setup_debug(\'')
            # SOURCE LINE 100
            __M_writer(filters.decode.utf8(element_id))
            __M_writer(u"',\n")
            # SOURCE LINE 101
            if edit_link:
                # SOURCE LINE 102
                __M_writer(u"        '")
                __M_writer(filters.decode.utf8(edit_link))
                __M_writer(u"',\n")
                # SOURCE LINE 103
            else:
                # SOURCE LINE 104
                __M_writer(u'        null,\n')
            # SOURCE LINE 106
            __M_writer(u"        {\n            'location': '")
            # SOURCE LINE 107
            __M_writer(filters.decode.utf8(location))
            __M_writer(u"',\n            'xqa_key': '")
            # SOURCE LINE 108
            __M_writer(filters.decode.utf8(xqa_key))
            __M_writer(u"',\n            'category': '")
            # SOURCE LINE 109
            __M_writer(filters.decode.utf8(category))
            __M_writer(u"',\n            'user': '")
            # SOURCE LINE 110
            __M_writer(filters.decode.utf8(user))
            __M_writer(u"'\n        }\n    );\n});\n</script>\n")
        # SOURCE LINE 116
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


