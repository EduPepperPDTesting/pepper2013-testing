# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465230993.672368
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/discussion/_discussion_module.html'
_template_uri = 'discussion/_discussion_module.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        discussion_visibility = context.get('discussion_visibility', UNDEFINED)
        discussion_id = context.get('discussion_id', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        # SOURCE LINE 2
        runtime._include_file(context, u'_underscore_templates.html', _template_uri)
        __M_writer(u'\n\n<div class="discussion-module" data-discussion-id="')
        # SOURCE LINE 4
        __M_writer(filters.html_escape(filters.decode.utf8(discussion_id )))
        __M_writer(u'" data-discussion-visibility="')
        __M_writer(filters.decode.utf8(discussion_visibility))
        __M_writer(u'">\n    <a class="discussion-show control-button" href="javascript:void(0)" data-discussion-id="')
        # SOURCE LINE 5
        __M_writer(filters.html_escape(filters.decode.utf8(discussion_id )))
        __M_writer(u'" data-discussion-visibility="')
        __M_writer(filters.decode.utf8(discussion_visibility))
        __M_writer(u'"><span class="show-hide-discussion-icon"></span><span class="button-text"></span></a>\n    <a class="discussion-show-default control-button" href="javascript:void(0)" data-discussion-id="')
        # SOURCE LINE 6
        __M_writer(filters.html_escape(filters.decode.utf8(discussion_id )))
        __M_writer(u'" data-discussion-visibility="')
        __M_writer(filters.decode.utf8(discussion_visibility))
        __M_writer(u'" style="display:none;"><span class="show-hide-discussion-icon"></span><span class="button-text">Show Discussion</span></a>\n    <a href="#" class="new-post-btn"><span class="icon icon-edit new-post-icon"></span>')
        # SOURCE LINE 7
        __M_writer(filters.decode.utf8(_("New Topic")))
        __M_writer(u'</a>    \n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


