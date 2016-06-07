# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218891.818593
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/xqa_interface.html'
_template_uri = u'courseware/xqa_interface.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        xqa_server = context.get('xqa_server', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<script type="text/javascript" src="/static/js/vendor/jquery.leanModal.min.js"></script>\n<script type="text/javascript">\n\nfunction setup_debug(element_id, edit_link, staff_context){\n\t$(\'#\' + element_id + \'_trig\').leanModal(); \n\t$(\'#\' + element_id + \'_xqa_log\').leanModal();\t\t\n\t$(\'#\' + element_id + \'_xqa_form\').submit(function () {sendlog(element_id, edit_link, staff_context);});\n\n\t$("#" + element_id + "_history_trig").leanModal();\n\t\n\t$(\'#\' + element_id + \'_history_form\').submit(\n\t\tfunction () {\n\t\t\tvar username = $("#" + element_id + "_history_student_username").val();\n\t\t\tvar location = $("#" + element_id + "_history_location").val();\n\n\t\t\t// This is a ridiculous way to get the course_id, but I\'m not sure\n\t\t\t// how to do it sensibly from within the staff debug code. \n\t\t\t// staff_problem_info.html is rendered through a wrapper to get_html\n\t\t\t// that\'s injected by the code that adds the histogram -- it\'s all \n\t\t\t// kinda bizarre, and it remains awkward to simply ask "what course\n\t\t\t// is this problem being shown in the context of."\n\t\t\tvar path_parts = window.location.pathname.split(\'/\');\n\t\t\tvar course_id = path_parts[2] + "/" + path_parts[3] + "/" + path_parts[4];\n\t\t\t$("#" + element_id + "_history_text").load(\'/courses/\' + course_id + \n\t\t\t\t"/submission_history/" + username + "/" + location);\n\t\t\treturn false;\n\t\t}\n\t);\n}\n\nfunction sendlog(element_id, edit_link, staff_context){\n\n\tvar xqaLog = {\n\t\t\tauthkey: staff_context.xqa_key,\n\t\t\tlocation: staff_context.location,\n\t\t\tcategory : staff_context.category,\n\t\t\t\'username\' : staff_context.user.username,\n\t\t\t\'return\' : \'query\',\n\t\t\tformat : \'html\',\n\t\t\temail : staff_context.user.email,\n\t\t\ttag:$(\'#\' + element_id + \'_xqa_tag\').val(),\n\t\t\tentry: $(\'#\' + element_id + \'_xqa_entry\').val()\n\t\t};\n\t\t\t\n\t$.ajax({\n\t\turl: \'')
        # SOURCE LINE 46
        __M_writer(filters.decode.utf8(xqa_server))
        __M_writer(u'/log\',\n\t\ttype: \'GET\',\n\t\tcontentType: \'application/json\',\n\t\tdata: JSON.stringify(xqaLog),\n\t\tcrossDomain: true,\n\t\tdataType: \'jsonp\',\n\t\tbeforeSend: function (xhr) { \n\t\t\txhr.setRequestHeader ("Authorization", "Basic eHFhOmFnYXJ3YWw="); },\n\t\ttimeout : 1000,\n\t\tsuccess: function(result) {\n\t\t\t\t$(\'#\' + element_id + \'_xqa_log_data\').html(result);\n\t\t},\n\t\terror: function() {\n\t\t\talert(\'Error: cannot connect to XQA server\');\n\t\t\tconsole.log(\'error!\');\n\t\t}\n\t});\n\treturn false;\n};\n\nfunction getlog(element_id, staff_context){\n\n\tvar xqaQuery = {\n\t\tauthkey: staff_context.xqa_key,\n\t\tlocation: staff_context.location,\n\t\tformat: \'html\'\n\t};\n\n\t$.ajax({\n\t\turl: \'')
        # SOURCE LINE 75
        __M_writer(filters.decode.utf8(xqa_server))
        __M_writer(u"/query',\n\t\ttype: 'GET',\n\t\tcontentType: 'application/json',\n\t\tdata: JSON.stringify(xqaQuery),\n\t\tcrossDomain: true,\n\t\tdataType: 'jsonp',\n\t\ttimeout : 1000,\n\t\tsuccess: function(result) {\n\t\t\t$('#' + element_id + '_xqa_log_data').html(result);\n\t\t},\n\t\terror: function() {\n\t\t\talert('Error: cannot connect to XQA server');\n\t\t}\n\t});\n\n\n};\n</script>")
        return ''
    finally:
        context.caller_stack._pop_frame()


