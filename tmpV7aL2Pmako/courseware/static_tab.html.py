# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465228647.435243
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/static_tab.html'
_template_uri = 'courseware/static_tab.html'
_source_encoding = 'utf-8'
_exports = [u'headextra', u'bodyclass', u'title']


# SOURCE LINE 1
from django.contrib.auth.models import User 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'/static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        is_global = context.get('is_global', UNDEFINED)
        def bodyclass():
            return render_bodyclass(context.locals_(__M_locals))
        def title():
            return render_title(context.locals_(__M_locals))
        int = context.get('int', UNDEFINED)
        request = context.get('request', UNDEFINED)
        course = context.get('course', UNDEFINED)
        static = _mako_get_namespace(context, 'static')
        tab = context.get('tab', UNDEFINED)
        def headextra():
            return render_headextra(context.locals_(__M_locals))
        tab_contents = context.get('tab_contents', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'bodyclass'):
            context['self'].bodyclass(**pageargs)
        

        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'headextra'):
            context['self'].headextra(**pageargs)
        

        # SOURCE LINE 8
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 10
        __M_writer(u'\n')
        # SOURCE LINE 11

        def get_portfolio_user():
          if request.GET.get('pf_id') != None:
            return User.objects.get(id=int(request.GET.get('pf_id')))
          else:
            return None
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['get_portfolio_user'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 17
        __M_writer(u'\n')
        # SOURCE LINE 18
        if not is_global:
            # SOURCE LINE 19
            runtime._include_file(context, u'/courseware/course_navigation.html', _template_uri, active_page='static_tab_{0}'.format(tab['url_slug']),portfolio_user=get_portfolio_user())
            __M_writer(u'\n')
        # SOURCE LINE 21
        __M_writer(u'\n<section class="container">\n  <div class="static_tab_wrapper">\n    ')
        # SOURCE LINE 24
        __M_writer(filters.decode.utf8(tab_contents))
        __M_writer(u'\n  </div>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headextra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def headextra():
            return render_headextra(context)
        static = _mako_get_namespace(context, 'static')
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 7
            __M_writer(filters.decode.utf8(static.css(group=u'course')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bodyclass(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        course = context.get('course', UNDEFINED)
        def bodyclass():
            return render_bodyclass(context)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(course.css_class))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        course = context.get('course', UNDEFINED)
        tab = context.get('tab', UNDEFINED)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'<title>')
        __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
        __M_writer(u' ')
        __M_writer(filters.decode.utf8(tab['name']))
        __M_writer(u'</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


