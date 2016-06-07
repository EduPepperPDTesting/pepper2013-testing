# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224816.489194
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/communities/community.html'
_template_uri = 'communities/community.html'
_source_encoding = 'utf-8'
_exports = [u'title']


# SOURCE LINE 2

from django.core.urlresolvers import reverse
from courseware.courses import course_image_url, get_course_about_section
from student.views import course_from_id
from administration.configuration import has_hangout_perms
from communities.utils import is_facilitator, is_member
from file_uploader.utils import get_file_url
from django.utils import timezone
from datetime import date


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 12
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'../static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'../main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        total_discussions = context.get('total_discussions', UNDEFINED)
        csrf_token = context.get('csrf_token', UNDEFINED)
        trending = context.get('trending', UNDEFINED)
        users = context.get('users', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        request = context.get('request', UNDEFINED)
        facilitator = context.get('facilitator', UNDEFINED)
        community = context.get('community', UNDEFINED)
        courses = context.get('courses', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        discussions = context.get('discussions', UNDEFINED)
        pager = context.get('pager', UNDEFINED)
        resources = context.get('resources', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\r\n')
        # SOURCE LINE 11
        __M_writer(u'\r\n')
        # SOURCE LINE 12
        __M_writer(u'\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 15
        __M_writer(u'\r\n<script type="text/javascript" src="/static/js/admin_ui_controls.js"></script>\r\n<script type="text/javascript" src="https://secure.skypeassets.com/i/scom/js/skype-uri.js"></script>\r\n<script type="text/javascript" src="/static/js/ckeditor/ckeditor.js" charset="utf-8"></script>\r\n<style type="text/css" media="screen">\r\n    #community-main {\r\n        width: 1185px;\r\n        margin: 30px auto;\r\n        text-align: left;\r\n    }\r\n    #community-main-content {\r\n        width: 880px;\r\n        float: left;\r\n    }\r\n    #community-main-sidebar {\r\n        width: 266px;\r\n        float: right;\r\n        top: 0;\r\n        text-align: center;\r\n    }\r\n    #community-sidebar-header {\r\n        border: 2px solid #ddd;\r\n        height: 53px;\r\n        text-align: center;\r\n        vertical-align: middle;\r\n        font: 700 1.2em/2.4em "Open Sans",Verdana,Geneva,sans-serif;\r\n    }\r\n    #community-sidebar {\r\n        width: 208px;\r\n        padding: 20px 20px 0 20px;\r\n        border: 2px solid #ddd;\r\n        margin: auto;\r\n        border-top: 0;\r\n        text-align: left;\r\n    }\r\n    .sidebar-section {\r\n        margin: 0 0 20px 0;\r\n    }\r\n    #community-member {\r\n        margin-top: 10px;\r\n    }\r\n    .sidebar-section h2 {\r\n        border-bottom: 2px solid #90BF70;\r\n        padding-bottom: 5px;\r\n        margin: 0 0 10px 0;\r\n        color: #006EBF;\r\n        font-weight: bold;\r\n        text-transform: none;\r\n        font-size: 1em;\r\n        line-height: 1em;\r\n    }\r\n    .sidebar-sub-section {\r\n        margin: 0 10px;\r\n    }\r\n    .trending-title {\r\n        display: block;\r\n        white-space: nowrap;\r\n        overflow: hidden;\r\n        text-overflow: ellipsis;\r\n    }\r\n    .trending-name {\r\n        font-size: 80%;\r\n        display: block;\r\n        margin-bottom: 5px;\r\n    }\r\n    .trending-name span {\r\n        font-weight: bold;\r\n    }\r\n    .status-name {\r\n        display: block;\r\n        margin-bottom: 5px;\r\n    }\r\n    #community-header {\r\n        border: 2px solid #ddd;\r\n        width: 100%;\r\n        position: relative;\r\n        min-height: 260px;\r\n    }\r\n    #community-header h1 {\r\n        text-align: left;\r\n        color: #006EBF;\r\n        margin: 15px 0 0 20px;\r\n        font-weight: bold;\r\n        font-size: 160%;\r\n    }\r\n    #community-header h2 {\r\n        margin: 15px 0 0 20px;\r\n        text-transform: none;\r\n        font-weight: bold;\r\n    }\r\n    #community-header h3 {\r\n        color: #006EBF;\r\n        padding: 10px 0;\r\n    }\r\n    #community-header h4 {\r\n        font-weight: bold;\r\n    }\r\n    #community-avatar {\r\n        width: 100px;\r\n        float: left;\r\n        margin: 0 15px 0 0;\r\n    }\r\n    #community-logo {\r\n        float: right;\r\n        width: 380px;\r\n        height: 260px;\r\n        overflow: hidden;\r\n        margin: 15px;\r\n        text-align: center;\r\n        background-color: white;\r\n    }\r\n    #community-logo img {\r\n        height: 260px;\r\n    }\r\n    .facilitator-wrap {\r\n        position: absolute;\r\n        width: 450px;\r\n        bottom: 20px;\r\n        left: 20px;\r\n    }\r\n    #community-content-area h1 {\r\n        color: #006EBF;\r\n        padding: 20px 3px;\r\n        font-size: 20px;\r\n        font-weight: bold;\r\n        text-align: left;\r\n        border-bottom: 2px solid #90BF70;\r\n        display: inline-block;\r\n    }\r\n    #community-content h1 {\r\n        width: 100%;\r\n    }\r\n    #community-content, #community-discussions {\r\n        color: #000;\r\n        padding: 20px 3px;\r\n    }\r\n    #community-content-area label {\r\n        font-style: normal;\r\n        display: inline-block;\r\n        width: 3.5em;\r\n        text-align: left;\r\n        font-weight: bold;\r\n    }\r\n    #community-content-area span {\r\n        /*font-size: 12px;*/\r\n    }\r\n    #community-content {\r\n        width: 270px;\r\n        height: 700px;\r\n        float: left;\r\n    }\r\n    #community-content-scroller {\r\n        width: 270px;\r\n        height: 640px;\r\n        overflow-y: scroll;\r\n        overflow-x: hidden;\r\n    }\r\n    #community-discussions {\r\n        width: 578px;\r\n        margin-right: 20px;\r\n        float: left;\r\n    }\r\n    .discussion {\r\n        clear: both;\r\n        position: relative;\r\n        border: 2px solid #ddd;\r\n        border-radius: 10px;\r\n        padding: 15px 20px 15px 94px;\r\n        background-color: #fff;\r\n        margin-bottom: 15px;\r\n    }\r\n    .discussion h2 {\r\n        margin-bottom: 5px;\r\n        width: 370px;\r\n        white-space: nowrap;\r\n        overflow: hidden;\r\n        text-overflow: ellipsis;\r\n    }\r\n    .discussion-post-info-header {\r\n        float: left;\r\n        width: 463px;\r\n    }\r\n    .discussion-post-info div {\r\n        display: inline-block;\r\n    }\r\n    .discussion-post-info span {\r\n        font-weight: bold;\r\n    }\r\n    .discussion-byline {\r\n        overflow: hidden;\r\n        height: 1.5em;\r\n        width: 370px;\r\n        white-space: nowrap;\r\n        text-overflow: ellipsis;\r\n    }\r\n    .discussion-stats-header {\r\n        float: left;\r\n        width: 100px;\r\n    }\r\n    .discussion-stats {\r\n        float: right;\r\n        width: 80px;\r\n    }\r\n    .discussion-stats span {\r\n        display: block;\r\n    }\r\n    .discussion-avatar {\r\n        position: absolute;\r\n        width: 64px;\r\n        display: block;\r\n        top: 15px;\r\n        left: 20px;\r\n    }\r\n    .community-clear {\r\n        clear: both;\r\n        height: 1px;\r\n        margin-top: -1px;\r\n    }\r\n    #discussion-pager {\r\n        text-align: center;\r\n        line-height: 24px;\r\n        clear: both;\r\n        margin: 20px 0;\r\n    }\r\n    #discussion-pager a {\r\n        width: auto;\r\n        line-height: 24px;\r\n        padding: 2px 5px;\r\n        color: #333;\r\n        border: 1px solid #ccc;\r\n        margin-left: 3px;\r\n    }\r\n    #discussion-pager a:hover {\r\n        color: #ff6600;\r\n    }\r\n    #discussion-pager .up_page {\r\n        display: inline-block;\r\n        width: 17px !important;\r\n        line-height: 24px;\r\n        height: 20px;\r\n        background: url(/static/tmp-resource/image/up_page.png) no-repeat;\r\n        border: none;\r\n        vertical-align: middle;\r\n    }\r\n    #discussion-pager .next_page {\r\n        display: inline-block;\r\n        width: 17px !important;\r\n        height: 20px;\r\n        background: url(/static/tmp-resource/image/next_page.png) no-repeat;\r\n        border: none;\r\n        margin-left: 13px;\r\n        vertical-align: middle;\r\n    }\r\n    #discussion-pager .page_active {\r\n        color: #ff6600 !important;\r\n    }\r\n    #discussion-pager .page_active:hover {\r\n        color: #ff9933 !important;\r\n    }\r\n    #discussion-pager .page_num {\r\n        display: inline-block;\r\n        padding: 2px 5px;\r\n    }\r\n    div.cke{\r\n        width:580px;\r\n    }\r\n    .community-resource {\r\n        display: block;\r\n        clear: both;\r\n        margin-bottom: 20px;\r\n        border: 0 solid #f0870c;\r\n        height: 160px;\r\n        width: 242px;\r\n        box-shadow: rgba(0, 0, 0, 0.1) 3px 7px 7px 0;\r\n        border-radius: 6px;\r\n        overflow: hidden;\r\n        position: relative;\r\n    }\r\n    .community-resource img {\r\n        display: block;\r\n        width: 242px;\r\n        border-radius: 6px;\r\n    }\r\n    .community-resource a {\r\n        display: block;\r\n        position: absolute;\r\n        bottom: 0;\r\n        left: 0;\r\n        height: 60px;\r\n        background: #f0870c;\r\n        color: #fff;\r\n        font-size: 14px;\r\n        border-radius: 0 0 6px 6px;\r\n    }\r\n    .community-resource div {\r\n        display: table-cell;\r\n        height: 60px;\r\n        vertical-align: middle;\r\n        width: 242px;\r\n        text-align: center;\r\n    }\r\n    #table-members th {\r\n        color: #006EBF;\r\n        padding: 20px 3px;\r\n        font-size: 20px;\r\n    }\r\n    .card-link span {\r\n        color: #FFFFFF;\r\n    }\r\n    .course-card {\r\n        margin: 0 0 20px 0 !important\r\n    }\r\n    div.card-bottom table tr:nth-child(2) {\r\n        display: none;\r\n    }\r\n    #members {\r\n        display: inline-block;\r\n        overflow-x: hidden;\r\n        padding: 10px 0;\r\n        width: 100%;\r\n        position: relative;\r\n    }\r\n    #members a {\r\n        margin-right: 5px;\r\n        display: inline-block;\r\n    }\r\n    #members a img {\r\n        vertical-align: middle;\r\n    }\r\n    .modal {\r\n        position: absolute;\r\n        opacity: 1;\r\n        z-index: 101;\r\n        left: 50%;\r\n        margin-left: -349px;\r\n        top: 40px;\r\n        background: none repeat scroll 0 0 rgba(255, 255, 255, 1);\r\n        border-radius: 5px;\r\n        box-shadow: 0px 15px 80px 15px rgba(0, 0, 0, 0.5);\r\n        padding: 0 0 8px 0;\r\n        width: 680px;\r\n        display: none;\r\n    }\r\n    #fixed-dialog, #skype-dialog {\r\n        position: fixed;\r\n    }\r\n    .modal .close-modal {\r\n        border-radius: 2px;\r\n        cursor: pointer;\r\n        display: inline-block;\r\n        vertical-align: baseline;\r\n        padding: 10px;\r\n        position: absolute;\r\n        right: 2px;\r\n        top: 0;\r\n        z-index: 3;\r\n        color: #333;\r\n    }\r\n    .modal .titlebar {\r\n        height: 70px;\r\n        background: #ccc;\r\n    }\r\n    .modal .dialog-title {\r\n        margin: 0;\r\n        padding: 20px 0 0 30px;\r\n        color: #666;\r\n    }\r\n    .modal .content {\r\n        color: #333;\r\n        text-align: left;\r\n        font-size: 16px;\r\n        padding: 20px 10px;\r\n        line-height: 20px;\r\n    }\r\n    .modal .discussion-error {\r\n        color: #f00;\r\n        font-weight: bold;\r\n        font-size: 120%;\r\n        line-height: 120%;\r\n    }\r\n    .modal .inner-wrapper form textarea {\r\n        height: 100px;\r\n    }\r\n    .hangout_container {\r\n        text-align: center;\r\n        padding-top: 20px;\r\n    }\r\n    .hangout_container img {\r\n        width: 120px;\r\n        vertical-align: top;\r\n    }\r\n    .hangout_container .side-button {\r\n        background: #8cbe41 url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAQAAAAngNWGAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAAAEgAAABIAEbJaz4AAAAJdnBBZwAAABQAAAAUAKM7KtEAAAB2SURBVCjPY/zPQBxgIlIdTRReYfiPFZ5HUsXNMJ/hP24A06P9/8r//4QVpvz/CuHgU8jzfzGCgxvo/b+O4DD+xx3iPxg4iAue38SGoynDZSQeXs9w/p9NjGcgwRPz/zNxChn+a0IC/AoOZVeR4pP7/3zGIZAeAdFoNZxQb6AuAAAAAElFTkSuQmCC) no-repeat 10px 10px;\r\n        height: 20px;\r\n    }\r\n    .side-button {\r\n        color: white !important;\r\n        display: block;\r\n        padding: 10px;\r\n        border-width: 1px;\r\n        border-style: solid;\r\n        text-align: center;\r\n        margin-top: 5px;\r\n    }\r\n    .blue-button {\r\n        border-color: #45719E;\r\n        background: #5A9BD5;\r\n    }\r\n    .green-button {\r\n        border-color: #595;\r\n        background: #8cbe41;\r\n    }\r\n    .red-button {\r\n        border-color: #df0000;\r\n        background: #ED2828;\r\n    }\r\n    #poll-form {\r\n        display: none;\r\n        margin-top: 15px;\r\n        clear: both;\r\n    }\r\n    .poll-answer-input {\r\n        width: 80% !important;\r\n        display: inline !important;\r\n    }\r\n    .discussion-attachment {\r\n        float: left;\r\n        padding-top: 16px;\r\n    }\r\n    .discussion-poll {\r\n        float: right;\r\n        display: block;\r\n        vertical-align: middle;\r\n        padding-top: 16px;\r\n    }\r\n    #members-title {\r\n        border-bottom: 2px solid #90BF70;\r\n        color: #006EBF;\r\n        font-size: 20px;\r\n        padding: 20px 3px;\r\n        font-weight: bold;\r\n        clear: both;\r\n    }\r\n    #table-members {\r\n        width: 100%;\r\n        table-layout: fixed;\r\n        margin-bottom: 20px;\r\n    }\r\n    #table-members tr {\r\n        border-bottom: 2px solid #90BF70;\r\n    }\r\n    .member-arrows {\r\n        width: 20px;\r\n        vertical-align: middle;\r\n    }\r\n    .member-arrows div {\r\n        cursor: pointer;\r\n        width: 17px;\r\n        height: 20px;\r\n    }\r\n    .member-arrow-left {\r\n        background: url(/static/tmp-resource/image/up_page.png);\r\n    }\r\n    .member-arrow-right {\r\n        background: url(/static/tmp-resource/image/next_page.png);\r\n    }\r\n    .member-column {\r\n        white-space: nowrap;\r\n    }\r\n    .discussion-error-box {\r\n        border-color: red !important;\r\n    }\r\n    #create-skype {\r\n        float: left;\r\n        margin: 0 20px 0 0;\r\n    }\r\n    .skype-container {\r\n        float: left;\r\n    }\r\n    .skype-button .side-button {\r\n        background: #5A9BD5 url(https://swx.cdn.skype.com/skypewebsdk/shareButton/v/latest/assets/images/s_logo.svg) no-repeat 10px 10px/20px 20px;\r\n        height: 20px;\r\n    }\r\n</style>\r\n<link rel="stylesheet" type="text/css"  href="static/tmp-resource/css/ppd-general01.css"/>\r\n<body style="text-align:center">\r\n<div id="community-main" class="clearfix">\r\n    <section id="community-main-content">\r\n        <div id="community-header">\r\n')
        # SOURCE LINE 504
        if community.logo:
            # SOURCE LINE 505
            __M_writer(u'                <div id="community-logo"><img src="')
            __M_writer(filters.decode.utf8(get_file_url(community.logo)))
            __M_writer(u'" alt="Community Logo"/></div>\r\n')
        # SOURCE LINE 507
        __M_writer(u'            <h1>')
        __M_writer(filters.decode.utf8(community.name))
        __M_writer(u'</h1>\r\n            <h2>')
        # SOURCE LINE 508
        __M_writer(filters.decode.utf8(community.motto))
        __M_writer(u'</h2>\r\n')
        # SOURCE LINE 509
        if facilitator:
            # SOURCE LINE 510
            __M_writer(u'                <div class="facilitator-wrap">\r\n                    <img src="')
            # SOURCE LINE 511
            __M_writer(filters.decode.utf8(reverse('user_photo', args=[facilitator.user.id])))
            __M_writer(u'" id="community-avatar" alt="Facilitator Avatar" />\r\n                    <h3>')
            # SOURCE LINE 512
            __M_writer(filters.decode.utf8(facilitator.user.first_name))
            __M_writer(u' ')
            __M_writer(filters.decode.utf8(facilitator.user.last_name))
            __M_writer(u'</h3>\r\n                    <h4>Community Facilitator</h4>\r\n                </div>\r\n')
        # SOURCE LINE 516
        __M_writer(u'            <div class="community-clear"></div>\r\n        </div>\r\n\r\n        <div id="community-content-area">\r\n            <div id="community-discussions">\r\n                <a name="discussions"></a>\r\n                <h1 class="discussion-post-info-header">Community Discussion</h1>\r\n                <h1 class="discussion-stats-header">Activity</h1>\r\n                <div class="discussions">\r\n')
        # SOURCE LINE 525
        for i,d in enumerate(discussions):
            # SOURCE LINE 526
            __M_writer(u'                    <div class="discussion">\r\n                        <img class="discussion-avatar" src="')
            # SOURCE LINE 527
            __M_writer(filters.decode.utf8(reverse('user_photo', args=[d.user.id])))
            __M_writer(u'">\r\n                        <div class="discussion-stats">\r\n                            <span>Replies: ')
            # SOURCE LINE 529
            __M_writer(filters.decode.utf8(d.replies))
            __M_writer(u'</span>\r\n                            <span>Views: ')
            # SOURCE LINE 530
            __M_writer(filters.decode.utf8(d.views))
            __M_writer(u'</span>\r\n                        </div>\r\n                        <h2><a href="')
            # SOURCE LINE 532
            __M_writer(filters.decode.utf8(reverse('community_discussion_view', args=[d.id])))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(d.subject))
            __M_writer(u'</a></h2>\r\n                        <div class="discussion-post-info">\r\n                            <div class="discussion-byline"><span>Posted By: </span>')
            # SOURCE LINE 534
            __M_writer(filters.decode.utf8(d.user.first_name))
            __M_writer(u' ')
            __M_writer(filters.decode.utf8(d.user.last_name))
            __M_writer(u'</div>\r\n                            <div class="discussion-date"><span> On: </span>')
            # SOURCE LINE 535
            __M_writer(filters.decode.utf8('{dt:%b}. {dt.day}, {dt.year}'.format(dt=d.date_create)))
            __M_writer(u'</div>\r\n                        </div>\r\n                        <div class="community-clear"></div>\r\n                    </div>\r\n')
        # SOURCE LINE 540
        __M_writer(u'                </div>\r\n                <div id="discussion-pager">\r\n                    <span>Total Discussions: ')
        # SOURCE LINE 542
        __M_writer(filters.decode.utf8(pager['total']))
        __M_writer(u'</span>&nbsp;&nbsp;&nbsp;\r\n')
        # SOURCE LINE 543
        if pager['page'] > 1:
            # SOURCE LINE 544
            __M_writer(u'                        <a href="#discussions" onclick="replaceDiscussions(')
            __M_writer(filters.decode.utf8(pager['page']-1))
            __M_writer(u')" class="up_page"></a>\r\n')
        # SOURCE LINE 546
        for p in pager['jumps']:
            # SOURCE LINE 547
            if p=='c':
                # SOURCE LINE 548
                __M_writer(u'                            <a href="#discussions" onclick="replaceDiscussions(')
                __M_writer(filters.decode.utf8(pager['page']))
                __M_writer(u')" class="page_active">')
                __M_writer(filters.decode.utf8(pager['page']))
                __M_writer(u'</a>\r\n')
                # SOURCE LINE 549
            else:
                # SOURCE LINE 550
                __M_writer(u'                            <a href="#discussions" onclick="replaceDiscussions(')
                __M_writer(filters.decode.utf8(p))
                __M_writer(u')">')
                __M_writer(filters.decode.utf8(p))
                __M_writer(u'</a>\r\n')
        # SOURCE LINE 553
        if pager['pages'] > pager['page']:
            # SOURCE LINE 554
            __M_writer(u'                        <a href="#discussions" onclick="replaceDiscussions(')
            __M_writer(filters.decode.utf8(pager['page']+1))
            __M_writer(u')" class="next_page"></a>\r\n')
        # SOURCE LINE 556
        __M_writer(u'                </div>\r\n            </div>\r\n            <div id="community-content">\r\n                <h1>Content Collections</h1>\r\n                <div id="community-content-scroller">\r\n')
        # SOURCE LINE 561
        for i,cc in enumerate(courses):
            # SOURCE LINE 562
            __M_writer(u'                        ')
            c=course_from_id(cc.course) 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['c'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\r\n                        ')
            # SOURCE LINE 563
            runtime._include_file(context, u'../course.html', _template_uri, course=c)
            __M_writer(u'\r\n')
        # SOURCE LINE 565
        for i,r in enumerate(resources):
            # SOURCE LINE 566
            __M_writer(u'                        <div class="community-resource">\r\n                            <img src="')
            # SOURCE LINE 567
            __M_writer(filters.decode.utf8(get_file_url(r.logo)))
            __M_writer(u'" alt="')
            __M_writer(filters.decode.utf8(r.name))
            __M_writer(u'" />\r\n                            <a href="')
            # SOURCE LINE 568
            __M_writer(filters.decode.utf8(r.link))
            __M_writer(u'" target="_blank">\r\n                                <div>\r\n                                    ')
            # SOURCE LINE 570
            __M_writer(filters.decode.utf8(r.name))
            __M_writer(u'\r\n                                </div>\r\n                            </a>\r\n                        </div>\r\n')
        # SOURCE LINE 575
        __M_writer(u'                </div>\r\n            </div>\r\n        </div>\r\n        \r\n        <div id="members-title">Members</div>\r\n        <table id="table-members" cellspacing="" cellpadding="" border="0">\r\n            <tr>\r\n                <td class="member-arrows">\r\n                    <div class="member-arrow-left" onclick="left()"> </div>\r\n                </td>\r\n                <td class="member-column">\r\n                    <div id="members">\r\n')
        # SOURCE LINE 587
        for u in users:
            # SOURCE LINE 588
            __M_writer(u'                            <a href="')
            __M_writer(filters.decode.utf8(reverse('dashboard',args=[u.user.id])))
            __M_writer(u'" target="_blank">\r\n                                <img src="')
            # SOURCE LINE 589
            __M_writer(filters.decode.utf8(reverse('user_photo',args=[u.user.id])))
            __M_writer(u'" alt="')
            __M_writer(filters.decode.utf8(u.user.first_name))
            __M_writer(u'" />\r\n                            </a>\r\n')
        # SOURCE LINE 592
        __M_writer(u'                    </div>\r\n                </td>\r\n                <td class="member-arrows">\r\n                    <div class="member-arrow-right" onclick="right()"></div>\r\n                </td>\r\n            </tr>\r\n        </table>\r\n    </section>\r\n    <section id="community-main-sidebar">\r\n        <div id="community-sidebar-header">\r\n            ')
        # SOURCE LINE 602
        __M_writer(filters.decode.utf8(request.user.username))
        __M_writer(u'\r\n        </div>\r\n        <div id="community-sidebar">\r\n            <div class="sidebar-section" style="text-align: center;">\r\n                <img src="/static/images/pcg_columns_transparent.png" alt="PCG Logo" />\r\n')
        # SOURCE LINE 607
        if is_member(request.user, community):
            # SOURCE LINE 608
            __M_writer(u'                    <div id="community-member">MEMBER</div>\r\n')
            # SOURCE LINE 609
        else:
            # SOURCE LINE 610
            __M_writer(u'                    <a href="#" class="side-button green-button" onclick="joinMe()">Add Me</a>\r\n')
        # SOURCE LINE 612
        __M_writer(u'            </div>\r\n            <div class="sidebar-section">\r\n                <h2>Community Status</h2>\r\n                <div class="sidebar-sub-section">\r\n                    <span class="status-name">Discussions: ')
        # SOURCE LINE 616
        __M_writer(filters.decode.utf8(total_discussions))
        __M_writer(u'</span>\r\n                    <!--<span class="trending-name">Messages: </span>-->\r\n                    <span class="status-name">Members: ')
        # SOURCE LINE 618
        __M_writer(filters.decode.utf8(users.count()))
        __M_writer(u'</span>\r\n                </div>\r\n            </div>\r\n            <div class="sidebar-section">\r\n                <h2>Trending</h2>\r\n                <div class="sidebar-sub-section">\r\n')
        # SOURCE LINE 624
        for i, d in enumerate(trending):
            # SOURCE LINE 625
            __M_writer(u'                        <span class="trending-title"><a href="')
            __M_writer(filters.decode.utf8(reverse('community_discussion_view', args=[d.id])))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(d.subject))
            __M_writer(u'</a></span>\r\n                        <span class="trending-name"><span>Posted: </span>')
            # SOURCE LINE 626
            __M_writer(filters.decode.utf8('{dt:%b}. {dt.day}, {dt.year}'.format(dt=d.date_create)))
            __M_writer(u'</span>\r\n')
        # SOURCE LINE 628
        __M_writer(u'                </div>\r\n            </div>\r\n            <div class="sidebar-section">\r\n                <a href="')
        # SOURCE LINE 631
        __M_writer(filters.decode.utf8(reverse('communities')))
        __M_writer(u'" class="blue-button side-button">My Communities</a>\r\n')
        # SOURCE LINE 632
        if is_member(request.user, community) or request.user.is_superuser:
            # SOURCE LINE 633
            __M_writer(u'                    <a href="#" class="blue-button side-button" id="newDiscussionButton" onclick="newDiscussion()">Start a New Discussion</a>\r\n')
        # SOURCE LINE 635
        if is_facilitator(request.user, community) or request.user.is_superuser:
            # SOURCE LINE 636
            __M_writer(u'                    <a href="')
            __M_writer(filters.decode.utf8(reverse('community_edit',args=[community.id])))
            __M_writer(u'" class="green-button side-button">Edit</a>\r\n                    <a href="')
            # SOURCE LINE 637
            __M_writer(filters.decode.utf8(reverse('community_delete',args=[community.id])))
            __M_writer(u'" class="red-button side-button delete-icon">Delete</a>\r\n                    <a href="')
            # SOURCE LINE 638
            __M_writer(filters.decode.utf8(reverse('community_mange_member',args=[community.id])))
            __M_writer(u'" class="blue-button side-button">Manage Members</a>\r\n')
        # SOURCE LINE 640
        if has_hangout_perms(request.user) and community.hangout:
            # SOURCE LINE 641
            __M_writer(u'                    <div class="hangout_container" id="hangout_div">\r\n                        <img src="/static/images/community_google_hangouts.png" class="" alt="" />\r\n                        <a class="side-button green-button" href="')
            # SOURCE LINE 643
            __M_writer(filters.decode.utf8(community.hangout))
            __M_writer(u'" target="_blank">Join Hangout</a>\r\n                    </div>\r\n')
        # SOURCE LINE 646
        if request.user.is_superuser:
            # SOURCE LINE 647
            __M_writer(u'                    <div class="skype-button">\r\n                        <a href="#" id="skype-start" class="side-button blue-button">Start Skype Call</a>\r\n                    </div>\r\n')
        # SOURCE LINE 651
        __M_writer(u'            </div>\r\n        </div>\r\n    </section>\r\n</div>\r\n<div style="" id="dialog" class="modal">\r\n    <div class="inner-wrapper" style="border:0;border-radius:5px;padding:0">\r\n        <div class="titlebar">\r\n            <h3 class="dialog-title"></h3>\r\n            <div class="close-modal" id="dialog_close">\u2715</div>\r\n        </div>\r\n        <div class="content"></div>\r\n    </div>\r\n</div>\r\n<div style="" id="fixed-dialog" class="modal">\r\n    <div class="inner-wrapper" style="border:0;border-radius:5px;padding:0">\r\n        <div class="titlebar">\r\n            <h3 class="dialog-title"></h3>\r\n            <div class="close-modal" id="dialog_close">\u2715</div>\r\n        </div>\r\n        <div class="content"></div>\r\n    </div>\r\n</div>\r\n<div style="" id="skype-dialog" class="modal">\r\n    <div class="inner-wrapper" style="border:0;border-radius:5px;padding:0">\r\n        <div class="titlebar">\r\n            <h3 class="dialog-title">Start Skype Call</h3>\r\n            <div class="close-modal" id="dialog_close">\u2715</div>\r\n        </div>\r\n        <div class="content">\r\n            <form>\r\n                <label>Participants (comma separated):<input type="text" name="skype-participants"></label>\r\n                <label>Topic (optional):<input type="text" name="skype-topic"></label>\r\n                <input type="button" value="Create" id="create-skype">\r\n                <div class="skype-container">\r\n                    <script type="text/javascript">\r\n                        function startSkype(params) {\r\n                            var skype_button = Skype.ui(params);\r\n                            if (skype_button) {\r\n                                var id = $(\'.skype-container\').attr(\'id\');\r\n                                $(\'#\' + id + \'_paraElement img\').css({\'margin\': \'0\', \'vertical-align\': \'0\'});\r\n                            }\r\n                        }\r\n                    </script>\r\n                </div>\r\n            </form>\r\n            <div class="community-clear"></div>\r\n        </div>\r\n    </div>\r\n</div>\r\n<script type="text/javascript">\r\n    function joinMe(){\r\n        var user_id = "')
        # SOURCE LINE 702
        __M_writer(filters.decode.utf8(request.user.id))
        __M_writer(u'";\r\n        $.post("')
        # SOURCE LINE 703
        __M_writer(filters.decode.utf8(reverse('community_join', args=[community.id])))
        __M_writer(u'",{user_ids:user_id}, function(r){\r\n            if(r.success)\r\n                window.location.reload();\r\n        });\r\n    }\r\n    function validateDiscussionForm() {\r\n        $(\'.discussion-error-box\').removeClass(\'discussion-error-box\');\r\n        var valid = true;\r\n        var errors = [\'The following errors occurred:\\n\'];\r\n        if (!/[A-Za-z]/.test($(\'.discussion-subject input\').val())) {\r\n            valid = false;\r\n            errors.push(\'Subject is required.\');\r\n            $(\'.discussion-subject input\').addClass(\'discussion-error-box\');\r\n        }\r\n        if (!/[A-Za-z]/.test($(\'.discussion-post textarea\').val())) {\r\n            valid = false;\r\n            errors.push(\'Discussion is required.\');\r\n            $(\'.discussion-post textarea\').addClass(\'discussion-error-box\');\r\n        }\r\n        if ($(\'#new-discussion-submit .poll-add\').is(\':checked\')) {\r\n            if (!/[A-Za-z]/.test($(\'.poll-question\').val())) {\r\n                valid = false;\r\n                errors.push(\'Question is required.\');\r\n                $(\'.poll-question\').addClass(\'discussion-error-box\');\r\n            }\r\n            if ($(\'.poll-answer-input\').length < 2) {\r\n                valid = false;\r\n                errors.push(\'You need at least two answers to choose from.\');\r\n            }\r\n            $(\'.poll-answer-input\').each(function() {\r\n                if (!/[A-Za-z]/.test($(this).val())) {\r\n                    valid = false;\r\n                    errors.push(\'Answers must be filled out.\');\r\n                    $(this).addClass(\'discussion-error-box\');\r\n                    return false;\r\n                }\r\n            });\r\n            if ($(\'.poll-expiration\').val() != \'\' && !/^\\d?\\d\\/\\d?\\d\\/\\d\\d\\d\\d$/.test($(\'.poll-expiration\').val())) {\r\n                valid = false;\r\n                errors.push(\'Expiration date must be in the format mm/dd/yyyy.\');\r\n                $(\'.poll-expiration\').addClass(\'discussion-error-box\');\r\n            }\r\n        }\r\n        if (!valid) {\r\n            var error = errors.join(\'\\n\');\r\n            alert(error);\r\n        }\r\n        return valid;\r\n    }\r\n    function newDiscussion() {\r\n        var content = \'<form id="new-discussion-submit" action="')
        # SOURCE LINE 753
        __M_writer(filters.decode.utf8(reverse('community_discussion_add')))
        __M_writer(u'" method="post" enctype="multipart/form-data">\';\r\n        content += \'<label class="discussion-subject">Subject:<input type="text" name="subject"></label>\';\r\n        content += \'<label class="discussion-post">Discussion:<textarea name="post" id="post"></textarea></label>\';\r\n        content += \'<label class="discussion-attachment">Attachment:<input type="file" name="attachment"></label>\';\r\n        content += \'<label class="discussion-poll"><img src="/static/images/poll-icon.png" alt="Add Poll"> <input type="checkbox" class="poll-add"> Add Poll</label>\';\r\n        content += \'<div id="poll-form">\';\r\n        content += \'<label>Question: <input class="poll-question" type="text" name="question"></label>\';\r\n        content += \'<label>Answers: <ol id="poll-answers">\';\r\n        content += \'<li class="poll-answer">\';\r\n        content += \'<input class="poll-answer-input" type="text" name="answers[0]">\';\r\n        content += \'</li>\';\r\n        content += \'<li class="poll-answer">\';\r\n        content += \'<input class="poll-answer-input" type="text" name="answers[1]"> <input type="button" class="add operation" value="+">\';\r\n        content += \'</li>\';\r\n        content += \'</ol></label>\';\r\n        content += \'<label>Expiration Date: <input class="poll-expiration" type="text" name="expiration" placeholder="mm/dd/yyyy"></label>\';\r\n        content += \'</div>\';\r\n        content += \'<input type="hidden" value="')
        # SOURCE LINE 770
        __M_writer(filters.decode.utf8(community.id))
        __M_writer(u'" name="community_id">\';\r\n        content += \'<input type="hidden" name="csrfmiddlewaretoken" value="')
        # SOURCE LINE 771
        __M_writer(filters.decode.utf8(csrf_token))
        __M_writer(u'"/>\';\r\n        content += \'<div class="community-clear"></div><br/>\';\r\n        content += \'<input type="submit" name="submit" value="Add">\';\r\n        content += \'</form><div class="discussion-error"></div>\';\r\n        var discussion_dialog = new Dialog($(\'#dialog\'));\r\n        discussion_dialog.show(\'New Discussion\', content);\r\n        CKEDITOR.replace(\'post\');\r\n\r\n        $(\'#new-discussion-submit\').submit(function(event) {\r\n            event.preventDefault();\r\n            for (var instanceName in CKEDITOR.instances) {\r\n                CKEDITOR.instances[instanceName].updateElement();\r\n            }\r\n            if (validateDiscussionForm()) {\r\n                var formData = new FormData($(this)[0]);\r\n                var formSelector = $(this);\r\n                $.ajax({\r\n                    url: \'')
        # SOURCE LINE 788
        __M_writer(filters.decode.utf8(reverse('community_discussion_add')))
        __M_writer(u"',\r\n                    type: 'POST',\r\n                    data: formData,\r\n                    async: false,\r\n                    cache: false,\r\n                    contentType: false,\r\n                    processData: false,\r\n                    success: function (data) {\r\n                        if (data.Success) {\r\n                            if ($('#new-discussion-submit .poll-add').is(':checked')) {\r\n                                var pollData = formSelector.serializeArray();\r\n                                pollData[pollData.length] = {name: 'poll_id', 'value': data.DiscussionID};\r\n                                $.post('")
        # SOURCE LINE 800
        __M_writer(filters.decode.utf8(reverse('poll_form_submit', args=['discussion'])))
        __M_writer(u"', pollData, function (data) {\r\n                                    if (data.Success) {\r\n                                        discussion_dialog.hide();\r\n                                        replaceDiscussions(1);\r\n                                    } else {\r\n                                        $('.discussion-error').append('There was an error adding your discussion. Please try again later.')\r\n                                    }\r\n                                });\r\n                            } else {\r\n                                discussion_dialog.hide();\r\n                                replaceDiscussions(1);\r\n                            }\r\n\r\n                        } else {\r\n                            $('.discussion-error').append('There was an error adding your discussion. Please try again later.')\r\n                        }\r\n                    }\r\n                });\r\n            }\r\n        });\r\n\r\n        $('.poll-add').click(function() {\r\n            $('#poll-form').toggle();\r\n        });\r\n        $('.poll-answer .add').click(function() {\r\n            newAnswer();\r\n        });\r\n    }\r\n    function replaceDiscussions(page) {\r\n        $.get('")
        # SOURCE LINE 829
        __M_writer(filters.decode.utf8(reverse('community_discussion_list', args=[community.id])))
        __M_writer(u'\', {\'page\': page}, function(data) {\r\n            var content = \'<div class="discussions">\';\r\n            for (var x = 0; x < data.discussions.length; x++) {\r\n                content += \'<div class="discussion">\';\r\n                content += \'<img class="discussion-avatar" src="\' + data.discussions[x].avatar + \'">\';\r\n                content += \'<div class="discussion-stats">\';\r\n                content += \'<span>Replies: \' + data.discussions[x].replies + \'</span>\';\r\n                content += \'<span>Views: \' + data.discussions[x].views + \'</span>\';\r\n                content += \'</div>\';\r\n                content += \'<h2><a href="\' + data.discussions[x].url + \'">\' + data.discussions[x].subject + \'</a></h2>\';\r\n                content += \'<div class="discussion-post-info">\';\r\n                content += \'<div class="discussion-byline"><span>Posted By: </span>\' + data.discussions[x].first_name + \' \' + data.discussions[x].last_name + \'</div>\';\r\n                content += \'<div class="discussion-date"><span>&nbsp;On: </span>\' + data.discussions[x].date_create + \'</div>\';\r\n                content += \'</div><div class="community-clear"></div></div>\';\r\n            }\r\n            content += \'</div>\';\r\n            $(\'#community-discussions .discussions\').replaceWith(content);\r\n\r\n            content = \'<div id="discussion-pager">\';\r\n            content += \'<span>Total Discussions: \' + data.pager.total + \'</span>&nbsp;&nbsp;&nbsp;\';\r\n            if (data.pager.page > 1) {\r\n                content += \'<a href="#discussions" onclick="replaceDiscussions(\' + (data.pager.page - 1) + \')" class="up_page"></a>\';\r\n            }\r\n            for (var p = 0; p < data.pager.jumps.length; p++) {\r\n                if (data.pager.jumps[p] == \'c\') {\r\n                    content += \'<a href="#discussions" onclick="replaceDiscussions(\' + data.pager.page + \')" class="page_active">\' + data.pager.page + \'</a>\';\r\n                } else {\r\n                    content += \'<a href="#discussions" onclick="replaceDiscussions(\' + data.pager.jumps[p] + \')">\' + data.pager.jumps[p] + \'</a>\';\r\n                }\r\n            }\r\n            if (data.pager.pages > data.pager.page) {\r\n                content += \'<a href="#discussions" onclick="replaceDiscussions(\' + (data.pager.page + 1) + \')" class="next_page"></a>\';\r\n            }\r\n            content += \'</div>\';\r\n            $(\'#discussion-pager\').replaceWith(content);\r\n\r\n            window.history.pushState(page, "')
        # SOURCE LINE 865
        __M_writer(filters.decode.utf8(community.name))
        __M_writer(u'", "')
        __M_writer(filters.decode.utf8(reverse('community_view', args=[community.id])))
        __M_writer(u'?page=" + page);\r\n        });\r\n    }\r\n    function newAnswer() {\r\n        var answer_num = $(\'.poll-answer\').length;\r\n        $(\'.poll-answer\').each(function(index) {\r\n            $(this).find(\'.operation\').replaceWith(\'<input type="button" class="minus operation" value="-" onclick="removeAnswer(\' + index + \')">\');\r\n        });\r\n        var entry = \'<li class="poll-answer">\';\r\n        entry += \'<input class="poll-answer-input" type="text" name="answers[\' + answer_num + \']"> <input type="button" class="add operation" value="+">\';\r\n        entry += \'</li>\';\r\n        $(\'#poll-answers\').append(entry);\r\n        $(\'.poll-answer .add\').click(function() {\r\n            newAnswer();\r\n        });\r\n    }\r\n    function removeAnswer(index) {\r\n        $(\'.poll-answer\').each(function(i) {\r\n            if (i == index) {\r\n                $(this).remove();\r\n            } else {\r\n                var num = 0;\r\n                if (i < index) {\r\n                    num = i;\r\n                }\r\n                if (i > index) {\r\n                    num = i - 1;\r\n                }\r\n                $(this).children(\'.poll-answer-input\').attr(\'name\', \'answers[\' + num + \']\');\r\n            }\r\n        });\r\n        $(\'.poll-answer .minus\').each(function(index) {\r\n            $(this).replaceWith(\'<input type="button" class="minus operation" value="-" onclick="removeAnswer(\' + index + \')">\');\r\n        });\r\n    }\r\n    function isScrolledIntoView(elem, view) {\r\n        var $elem = $(elem);\r\n        var $view = $(view);\r\n        var docViewLeft = $view.offset().left;\r\n        var docViewRight = docViewLeft + $view.width();\r\n        var elLeft = $elem.offset().left;\r\n        var elRight = elLeft + $elem.width();\r\n        // return ((elemRight <= docViewRight) && (elemLeft >= docViewLeft)); // partly visible\r\n        return ((docViewLeft < elLeft) && (docViewRight > elRight));\r\n    }\r\n    function left(){\r\n        var lastHideLeft = null;\r\n        var n=-1;\r\n        $("#members").find("a").each(function(i){\r\n            if(!isScrolledIntoView(this, $("#members"))){\r\n                lastHideLeft=this;\r\n                n=i;\r\n            }else{\r\n                return false;\r\n            }\r\n        });\r\n        if(lastHideLeft) {\r\n            //$(lastHideLeft).css(\'border\',"1px solid #f00");\r\n            $("#members").scrollLeft($("#members").scrollLeft()  + $(lastHideLeft).position().left-1);\r\n        }\r\n    }\r\n    function right(){\r\n        var firstHideRight=null;\r\n        var foundVisible=false;\r\n        var n=-1;\r\n        $("#members").find("a").each(function(i){\r\n            if(!isScrolledIntoView(this, $("#members"))){\r\n                if(foundVisible){\r\n                    firstHideRight=this;\r\n                    n=i;\r\n                    return false;\r\n                }\r\n            }else{\r\n                foundVisible=true;\r\n            }\r\n        });\r\n        if(firstHideRight) {\r\n            $("#members").scrollLeft($("#members").scrollLeft()\r\n                    + $(firstHideRight).position().left\r\n                    - $("#members").width() + $(firstHideRight).width() + 1);\r\n        }\r\n    }\r\n    $(document).ready(function() {\r\n        $("#members").scrollLeft(0);\r\n        $(\'.card-link\').attr(\'target\', \'_blank\');\r\n        $(\'.delete-icon\').click(function(event) {\r\n            event.preventDefault();\r\n            var title = \'Really Delete This Community?\';\r\n            var content = \'If you delete this community, all discussions, memberships and resources will be removed as well. This operation cannot be undone\';\r\n            var continue_url = $(this).attr(\'href\');\r\n            new Dialog($(\'#fixed-dialog\')).showYesNo(title, content, function(ans) {\r\n                this.hide();\r\n                if (!ans) return;\r\n                window.location.href = continue_url;\r\n            });\r\n        });\r\n        $("#newDiscussionButton").click(function(e){\r\n            e.preventDefault();\r\n            scroll(0,0)\r\n        });\r\n        $(\'#skype-start\').click(function(e) {\r\n            e.preventDefault();\r\n            $(\'.skype-container\').attr(\'id\', \'\');\r\n            $(\'.skype-container\').children(\'p\').remove();\r\n            $(\'#create-skype\').off(\'click\');\r\n            var dialog = new Dialog(\'#skype-dialog\');\r\n            dialog.showOverlay();\r\n            dialog.$ei.fadeIn(200);\r\n            $(\'#create-skype\').click(function() {\r\n                var participants = $("input[name=\'skype-participants\']").val().split(/, ?/);\r\n                var topic = $("input[name=\'skype-topic\']").val();\r\n                var skype_params = {\r\n                    name: "call",\r\n                    element: "SkypeButton_Call_" + participants[0] + "_1",\r\n                    participants: participants,\r\n                    imageSize: 24,\r\n                    imageColor: "skype",\r\n                    video: "true",\r\n                    topic: topic\r\n                };\r\n                $(\'.skype-container\').attr(\'id\', \'\');\r\n                $(\'.skype-container\').attr(\'id\', "SkypeButton_Call_" + participants[0] + "_1");\r\n                $(\'.skype-container\').children(\'p\').remove();\r\n                startSkype(skype_params);\r\n            });\r\n        });\r\n    });\r\n</script>\r\n</body>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        community = context.get('community', UNDEFINED)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 13
        __M_writer(u'\r\n    <title>')
        # SOURCE LINE 14
        __M_writer(filters.decode.utf8(community.name))
        __M_writer(u'</title>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


