# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224098.386985
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/welcome-back.html'
_template_uri = 'courseware/welcome-back.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        chapter_module = context.get('chapter_module', UNDEFINED)
        prev_section_url = context.get('prev_section_url', UNDEFINED)
        prev_section = context.get('prev_section', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<h2>')
        # SOURCE LINE 2
        __M_writer(filters.decode.utf8(chapter_module.display_name_with_default))
        __M_writer(u'</h2>\n\n<p>')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(_("You were most recently in {section_link}.  If you\'re done with that, choose another section on the left.").format(
	    section_link=u'<a href="{url}">{section_name}</a>'.format(
	        url=prev_section_url,
	        section_name=prev_section.display_name_with_default,
	    )
    )))
        # SOURCE LINE 9
        __M_writer(u'</p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


