# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223007.348104
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/problem.html'
_template_uri = 'problem.html'
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
    # SOURCE LINE 3
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        check_button = context.get('check_button', UNDEFINED)
        reset_button = context.get('reset_button', UNDEFINED)
        attempts_allowed = context.get('attempts_allowed', UNDEFINED)
        save_button = context.get('save_button', UNDEFINED)
        problem = context.get('problem', UNDEFINED)
        attempts_used = context.get('attempts_used', UNDEFINED)
        answer_available = context.get('answer_available', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n<h2 class="problem-header">\n  ')
        # SOURCE LINE 5
        __M_writer(filters.decode.utf8( problem['name'] ))
        __M_writer(u'\n</h2>\n\n<section class="problem-progress">\n</section>\n\n<section class="problem">\n  ')
        # SOURCE LINE 12
        __M_writer(filters.decode.utf8( problem['html'] ))
        __M_writer(u'\n\n  <section class="action">\n    <input type="hidden" name="problem_id" value="')
        # SOURCE LINE 15
        __M_writer(filters.decode.utf8( problem['name'] ))
        __M_writer(u'" />\n\n')
        # SOURCE LINE 17
        if check_button:
            # SOURCE LINE 18
            __M_writer(u'    <input class="check ')
            __M_writer(filters.decode.utf8( check_button ))
            __M_writer(u'" type="button" value="')
            __M_writer(filters.decode.utf8( check_button ))
            __M_writer(u'" />\n')
        # SOURCE LINE 20
        if reset_button:
            # SOURCE LINE 21
            __M_writer(u'    <input class="reset" type="button" value="')
            __M_writer(filters.decode.utf8(_('Reset')))
            __M_writer(u'" />\n')
        # SOURCE LINE 23
        if save_button:
            # SOURCE LINE 24
            __M_writer(u'    <input class="save" type="button" value="')
            __M_writer(filters.decode.utf8(_('Save')))
            __M_writer(u'" />\n')
        # SOURCE LINE 26
        if answer_available:
            # SOURCE LINE 27
            __M_writer(u'    <button class="show"><span class="show-label">')
            __M_writer(filters.decode.utf8(_('Show Answer(s)')))
            __M_writer(u'</span> <span class="sr">')
            __M_writer(filters.decode.utf8(_("(for question(s) above - adjacent to each field)")))
            __M_writer(u'</span></button>\n')
        # SOURCE LINE 29
        if attempts_allowed :
            # SOURCE LINE 30
            __M_writer(u'    <section class="submission_feedback">\n      ')
            # SOURCE LINE 31
            __M_writer(filters.decode.utf8(_("You have used {num_used} of {num_total} submissions").format(num_used=attempts_used, num_total=attempts_allowed)))
            __M_writer(u'\n    </section>\n')
        # SOURCE LINE 34
        __M_writer(u'  </section>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


