# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465221571.732368
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/index.html'
_template_uri = 'index.html'
_source_encoding = 'utf-8'
_exports = [u'js_extra']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 2
from django.core.urlresolvers import reverse 

# SOURCE LINE 3
from time import strftime 

# SOURCE LINE 7
navbar_show_extended=False 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 9
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def js_extra():
            return render_js_extra(context.locals_(__M_locals))
        show_signup_immediately = context.get('show_signup_immediately', UNDEFINED)
        MITX_ROOT_URL = context.get('MITX_ROOT_URL', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n\n')
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        # SOURCE LINE 9
        __M_writer(u'\n<link rel="stylesheet" type="text/css"  href="/static/tmp-resource/css/ppd-general01.css"/>\n<style type="text/css" media="screen">\n  #btn-logged-user{display:none;}\n\n  /*@ mouser up */\n  a.btnxf:hover {\n  background:#6e8194;\n  transition-delay: 0s, 0s, 0s;\n  transition-duration: 0.25s, 0.25s, 0.25s;\n  transition-property:color, background,\u200b box-shadow;\n  transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  transition-duration:0.25s,\u200b 0.25s,\u200b 0.25s;\n  color:#fff;\n  }\n  \n  /*@ background */\n  a.btnxf {\n  background-color:#556370;\n  text-decoration: none;\n  padding-bottom: 7px;\n  padding-left: 10px;\n  padding-right: 10px;\n  padding-top: 7px;\n  cursor: pointer;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  box-shadow: 0px 0px 0px 2px #fff;\n  color:#fff;\n  transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  \n  a.btnxf:normal {\n  background-color:#126F9A;\n  text-decoration: none;\n  cursor: pointer;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n</style>\n<!--@end-->\n\n<!--@begin:Show two horizontal pages on the top-->\n<!--@date:2013-11-02-->\n<div style="text-align:center;border-bottom:1px solid #ccc;padding-bottom:1px;">\n\t<img src="static/images/ppd-index-mainlogo.jpg" width="720" height="205" style="maring:auto"/>\n</div>\n<div style="text-align:center; background:#fff;border-bottom:1px solid #666;">\n  <img src="static/images/ppd-index-maintitle.jpg" width="720" height="62" style="maring:auto"/>\n</div>\n<!--@end-->\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'js_extra'):
            context['self'].js_extra(**pageargs)
        

        # SOURCE LINE 68
        __M_writer(u'\n')
        # SOURCE LINE 69
        if show_signup_immediately is not UNDEFINED:
            # SOURCE LINE 72
            __M_writer(u'<script type="text/javascript">\n  $(window).load(function() {$(\'#signup_action\').trigger("click");});\n</script>\n')
        # SOURCE LINE 76
        __M_writer(u'\n<!--@begin:Two illustrations-->\n<!--@date:2013-11-02-->\n<div id="blocks" style="text-align:center;background:#f7f7f7;padding:25px 0 25px 0;">\n  <div style="width:963px;height:225px;border:1px solid #666;margin:auto;text-align:left;background:#fff;">\n\t<!--@begin:add the video-->\n\t<!--@date:2013-11-15-->\n\t<div id="ppd_video_main" style=" width:950px; height:530px; z-index:99; position:fixed;margin:auto;left:0; right:0; top:0; bottom:0;display:none;">\n      <div id="ppd_video_close" style="width:20px;height:20px;position:absolute;right:0px;cursor:pointer;z-index:1;">\n        <img src="static/images/ppd-video-close01.png" width="20" height="20" onclick="$(\'#frmVideo\')[0].src+=\'\'"/>\n      </div>\n\t  <iframe src="//player.vimeo.com/video/80954694" id="frmVideo" width="950" height="530" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>\n\t</div>\n\t<!--@end-->\n\t<img style="float:left;" src="')
        # SOURCE LINE 90
        __M_writer(filters.decode.utf8(MITX_ROOT_URL))
        __M_writer(u'/static/images/ppd-index-banner-left01.jpg" width="376" height="225"/>\n\t<div style="width:587px;height:225px;float:right;background:url(/static/images/ppd-index-banner-right01.jpg);">\n\n\t  <!--@begin:change font color-->\n\t  <!--@date:2013-11-02-->\n\t  <div class="_banner_index_title_font" style="width:500px;padding-left:32px;padding-top:26px;">PROFESSIONAL DEVELOPMENT COURSES</div>\n\t  <!--@end-->\n\t  \n\t  <!--@begin:add code(class="_body_content_font") to modify font style-->\n\t  <!--@date:2013-11-02-->\n\t  <div class="_banner_index_content_font" style="width:500px;padding-left:32px;padding-top:11px;">\n\t\tExplore our ever-expanding Mathematics and English Language Arts catalog of courses.  \n\t  </div>\t\n\n\t  <div class="_banner_index_content_font" style="width:500px;padding-left:32px;padding-top:7px;">\n\t\tFind a PD course and let\u2019s start building\u2026together. \n\t  </div>\t\n\t  <!--@end-->\n\t  \n\t  <!--@begin:modify button position-->\n\t  <!--@date:2013-11-02-->\n\t  <div style="width:500px;padding-left:32px;padding-top:19px;">\n\t\t<a href="/courses" class="btnxf" style="color:#fff;font-size:11px;text-decoration:none;">VIEW ALL COURSES</a>\n\t  </div>\n\t  <!--@end-->\n\t</div>\n  </div>\n  \n  <div style="width:963px;height:225px;border:1px solid #666;margin:auto;text-align:left;margin-top:25px;background:#fff;">\n\t<img style="float:left;" src="')
        # SOURCE LINE 119
        __M_writer(filters.decode.utf8(MITX_ROOT_URL))
        __M_writer(u'/static/images/ppd-index-banner-left02.jpg" width="376" height="225"/>\n\t<div style="width:587px;height:225px;float:right;background:url(/static/images/ppd-index-banner-right02.jpg);">\n\t  \n\t  <!--@begin:change font color-->\n\t  <!--@date:2013-11-02-->\n\t  <div class="_banner_index_title_font" style="width:500px;padding-left:32px;padding-top:41px;">WHAT IS PEPPER?</div>\n\t  <!--@end-->\n\t  \n\t  <!--@begin:add code(class="_body_content_font") to modify font style-->\n\t  <!--@date:2013-11-02-->\n\t  <div class="_banner_index_content_font" style="width:500px;padding-left:32px;padding-top:11px;">\n\t\tUse the latest in peer-to-peer social learning tools and connect with motivated and passionate educators - just like you - from around the nation.\n\t  </div>\n\t  <div class="_banner_index_content_font" style="width:500px;padding-left:32px;padding-top:7px;">\n\t\tWork at your own pace to become a Common Core specialist.\n\t  </div>\n\t  <!--@end-->\n\n\t  <!--@begin:modify button position,button content-->\n\t  <!--@date:2013-11-02-->\n\t  <div id="ppd_btn_video" style="width:500px;padding-left:32px;padding-top:19px;">\n\t\t<a href="javascript:void(0)" class="btnxf" style="color:#fff;font-size:11px !important;text-decoration:none;">WATCH PEPPER VIDEO</a>\n\t  </div>\n\t  <!--@end-->\n\t</div>\n  </div>\n</div>\n<!--@end-->\n\n<!--@begin:add jq/js code to control the video-->\n<!--@date:2013-11-15-->\n<script>\njQuery(function($){\n\tvar id_ppd_video_main = document.getElementById(\'ppd_video_main\');\n\tvar id_ppd_btn_video = document.getElementById(\'ppd_btn_video\');\n\tvar id_ppd_video_close = document.getElementById(\'ppd_video_close\');\n\t\n\tid_ppd_btn_video.onmousedown = function()\n\t{\n\t\t$("#ppd_video_main").fadeIn(600);\n\t\t//document.getElementById(\'sampleMovie\').play();\n\t}\n\t\n\tid_ppd_video_close.onmousedown = function()\n\t{\n\t\t$("#ppd_video_main").fadeOut(300);\n\t\t//document.getElementById(\'sampleMovie\').pause();\n\t\t//document.getElementById(\'sampleMovie\').currentTime = 0;\n\t}\n});\n</script>\n<!--@end-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js_extra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def js_extra():
            return render_js_extra(context)
        __M_writer = context.writer()
        # SOURCE LINE 60
        __M_writer(u'\n   <script type="text/javascript">\n      $(window).load(function() {\n         if(getParameterByName(\'next\')) {\n              $(\'#login\').trigger("click");\n         }\n      })\n   </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


