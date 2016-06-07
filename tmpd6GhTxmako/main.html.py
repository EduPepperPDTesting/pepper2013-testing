# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223427.712847
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/main.html'
_template_uri = u'main.html'
_source_encoding = 'utf-8'
_exports = [u'bodyclass', u'bodyextra', u'title', 'stanford_theme_enabled', u'js_extra', 'theme_enabled', 'login_query', u'headextra']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 4
from django.utils import html 

# SOURCE LINE 77

navbar_show_extended=True


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def bodyclass():
            return render_bodyclass(context.locals_(__M_locals))
        settings = context.get('settings', UNDEFINED)
        self = context.get('self', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        def stanford_theme_enabled():
            return render_stanford_theme_enabled(context.locals_(__M_locals))
        course = context.get('course', UNDEFINED)
        def js_extra():
            return render_js_extra(context.locals_(__M_locals))
        static = _mako_get_namespace(context, 'static')
        def theme_enabled():
            return render_theme_enabled(context.locals_(__M_locals))
        suppress_toplevel_navigation = context.get('suppress_toplevel_navigation', UNDEFINED)
        def bodyextra():
            return render_bodyextra(context.locals_(__M_locals))
        def headextra():
            return render_headextra(context.locals_(__M_locals))
        MITX_ROOT_URL = context.get('MITX_ROOT_URL', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 12
        __M_writer(u'\n\n')
        # SOURCE LINE 16
        __M_writer(u'\n\n<!DOCTYPE html>\n<html>\n<head>\n\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 41
        __M_writer(u'\n\n  <script type="text/javascript" src="/jsi18n/"></script>\n\n  <link rel="icon" type="image/x-icon" href="')
        # SOURCE LINE 45
        __M_writer(filters.decode.utf8(static.url(settings.FAVICON_PATH)))
        __M_writer(u'" />\n\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 47
            __M_writer(filters.decode.utf8(static.css(group=u'application')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 49
            __M_writer(filters.decode.utf8(static.js(group=u'main_vendor')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'headextra'):
            context['self'].headextra(**pageargs)
        

        # SOURCE LINE 50
        __M_writer(u'\n')
        # SOURCE LINE 51
        if theme_enabled():
            # SOURCE LINE 52
            __M_writer(u'    ')
            runtime._include_file(context, u'theme-head-extra.html', _template_uri)
            __M_writer(u'\n')
        # SOURCE LINE 54
        __M_writer(u'\n  <!--[if lt IE 9]>\n  <script src="')
        # SOURCE LINE 56
        __M_writer(filters.decode.utf8(static.url('js/html5shiv.js')))
        __M_writer(u'"></script>\n  <![endif]-->\n\n  <!--[if lte IE 9]>\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 60
            __M_writer(filters.decode.utf8(static.css(group=u'ie-fixes')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n  <![endif]-->\n  <meta name="path_prefix" content="')
        # SOURCE LINE 62
        __M_writer(filters.decode.utf8(MITX_ROOT_URL))
        __M_writer(u'">\n  <meta name="google-site-verification" content="_mipQ4AtZQDNmbtOkwehQDOgCxUUV2fb_C0b6wbiRHY" />\n\n')
        # SOURCE LINE 65
        if not course:
            # SOURCE LINE 66
            if theme_enabled():
                # SOURCE LINE 67
                __M_writer(u'      ')
                runtime._include_file(context, u'theme-google-analytics.html', _template_uri)
                __M_writer(u'\n')
                # SOURCE LINE 68
            else:
                # SOURCE LINE 69
                __M_writer(u'      ')
                runtime._include_file(context, u'google_analytics.html', _template_uri)
                __M_writer(u'\n')
        # SOURCE LINE 72
        __M_writer(u'\n  ')
        # SOURCE LINE 73
        runtime._include_file(context, u'widgets/segment-io.html', _template_uri)
        __M_writer(u'\n\n</head>\n\n')
        # SOURCE LINE 79
        __M_writer(u'\n\n<body class="')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'bodyclass'):
            context['self'].bodyclass(**pageargs)
        

        # SOURCE LINE 81
        __M_writer(u'">\n\n')
        # SOURCE LINE 83
        if theme_enabled():
            # SOURCE LINE 84
            __M_writer(u'  ')
            runtime._include_file(context, u'theme-header.html', _template_uri)
            __M_writer(u'\n')
            # SOURCE LINE 85
        elif not suppress_toplevel_navigation:
            # SOURCE LINE 86
            __M_writer(u'  ')
            runtime._include_file(context, u'navigation.html', _template_uri, show_extended=self.attr.navbar_show_extended)
            __M_writer(u'\n')
        # SOURCE LINE 88
        __M_writer(u'  \n<!--@begin:Main module page, change the bottom margin in the body text-->\n<!--@date:2013-11-02-->\n  <section class="content-wrapper" style="padding-bottom:0px;">\n    ')
        # SOURCE LINE 92
        __M_writer(filters.decode.utf8(self.body()))
        __M_writer(u'\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'bodyextra'):
            context['self'].bodyextra(**pageargs)
        

        # SOURCE LINE 93
        __M_writer(u'\n  </section>\n<!--@end-->\n\n')
        # SOURCE LINE 97
        if theme_enabled():
            # SOURCE LINE 98
            __M_writer(u'  ')
            runtime._include_file(context, u'theme-footer.html', _template_uri)
            __M_writer(u'\n')
            # SOURCE LINE 99
        elif not suppress_toplevel_navigation:
            # SOURCE LINE 100
            __M_writer(u'  ')
            runtime._include_file(context, u'footer.html', _template_uri)
            __M_writer(u'\n')
        # SOURCE LINE 102
        __M_writer(u'\n\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 104
            __M_writer(filters.decode.utf8(static.js(group=u'application')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 105
            __M_writer(filters.decode.utf8(static.js(group=u'module-js')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'js_extra'):
            context['self'].js_extra(**pageargs)
        

        # SOURCE LINE 106
        __M_writer(u'\n\n</body>\n</html>\n\n')
        # SOURCE LINE 116
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bodyclass(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def bodyclass():
            return render_bodyclass(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bodyextra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def bodyextra():
            return render_bodyextra(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def stanford_theme_enabled():
            return render_stanford_theme_enabled(context)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 22
        __M_writer(u'\n')
        # SOURCE LINE 23
        if stanford_theme_enabled():
            # SOURCE LINE 24
            __M_writer(u'      <title>')
            __M_writer(filters.decode.utf8(_("Home")))
            __M_writer(u' | class.stanford.edu</title>\n')
            # SOURCE LINE 25
        else:
            # SOURCE LINE 27
            __M_writer(u'<!--@begin:Main module page, change the title-->\n<!--@date:2013-11-02-->      \n      <title>Pepper</title>\n<!--@end-->\n\n      <script type="text/javascript">\n        /* immediately break out of an iframe if coming from the marketing website */\n        (function(window) {\n          if (window.location !== window.top.location) {\n            window.top.location = window.location;\n          }\n        })(this);\n      </script>\n')
        # SOURCE LINE 41
        __M_writer(u'  ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_stanford_theme_enabled(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        getattr = context.get('getattr', UNDEFINED)
        def theme_enabled():
            return render_theme_enabled(context)
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 14
        __M_writer(u'\n  ')
        # SOURCE LINE 15
        return theme_enabled() and getattr(settings, "THEME_NAME") == "stanford" 
        
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js_extra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def js_extra():
            return render_js_extra(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_theme_enabled(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'\n  ')
        # SOURCE LINE 11
        return settings.MITX_FEATURES["USE_CUSTOM_THEME"] 
        
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_login_query(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        course_id = context.get('course_id', UNDEFINED)
        enrollment_action = context.get('enrollment_action', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 111
        __M_writer(filters.decode.utf8(
  "?course_id={0}&enrollment_action={1}".format(
    html.escape(course_id),
    html.escape(enrollment_action)
  ) if course_id and enrollment_action else ""
))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headextra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def headextra():
            return render_headextra(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


