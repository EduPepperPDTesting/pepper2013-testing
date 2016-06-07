# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229650.300758
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/static_templates/server-error.html'
_template_uri = 'static_templates/server-error.html'
_source_encoding = 'utf-8'
_exports = []


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
        __M_writer = context.writer()
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n<section class="outside-app">\n  <h1>')
        # SOURCE LINE 5
        __M_writer(filters.decode.utf8(_("There has been a 500 error on the <em>{platform_name}</em> servers").format(platform_name=settings.PLATFORM_NAME)))
        __M_writer(u'</h1>\n  <p>')
        # SOURCE LINE 6
        __M_writer(filters.decode.utf8(_('Please wait a few seconds and then reload the page. If the problem persists, please email us at <a href="{email}">{email}</a>.').format(email=settings.TECH_SUPPORT_EMAIL)))
        __M_writer(u'</p>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


