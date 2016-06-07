# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218891.78987
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/course_navigation.html'
_template_uri = u'/courseware/course_navigation.html'
_source_encoding = 'utf-8'
_exports = [u'extratabs']


# SOURCE LINE 66
from courseware.tabs import get_course_tabs 

# SOURCE LINE 67
from django.utils.translation import ugettext as _ 

# SOURCE LINE 68
from courseware.courses import course_author_image_url 

def render_body(context,active_page=None,portfolio_user=None,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(portfolio_user=portfolio_user,pageargs=pageargs,active_page=active_page)
        masquerade = context.get('masquerade', UNDEFINED)
        request = context.get('request', UNDEFINED)
        def extratabs():
            return render_extratabs(context.locals_(__M_locals))
        course = context.get('course', UNDEFINED)
        user = context.get('user', UNDEFINED)
        active_page_context = context.get('active_page_context', UNDEFINED)
        staff_access = context.get('staff_access', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n<!--@begin:Hide the Dashboard button in this page-->\n<!--@date:2013-11-02-->\n<style type="text/css" media="screen">\n  .mychunks_linkwin{\n    background:#fff;\n    border: 1px solid rgba(0, 0, 0, 0.9);\n    border-radius: 0;\n    box-shadow: 0 15px 80px 15px rgba(0, 0, 0, 0.5);\n    display: none;\n    left: 50%;\n    padding: 8px;\n    position: absolute;\n    width: 480px;\n    display: none;\n    margin-left:-250px;\n    top: 320px;\n    z-index: 11000;\n    height:200px;\n  }\n  .mychunks_style_button {\n    width:100px;\n    text-align:center;\n    display: block;\n    text-decoration: none!important;\n    font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n    padding: 3px 3px;\n    border-radius: 3px;\n    -moz-border-radius: 3px;\n    box-shadow: inset 0px 0px 2px #fff;\n    -o-box-shadow: inset 0px 0px 2px #fff;\n    -webkit-box-shadow: inset 0px 0px 2px #fff;\n    -moz-box-shadow: inset 0px 0px 2px #fff;\n    cursor:pointer;\n  }\n  .course-tabs li{\n    margin-top:10px;\n  }\n</style>\n<!--@end-->\n\n')
        # SOURCE LINE 43
        if context.get("curr_user"):
            # SOURCE LINE 44
            __M_writer(u'  ')
            curr_user=context.get("curr_user") 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['curr_user'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            # SOURCE LINE 45
        else:
            # SOURCE LINE 46
            __M_writer(u'  ')
            curr_user=user 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['curr_user'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
        # SOURCE LINE 48
        __M_writer(u'\n')
        # SOURCE LINE 49

        if active_page is None and active_page_context is not UNDEFINED:
          # If active_page is not passed in as an argument, it may be in the context as active_page_context
          active_page = active_page_context
        
        def url_class(is_active):
          if is_active:
            return "active"
          return ""
        def url_class(tab):
          s=""
          if tab.name.strip().lower()=='live hangout!':
            s="live_hangout"
          if tab.is_active:
            s+=" active"
          return s
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['url_class','active_page'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 65
        __M_writer(u'\n')
        # SOURCE LINE 66
        __M_writer(u'\n')
        # SOURCE LINE 67
        __M_writer(u'\n')
        # SOURCE LINE 68
        __M_writer(u'\n<style>\n  /*nav.course-material ol.course-tabs li a.live_hangout{color:#8C9641;}*/\n</style>\n\n<nav class="')
        # SOURCE LINE 73
        __M_writer(filters.decode.utf8(active_page))
        __M_writer(u' course-material">\n  <div class="inner-wrapper">\n    <ol class="course-tabs">\n')
        # SOURCE LINE 76
        for tab in get_course_tabs(user, course, active_page):
            # SOURCE LINE 77
            if portfolio_user == user and request.GET.get('pf_id')==None or portfolio_user == None and request.GET.get('pf_id')==None or portfolio_user.id == user.id:
                # SOURCE LINE 78
                __M_writer(u'          <!--20151124 use new parameter "hide_discussions" to judge whether show "Discussion" in course navigation-->\n          <!--begin-->\n          <li>\n')
                # SOURCE LINE 81
                if tab.name!='Discussion' or tab.name=='Discussion' and not course.hide_discussions:
                    # SOURCE LINE 82
                    __M_writer(u'              <a href="')
                    __M_writer(filters.html_escape(filters.decode.utf8(tab.link )))
                    __M_writer(u'" class="')
                    __M_writer(filters.decode.utf8(url_class(tab)))
                    __M_writer(u'">\n              ')
                    # SOURCE LINE 83
                    __M_writer(filters.html_escape(filters.decode.utf8(tab.name )))
                    __M_writer(u'\n')
                    # SOURCE LINE 84
                    if tab.is_active == True:
                        # SOURCE LINE 85
                        __M_writer(u'                  <span class="sr">, current location</span> \n')
                    # SOURCE LINE 87
                    if tab.has_img == True:
                        # SOURCE LINE 88
                        __M_writer(u'                  <img src="')
                        __M_writer(filters.decode.utf8(tab.img))
                        __M_writer(u'"/> \n')
                    # SOURCE LINE 90
                    __M_writer(u'              </a>\n')
                # SOURCE LINE 92
                __M_writer(u'          </li>\n          <!--end-->\n')
                # SOURCE LINE 94
            else:
                # SOURCE LINE 95
                if tab.name=='My Course Portfolio':
                    # SOURCE LINE 96
                    __M_writer(u'          <li>\n          <a href="')
                    # SOURCE LINE 97
                    __M_writer(filters.html_escape(filters.decode.utf8(tab.link )))
                    __M_writer(u'?pf_id=')
                    __M_writer(filters.decode.utf8(portfolio_user.id))
                    __M_writer(u'" class="')
                    __M_writer(filters.decode.utf8(url_class(tab)))
                    __M_writer(u'">\n            ')
                    # SOURCE LINE 98
                    __M_writer(filters.html_escape(filters.decode.utf8(tab.name )))
                    __M_writer(u'\n')
                    # SOURCE LINE 99
                    if tab.is_active == True:
                        # SOURCE LINE 100
                        __M_writer(u'                <span class="sr">, current location</span> \n')
                    # SOURCE LINE 102
                    if tab.has_img == True:
                        # SOURCE LINE 103
                        __M_writer(u'                <img src="')
                        __M_writer(filters.decode.utf8(tab.img))
                        __M_writer(u'"/> \n')
                    # SOURCE LINE 105
                    __M_writer(u'          </a>\n      </li>\n')
                    # SOURCE LINE 107
                else:
                    # SOURCE LINE 108
                    __M_writer(u'          <li>\n          <a href="javascript:void(0);" disabled="disabled" style="color:#A4A4A4">\n            ')
                    # SOURCE LINE 110
                    __M_writer(filters.html_escape(filters.decode.utf8(tab.name )))
                    __M_writer(u'\n')
                    # SOURCE LINE 111
                    if tab.is_active == True:
                        # SOURCE LINE 112
                        __M_writer(u'                <span class="sr">, current location</span> \n')
                    # SOURCE LINE 114
                    if tab.has_img == True:
                        # SOURCE LINE 115
                        __M_writer(u'                <img src="')
                        __M_writer(filters.decode.utf8(tab.img))
                        __M_writer(u'"/> \n')
                    # SOURCE LINE 117
                    __M_writer(u'          </a>\n      </li>\n')
        # SOURCE LINE 122
        __M_writer(u'    \n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extratabs'):
            context['self'].extratabs(**pageargs)
        

        # SOURCE LINE 123
        __M_writer(u'\n')
        # SOURCE LINE 124
        if masquerade is not UNDEFINED:
            # SOURCE LINE 125
            if staff_access and masquerade is not None:
                # SOURCE LINE 126
                __M_writer(u'          <li><a href="#" id="staffstatus">')
                __M_writer(filters.decode.utf8(_("Staff view")))
                __M_writer(u'</a></li>\n')
        # SOURCE LINE 129
        __M_writer(u'    <li class="my_chunks_nav_icon" style="float:right;display:none;margin-top:0px;">\n      <a style="text-decoration:none !important;padding:5px;display:none;" id="my_chunks_link" href="javascript:void(0);" user_id="')
        # SOURCE LINE 130
        __M_writer(filters.decode.utf8(curr_user.id))
        __M_writer(u'">\n        <div style="width: 50px; height: 50px; background: url(\'/static/images/unchuncked.png\') repeat scroll 0% 0% transparent;" class="my_chunks_btn"></div>\n      </a>\n    </li>\n    </ol>\n  </div>\n</nav>\n\n')
        # SOURCE LINE 138
        if masquerade is not UNDEFINED:
            # SOURCE LINE 139
            if staff_access and masquerade is not None:
                # SOURCE LINE 140
                __M_writer(u'<script type="text/javascript">\nmasq = (function(){\n    var el = $(\'#staffstatus\');\n    var setstat = function(status){\n        if (status==\'student\'){\n            el.html(\'<font color="green">Student view</font>\');\n        }else{\n            el.html(\'<font color="red">Staff view</font>\');\n        }\n    }\n    setstat(\'')
                # SOURCE LINE 150
                __M_writer(filters.decode.utf8(masquerade))
                __M_writer(u"');\n\n    el.click(function(){\n        $.ajax({ url: '/masquerade/toggle',\n                 type: 'GET',\n                 success: function(result){\n                     setstat(result.status);\n                     location.reload();\n                 },\n                 error: function() {\n                     alert('Error: cannot connect to server');\n                 }\n               });\n    });\n}() );\n</script>\n")
        # SOURCE LINE 168
        __M_writer(u'<section id="show_mychunks" class="modal" style="width:600px;">\n  <div class="inner-wrapper" style="width:578px;padding-bottom:10px !important;">\n    <header>\n      <h2 class="mychunks_title">')
        # SOURCE LINE 171
        __M_writer(filters.decode.utf8(_("ADD THIS CHUNK")))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n  <div class="mychunks_info" style="height:200px;overflow-y:auto;overflow-x:hidden;color:#000000;">\n    <center><div><img width="280" height="100" alt="course author image" src="')
        # SOURCE LINE 175
        __M_writer(filters.decode.utf8(course_author_image_url(course)))
        __M_writer(u'"></div></center>\n    <div style="margin:10px 0px 10px 30px"><b>Course: </b><span id="mychunks_course_title"></span></div>\n    <div style="margin:10px 0px 10px 30px"><b>Chunk: </b><span id="mychunks_chunk_title"></span></div>\n  </div>\n  <form id="" method="post" style="padding:0px;line-height:18px;">\n   \n        <div style="width:520px;margin:10px;">\n         <div class="mychunks_content" contenteditable="true" style="width:530px;height:150px;background-color:#fff;color:black;padding:10px;border:1px solid #ccc;overflow-y:auto;"><p style="color:#D4D0C8"></p></div>\n\n          <div style="color:black;font-size:12px;color:#aaa;">\n            Maximum to 1000 Characters  (<span id="mychunks_curr_char_num">0</span>)\n          </div>\n          <div style="width:530px;height:20px;">\n            <table width="530" border="0" cellpadding="0" cellspacing="0">\n              <tr height="30" style="color:#000;">\n                <td widht="265" style="vertical-align:middle;">\n                  <span class="mychunks_uploadBtn" style="width:110px;cursor:pointer;">\n                    <img src="/static/images/personalmsg_upload.png" width="22" height="22"/>\n                    <span style="padding-left:2px;font-size:14px;color:#aaa;">Add Photos</span>\n                  </span>\n                  \n                  <span class="mychunks_linkBtn" style="width:100px;cursor:pointer;margin-left:5px;">\n                      <img src="/static/images/personalmsg_link.jpg" width="22" height="22"/>\n                      <span style="padding-left:2px;font-size:14px;color:#aaa;">Link</span>\n                  </span>\n                  \n                </td>\n                <td align="right" style="vertical-align:middle;">\n                  <div class="mychunks_ftg_button mychunks_style_button ftg_yellow">Update</div>\n                  <div class="mychunks_delBtn mychunks_style_button ftg_yellow" style="margin-top:10px;display:none;">Delete</div>\n                </td>\n              </tr>\n            </table>\n          </div>\n        </div>\n        <input id="mychunks_browseFile" type="file" onchange="mychunks_upload_file()" style="width:0px;"/>\n  </form>\n  <br/>\n    <div class="close-modal" id="mychunks_close">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="del_mychunks" class="modal" style="width:600px;">\n  <div class="inner-wrapper" style="width:578px;padding-bottom:10px !important;">\n    <header>\n      <h2 class="mychunks_title">')
        # SOURCE LINE 223
        __M_writer(filters.decode.utf8(_("DELETE THE CHUNK")))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="" method="post" style="padding:0px;line-height:18px;">\n   \n        <div style="width:560px;margin:10px;">\n        <div style="color:black;font-size:16px;width:540px;height:80px;padding:10px;"><center><b>Are you sure you want to delete this chunk of content?</b></center></div>\n         <center><div class="mychunks_del_button mychunks_style_button ftg_yellow">Delete</div></center>\n        </div>\n    </form>\n  <br/>\n    <div class="close-modal" id="mychunks_close">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="add_mychunks" class="modal" style="width:600px;">\n  <div class="inner-wrapper" style="width:578px;padding-bottom:10px !important;">\n    <header>\n      <h2 class="mychunks_title">')
        # SOURCE LINE 244
        __M_writer(filters.decode.utf8(_("CHUNK ADDED")))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="" method="post" style="padding:0px;line-height:18px;">\n   \n        <div style="width:560px;margin:10px;">\n        <div style="color:black;font-size:16px;width:540px;height:80px;padding:10px;"><center><b>You have successfully added this chunk to your personal collection.</b></center></div>\n         <center><div class="mychunks_add_button mychunks_style_button ftg_yellow">Done</div></center>\n        </div>\n    </form>\n  <br/>\n    <div class="close-modal" id="mychunks_add_close">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<div class="mychunks_linkwin">\n    <h3 style="padding-left:10px;"><b>Insert Hyperlink</b></h3>\n    <hr/>\n    <form style="padding: 0px; margin: 0px; float: left; width: 100%; text-align: center; position: relative;">\n      <table>\n        <tr>\n          <td style="vertical-align:middle">Insert URL:</td>\n          <td><input type="text" id="mychunks_link_url_val"style="width:100%"></td>\n        </tr>\n        <tr>\n          <td width="100" style="vertical-align:middle">Title:</td>\n          <td width="350"><input id="mychunks_link_title_val" type="text" style="width:100%"></td>\n        </tr>\n      </table>\n      <input id="mychunks_hyperlink_okBtn" type="button" value="OK" style="margin: 10px; display: inline; width: 7em;">\n      <input id="mychunks_hyperlink_cancelBtn" type="button" value="Cancel" style="margin: 10px; display: inline; width: 7em;">\n    </form>\n </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extratabs(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def extratabs():
            return render_extratabs(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


