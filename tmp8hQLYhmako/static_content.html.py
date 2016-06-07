# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229228.062058
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/djangoapps/pipeline_mako/templates/static_content.html'
_template_uri = u'static_content.html'
_source_encoding = 'utf-8'
_exports = ['url', 'include', 'css', 'js']


# SOURCE LINE 1

from staticfiles.storage import staticfiles_storage
from pipeline_mako import compressed_css, compressed_js


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 11
        __M_writer(u'\n\n')
        # SOURCE LINE 21
        __M_writer(u'\n')
        # SOURCE LINE 30
        __M_writer(u'\n\n')
        # SOURCE LINE 35
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_url(context,file):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6

        try:
            url = staticfiles_storage.url(file)
        except:
            url = file
        
        
        # SOURCE LINE 11
        __M_writer(filters.decode.utf8(url))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_include(context,path):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 32

        from django.template.loaders.filesystem import _loader
        source, template_path = _loader.load_template_source(path)
        
        
        # SOURCE LINE 35
        __M_writer(filters.decode.utf8(source))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_css(context,group):
    __M_caller = context.caller_stack._push_frame()
    try:
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 13
        __M_writer(u'\n')
        # SOURCE LINE 14
        if settings.MITX_FEATURES['USE_DJANGO_PIPELINE']:
            # SOURCE LINE 15
            __M_writer(u'    ')
            __M_writer(filters.decode.utf8(compressed_css(group)))
            __M_writer(u'\n')
            # SOURCE LINE 16
        else:
            # SOURCE LINE 17
            for filename in settings.PIPELINE_CSS[group]['source_filenames']:
                # SOURCE LINE 18
                __M_writer(u'      <link rel="stylesheet" href="')
                __M_writer(filters.decode.utf8(staticfiles_storage.url(filename.replace('.scss', '.css'))))
                __M_writer(u'" type="text/css" media="all" / >\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js(context,group):
    __M_caller = context.caller_stack._push_frame()
    try:
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 22
        __M_writer(u'\n')
        # SOURCE LINE 23
        if settings.MITX_FEATURES['USE_DJANGO_PIPELINE']:
            # SOURCE LINE 24
            __M_writer(u'    ')
            __M_writer(filters.decode.utf8(compressed_js(group)))
            __M_writer(u'\n')
            # SOURCE LINE 25
        else:
            # SOURCE LINE 26
            for filename in settings.PIPELINE_JS[group]['source_filenames']:
                # SOURCE LINE 27
                __M_writer(u'      <script type="text/javascript" src="')
                __M_writer(filters.decode.utf8(staticfiles_storage.url(filename.replace('.coffee', '.js'))))
                __M_writer(u'"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


