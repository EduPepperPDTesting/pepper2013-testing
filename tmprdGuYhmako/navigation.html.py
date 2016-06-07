# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218681.729225
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/navigation.html'
_template_uri = u'navigation.html'
_source_encoding = 'utf-8'
_exports = [u'navigation_dropdown_menu_links', u'navigation_global_links', u'navigation_global_links_authenticated', u'navigation_top', u'navigation_logo']


# SOURCE LINE 7

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

# App that handles subdomain specific branding
import branding
# app that handles site status messages
from status.status import get_site_status_msg
from permissions.utils import check_user_perms


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 5
    ns = runtime.TemplateNamespace('__anon_0x8165d10', context._clean_inheritance_tokens(), templateuri=u'main.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x8165d10')] = ns

    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def render_body(context,show_extended=True,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(show_extended=show_extended,pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x8165d10')._populate(_import_ns, [u'login_query', u'stanford_theme_enabled'])
        index = _import_ns.get('index', context.get('index', UNDEFINED))
        marketing_link = _import_ns.get('marketing_link', context.get('marketing_link', UNDEFINED))
        settings = _import_ns.get('settings', context.get('settings', UNDEFINED))
        def navigation_global_links():
            return render_navigation_global_links(context.locals_(__M_locals))
        def navigation_global_links_authenticated():
            return render_navigation_global_links_authenticated(context.locals_(__M_locals))
        def navigation_top():
            return render_navigation_top(context.locals_(__M_locals))
        request = _import_ns.get('request', context.get('request', UNDEFINED))
        def navigation_dropdown_menu_links():
            return render_navigation_dropdown_menu_links(context.locals_(__M_locals))
        course = _import_ns.get('course', context.get('course', UNDEFINED))
        static = _mako_get_namespace(context, 'static')
        user = _import_ns.get('user', context.get('user', UNDEFINED))
        def navigation_logo():
            return render_navigation_logo(context.locals_(__M_locals))
        def __M_anon_20():
            __M_caller = context.caller_stack._push_frame()
            try:
                __M_writer = context.writer()
                # SOURCE LINE 20
                __M_writer(u'\n    ')
                # SOURCE LINE 21

        # print index
                try:
                    course_id = course.id
                except:
                    # can't figure out a better way to get at a possibly-defined course var
                    course_id = None
                site_status_msg = get_site_status_msg(course_id)
                    
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['course_id','site_status_msg'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 29
                __M_writer(u'\n')
                # SOURCE LINE 30
                if site_status_msg:
                    # SOURCE LINE 31
                    __M_writer(u'        <div class="site-status">\n            <div class="inner-wrapper">\n                <span class="white-error-icon"></span>\n                <p>')
                    # SOURCE LINE 34
                    __M_writer(filters.decode.utf8(site_status_msg))
                    __M_writer(u'</p>\n            </div>\n        </div>\n')
                return ''
            finally:
                context.caller_stack._pop_frame()
        login_query = _import_ns.get('login_query', context.get('login_query', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        # SOURCE LINE 5
        __M_writer(u'\n\n')
        # SOURCE LINE 16
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation_top'):
            context['self'].navigation_top(**pageargs)
        

        # SOURCE LINE 19
        __M_writer(u'\n')
        __M_anon_20()
        # SOURCE LINE 38
        __M_writer(u'\n\n<style type="text/css" media="screen">\n    *{font-family:"open sans" !important;}\n    p{font-family:"open sans" !important;}\n\n    a.blue{\n        color:#556370 !important;\n    }\n\n    a.blue-underline{\n        color:#556370 !important;\n        text-decoration:underline !important;\n        border:none;\n    }\n\n    a.blue-underline:normal{\n        color:#556370 !important;\n        text-decoration:underline !important;\n        border:none;\n    }\n\n    a.blue-underline:hover{\n        color:#556370 !important;\n        text-decoration:underline !important;\n        border:none;\n    }\n\n    a.main-link{\n        font-family:\'open sans\';\n        font-size:16px;\n        text-transform:none;\n        font-weight:normal !important;\n    }\n    .imessage_style{\n        margin-right: 0px;\n        display: block;\n        float: left;\n        margin: 0px;\n        padding: 5px 8px 7px 8px;\n        margin-top:-14px;\n    }\n\n    #view_all_note:hover {\n        background:#6e8194;\n        transition-delay: 0s, 0s, 0s;\n        transition-duration: 0.25s, 0.25s, 0.25s;\n        transition-property:color, background,? box-shadow;\n        transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n        transition-duration:0.25s,? 0.25s,? 0.25s;\n        color:#fff;\n    }\n    #view_all_note{\n        border-width:0;\n        background:#556370;\n        text-decoration: none;\n        padding-bottom: 10px;\n        padding-left: 90px;\n        padding-right: 90px;\n        padding-top: 10px;\n        border-bottom-left-radius: 2px;\n        border-bottom-right-radius: 2px;\n        cursor: pointer;\n        border-top-left-radius: 2px;\n        border-top-right-radius: 2px;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        box-shadow: #949494 0px 2px 1px 0px;\n        color:#fff;\n        transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n    }\n    #view_all_note:normal {\n        background:#126F9A;\n        text-decoration: none;\n        border-bottom-left-radius: 2px;\n        border-bottom-right-radius: 2px;\n        cursor: pointer;\n        border-top-left-radius: 2px;\n        border-top-right-radius: 2px;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        box-shadow: rgb(10, 74, 103) 0px 2px 1px 0px;\n        color:#fff;\n        transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n    }\n    .ftg_button {\n        width:100px;\n        text-align:center;\n        display: block;\n        text-decoration: none!important;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        padding: 3px 3px;\n        border-radius: 3px;\n        -moz-border-radius: 3px;\n        box-shadow: inset 0px 0px 2px #fff;\n        -o-box-shadow: inset 0px 0px 2px #fff;\n        -webkit-box-shadow: inset 0px 0px 2px #fff;\n        -moz-box-shadow: inset 0px 0px 2px #fff;\n    }\n    .ftg_yellow {\n        color: #fff;\n        border: 1px solid #57c4be;\n        background-color: #57c4be;\n    }\n    .linkwin{\n        background:#fff;\n        border: 1px solid rgba(0, 0, 0, 0.9);\n        border-radius: 0;\n        box-shadow: 0 15px 80px 15px rgba(0, 0, 0, 0.5);\n        display: none;\n        left: 50%;\n        padding: 8px;\n        position: absolute;\n        width: 480px;\n        display: none;\n        margin-left:-250px;\n        top: 320px;\n        z-index: 11000;\n        height:200px;\n    }\n    #show_personalmessage, #show_notifications {\n        background: rgba(0, 0, 0, 0.6) none repeat scroll 0 0;\n        border: 1px solid rgba(0, 0, 0, 0.9);\n        border-radius: 0;\n        box-shadow: 0 15px 80px 15px rgba(0, 0, 0, 0.5);\n        color: #FFF;\n        left: 50%;\n        top: 20px;\n        padding: 8px;\n        display: none;\n        margin-left: -309px;\n        opacity: 1;\n        position: absolute;\n        width: 600px;\n        z-index: 11000;\n    }\n    .message_board_txt_prompt\n    {\n        color:#646464;\n        font-style:italic;\n        font-weight:bold;\n    }\n    .message_board_empty_info\n    {\n        color:#000000;\n        margin-top:80px;\n        text-align:center;\n        font-weight:bold;\n    }\n\n    #show_notifications_link:focus { outline: none!important;}\n    [class^="icon-"], [class*=" icon-"] {font-family: "FontAwesome" !important;}\n</style>\n<script type="text/javascript" src="/static/js/record_time.js"></script>\n<style type="text/css" media="screen">\n    a.configuration{\n        color:#646464;\n        font-family:\'open sans\';\n        font-size:16px;\n    }\n    a.configuration:hover{\n        text-decoration:none;\n        color:#1d9dd9;\n    }\n    ul.admin-dropdown-menu.expanded {\n        display: block;\n    }\n    ul.admin-dropdown-menu {\n        background: #FCFCFC none repeat scroll 0% 0%;\n        border-radius: 4px;\n        box-shadow: 0px 2px 24px 0px rgba(0, 0, 0, 0.3);\n        border: 1px solid #646464;\n        display: none;\n        padding: 5px 10px;\n        position: absolute;\n        right: -12px;\n        top: 34px;\n        width: 200px;\n        z-index: 3;\n    }\n    ul.admin-dropdown-menu li {\n        display: block;\n        border-top: 1px dotted #C8C8C8;\n        box-shadow: 0px 1px 0px 0px rgba(255, 255, 255, 0.05) inset;\n    }\n    ul.admin-dropdown-menu li > a {\n        border: 1px solid transparent;\n        border-radius: 3px;\n        box-sizing: border-box;\n        color: #1D9DD9;\n        cursor: pointer;\n        display: block;\n        margin: 5px 0px;\n        overflow: hidden;\n        padding: 3px 5px 4px;\n        text-overflow: ellipsis;\n        transition: padding 0.15s linear 0s;\n        white-space: nowrap;\n        width: 100%;\n    }\n    ul.admin-dropdown-menu li:first-child {\n        border: medium none;\n        box-shadow: none;\n    }\n    ul.admin-dropdown-menu:before {\n        background: transparent none repeat scroll 0% 0%;\n        border-width: 6px;\n        border-style: solid;\n        border-color: #FCFCFC #FCFCFC transparent transparent;\n        box-shadow: 1px 0px 0px 0px #646464, 0px -1px 0px 0px #646464;\n        content: "";\n        display: block;\n        height: 0px;\n        position: absolute;\n        transform: rotate(-45deg);\n        right: 12px;\n        top: -6px;\n        width: 0px;\n    }\n</style>\n\n')
        # SOURCE LINE 257
        if course:
            # SOURCE LINE 258
            __M_writer(u'    <header class="global slim" aria-label="')
            __M_writer(filters.decode.utf8(_('Global Navigation')))
            __M_writer(u'">\n')
            # SOURCE LINE 259
        else:
            # SOURCE LINE 260
            __M_writer(u'    <header class="global" aria-label="')
            __M_writer(filters.decode.utf8(_('Global Navigation')))
            __M_writer(u'">\n')
        # SOURCE LINE 262
        __M_writer(u'    <nav id="page-nav">\n        <style type="text/css" media="screen">\n            header.global.slim h1.logo::before{top:5px}\n        </style>\n        <h1 class="logo">\n            <!--@begin:Choose the link of the top logo according user\'s login status-->\n            <!--@date:2013-11-02-->\n\n')
        # SOURCE LINE 270
        if context.get("curr_user"):
            # SOURCE LINE 271
            __M_writer(u'                ')
            curr_user=context.get("curr_user") 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['curr_user'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            # SOURCE LINE 272
        else:
            # SOURCE LINE 273
            __M_writer(u'                ')
            curr_user=user 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['curr_user'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
        # SOURCE LINE 275
        __M_writer(u'\n')
        # SOURCE LINE 276
        if curr_user==request.user:
            # SOURCE LINE 277
            if curr_user.is_authenticated():
                # SOURCE LINE 278
                __M_writer(u'                    <a href="/dashboard">\n')
                # SOURCE LINE 279
            else:
                # SOURCE LINE 280
                __M_writer(u'                    <a href="/">\n')
            # SOURCE LINE 282
        else:
            # SOURCE LINE 283
            __M_writer(u'                <a href="" style="cursor:default;" onclick="return false;">\n')
        # SOURCE LINE 285
        __M_writer(u'            <!--@end-->\n\n            ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation_logo'):
            context['self'].navigation_logo(**pageargs)
        

        # SOURCE LINE 293
        __M_writer(u'\n        </a>\n        </h1>\n\n')
        # SOURCE LINE 297
        if course:
            # SOURCE LINE 298
            __M_writer(u'            <h2 style="width:605px;margin-top:15px;"><span class="provider">')
            __M_writer(filters.html_escape(filters.decode.utf8(course.display_org_with_default )))
            __M_writer(u':</span> ')
            __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
            __M_writer(u' ')
            __M_writer(filters.decode.utf8(course.display_name_with_default))
            __M_writer(u'</h2>\n')
        # SOURCE LINE 300
        __M_writer(u'        <!--@begin:Top navigation tabs and styles before login-->\n        <!--@date:2013-11-02-->\n        <style>\n            ol.nav-left li a{\n                color:#555;\n                padding-top:20px;\n            }\n\n        </style>\n\n')
        # SOURCE LINE 310
        if curr_user!=request.user:
            # SOURCE LINE 311
            __M_writer(u'            <style type="text/css" media="screen">\n                a.main-link{\n                    color:#ccc !important;\n                }\n                a.main-link:hover{\n                    color:#ccc !important;\n                }\n            </style>\n')
        # SOURCE LINE 320
        __M_writer(u'\n')
        # SOURCE LINE 321
        if curr_user==request.user and curr_user.is_authenticated():
            # SOURCE LINE 322
            __M_writer(u'            <ol class="left nav-global authenticated">\n')
            # SOURCE LINE 323
        else:
            # SOURCE LINE 324
            __M_writer(u'            <ol class="left nav-global">\n')
        # SOURCE LINE 326
        __M_writer(u'\n')
        # SOURCE LINE 327
        if curr_user==request.user and not curr_user.is_authenticated():
            # SOURCE LINE 328
            __M_writer(u'            <li><a href="/what_is_pepper" class="main-link">What is Pepper?</a></li>\n')
        # SOURCE LINE 330
        __M_writer(u'\n')
        # SOURCE LINE 331
        if request.user.is_authenticated():
            # SOURCE LINE 332
            if curr_user==request.user:
                # SOURCE LINE 333
                __M_writer(u'                <li><a href="/courses" class="main-link">Courses &amp; Workshops</a></li>\n')
                # SOURCE LINE 334
            else:
                # SOURCE LINE 335
                __M_writer(u'                <li><a href="" class="main-link" style="cursor:default;" onclick="return false;">Courses</a></li>\n')
        # SOURCE LINE 338
        __M_writer(u'\n')
        # SOURCE LINE 339
        if curr_user==request.user and not curr_user.is_authenticated():
            # SOURCE LINE 340
            __M_writer(u'            <li><a href="/contact" class="main-link">Districts</a></li>\n')
        # SOURCE LINE 342
        __M_writer(u'\n')
        # SOURCE LINE 343
        if request.user.is_authenticated():
            # SOURCE LINE 344
            if curr_user==request.user:
                # SOURCE LINE 345
                __M_writer(u'                <li><a href="/communities" class="main-link">Communities</a></li>\n                <li><a href="/my_chunks" class="main-link">My Chunks</a></li>\n                <li><a href="/resource_library_global" class="main-link">Resources</a></li>\n                <li><a href="')
                # SOURCE LINE 348
                __M_writer(filters.decode.utf8(reverse('people')))
                __M_writer(u'" class="main-link">People</a></li>\n                <!-- <li><a href="/course_credits" class="main-link">Course Credits</a></li> -->\n')
                # SOURCE LINE 350
            else:
                # SOURCE LINE 351
                __M_writer(u'                <li><a href="" class="main-link" style="cursor:default;" onclick="return false;">Communities</a></li>\n                <li><a href="" class="main-link" style="cursor:default;" onclick="return false;">My Chunks</a></li>\n                <li><a href="" class="main-link" style="cursor:default;" onclick="return false;">Resources</a></li>\n                <li><a href="" class="main-link" style="cursor:default;" onclick="return false;">People</a></li>\n                <!-- <li><a href="" class="main-link" style="cursor:default;" onclick="return false;">Course Credits</a></li> -->\n')
        # SOURCE LINE 358
        __M_writer(u'\n')
        # SOURCE LINE 359
        if curr_user.is_authenticated():
            # SOURCE LINE 360
            __M_writer(u'        ')
            if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation_global_links_authenticated'):
                context['self'].navigation_global_links_authenticated(**pageargs)
            

            # SOURCE LINE 364
            __M_writer(u'\n        </ol>\n            <!--@end-->\n\n            <link rel="stylesheet" href="/static/css/admin_ui_controls.css" type="text/css" media="screen" />\n            <script type="text/javascript" src="/static/js/admin_ui_controls.js"></script>\n\n')
            # SOURCE LINE 371
            if curr_user==request.user:
                # SOURCE LINE 372
                __M_writer(u'        <ol class="user admin" >\n')
                # SOURCE LINE 373
                if show_extended and check_user_perms(curr_user, ['certificate', 'pepconn', 'permissions', 'time_report', 'sso', 'tnl', 'studio', 'alert_message']):
                    # SOURCE LINE 374
                    __M_writer(u'                <!-- Administration -->\n                <li style="display:block;float:left;padding-top:10px;margin-right:0px;" class="admin-menu-holder">\n                    <a href="#" class="configuration" onclick="$(\'.admin ul.admin-dropdown-menu\').toggle()">Tools &#9662;</a>\n                    <ul class="admin-dropdown-menu">\n')
                    # SOURCE LINE 378
                    if check_user_perms(curr_user, 'certificate'):
                        # SOURCE LINE 379
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('configuration')))
                        __M_writer(u'">Configuration</a></li>\n')
                    # SOURCE LINE 381
                    if check_user_perms(curr_user, 'pepconn'):
                        # SOURCE LINE 382
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('pepconn')))
                        __M_writer(u'">PepConn</a></li>\n')
                    # SOURCE LINE 384
                    if check_user_perms(curr_user, 'permissions'):
                        # SOURCE LINE 385
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('permissions_view')))
                        __M_writer(u'">Roles &amp; Permissions</a></li>\n')
                    # SOURCE LINE 387
                    if check_user_perms(curr_user, 'time_report'):
                        # SOURCE LINE 388
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('time_report')))
                        __M_writer(u'">Time Report</a></li>\n')
                    # SOURCE LINE 390
                    if check_user_perms(curr_user, 'sso'):
                        # SOURCE LINE 391
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('sso_idp_metadata_edit')))
                        __M_writer(u'">SSO Metadata</a></li>\n')
                    # SOURCE LINE 393
                    if check_user_perms(curr_user, 'tnl'):
                        # SOURCE LINE 394
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('tnl_configuration')))
                        __M_writer(u'">TNL Configuration</a></li>\n')
                    # SOURCE LINE 396
                    if check_user_perms(curr_user, 'studio'):
                        # SOURCE LINE 397
                        __M_writer(u'                            <li><a href="#" target="_blank" id="studio_url">Studio</a></li>\n')
                    # SOURCE LINE 399
                    if check_user_perms(curr_user, 'alert_message'):
                        # SOURCE LINE 400
                        __M_writer(u'                            <li><a href="')
                        __M_writer(filters.decode.utf8(reverse('alert_message')))
                        __M_writer(u'">Alert</a></li>\n')
                    # SOURCE LINE 402
                    __M_writer(u'                        <script type="text/javascript">\n                            $(document).on(\'click\', function(event) {\n                                if (!$(event.target).closest(\'.admin-menu-holder\').length) {\n                                    $(".admin-dropdown-menu").hide();\n                                } else if ($(event.target).closest(".outside_menu").length) {\n                                    $(".admin-dropdown-menu").hide();\n                                }\n                            });\n\n                            url_studio = ["https://studio0.pepperpd.com",\n                                          "https://studio-staging.pepperpd.com",\n                                          "https://studio-demo.pepperpd.com",\n                                          "https://studio.pepperpd.com",\n                                          "https://studio-dev.pepperpd.com",\n                                          "https://studio-major.pepperpd.com",\n                                          "https://studio-patch.pepperpd.com",\n                                          "https://studio-test.pepperpd.com"];\n                            url_split_array = window.location.href.split(\'/\');\n                            split_array_1 = "";\n                            split_keyword = "";\n                            url_using= "#";\n\n                            if (url_split_array.length>2){\n                                split_array_1 = url_split_array[2].split(\'.\');\n                                split_keyword = split_array_1[0];\n                            }\n                            \n                            if (split_keyword == "www0"){\n                               url_using = url_studio[0];\n                            }\n                            else if(split_keyword == "staging"){\n                                url_using = url_studio[1];\n                            }\n                            else if(split_keyword == "demo"){\n                                url_using = url_studio[2];\n                            }\n                            else if(split_keyword == "www"){\n                                url_using = url_studio[3];\n                            }\n                            else if(split_keyword == "dev"){\n                                url_using = url_studio[4];\n                            }\n                            else if(split_keyword == "major"){\n                                url_using = url_studio[5];\n                            }\n                            else if(split_keyword == "patch"){\n                                url_using = url_studio[6];\n                            }\n                            else if(split_keyword == "test"){\n                                url_using = url_studio[7];\n                            }\n                            $("#studio_url").attr("href",url_using);\n                        </script>\n                    </ul>\n                </li>\n')
                # SOURCE LINE 458
                if show_extended:
                    # SOURCE LINE 459
                    __M_writer(u'                <!-- Notifications -->\n                <li class="imessage_style" style="margin-right:5px;">\n                    <a href="#show_notifications" rel="leanModal" id="show_notifications_link" style="text-decoration:none !important;">\n                        <div class="info_count_btn" style="width:50px;height:50px;background:url(/static/images/ppd-iMessage.jpg);display:none;">\n                            <table  width="50" height="50" border="0" cellpadding="0" cellspacing="0">\n                                <tr height="26">\n                                    <td width="19"></td>\n                                    <td width="31"></td>\n                                </tr>\n                                <tr height="24">\n                                    <td width="19" >&nbsp;</td>\n                                    <td class="info_count" width="31" align="center" style="color:#f00;font-weight:bold;font-size:13px;">33</td>\n                                </tr>\n                            </table>\n                        </div>\n                        <div class="info_btn" style="width:50px;height:50px;background:url(/static/images/ppd-iMessage-none.jpg);"></div>\n                    </a>\n                </li>\n')
                # SOURCE LINE 478
                __M_writer(u'\n')
                # SOURCE LINE 479
                if show_extended:
                    # SOURCE LINE 480
                    __M_writer(u'                <!-- Dashboard button with dropdown -->\n                <li class="primary">\n                    <a href="')
                    # SOURCE LINE 482
                    __M_writer(filters.decode.utf8(reverse('dashboard')))
                    __M_writer(u'" class="user-link" style="overflow-y:visible;height:28px;margin-top:6px;">\n                        <span class="avatar"></span>\n                        <span class="sr">')
                    # SOURCE LINE 484
                    __M_writer(filters.decode.utf8(_("Dashboard for:")))
                    __M_writer(u' </span>\n                        <span style="display:block;max-width:90px;text-overflow:ellipsis;line-height:12px;height:18px;font-weight:bold;overflow-x:hidden;vertical-align:top;">')
                    # SOURCE LINE 485
                    __M_writer(filters.decode.utf8(curr_user.username))
                    __M_writer(u'</span>\n                    </a>\n                </li>\n                <li class="primary">\n                    <a href="#" class="dropdown" style="height:28px;margin-top:6px;"><span class="sr">')
                    # SOURCE LINE 489
                    __M_writer(filters.decode.utf8(_("More options dropdown")))
                    __M_writer(u'</span> &#9662;</a>\n                    <ul class="dropdown-menu">\n                        ')
                    if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation_dropdown_menu_links'):
                        context['self'].navigation_dropdown_menu_links(**pageargs)
                    

                    # SOURCE LINE 493
                    __M_writer(u'\n                        <li><a href="/course_credits" class="main-link">Course Credits</a></li>\n                        <li><a href="')
                    # SOURCE LINE 495
                    __M_writer(filters.decode.utf8(reverse('logout')))
                    __M_writer(u'">')
                    __M_writer(filters.decode.utf8(_("Log Out")))
                    __M_writer(u'</a></li>\n                    </ul>\n                </li>\n')
                # SOURCE LINE 499
                __M_writer(u'        </ol>\n')
            # SOURCE LINE 501
            if not show_extended:
                # SOURCE LINE 502
                __M_writer(u'            <ol class="right nav-courseware" id="btn-dashboard">\n                <li class="nav-courseware-01">\n                    <a class="cta cta-login" href="/dashboard">Dashboard</a>\n                </li>\n            </ol>\n')
            # SOURCE LINE 508
            __M_writer(u'\n')
            # SOURCE LINE 509
        else:
            # SOURCE LINE 510
            __M_writer(u'        ')
            if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation_global_links'):
                context['self'].navigation_global_links(**pageargs)
            

            # SOURCE LINE 522
            __M_writer(u'\n\n')
            # SOURCE LINE 524
            if not settings.MITX_FEATURES['DISABLE_LOGIN_BUTTON']:
                # SOURCE LINE 525
                if course and settings.MITX_FEATURES.get('RESTRICT_ENROLL_BY_REG_METHOD') and course.enrollment_domain:
                    # SOURCE LINE 526
                    __M_writer(u'                <!--@begin:Change Register Now to Become a Member-->\n                <!--@date:2013-11-02-->\n                <a  class="main-link" href="')
                    # SOURCE LINE 528
                    __M_writer(filters.decode.utf8(reverse('course-specific-register', args=[course.id])))
                    __M_writer(u'">Become a Member</a>\n')
                    # SOURCE LINE 529
                else:
                    # SOURCE LINE 530
                    __M_writer(u'                <li><a  class="main-link" href="/contact">Become a Member</a></li>\n                <!--@end-->\n')
            # SOURCE LINE 534
            __M_writer(u'            <!--@begin:Add tab About Us-->\n            <!--@date:2013-11-02-->\n            <li><a href="/about_pepper" class="main-link">About Us</a></li>\n            <!--@end-->\n        </ol>\n\n            <ol class="right nav-courseware">\n                <!--@begin:Add Paypal-->\n                <!--@date:2016-05-19-->\n                <li class="nav-courseware-01">\n')
            # SOURCE LINE 544
            if not settings.MITX_FEATURES['DISABLE_LOGIN_BUTTON']:
                # SOURCE LINE 545
                if course and settings.MITX_FEATURES.get('RESTRICT_ENROLL_BY_REG_METHOD') and course.enrollment_domain:
                    # SOURCE LINE 546
                    __M_writer(u'                            <a  class="main-link" href="')
                    __M_writer(filters.decode.utf8(reverse('course-specific-register', args=[course.id])))
                    __M_writer(u'" target="_blank" style="margin-right:30px;"><img src="/static/images/paypal.png" width="100" height="27"/></a>\n')
                    # SOURCE LINE 547
                else:
                    # SOURCE LINE 548
                    __M_writer(u'                            <a  class="main-link" href="/contact" target="_blank" ><img src="/static/images/paypal.png" width="100" height="27"/></a>        \n')
            # SOURCE LINE 551
            __M_writer(u'                </li>\n                <!--@end-->\n                <li class="nav-courseware-01">\n')
            # SOURCE LINE 554
            if not settings.MITX_FEATURES['DISABLE_LOGIN_BUTTON']:
                # SOURCE LINE 555
                if course and settings.MITX_FEATURES.get('RESTRICT_ENROLL_BY_REG_METHOD') and course.enrollment_domain:
                    # SOURCE LINE 556
                    __M_writer(u'                            <!--@begin:Change the text in Log in to Login-->\n                            <!--@date:2013-11-02-->\n                            <a class="cta cta-login" href="')
                    # SOURCE LINE 558
                    __M_writer(filters.decode.utf8(reverse('course-specific-login', args=[course.id])))
                    __M_writer(filters.decode.utf8(login_query()))
                    __M_writer(u'">')
                    __M_writer(filters.decode.utf8(_("Login")))
                    __M_writer(u'</a>\n')
                    # SOURCE LINE 559
                else:
                    # SOURCE LINE 560
                    __M_writer(u'                            <a class="cta cta-login" href="/login')
                    __M_writer(filters.decode.utf8(login_query()))
                    __M_writer(u'">')
                    __M_writer(filters.decode.utf8(_("Login")))
                    __M_writer(u'</a>\n                            <!--@end-->\n')
            # SOURCE LINE 564
            __M_writer(u'                </li>\n            </ol>\n')
        # SOURCE LINE 567
        __M_writer(u'    </nav>\n</header>\n\n')
        # SOURCE LINE 570
        if course:
            # SOURCE LINE 571
            __M_writer(u'    <div class="ie-banner">')
            __M_writer(filters.decode.utf8(_('<strong>Warning:</strong> Your browser is not fully supported. We strongly recommend using {chrome_link_start}Chrome{chrome_link_end} or {ff_link_start}Firefox{ff_link_end}.').format(chrome_link_start='<a href="https://www.google.com/intl/en/chrome/browser/" target="_blank">', chrome_link_end='</a>', ff_link_start='<a href="http://www.mozilla.org/en-US/firefox/new/" target="_blank">', ff_link_end='</a>')))
            __M_writer(u'</div>\n')
        # SOURCE LINE 573
        __M_writer(u'\n')
        # SOURCE LINE 574
        if not curr_user.is_authenticated():
            # SOURCE LINE 575
            __M_writer(u'    ')
            runtime._include_file(context, u'forgot_password_modal.html', _template_uri)
            __M_writer(u'\n')
        # SOURCE LINE 577
        __M_writer(u'\n')
        # SOURCE LINE 578
        runtime._include_file(context, u'help_modal.html', _template_uri)
        __M_writer(u'\n\n    <!--@begin:show_notifications-->\n    <!--@date:2014-06-19-->\n')
        # SOURCE LINE 582
        if request.user.is_authenticated():
            # SOURCE LINE 583
            if curr_user==request.user:
                # SOURCE LINE 584
                __M_writer(u'        <section id="show_notifications" class="modal modal-wide" data-id="')
                __M_writer(filters.decode.utf8(curr_user.id))
                __M_writer(u'" data-name="')
                __M_writer(filters.decode.utf8(curr_user.username))
                __M_writer(u'" data-fullname="')
                __M_writer(filters.decode.utf8(curr_user.first_name))
                __M_writer(u' ')
                __M_writer(filters.decode.utf8(curr_user.last_name))
                __M_writer(u'">\n            <div class="inner-wrapper" style="width:578px;">\n                <header>\n                    <h2>')
                # SOURCE LINE 587
                __M_writer(filters.decode.utf8(_("notifications")))
                __M_writer(u'</h2>\n                    <hr/>\n                </header>\n\n                <div class="info_list"></div>\n                <br/>\n                <br/>\n                <br/>\n                <div style="width:500px;height:40px;margin:0 auto;text-align:center;">\n                    <a href="')
                # SOURCE LINE 596
                __M_writer(filters.decode.utf8(reverse('notifications')))
                __M_writer(u'" id="view_all_note" style="color:#fff !important;font-size:18px;">\n                        <div id="view_all_note_text" style="display:inline-block;text-align:center;width:250px;">View All Notifications (0)</div>\n                    </a>\n                </div>\n                <div class="close-modal" id="notifications_close">\n                    <div class="inner">\n                        <p>&#10005;</p>\n                    </div>\n                </div>\n            </div>\n        </section>\n')
        # SOURCE LINE 609
        __M_writer(u'    <script>\n        //---------------------Notifications variable-----------------------------------------//\n\n        var interactive_update_window_top = 0;\n\n        //---------------------Message board variable-----------------------------------------//\n\n        var message_people = null;\n        var user_info = null;\n        var message_board_isload = false;\n        var message_board_loadNum = 0;\n        var message_board_totalNum = 0;\n        var message_board_focus = 0;\n        var message_board_maxCharNum = 1000;\n        var message_board_hover = 0;\n\n        //---------------------Record time variable-------------------------------------------//\n\n        var courseTimer = null;\n        var externalTimer = null;\n        RecordTime.firstRun = true;\n        var timer_record = false;\n        \n        //---------------------Pepper stats refresh-------------------------------------------//\n\n        function pepper_stats_refresh() {\n            if (document.URL.indexOf(\'dashboard\') >= 0) {\n                $.post("')
        # SOURCE LINE 636
        __M_writer(filters.decode.utf8(reverse('get_pepper_stats')))
        __M_writer(u'", {\n                 \'user_id\': "')
        # SOURCE LINE 637
        __M_writer(filters.decode.utf8(curr_user.id))
        __M_writer(u'"\n               }, function(data) {\n                 $(\'#all_course_time\').html(data.all_course_time);\n                 $(\'#collaboration_time\').html(data.collaboration_time);\n                 //hide totle adjustment time\n                 //$(\'#totle_adjustment_time\').html(data.totle_adjustment_time);\n                 $(\'#total_time_in_pepper\').html(data.total_time_in_pepper);\n                 $(".course-time,.course-time-completed").each(function() {\n                   var course_id = $(this).attr(\'course_id\');\n                   var time_type = $(this).attr(\'time_type\');\n                   if (time_type == \'course\') {\n                     $(this).children(\'span\').html(data.course_times[course_id]);\n                   } else {\n                     $(this).children(\'span\').html(data.external_times[course_id]);\n                   }\n                 });\n               });\n            }\n        }\n    \n        //---------------------Record time (Page switching)----------------------------------//\n\n        function record_time(position) {\n            timer_record = false;\n')
        # SOURCE LINE 661
        if request.user.id is not None:
            # SOURCE LINE 662
            __M_writer(u'                sessionStorage[\'user_id\'] = "')
            __M_writer(filters.decode.utf8(request.user.id))
            __M_writer(u'";\n')
        # SOURCE LINE 664
        if course:
            # SOURCE LINE 665
            __M_writer(u'                RecordTime.setSessionCourseID("')
            __M_writer(filters.decode.utf8(course.id))
            __M_writer(u'");\n')
        # SOURCE LINE 667
        __M_writer(u'            courseTimer.start();\n            RecordTime.coursePosition = position;\n            RecordTime.sessionInit();\n            var vertical_id = $("#sequence-list li .active").attr("data-id");\n            var time = new Date().toISOString();\n            var path = RecordTime.getCourseFullPath(document.URL, position);\n            var data = {\n                \'type\': \'course_page\',\n                \'user_id\': RecordTime.userID,\n                \'time\': time,\n                \'new_vertical_id\': vertical_id,\n                \'prev_vertical_id\': RecordTime.getSessionVerticalId(),\n                \'prev_time\': RecordTime.getSessionTime(),\n                \'location\': path\n            };\n            if (RecordTime.getSessionVerticalId() != vertical_id) {\n                RecordTime.ajaxRecordTime(data, function() {\n                    RecordTime.setSessionVerticalId(vertical_id);\n                    RecordTime.setSessionTime(time);\n                    courseTimer.load();\n                    timer_record = true;\n                });\n\n            } else {\n                if (RecordTime.firstRun) {\n                    RecordTime.ajaxRecordTime(data, function() {\n                        RecordTime.setSessionVerticalId(vertical_id);\n                        RecordTime.setSessionTime(time);\n                        RecordTime.firstRun = false;\n                        timer_record = true;\n                    });\n                }\n            }\n        }\n        //---------------------Record time (Course refresh or exit)--------------------------//\n\n        function course_refresh_or_exit() {\n')
        # SOURCE LINE 704
        if request.user.id is not None:
            # SOURCE LINE 705
            __M_writer(u'                sessionStorage[\'user_id\'] = "')
            __M_writer(filters.decode.utf8(request.user.id))
            __M_writer(u'";\n                RecordTime.sessionInit();\n')
            # SOURCE LINE 707
        else:
            # SOURCE LINE 708
            __M_writer(u"                RecordTime.setSessionVerticalId('');\n                RecordTime.setSessionCourseTime(0);\n")
        # SOURCE LINE 711
        if course:
            # SOURCE LINE 712
            __M_writer(u'                RecordTime.setSessionCourseID("')
            __M_writer(filters.decode.utf8(course.id))
            __M_writer(u'");\n')
        # SOURCE LINE 714
        __M_writer(u'            //RecordTime.sessionInit();\n            if (RecordTime.getSessionVerticalId() != "" && document.URL.indexOf(\'courseware\') < 1 && !timer_record) {\n                var data = {\n                    \'type\': \'new_page\',\n                    \'user_id\': RecordTime.userID,\n                    \'time\': (new Date()).toISOString(),\n                    \'prev_vertical_id\': RecordTime.getSessionVerticalId(),\n                    \'prev_time\': RecordTime.getSessionTime()\n                };\n                RecordTime.ajaxRecordTime(data, function() {\n                    RecordTime.setSessionVerticalId("");\n                    RecordTime.setSessionTime("");\n                    pepper_stats_refresh();\n                });\n                timer_record = true;\n            }\n            var verticalId = RecordTime.getSessionVerticalId()||\'\';\n            var time = RecordTime.getSessionCourseTime(RecordTime.getSessionCourseType())||0;\n            if(verticalId == \'\' && time == 0){\n                pepper_stats_refresh();\n            }\n        }\n\n        //---------------------------------------------------------------------------//\n        function onfocusEventDelay(e){\n            course_refresh_or_exit();\n            var is_press_logout = $(document.activeElement).is(\'.dropdown\');\n            if (document.URL.indexOf(\'courseware\') < 0) {\n                if(courseTimer.loadComplete && !is_press_logout){\n                    courseTimer.isrun = false;\n                    courseTimer.create();\n                }\n            } else {\n                if (RecordTime.getSessionVerticalId() == "" && !is_press_logout && timer_record) {\n                    record_time(RecordTime.coursePosition);\n                }\n            }\n\n        }\n        function onblurEventDelay(e){\n            //console.log(e.type);\n            //var isfocusOut = $(document.activeElement).is(\'.courseware,.dropdown,.seq_other,.sequence-nav-buttons li a\');\n            var isfocusOut = $(document.activeElement).get(0).tagName!=\'IFRAME\';\n            course_refresh_or_exit();\n            if (document.URL.indexOf(\'courseware\') < 0) {\n                courseTimer.stop();\n                courseTimer.save();\n            }\n            if (RecordTime.getSessionVerticalId() != "" && document.URL.indexOf(\'courseware\') >= 0 && isfocusOut) {\n                RecordTime.sessionInit();\n                var data = {\n                    \'type\': \'new_page\',\n                    \'user_id\': RecordTime.userID,\n                    \'time\': (new Date()).toISOString(),\n                    \'prev_vertical_id\': RecordTime.getSessionVerticalId(),\n                    \'prev_time\': RecordTime.getSessionTime()\n                };\n                RecordTime.ajaxRecordTime(data, function () {\n                    RecordTime.setSessionVerticalId("");\n                    RecordTime.setSessionTime("");\n                    courseTimer.load();\n                });\n                \n            }\n        }\n        $(function() {\n            $(window).blur(function(e) {\n                setTimeout(function(){onblurEventDelay(e);}, 200);\n            });\n            $(window).focus(function(e) {\n                setTimeout(function(){onfocusEventDelay(e);}, 200);\n            });\n            $(\'.dropdown\').mouseup(function(e){\n                if (document.URL.indexOf(\'courseware\') > 0) {\n                    if (RecordTime.getSessionVerticalId() != ""){\n                        setTimeout(function(){onblurEventDelay(null);}, 200); \n                    }\n                }\n                else{\n                    if(RecordTime.getSessionCourseTime(RecordTime.getSessionCourseType()) > 0){\n                        setTimeout(function(){onblurEventDelay(null);}, 200);\n                    }\n                }\n            })\n\n            course_refresh_or_exit();\n            courseTimer = new CourseTimer();\n            externalTimer = new ExternalTimer();\n            //courseTimer.isrun = false;\n            //courseTimer.create();\n            \n            interactive_update();\n            $(".info_count_btn").click(function() {\n                interactive_update();\n            });\n\n            $(".info_btn").click(function() {\n                interactive_update();\n            });\n\n            $(".ftg_button").click(function() {\n                message_board_saveInfo();\n            });\n\n            $(".message_board_uploadBtn").click(function() {\n                $("#message_board_browseFile").click();\n            });\n\n            $(".message_board_linkBtn").click(function() {\n                $(".linkwin").show();\n            });\n\n            $("#hyperlink_okBtn").click(function() {\n                var content = $(".message_board_content");\n                if ($("#link_url_val").val() != \'\') {\n                    if (!message_board_focus) {\n                        content.html("");\n                        message_board_focus = 1;\n                    }\n                    content.html(content.html() + message_board_hyperlinks($("#link_url_val").val(), $("#link_title_val").val()));\n                    $(".linkwin").hide();\n                }\n            });\n\n            $("#hyperlink_cancelBtn").click(function() {\n                $(".linkwin").hide();\n            });\n\n            $("#message_board_close").click(function() {\n                $(".linkwin").hide();\n                message_board_clearContent();\n            });\n\n            //-----------------------------------------------------------------\n            $(".message_board_content").focusin(function() {\n                if (!message_board_focus) {\n                    $(this).html("");\n                    message_board_focus = 1;\n                }\n            });\n\n            $(".message_board_content").keyup(function(event) {\n                message_board_updateMaxCharNum();\n            });\n\n            $("#show_personalmessage").hover(function() {\n                $("body").css("overflow", "hidden");\n                message_board_hover = 1;\n            }, function() {\n                $("body").css("overflow", "");\n                message_board_hover = 0;\n            });\n\n            $(".message_board_listCon").scroll(function(event) {\n                var scrollTop = $(this).scrollTop();\n                var scrollHeight = $(".message_board_list").height();\n                var windowHeight = $(this).height();\n                /*\n                  if((scrollTop + windowHeight == scrollHeight) && message_board_isload)\n                  {\n                  message_board_getMessage(message_board_loadNum);\n                  }\n                */\n                if (scrollTop == 0 && message_board_isload) {\n                    message_board_getMessage(message_board_loadNum);\n                }\n            });\n        });\n\n        function interactive_update_createItem(data) {\n            var body = data.body == undefined ? \'\' : data.body;\n            interactive_update_switchType(data);\n            element = $(\'<table width="530" height="70" border="0" cellpadding="0" cellspacing="0" style="margin:auto;background-color:\' + interactive_update_getActivateStyle(data).backgroundColor + \';cursor:pointer;"><tr><td width="76"><div style="width:60px;height:60px;margin-left:5px;margin-top:5px;background:url(/user_photo/\' + data.interviewer_id + \');background-size:contain;background-repeat:no-repeat;"></div></td><td width="424"><table width="454" border="0" cellpadding="0" cellspacing="0"><tr height="46"><td style="padding-right:5px;color:#388e9b;font-size:14px;line-height:20px;padding-top:7px;"><div>\' + data.type_text + \'</div><div style="color:#000;text-overflow:ellipsis;overflow:hidden;width:320px;white-space:nowrap;">\' + body + \'</div></td></tr><tr height="24"><td style="vertical-align:middle;font-size:12px;color:#aaa;">\' + interactive_update_dateFormat(data).full_date + \'</td></tr></table></td></tr></table><br/>\');\n            $(\'.info_list\').append(element);\n            element.click(function() {\n                if (data.activate == \'false\') {\n                    interactive_update_activateItem(data);\n                } else {\n                    interactive_update_openWindow(data)\n                }\n            });\n        }\n\n        function interactive_update_switchType(data) {\n            switch (data.type) {\n                case \'discussion\':\n                    data.type_text = "<b>" + data.interviewer_name + "</b> has added a comment to your discussion topic or comment in course " + data.course_number + ".";\n                    break;\n                case \'portfolio\':\n                    data.type_text = "<b>" + data.interviewer_name + "</b> has commented on " + (data.portfolio_username || \'your\') + "\'s portfolio in course " + data.course_number + ".";\n                    break;\n                case \'add_network\':\n                    data.type_text = "<b>" + data.interviewer_name + "</b> has added you to their personal network."\n                    break;\n                case \'view_portfolio\':\n                    data.type_text = "<b>" + data.interviewer_name + "</b> is checking out your " + data.course_number + " portfolio."\n                    break;\n                case \'message\':\n                    data.type_text = "Personal Message from <b>" + data.interviewer_name + "</b>"\n                    break;\n                case \'my_chunks\':\n                    data.type_text = "<b>" + data.interviewer_name + "</b> has sent you a chunk of content from course " + data.course_number + ".";\n                    break;\n            }\n        }\n\n        function interactive_update() {\n            datainfo = {};\n            $.post("')
        # SOURCE LINE 922
        __M_writer(filters.decode.utf8(reverse('get_interactive_update')))
        __M_writer(u'", datainfo, function(data) {\n                interactive_update_init(data);\n            });\n        }\n\n        function interactive_update_init(data) {\n            $("#view_all_note_text").text("View All Notifications (" + data.count + ")");\n            if (data.count > 0) {\n                $(".info_btn").hide();\n                $(".info_count_btn").show();\n                var count = data.count > 999 ? 999 : data.count;\n                $(".info_count_btn").find(".info_count").text(count);\n            }\n            $(\'.info_list\').empty();\n            for (var i = 0; i < data.results.length; i++) {\n                interactive_update_createItem(data.results[i]);\n            }\n        }\n\n        function fillZero(val) {\n            return val < 10 ? \'0\' + val : val;\n        }\n\n        function interactive_update_dateFormat(data) {\n            dateinfo = {};\n            interval = interactive_update_getTimeInterval(data);\n            var darr = new Date(data.date).toString().split(\' \');\n            var sign = \'am\';\n            if (interval < 1) {\n                dateinfo.date = "Today";\n            } else if (interval < 2) {\n                dateinfo.date = "Yesterday";\n            } else {\n                dateinfo.date = darr[1] + " " + darr[2];\n            }\n            var timeArr = darr[4].substr(0, 5).split(":");\n            if (timeArr[0] > 12 && timeArr[0] < 24) {\n                timeArr[0] = fillZero(timeArr[0] - 12);\n                sign = \'pm\';\n            }\n            var time = timeArr[0] + ":" + timeArr[1] + sign;\n            dateinfo.full_date = dateinfo.date + " at " + time;\n            dateinfo.time = time;\n            return dateinfo;\n        }\n\n        function interactive_update_activateItem(data) {\n            var user_id = "')
        # SOURCE LINE 969
        __M_writer(filters.decode.utf8(curr_user.id))
        __M_writer(u'";\n            $.post("')
        # SOURCE LINE 970
        __M_writer(filters.decode.utf8(reverse('set_interactive_update')))
        __M_writer(u'", {\n                _id: data._id,\n                _name: \'activate\',\n                _value: \'true\',\n                _user_id: user_id,\n                _record_id: data.user_id,\n                _ismultiple: data.multiple\n            }, function(rdata) {\n                interactive_update_openWindow(data);\n            });\n        }\n\n        function interactive_update_getActivateStyle(data) {\n            var notActivateColor = data.user_id != 0 ? "#eeeff4" : "#ffffcc";\n            //bcolor=((data.activate==\'true\')||(interactive_update_getTimeInterval(data)>4&&data.user_id!=0))?\'#ffffff\':notActivateColor;\n            bcolor = data.activate == \'true\' ? \'#ffffff\' : notActivateColor;\n            return {\n                \'backgroundColor\': bcolor\n            };\n        }\n\n        function interactive_update_getTimeInterval(data) {\n            var t = new Date();\n            var today = new Date(t.getFullYear(), t.getMonth(), t.getDate());\n            var d = new Date(data.date);\n            var date = new Date(d.getFullYear(), d.getMonth(), d.getDate());\n            return parseInt((today - date) / 3600000 / 24);\n        }\n\n        function interactive_update_openWindow(data) {\n            if (data.type == "message" || data.type == "view_portfolio") {\n                $("#show_notifications").hide();\n                if ($("#show_personalmessage").css("zIndex") < 10000) {\n                    $("#show_personalmessage").addClass("leanmodalStyle");\n                }\n                $("#lean_overlay").show();\n                $("#show_personalmessage").show();\n                $("#show_personalmessage").find(".close-modal").click(function() {\n                    $("#show_personalmessage").hide();\n                    $(".linkwin").hide();\n                    $("#lean_overlay").hide();\n                    $(window).scrollTop(interactive_update_window_top);\n                })\n                message_board_clearContent();\n                $("#lean_overlay").click(function() {\n                    $("#show_personalmessage").hide();\n                    $(".linkwin").hide();\n                    $(this).hide();\n                    $(window).scrollTop(interactive_update_window_top);\n                })\n                var userInfo = [];\n                var data_ele = $("#show_notifications");\n                userInfo[\'message_people\'] = {\n                    id: data.interviewer_id,\n                    fullname: data.interviewer_fullname,\n                    name: data.interviewer_name\n                };\n                userInfo[\'user\'] = {\n                    id: data_ele.data(\'id\'),\n                    fullname: data_ele.data(\'fullname\'),\n                    name: data_ele.data(\'name\')\n                };\n                message_board(userInfo);\n                return 0;\n            }\n            if (data.location.indexOf("/dashboard") >= 0) {\n                window.open(data.location);\n                return 0;\n            }\n            if (data.location.indexOf("/my_coursework") >= 0) {\n                var curr_user_id = "')
        # SOURCE LINE 1040
        __M_writer(filters.decode.utf8(curr_user.id))
        __M_writer(u'";\n                var user_id = data.location.substring(data.location.indexOf("/my_coursework") + 15, data.location.lastIndexOf("/"));\n                if (curr_user_id != user_id) {\n                    window.open(data.location, \'_blank\');\n                    return 0;\n                }\n            }\n            if (data.location.indexOf("/my_discussions") >= 0) {\n                var curr_user_id = "')
        # SOURCE LINE 1048
        __M_writer(filters.decode.utf8(curr_user.id))
        __M_writer(u'";\n                var user_id = data.location.substring(data.location.indexOf("/my_discussions") + 16, data.location.indexOf("?"));\n                if (curr_user_id != user_id) {\n                    window.open(data.location, \'_blank\');\n                    return 0;\n                }\n            }\n            if (window.location.href.indexOf("/courses") >= 0) {\n                var curr_url = "/courses" + window.location.href.split("/courses")[1].split("#")[0];\n                var location = data.location.split("#")[0];\n                if (curr_url != location) {\n                    window.open(data.location, \'_self\');\n                } else {\n                    window.location.href = data.location;\n                    window.location.reload();\n                }\n            } else {\n                window.open(data.location, \'_self\');\n            }\n\n        }\n        //-------------------------message_board---------------------//\n\n        function message_board(_user_info) {\n            user_info = _user_info;\n            message_people = user_info["message_people"];\n            $(\'.message_item\').remove();\n            message_board_hideLoadMore();\n            message_board_isload = false;\n            message_board_loadNum = 0;\n            message_board_totalNum = 0;\n            message_board_focus = 0;\n            message_board_clearContent();\n            message_board_multiplayerSend_init();\n            message_board_getMessage(message_board_loadNum);\n        }\n\n        function message_board_getMessage(skip) {\n            message_board_isload = false;\n            $.post("')
        # SOURCE LINE 1087
        __M_writer(filters.decode.utf8(reverse('get_message')))
        __M_writer(u'", {\n                message_people: message_people.id,\n                skip: skip,\n                limit: 6\n            }, function(data) {\n                message_board_init(data)\n            });\n        }\n\n        function message_board_init(data) {\n            message_board_loadNum += 6;\n            message_board_totalNum = data.count;\n            $(".message_board_full_name").text(message_people.fullname);\n            $(\'.message_board_empty_info\').remove();\n            if (data.results.length == 0) {\n                $(\'.message_board_list\').append(\'<div class="message_board_empty_info">You do not currently have any messages with \' + message_people.fullname.split(\' \')[0] + \'.</div>\');\n            } else {\n                $(\'.message_board_empty_info\').remove();\n            }\n            for (var i = 0; i < data.results.length; i++) {\n                message_board_createItem(data.results[i], 1);\n            }\n\n            if (message_board_loadNum >= message_board_totalNum) {\n                message_board_isload = false;\n                message_board_hideLoadMore();\n            } else {\n                message_board_isload = true;\n                message_board_hideLoadMore();\n                message_board_showLoadMore();\n            }\n            $(\'.message_board_listCon\').scrollTop($(".message_board_list").height());\n        }\n\n        function message_board_saveInfo() {\n            var content = $(".message_board_content");\n            var msReturnVal = message_board_multiplayerSend_returnVal();\n            var winR = 1;\n            if (msReturnVal) {\n                winR = confirm("Do you want to send this message to all users?", "Warning");\n                if (!winR) {\n                    return 0;\n                }\n            }\n            if (content.text().length > 0 && content.text().length <= message_board_maxCharNum && message_board_focus && winR) {\n                var recipient_id = msReturnVal ? 0 : message_people.id.toString();\n                var datainfo = {\n                    \'info\': JSON.stringify({\n                        \'sender_id\': \'')
        # SOURCE LINE 1135
        __M_writer(filters.decode.utf8(user.id))
        __M_writer(u'\',\n                        \'recipient_id\': recipient_id,\n                        \'date\': (new Date()).toISOString(),\n                        \'body\': content.html()\n                    })\n                };\n                $.post("')
        # SOURCE LINE 1141
        __M_writer(filters.decode.utf8(reverse('save_message')))
        __M_writer(u'", datainfo, function(rdata) {\n                    if ($(".message_board_list").find(\'.message_board_empty_info\').length > 0) {\n                        $(\'.message_board_empty_info\').remove();\n                    }\n                    message_board_createItem(JSON.parse(datainfo.info));\n                    $(\'.message_board_listCon\').scrollTop($(".message_board_list").height());\n                    message_board_updateMaxCharNum();\n                    var interviewer_id = user_info["user"].id.toString();\n                    var interviewer_name = user_info["user"].name;\n                    var interviewer_fullname = user_info["user"].fullname;\n                    var body = content.text().length > 100 ? content.text().substr(0, 100) : content.text();\n                    var messageinfo = {\n                        \'info\': JSON.stringify({\n                            \'user_id\': recipient_id,\n                            \'interviewer_id\': interviewer_id,\n                            \'interviewer_name\': interviewer_name,\n                            \'interviewer_fullname\': interviewer_fullname,\n                            \'type\': \'message\',\n                            \'body\': body,\n                            \'date\': (new Date()).toISOString(),\n                            \'activate\': \'false\'\n                        })\n                    };\n                    $.post("')
        # SOURCE LINE 1164
        __M_writer(filters.decode.utf8(reverse('save_interactive_update')))
        __M_writer(u'", messageinfo, function() {});\n                    content.html("");\n                });\n            } else {\n                if (content.text().length > message_board_maxCharNum)\n                    alert(\'Exceed the maximum number of characters.\');\n            }\n        }\n\n        function message_board_user(data) {\n            var userObj = [];\n            userObj[message_people.id] = message_people;\n            userObj[user_info["user"].id] = user_info["user"];\n            return userObj[data.sender_id];\n        }\n\n        function message_board_createItem(data, _pos) {\n            pos = _pos || 0;\n            var element = $(\'<div class="message_item"><table width="530" border="0" cellpadding="0" cellspacing="0" style="margin:auto;background-color:#fff;font-size:14px;"><tr><td width="76" rowspan="2"><div style="width:60px;height:60px;margin-left:5px;margin-top:5px;background:url(/user_photo/\' + data.sender_id + \');background-size:contain;background-repeat:no-repeat;"/></td><td width="227" height="30" style="color:#388e9b;font-weight:bold;vertical-align:middle;">\' + message_board_user(data).name + \'</td><td width="227" align="right" style="padding-right:6px;font-size:12px;color:#aaa;vertical-align:middle;">\' + interactive_update_dateFormat(data).full_date + \'</td></tr><tr><td colspan="2" style="font-size:14px;color:#000;padding-top:2px;padding-right:6px;padding-bottom:8px;line-height:18px;"><div style="word-wrap:break-word;overflow:hidden;width:454px;">\' + data.body + \'</div></td></tr></table><div style="height:2px;"></div></div>\');\n            if (pos) {\n                $(\'.message_board_list\').prepend(element);\n            } else {\n                $(\'.message_board_list\').append(element);\n            }\n\n        }\n\n        function message_board_changeImg(objImg) {\n            var max = 300;\n            if (objImg.width > max) {\n                var scaling = 1 - (objImg.width - max) / objImg.width;\n                objImg.width = objImg.width * scaling;\n                objImg.height = objImg.height;\n            }\n            $(\'.message_board_listCon\').scrollTop($(".message_board_list").height());\n        }\n\n        function message_board_upload_file() {\n            var fd, files, max_filesize, settings;\n            var content = $(".message_board_content");\n            max_filesize = 0.5 * 1000 * 1000;\n            if (/\\.(bmp|gif|jpg|jpeg|png|BMP|GIF|JPG|PNG)$/.test($("#message_board_browseFile")[0].files[0].name)) {\n                files = "";\n                files = $("#message_board_browseFile")[0].files[0];\n                if (files != void 0) {\n                    if (files.size > max_filesize) {\n                        files = "";\n                        alert("File is too large. Max file size is 500 Kb.");\n                        $("#message_board_browseFile")[0].files = [];\n                        return false;\n                    }\n                }\n                fd = new FormData();\n                fd.append(\'image_file\', files);\n                settings = {\n                    type: "POST",\n                    data: fd,\n                    processData: false,\n                    contentType: false,\n                    async: false,\n                    success: function(response) {\n                        if (response == null) {\n                            alert("Network error. Please try again.");\n                            return false;\n                        }\n                        if (response.success == true) {\n                            alert("Upload success!");\n                        } else {\n                            alert("Upload fail");\n                        }\n                        if (!message_board_focus) {\n                            content.html("");\n                            message_board_focus = 1;\n                        }\n                        content.html(content.html() + "<img src=\'" + response.file_info + "\' onload=\'message_board_changeImg(this);\' alt=\'[Image loading ...]\'> </img>");\n                        message_board_updateMaxCharNum();\n                    }\n                };\n                return $.ajax("')
        # SOURCE LINE 1242
        __M_writer(filters.decode.utf8(reverse('upload_message_image')))
        __M_writer(u'", settings);\n\n            } else {\n                alert("The file format is not supported.");\n            }\n        }\n\n        function message_board_showLoadMore() {\n            var element = $(\'<div class="loadMoreBtn" style="width:530px;height:20px;text-align:center;font-size:14px;padding-top:8px;color:#388e9b;background-color:#EDEFF4;margin:auto;">Load more</div>\');\n            $(\'.message_board_list\').prepend(element);\n        }\n\n        function message_board_hideLoadMore() {\n            $(".loadMoreBtn").remove();\n        }\n\n        function message_board_updateMaxCharNum() {\n            var charNum = $(".message_board_content").text().length;\n            var num = charNum > message_board_maxCharNum ? "<font color=\'#ff0000\'>" + charNum + "</font>" : charNum;\n            $("#curr_char_num").html(num);\n        }\n\n        function message_board_hyperlinks(url, title) {\n            //return str.replace(new RegExp("("+"[a-zA-z]+://[^ ]*"+")",\'g\'),"<a href=\'$1\' target=\'_blank\'>$1</a>");\n            if (title == "")\n                title = url;\n            if (url.indexOf(\'://\') < 0)\n                url = "http://" + url;\n            return "<a href=\'" + url + "\' target=\'_blank\'>" + title + "</a><br/>";\n        }\n\n        function message_board_multiplayerSend_init() {\n            var isStaff = "')
        # SOURCE LINE 1274
        __M_writer(filters.decode.utf8(curr_user.is_staff))
        __M_writer(u'";\n            var ms = $("#multiplayer_send_div");\n            ms.find("input").attr("checked", false);\n            if (isStaff == "True") {\n                ms.show();\n            } else {\n                ms.hide();\n            }\n        }\n\n        function message_board_multiplayerSend_returnVal() {\n            var msCBox = $("#multiplayer_send_div").find("input");\n            return (msCBox.is(":visible") && msCBox.is(":checked")) ? true : false;\n        }\n\n        function message_board_clearContent() {\n            var content = $(\'.message_board_content\');\n            content.html("");\n            message_board_updateMaxCharNum();\n            $(\'.message_board_listCon\').scrollTop(0);\n            content.html("<p class=\'message_board_txt_prompt\'>Type Your Message Here</p>");\n        }\n    </script>\n    <!--@end-->\n\n    <!--@begin:show_personalmessage-->\n    <!--@date:2014-06-30-->\n')
        # SOURCE LINE 1301
        if request.user.is_authenticated():
            # SOURCE LINE 1302
            if curr_user==request.user:
                # SOURCE LINE 1303
                __M_writer(u'        <section id="show_personalmessage" class="modal modal-wide">\n            <div class="inner-wrapper" style="width:578px;padding-bottom:0 !important;">\n                <header>\n                    <h2 class="message_board_full_name">')
                # SOURCE LINE 1306
                __M_writer(filters.decode.utf8(_("namename")))
                __M_writer(u'</h2>\n                    <hr/>\n                </header>\n                <div class="message_board_listCon" style="height:350px;overflow-y:auto;overflow-x:hidden;"><div class="message_board_list"></div></div>\n                <form id="" method="post" style="padding:0px;line-height:18px;">\n\n                    <div style="width:520px;margin:10px;">\n                        <div class="message_board_content" contenteditable="true" style="width:530px;height:150px;background-color:#fff;color:black;padding:10px;border:1px solid #ccc;overflow-y:auto;"><p class="message_board_txt_prompt">Type Your Message Here</p></div>\n\n                        <div style="color:black;font-size:12px;color:#aaa;">\n                            Maximum to 1000 Characters  (<span id="curr_char_num">0</span>)\n                        </div>\n                        <div style="width:530px;height:30px;">\n                            <table width="530" border="0" cellpadding="0" cellspacing="0">\n                                <tr height="30" style="color:#000;">\n                                    <td widht="265" style="vertical-align:middle;">\n                  <span class="message_board_uploadBtn" style="width:110px;cursor:pointer;">\n                    <img src="/static/images/personalmsg_upload.png" width="22" height="22"/>\n                    <span style="padding-left:2px;font-size:14px;color:#aaa;">Add Photos</span>\n                  </span>\n                  \n                  <span class="message_board_linkBtn" style="width:100px;cursor:pointer;margin-left:5px;">\n                    <img src="/static/images/personalmsg_link.jpg" width="22" height="22"/>\n                    <span style="padding-left:2px;font-size:14px;color:#aaa;">Link</span>\n                  </span>\n\n                                    </td>\n                                    <td align="right" style="vertical-align:middle;">\n                                        <div class="ftg_button ftg_yellow" style="cursor:pointer;">Send</div>\n                                    </td>\n                                </tr>\n                                <tr><td><div id="multiplayer_send_div" style="width:300px;color:#000;margin-left:5px;display:none;"><label><input type="checkbox"/>Send to All Users</label></div></td></tr>\n                            </table>\n                        </div>\n                    </div>\n                    <input id="message_board_browseFile" type="file" onchange="message_board_upload_file()" style="width:0px;"/>\n                </form>\n                <br/>\n                <!--\n                <div style="width:500px;height:40px;margin:0 auto;text-align:center;">\n                <a href="/dashboard" id="view_all_note" class="dashboard_link" style="color:#fff !important;font-size:18px;">\n                <div style="display:inline-block;text-align:center;width:250px;">Dashboard</div>\n                </a>\n                </div>\n                -->\n                <div class="close-modal" id="message_board_close">\n                    <div class="inner">\n                        <p>&#10005;</p>\n                    </div>\n                </div>\n            </div>\n        </section>\n')
        # SOURCE LINE 1360
        __M_writer(u'    <div class="linkwin">\n        <h3 style="padding-left:10px;"><b>Insert Hyperlink</b></h3>\n        <hr/>\n        <form style="padding: 0px; margin: 0px; float: left; width: 100%; text-align: center; position: relative;">\n            <table>\n                <tr>\n                    <td style="vertical-align:middle">Insert URL:</td>\n                    <td><input type="text" id="link_url_val"style="width:100%"></td>\n                </tr>\n                <tr>\n                    <td width="100" style="vertical-align:middle">Title:</td>\n                    <td width="350"><input id="link_title_val" type="text" style="width:100%"></td>\n                </tr>\n            </table>\n            <input id="hyperlink_okBtn" type="button" value="OK" style="margin: 10px; display: inline; width: 7em;">\n            <input id="hyperlink_cancelBtn" type="button" value="Cancel" style="margin: 10px; display: inline; width: 7em;">\n        </form>\n    </div>\n    <!--@end-->\n\n    <!-- task panel -->\n')
        # SOURCE LINE 1381
        if curr_user.is_superuser or check_user_perms(request.user, 'time_report'):
            # SOURCE LINE 1382
            __M_writer(u'    <div class="global_task_panel_wrapper">\n        <div class="control global_task_panel">\n            <input type="button" name="" value="? running tasks" class="task_pannel_toggle"/>\n            <div class="content"></div>\n      <textarea class="setting">\n        {\n          "interval": 5000,\n          "urls": {\n            "count": "')
            # SOURCE LINE 1390
            __M_writer(filters.decode.utf8(reverse('pepconn_import_user_tasks')))
            __M_writer(u'",\n            "close": "')
            # SOURCE LINE 1391
            __M_writer(filters.decode.utf8(reverse('pepconn_task_close')))
            __M_writer(u'"\n          }\n        }\n      </textarea>\n        </div>\n    </div>\n    <script type="text/javascript">\n        $(".control.global_task_panel").each(function(){new GlobalTaskPanelControl(this)});\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation_dropdown_menu_links(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x8165d10')._populate(_import_ns, [u'login_query', u'stanford_theme_enabled'])
        def navigation_dropdown_menu_links():
            return render_navigation_dropdown_menu_links(context)
        __M_writer = context.writer()
        # SOURCE LINE 491
        __M_writer(u'\n                            <li><a href="/static/resource/Pepper_User_Guide_V2_100615.pdf" target="_blank">')
        # SOURCE LINE 492
        __M_writer(filters.decode.utf8(_("Help")))
        __M_writer(u'</a></li>\n                        ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation_global_links(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x8165d10')._populate(_import_ns, [u'login_query', u'stanford_theme_enabled'])
        def navigation_global_links():
            return render_navigation_global_links(context)
        marketing_link = _import_ns.get('marketing_link', context.get('marketing_link', UNDEFINED))
        settings = _import_ns.get('settings', context.get('settings', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 510
        __M_writer(u'\n')
        # SOURCE LINE 511
        if settings.MITX_FEATURES.get('ENABLE_MKTG_SITE'):
            # SOURCE LINE 512
            __M_writer(u'                <li class="nav-global-01">\n                    <a href="')
            # SOURCE LINE 513
            __M_writer(filters.decode.utf8(marketing_link('HOW_IT_WORKS')))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(_("How it Works")))
            __M_writer(u'</a>\n                </li>\n                <li class="nav-global-02">\n                    <a href="')
            # SOURCE LINE 516
            __M_writer(filters.decode.utf8(marketing_link('COURSES')))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(_("Courses")))
            __M_writer(u'</a>\n                </li>\n                <li class="nav-global-03">\n                    <a href="')
            # SOURCE LINE 519
            __M_writer(filters.decode.utf8(marketing_link('SCHOOLS')))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(_("Schools")))
            __M_writer(u'</a>\n                </li>\n')
        # SOURCE LINE 522
        __M_writer(u'        ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation_global_links_authenticated(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x8165d10')._populate(_import_ns, [u'login_query', u'stanford_theme_enabled'])
        marketing_link = _import_ns.get('marketing_link', context.get('marketing_link', UNDEFINED))
        def navigation_global_links_authenticated():
            return render_navigation_global_links_authenticated(context)
        __M_writer = context.writer()
        # SOURCE LINE 360
        __M_writer(u'\n            <li class="nav-global-01" style="display:none;">\n                <a href="')
        # SOURCE LINE 362
        __M_writer(filters.decode.utf8(marketing_link('COURSES')))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8(_('Find Courses')))
        __M_writer(u'</a>\n            </li>\n        ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation_top(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x8165d10')._populate(_import_ns, [u'login_query', u'stanford_theme_enabled'])
        def navigation_top():
            return render_navigation_top(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation_logo(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x8165d10')._populate(_import_ns, [u'login_query', u'stanford_theme_enabled'])
        index = _import_ns.get('index', context.get('index', UNDEFINED))
        static = _mako_get_namespace(context, 'static')
        request = _import_ns.get('request', context.get('request', UNDEFINED))
        def navigation_logo():
            return render_navigation_logo(context)
        __M_writer = context.writer()
        # SOURCE LINE 287
        __M_writer(u"\n                <!--@begin:Choose the image of the top logo according to user's login status-->\n")
        # SOURCE LINE 289
        if index != 1:
            # SOURCE LINE 290
            __M_writer(u'                <img style="height:auto;vertical-align:top" src="')
            __M_writer(filters.decode.utf8(static.url(branding.get_logo_url(request.META.get('HTTP_HOST')))))
            __M_writer(u'" alt="')
            __M_writer(filters.decode.utf8(_('{settings.PLATFORM_NAME} home')))
            __M_writer(u'" />\n')
        # SOURCE LINE 292
        __M_writer(u'                <!--@end-->\n            ')
        return ''
    finally:
        context.caller_stack._pop_frame()


