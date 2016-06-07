# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224816.525947
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/course.html'
_template_uri = u'communities/../course.html'
_source_encoding = 'utf-8'
_exports = ['format_courseOrg']


# SOURCE LINE 45

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from courseware.courses import course_image_url, get_course_about_section


# SOURCE LINE 50

correspondOrg={}
correspondOrg['CT Core Standards']='CT'
correspondOrg['Understanding Language Initiative at Stanford']='UL at Stanford'
correspondOrg['Manteca Unified School District']='MUSD'


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 3
    ns = runtime.TemplateNamespace('__anon_0x81b7fd0', context._clean_inheritance_tokens(), templateuri=u'main.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x81b7fd0')] = ns

    # SOURCE LINE 2
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def render_body(context,course,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(course=course,pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x81b7fd0')._populate(_import_ns, [u'stanford_theme_enabled'])
        def format_courseOrg(orgStr):
            return render_format_courseOrg(context.locals_(__M_locals),orgStr)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n<!--@begin:Show wireframes before implementing the functionalities of the page-->\n<!--@date:2013-11-02-->\n<style type="text/css" media="screen">\n  a.btnx:hover {\n  background:#638194;\n  transition-delay: 0s, 0s, 0s;\n  transition-duration: 0.25s, 0.25s, 0.25s;\n  transition-property:color, background,\u200b box-shadow;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  transition-duration:0.25s,\u200b 0.25s,\u200b 0.25s;\n  color:#fff;\n  }\n  a.btnx {\n  background-color:#556370;\n  text-decoration: none;\n  padding-bottom: 7px;\n  padding-left: 10px;\n  padding-right: 10px;\n  padding-top: 7px;\n  cursor: pointer;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n  a.btnx:normal {\n  background-color:#126F9A;\n  text-decoration: none;\n  cursor: pointer;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n  #blocks *{font-family:\'Open Sans\',\u200bArial;}\n  #blocks p{margin-top:10px;}\n/*@begin:tag \'p\' sytle of short_description read from course_overview*/\n/*@date:2013-12-09*/\n  p{line-height:15px;}\n/*@end*/\n</style>\n\n')
        # SOURCE LINE 49
        __M_writer(u'\n')
        # SOURCE LINE 55
        __M_writer(u'\n')
        # SOURCE LINE 62
        __M_writer(u'\n')
        # SOURCE LINE 63
        __M_writer(u'\n<style type="text/css" media="screen">\n  *{font-family: \'Open Sans\'}\n  .course-card{\n    background-color: #FFFFFF;\n    border-radius: 6px;\n    -moz-border-radius: 6px;\n    -webkit-border-radius: 6px;\n    box-shadow: 3px 3px 7px 0px rgba(0,0,0,0.1);\n    float: left;\n    width: 242px;\n    min-height: 242px;\n    margin: 20px;\n    position: relative;\n    cursor: auto!important;\n  }\n  .card-top{position: relative;}\n  .image-style{\n    border-radius: 6px 6px 0px 0px;\n    -moz-border-radius: 6px 6px 0px 0px;\n    -webkit-border-radius: 6px 6px 0px 0px;\n    display: block;\n  }\n  .card-link{\n    display: table-cell;\n    width: 242px;\n    height: 60px;\n    vertical-align: middle;\n    padding: 0 17px;\n    font-size: 22px;\n    color: #FFFFFF;\n    background: rgba(18,111,154,0.95);\n    text-decoration: none!important;\n  }\n  .course-title {\n    display: table;\n    height: 60px;\n    position: absolute;\n    bottom: 0;\n    font-size:14px;\n  }\n</style>\n<script>\n  $(function()\n  {\n    $(".card-link").hover(\n      function () {\n        $(this).find("span").html("<span style=\'margin-right:80px;\'>Course Details</span><span>\u203a</span>");\n      },\n      function () {\n        $(this).find("span").html($(this).attr("title"));\n      });\n      $(".card-link").each(function(){\n        if($(this).height()>60)\n        {\n          $(this).css("fontSize","12px");\n        }\n    });\n  })\n</script>\n\n<div class="course-card" style="cursor:pointer;margin-left:45px;">\n  <div class="card-top">\n    <div><div class="field-items"><figure><img typeof="foaf:Image" class="image-style" src="')
        # SOURCE LINE 126
        __M_writer(filters.decode.utf8(course_image_url(course)))
        __M_writer(u'" width="242" height="150" alt="')
        __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
        __M_writer(u' ')
        __M_writer(filters.decode.utf8(get_course_about_section(course, 'title')))
        __M_writer(u' Cover Image"></figure></div></div>\n    <div class="course-title"><div class="field-content"><a href="')
        # SOURCE LINE 127
        __M_writer(filters.decode.utf8(reverse('cabout', args=[course.id])))
        __M_writer(u'" class="card-link" title="')
        __M_writer(filters.decode.utf8(get_course_about_section(course, 'title')))
        __M_writer(u'"><span>')
        __M_writer(filters.decode.utf8(get_course_about_section(course, 'title')))
        __M_writer(u'</span></a></div></div>  \n  </div>\n    <div class="card-bottom" style="text-align:left;padding:10px 0 0 10px;">\n    <table><tr>\n    <td height="45"><div class="field-content"><span class="course-org" style="font-size:14px;font-weight:bold;color:#146C99">')
        # SOURCE LINE 131
        __M_writer(filters.decode.utf8(format_courseOrg(course.display_organization)))
        __M_writer(u'</span> | <span class="course-number" style="font-size:14px;font-weight:bold;">')
        __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
        __M_writer(u'</span></div>\n    <div class="course-grade" style="font-size:14px;font-weight:bold;margin-top:5px;">')
        # SOURCE LINE 132
        __M_writer(filters.decode.utf8(course.display_grades))
        __M_writer(u'</div></td>\n    <td style="text-align:center;">\n')
        # SOURCE LINE 134
        if course.display_credit:
            # SOURCE LINE 135
            __M_writer(u'      <img src="/static/images/credit.jpg" width="30" height="30" title="Qualifies for Credit"/>\n')
        # SOURCE LINE 137
        __M_writer(u'    </td>\n    </tr>\n    <tr>\n    <td width="190">\n')
        # SOURCE LINE 141
        if course.display_prerequisite:
            # SOURCE LINE 142
            __M_writer(u'        <span style="font-size:12px;">')
            __M_writer(filters.decode.utf8(_("Prerequisite Recommended")))
            __M_writer(u'</span>\n')
        # SOURCE LINE 144
        __M_writer(u'    </td>\n    <td width="40" style="text-align:center;">\n')
        # SOURCE LINE 146
        if course.is_newish:
            # SOURCE LINE 147
            __M_writer(u'        <span style="font-size:10px;background:#99cc33;color:#fff;padding:2px;width:27px;">NEW</span>\n')
        # SOURCE LINE 149
        __M_writer(u'      </td></tr></table>\n</div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_format_courseOrg(context,orgStr):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x81b7fd0')._populate(_import_ns, [u'stanford_theme_enabled'])
        __M_writer = context.writer()
        # SOURCE LINE 56
        __M_writer(u'\n')
        # SOURCE LINE 57
        if correspondOrg.has_key(orgStr):
            # SOURCE LINE 58
            __M_writer(u'    ')
            __M_writer(filters.decode.utf8(correspondOrg[orgStr]))
            __M_writer(u'\n')
            # SOURCE LINE 59
        else:
            # SOURCE LINE 60
            __M_writer(u'    ')
            __M_writer(filters.decode.utf8(orgStr))
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


