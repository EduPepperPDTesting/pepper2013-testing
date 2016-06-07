# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218891.761888
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/discussion/_js_head_dependencies.html'
_template_uri = u'courseware/../discussion/_js_head_dependencies.html'
_source_encoding = 'utf-8'
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 1
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'../static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        static = _mako_get_namespace(context, 'static')
        __M_writer = context.writer()
        __M_writer(u'\n\n<script type="text/javascript" src="')
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(static.url('js/split.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(static.url('js/jquery.ajaxfileupload.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 5
        __M_writer(filters.decode.utf8(static.url('js/Markdown.Converter.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 6
        __M_writer(filters.decode.utf8(static.url('js/Markdown.Sanitizer.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 7
        __M_writer(filters.decode.utf8(static.url('js/Markdown.Editor.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 8
        __M_writer(filters.decode.utf8(static.url('js/jquery.autocomplete.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 9
        __M_writer(filters.decode.utf8(static.url('js/jquery.timeago.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 10
        __M_writer(filters.decode.utf8(static.url('js/jquery.tagsinput.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 11
        __M_writer(filters.decode.utf8(static.url('js/mustache.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 12
        __M_writer(filters.decode.utf8(static.url('js/URI.min.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 13
        __M_writer(filters.decode.utf8(static.url('js/vendor/underscore-min.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 14
        __M_writer(filters.decode.utf8(static.url('js/vendor/backbone-min.js')))
        __M_writer(u'"></script>\n\n<link href="')
        # SOURCE LINE 16
        __M_writer(filters.decode.utf8(static.url('css/vendor/jquery.tagsinput.css')))
        __M_writer(u'" rel="stylesheet" type="text/css">\n<link href="')
        # SOURCE LINE 17
        __M_writer(filters.decode.utf8(static.url('css/vendor/jquery.autocomplete.css')))
        __M_writer(u'" rel="stylesheet" type="text/css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


