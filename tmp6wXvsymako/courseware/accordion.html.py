# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218891.589533
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/accordion.html'
_template_uri = 'courseware/accordion.html'
_source_encoding = 'utf-8'
_exports = ['make_chapter']


# SOURCE LINE 1

from django.core.urlresolvers import reverse
from xmodule.util.date_utils import get_default_time_display
from django.utils.translation import ugettext as _


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        toc = context.get('toc', UNDEFINED)
        def make_chapter(chapter):
            return render_make_chapter(context.locals_(__M_locals),chapter)
        __M_writer = context.writer()
        # SOURCE LINE 5
        __M_writer(u'\n\n')
        # SOURCE LINE 37
        __M_writer(u'\n\n')
        # SOURCE LINE 39
        for chapter in toc:
            # SOURCE LINE 40
            __M_writer(u'    ')
            __M_writer(filters.decode.utf8(make_chapter(chapter)))
            __M_writer(u'\n')
        # SOURCE LINE 42
        __M_writer(u'\n<script>\nvar sections=[];\nvar SHOW_GLOBAL_SEQUENCE=1;\n$.each($(".section_link"),function(i,el){\n  $(el).attr("index",i);\n  sections.push( $(el).attr("href"));\n})\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_make_chapter(context,chapter):
    __M_caller = context.caller_stack._push_frame()
    try:
        course_id = context.get('course_id', UNDEFINED)
        show_timezone = context.get('show_timezone', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n  <div class="chapter">\n      ')
        # SOURCE LINE 9

        if chapter.get('active'):
            aria_label = _('{chapter}, current chapter').format(chapter=chapter['display_name'])
            active_class = ' class="active"'
        else:
            aria_label = chapter['display_name']
            active_class = ''
              
        
        # SOURCE LINE 16
        __M_writer(u'\n      <h3 ')
        # SOURCE LINE 17
        __M_writer(filters.decode.utf8(active_class))
        __M_writer(u' aria-label="')
        __M_writer(filters.decode.utf8(aria_label))
        __M_writer(u'">\n        <a href="#">\n          ')
        # SOURCE LINE 19
        __M_writer(filters.decode.utf8(chapter['display_name']))
        __M_writer(u'\n        </a>\n      </h3>\n\n    <ul>\n')
        # SOURCE LINE 24
        for i,section in enumerate(chapter['sections']):
            # SOURCE LINE 25
            __M_writer(u'          <li class="')
            __M_writer(filters.decode.utf8('active' if 'active' in section and section['active'] else ''))
            __M_writer(u' ')
            __M_writer(filters.decode.utf8('graded'  if 'graded' in section and section['graded'] else ''))
            __M_writer(u'">\n            <a href="')
            # SOURCE LINE 26
            __M_writer(filters.decode.utf8(reverse('courseware_section', args=[course_id, chapter['url_name'], section['url_name']])))
            __M_writer(u'" class="section_link">\n              <p>')
            # SOURCE LINE 27
            __M_writer(filters.decode.utf8(section['display_name']))
            __M_writer(u' ')
            __M_writer(filters.decode.utf8('<span class="sr">, current section</span>' if 'active' in section and section['active'] else ''))
            __M_writer(u'</p>\n<!--@begin:Hide subtitle-->\n<!--@date:2013-11-11-->              \n              <p class="subtitle" style="display:none;">')
            # SOURCE LINE 30
            __M_writer(filters.decode.utf8(section['format']))
            __M_writer(u' ')
            __M_writer(filters.decode.utf8("due " + get_default_time_display(section['due'], show_timezone) if section.get('due') is not None else ''))
            __M_writer(u'</p>\n<!--@end-->\n            </a>\n          </li>\n')
        # SOURCE LINE 35
        __M_writer(u'    </ul>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


