# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223499.54088
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/footer.html'
_template_uri = u'footer.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 2
from django.core.urlresolvers import reverse 

# SOURCE LINE 3
from django.utils.translation import ugettext as _ 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        MITX_ROOT_URL = context.get('MITX_ROOT_URL', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n<style>\n .nav-colophon li{line-height:45px;}\n .nav-colophon a.logo{transition:none !important;border-bottom:none;margin:0 0 0 20px;}\n .nav-colophon a.logo:hover,.nav-colophon a.logo:active{border:none !important;}\n .nav-colophon a.logo img{vertical-align:bottom;}\n</style>\n\n<div class="wrapper wrapper-footer" style="border-top:1px solid #8a8c8f;box-shadow:0 -1px 5px 0 rgba(0, 0, 0, 0.1);z-index:11">\n  <footer id="page-footer">\n    <div class="colophon" style="width:600px;">\n      <nav class="nav-colophon">\n        <ol>\n          <li class="nav-colophon-03">\n            <a id="press" href="/press"> ')
        # SOURCE LINE 19
        __M_writer(filters.decode.utf8(_("Press")))
        __M_writer(u' </a>\n          </li>\n          <li class="nav-colophon-04">\n            <a id="faq" href="/faq"> ')
        # SOURCE LINE 22
        __M_writer(filters.decode.utf8(_("FAQ")))
        __M_writer(u' </a>\n          </li>\n          <li class="nav-colophon-05">\n            <a id="contact" href="/contact"> ')
        # SOURCE LINE 25
        __M_writer(filters.decode.utf8(_("Contact")))
        __M_writer(u' </a>\n          </li>\n          <li>\n            <a href="https://twitter.com/Pepper_PD" target="_blank" class="logo"><img src="/static/images/twitter_bird_logo.png" width="50"/></a>\n          </li>\n          <li>\n            <a href="https://www.facebook.com/PepperPD" target="_blank" class="logo"><img src="/static/images/facebook_logo.png" width="50"/></a>\n          </li>\n          <li>\n            <a href="https://www.linkedin.com/groups?mostRecent=&gid=6742057&trk=my_groups-tile-flipgrp" target="_blank" class="logo"><img src="/static/images/linkedin-logo.jpg" width="50"/></a>\n          </li>\n          <li>\n            <a href="https://www.youtube.com/channel/UCIgkrFJRifhIN5Thpw5MUFQ" target="_blank" class="logo"><img src="/static/images/new_youtube_logo.png" width="50"/></a>\n          </li>\n        </ol>\n      </nav>\n    </div>\n    <img style="float:right;" src="')
        # SOURCE LINE 42
        __M_writer(filters.decode.utf8(MITX_ROOT_URL))
        __M_writer(u'/static/images/pcgeducationdown.jpg" width="285" height="58"/>\n    <div class="references">\n    </div>\n  </footer>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


