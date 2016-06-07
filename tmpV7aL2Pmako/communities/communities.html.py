# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224802.435851
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/communities/communities.html'
_template_uri = 'communities/communities.html'
_source_encoding = 'utf-8'
_exports = [u'title']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 2

from django.core.urlresolvers import reverse
from courseware.courses import course_image_url, get_course_about_section
from courseware.access import has_access
from certificates.models import CertificateStatuses
from xmodule.modulestore import MONGO_MODULESTORE_TYPE
from xmodule.modulestore.django import modulestore
from student.models import State,District,Transaction,Cohort,School,SubjectArea,GradeLevel,YearsInEducation, UserProfile, User
from baseinfo.models import Enum
from communities.models import CommunityCommunities, CommunityUsers
from communities.views import user_in_community, community_in_state, community_in_district



# SOURCE LINE 15
navbar_show_extended=False 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 17
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'../static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'../main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        communities = context.get('communities', UNDEFINED)
        request = context.get('request', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 14
        __M_writer(u'\n')
        # SOURCE LINE 15
        __M_writer(u'\n')
        # SOURCE LINE 16
        __M_writer(u'\n')
        # SOURCE LINE 17
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 18
        __M_writer(u'\n<link rel="stylesheet" type="text/css"  href="/static/tmp-resource/css/ppd-general01.css"/>\n\n<style type="text/css" media="screen">\n    a.district-button, a.school-button, a.user-button {\n            outline: none;\n        }\n\n        .section-tab.public {\n            border-color: rgb(103, 141, 11) rgb(103, 141, 11) rgb(83, 121, 11);\n            box-shadow: 0 1px 0 0 rgb(123, 221, 91) inset;\n            background-color: rgb(123, 181, 51);\n            background-image: linear-gradient(to bottom, rgb(123, 221, 91) 0%, rgb(123, 181, 51) 50%, rgb(103, 161, 31) 50%, rgb(103, 161, 31) 100%);\n            text-shadow: 0 -1px 1px rgb(83, 121, 11);\n        }\n        .section-tab.private {\n            border-color: rgb(47, 107, 189) rgb(47, 107, 189) rgb(47, 87, 169);\n            box-shadow: 0 1px 0 0 rgb(47, 207, 269) inset;\n            background-color: rgb(47, 167, 229);\n            background-image: linear-gradient(to bottom, rgb(47, 207, 269) 0%, rgb(47, 167, 229) 50%, rgb(47, 147, 209) 50%, rgb(47, 147, 209) 100%);\n            text-shadow: 0 -1px 1px rgb(47, 87, 169);\n            padding-top: 10px;\n        }\n        .section-tab.mydistrict {\n            border-color: rgb(174, 50, 7) rgb(174, 50, 7) rgb(154, 30, 7);\n            box-shadow: 0 1px 0 0 rgb(294, 170, 67) inset;\n            background-color: rgb(234, 110, 7);\n            background-image: linear-gradient(to bottom, rgb(294, 170, 67) 0%, rgb(234, 110, 7) 50%, rgb(214, 90, 7) 50%, rgb(214, 90, 7) 100%);\n            text-shadow: 0 -1px 1px rgb(154, 30, 7);\n        }\n\n    .section-tab {\n            border-width: 0 1px 1px 1px;\n            border-style: solid;\n            -moz-border-top-colors: none;\n            -moz-border-right-colors: none;\n            -moz-border-bottom-colors: none;\n            -moz-border-left-colors: none;\n            border-image: none;\n            border-radius: 0 0 5px 5px;\n            color: #FFF;\n            display: inline-block;\n            text-align: center;\n            text-decoration: none;\n            font: 1.2rem/1.6rem "Open Sans",Verdana,Geneva,sans-serif;\n            letter-spacing: 1px;\n            padding: 4px 20px;\n            text-transform: uppercase;\n            vertical-align: top;\n            margin-left: 5px;\n        }\n    #page-nav,#page-footer {\n        width: 1180px;\n    }\n    #btn-logged-user{\n        display: none;\n    }\n    .form-select {\n        font-size: 14px !important;\n        width: 180px;\n    }\n    .image-link-style {\n        border-radius: 6px;\n        -moz-border-radius: 6px;\n        -webkit-border-radius: 6px;\n        display: block;\n        float: left;\n        margin: 30px;\n        width:240px;\n        height:150px;\n        background-size: auto 100px;\n        background-color: white;\n        background-position: 50% 0;\n        background-repeat: no-repeat;\n    }\n    .image-bottom-style {\n        border-radius: 0 0 6px 6px;\n        -moz-border-radius: 0 0 6px 6px;\n        -webkit-border-radius: 0 0 6px 6px;\n        display: block;\n    }\n    .card-link {\n        display: table-cell;\n        width: 240px;\n        height: 60px;\n        vertical-align: middle;\n        padding: 0 17px;\n        font-size: 22px;\n        background: rgba(18,111,154,0.95);\n        text-decoration: none !important;\n    }\n    .card-link span {\n        color: #FFFFFF;\n    }\n    .data_import_top {\n    padding-top: 20px;\n}\n\n.data_import_content {\n    margin: auto;\n    background: #e4e4e4;\n    width: 960px;\n}\n    .grade_title {\n        float: left;\n        width: 920px;\n        height: 20px;\n        background-color: #fff;\n        text-align: left;\n        padding-left: 40px;\n        color: #666;\n        font-size: 16px;\n        font-weight: bold;\n        font-family: "Open Sans",Verdana,Geneva,sans-serif;\n        padding-top: 4px;\n        padding-bottom: 2px;\n    }\n    a.btnx:hover {\n        background: #638194;\n        transition-delay: 0s, 0s, 0s;\n        transition-duration: 0.25s, 0.25s, 0.25s;\n        transition-property:color, background,\u200bbox-shadow;\n        transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n        color: #fff;\n    }\n    a.btnx {\n        background-color: #556370;\n        padding-bottom: 2px !important;\n        padding-left: 10px;\n        padding-right: 10px;\n        padding-top: 2px !important;\n        text-decoration: none !important;\n        cursor: pointer;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        color: #fff;\n        transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n    }\n    a.btnx:normal {\n        background-color: #126F9A;\n        text-decoration: none;\n        cursor: pointer;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        color: #fff;\n        transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n    }\n    div.expand_title {\n            color: #08a;\n            font-size: 20px;\n            padding: 5px 5px 10px 5px;\n            cursor: pointer;\n            background-color: #ccc;\n            box-shadow: 0 1px 0 0 #fff inset;\n            background-image: linear-gradient(to bottom, #fff 0%, #ddd 50%, #ccc 50%, #ccc 100%);\n            text-shadow: 0 -1px 1px #aaa;\n        }\n\n        div.expand_title .icon {\n            display: inline-block;\n            position: relative;\n            top: 5px;\n            width: 23px;\n            height: 23px;\n            background: url("../images/arrows.png") no-repeat 0 0;\n        }\n    div.expand_div{\n        display:block !important;\n    }\n</style>\n<script>\n    function fsubmit(){\n        var communities = [];\n')
        # SOURCE LINE 189
        for community in communities:
            # SOURCE LINE 190
            __M_writer(u'            communities[')
            __M_writer(filters.decode.utf8(community['id']))
            __M_writer(u'] = "')
            __M_writer(filters.decode.utf8(reverse('community_view', args=[community['id']])))
            __M_writer(u'";\n')
        # SOURCE LINE 192
        __M_writer(u'        var community = $("#community_list_form .form-select").val();\n        window.location.href =  communities[community];\n        return false;\n    }\n</script>\n<section class="find-courses" style="text-align:center;background:#F5F5F5;">\n    <!--@begin:use new image name(ppd-...); use (background:url..) replace <img src=...>-->\n    <!--@date:2013-11-02-->\n    <div style="margin:0 auto;width:960px;height:195px;background:url(/static/images/ppd-courses-banner.jpg);border-bottom:1px solid #000;">\n        <!--@end-->\n\n        <!--@begin:use html text to replace the text on the picture; add code(class="_...") to modify font style-->\n        <!--@date:2013-11-02-->\n        <div class="_banner_whatis_title_font">\n            PROFESSIONAL\n            <br/>\n            LEARNING COMMUNITIES\n            <div class="_banner_whatis_title_content_font">\n                build and enhance your community of practice\n            </div>\n        </div>\n        <!--@end-->\n    </div>\n\n    <section style="margin:auto;text-align:center;width:960px;background:#E6F5FC;">\n        <form method="" id="community_list_form" action="">\n            <div style="padding:20px;color:#666;display:inline-block;">\n                <span style="color:#666">Find a Community</span>\n            </div>\n            <div style="display:inline-block;padding:0 1em 0 0;">\n                <select name="subject_id" class="form-select">\n')
        # SOURCE LINE 223
        for community in communities:
            # SOURCE LINE 224
            __M_writer(u'                        <option value="')
            __M_writer(filters.decode.utf8(community['id']))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(community['name']))
            __M_writer(u'</option>\n')
        # SOURCE LINE 226
        __M_writer(u'                </select>\n            </div>\n            <a href="#" class="btnx" onClick="fsubmit();">Find</a>\n')
        # SOURCE LINE 229
        if request.user.is_superuser:
            # SOURCE LINE 230
            __M_writer(u'                <div style="padding:20px;color:#666;display:inline-block;">\n                    <span style="color:#666"><a href="')
            # SOURCE LINE 231
            __M_writer(filters.decode.utf8(reverse('community_add')))
            __M_writer(u'">Create a New Community</a></span>\n                </div>\n')
        # SOURCE LINE 234
        __M_writer(u'        </form>\n    </section>\n    <!-- Begin Tabs -->\n\n<div class="data_import_top">\n  <div class="main, data_import_content">\n    <div class="expand_title expand_title_collapse">\n      Pepper Communities <div class="icon"></div>\n    </div>\n\n      <div class="expand_div">\n        <a href="#" onclick="toggle(\'private\')" class="private-button"><div class="section-tab private">My Communities</div></a>\n        <a href="#" onclick="toggle(\'public\')" class="public-button"><div class="section-tab public">Public Communities</div></a>\n        <a href="#" onclick="toggle(\'mydistrict\')" class="mydistrict-button"><div class="section-tab mydistrict">My District Communities</div></a>\n        <div class="private-section import-section">\n            <section style="margin:auto;width:960px;background:#E4E4E4;">\n                <section class="courses" style="padding-top:5px!important;">\n                    <div class="courses-listing">\n                        <div style="padding-left:25px;">\n')
        # SOURCE LINE 253
        for community in communities:
            # SOURCE LINE 254
            if user_in_community(community['id'], request.user.id):
                # SOURCE LINE 255
                __M_writer(u'                                    <div class="image-link-style" style="background-image: url(\'')
                __M_writer(filters.decode.utf8(community['logo']))
                __M_writer(u'\');">\n                                        <div style="height:100px;"></div>\n                                        <a href="')
                # SOURCE LINE 257
                __M_writer(filters.decode.utf8(reverse('community_view', args=[community['id']])))
                __M_writer(u'" class="card-link image-bottom-style"><span>')
                __M_writer(filters.decode.utf8(community['name']))
                __M_writer(u'</span></a>\n                                    </div>\n')
        # SOURCE LINE 261
        __M_writer(u'                        </div>\n                    </div>\n                </section>\n            </section>\n        </div>\n        <div class="public-section import-section">\n            <section style="margin:auto;width:960px;background:#E4E4E4;">\n                <section class="courses" style="padding-top:5px!important;">\n                    <div class="courses-listing">\n                        <div style="padding-left:25px;">\n')
        # SOURCE LINE 271
        for community in communities:
            # SOURCE LINE 272
            if community['private'] == 0:
                # SOURCE LINE 273
                __M_writer(u'                                    <div class="image-link-style" style="background-image: url(\'')
                __M_writer(filters.decode.utf8(community['logo']))
                __M_writer(u'\');">\n                                        <div style="height:100px;"></div>\n                                        <a href="')
                # SOURCE LINE 275
                __M_writer(filters.decode.utf8(reverse('community_view', args=[community['id']])))
                __M_writer(u'" class="card-link image-bottom-style"><span>')
                __M_writer(filters.decode.utf8(community['name']))
                __M_writer(u'</span></a>\n                                    </div>\n')
        # SOURCE LINE 279
        __M_writer(u'                        </div>\n                    </div>\n                </section>\n            </section>\n        </div>\n    <div class="mydistrict-section import-section">\n            <section style="margin:auto;width:960px;background:#E4E4E4;">\n                <section class="courses" style="padding-top:5px!important;">\n                    <div class="courses-listing">\n                        <div style="padding-left:25px;">\n')
        # SOURCE LINE 289
        for community in communities:
            # SOURCE LINE 290
            if community_in_district(community['id'], request.user.id):
                # SOURCE LINE 291
                __M_writer(u'                                    <div class="image-link-style" style="background-image: url(\'')
                __M_writer(filters.decode.utf8(community['logo']))
                __M_writer(u'\');">\n                                        <div style="height:100px;"></div>\n                                        <a href="')
                # SOURCE LINE 293
                __M_writer(filters.decode.utf8(reverse('community_view', args=[community['id']])))
                __M_writer(u'" class="card-link image-bottom-style"><span>')
                __M_writer(filters.decode.utf8(community['name']))
                __M_writer(u'</span></a>\n                                    </div>\n')
        # SOURCE LINE 297
        __M_writer(u'                        </div>\n                    </div>\n                </section>\n            </section>\n    </div>\n</div>\n      </div></div>\n    <!-- End Tabs -->\n\n</section>\n<script>\n$(document).ready(function(){\n   $(".public-button, .private-button, .mystate-button, .mydistrict-button").click(function(e){\n       e.preventDefault();\n   });\n    toggle("private");\n});\nfunction toggle(which) {\n    $(".import-section").hide();\n    $("." + which + "-section").show();\n    $(".section-tab").css("padding-top", "4px");\n    $(".section-tab." + which).css("padding-top", "10px")\n}\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 18
        __M_writer(u'<title>Communities</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


