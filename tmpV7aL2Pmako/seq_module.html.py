# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224104.556259
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/seq_module.html'
_template_uri = 'seq_module.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        item_id = context.get('item_id', UNDEFINED)
        position = context.get('position', UNDEFINED)
        element_id = context.get('element_id', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        items = context.get('items', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<div id="sequence_')
        # SOURCE LINE 3
        __M_writer(filters.decode.utf8(element_id))
        __M_writer(u'" class="sequence" data-id="')
        __M_writer(filters.decode.utf8(item_id))
        __M_writer(u'" data-position="')
        __M_writer(filters.decode.utf8(position))
        __M_writer(u'" data-course_modx_root="/course/modx" >\n  <nav aria-label="')
        # SOURCE LINE 4
        __M_writer(filters.decode.utf8(_('Section Navigation')))
        __M_writer(u'" class="sequence-nav">\n    <ul class="sequence-nav-buttons">\n      <li class="prev"><a href="#">')
        # SOURCE LINE 6
        __M_writer(filters.decode.utf8(_('Previous')))
        __M_writer(u'</a></li>\n    </ul>\n\n    <div class="sequence-list-wrapper">\n      <ol id="sequence-list">\n')
        # SOURCE LINE 11
        for idx, item in enumerate(items):
            # SOURCE LINE 16
            __M_writer(u'        <li>\n        <a class="seq_')
            # SOURCE LINE 17
            __M_writer(filters.decode.utf8(item['type']))
            __M_writer(u' inactive progress-')
            __M_writer(filters.decode.utf8(item['progress_status']))
            __M_writer(u'"\n           data-id="')
            # SOURCE LINE 18
            __M_writer(filters.decode.utf8(item['id']))
            __M_writer(u'"\n           data-element="')
            # SOURCE LINE 19
            __M_writer(filters.decode.utf8(idx+1))
            __M_writer(u'"\n           href="javascript:void(0);">\n            <p>')
            # SOURCE LINE 21
            __M_writer(filters.decode.utf8(item['title']))
            __M_writer(u'<span class="sr">, ')
            __M_writer(filters.decode.utf8(item['type']))
            __M_writer(u'</span></p>\n          </a>\n        </li>\n')
        # SOURCE LINE 25
        __M_writer(u'      </ol>\n    </div>\n\n    <ul class="sequence-nav-buttons">\n      <li class="next"><a href="#">')
        # SOURCE LINE 29
        __M_writer(filters.decode.utf8(_("Next")))
        __M_writer(u'</a></li>\n    </ul>\n  </nav>\n\n')
        # SOURCE LINE 33
        for item in items:
            # SOURCE LINE 34
            __M_writer(u'  <div class="seq_contents tex2jax_ignore asciimath2jax_ignore">')
            __M_writer(filters.html_escape(filters.decode.utf8(item['content'] )))
            __M_writer(u'</div>\n')
        # SOURCE LINE 36
        __M_writer(u'  <div id="seq_content"></div>\n\n  <nav class="sequence-bottom">\n    <ul aria-label="')
        # SOURCE LINE 39
        __M_writer(filters.decode.utf8(_('Section Navigation')))
        __M_writer(u'" class="sequence-nav-buttons">\n      <li class="prev"><a href="#">')
        # SOURCE LINE 40
        __M_writer(filters.decode.utf8(_("Previous")))
        __M_writer(u'</a></li>\n      <li class="next"><a href="#">')
        # SOURCE LINE 41
        __M_writer(filters.decode.utf8(_("Next")))
        __M_writer(u'</a></li>\n    </ul>\n  </nav>\n</div>\n\n\n\n<script type="text/javascript">\n  var sequenceNav;\n  $(document).ready(function() {\n    sequenceNav = new SequenceNav($(\'.sequence-nav\'));\n  });\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


