# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224803.446497
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/static_templates/404.html'
_template_uri = 'static_templates/404.html'
_source_encoding = 'utf-8'
_exports = [u'title']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'../main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        settings = context.get('settings', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 4
        __M_writer(u'\n\n<section class="outside-app">\n<h1>')
        # SOURCE LINE 7
        __M_writer(filters.decode.utf8(_("Page not found")))
        __M_writer(u'</h1>\n<p>')
        # SOURCE LINE 8
        __M_writer(filters.decode.utf8(_('The page that you were looking for was not found. Go back to the {link_start}homepage{link_end} or let us know about any pages that may have been moved at {email}.').format(
    link_start='<a href="/">', link_end='</a>', email='<a href="mailto:{email}">{email}</a>'.format(email=settings.TECH_SUPPORT_EMAIL))))
        # SOURCE LINE 9
        __M_writer(u'</p>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'<title>404</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


