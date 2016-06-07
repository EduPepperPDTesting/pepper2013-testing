# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218681.671206
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/djangoapps/pipeline_mako/templates/mako/css.html'
_template_uri = 'mako/css.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        url = context.get('url', UNDEFINED)
        media = context.get('media', UNDEFINED)
        charset = context.get('charset', UNDEFINED)
        type = context.get('type', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<link href="')
        __M_writer(filters.decode.utf8(url))
        __M_writer(u'" rel="stylesheet" type="')
        __M_writer(filters.decode.utf8(type))
        __M_writer(u'" ')
        # SOURCE LINE 2
        if media:
            # SOURCE LINE 3
            __M_writer(u'media="')
            __M_writer(filters.decode.utf8(media))
            __M_writer(u'" ')
        # SOURCE LINE 5
        if title:
            # SOURCE LINE 6
            __M_writer(u'title="')
            __M_writer(filters.decode.utf8(title))
            __M_writer(u'" ')
        # SOURCE LINE 8
        if charset:
            # SOURCE LINE 9
            __M_writer(u'charset="')
            __M_writer(filters.decode.utf8(charset))
            __M_writer(u'" ')
        # SOURCE LINE 11
        __M_writer(u'/>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


