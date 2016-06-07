# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229564.597235
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/help_modal.html'
_template_uri = u'help_modal.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 4
from datetime import datetime 

# SOURCE LINE 5
import pytz 

# SOURCE LINE 6
from django.conf import settings 

# SOURCE LINE 7
from courseware.tabs import get_discussion_link 

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
        course = context.get('course', UNDEFINED)
        marketing_link = context.get('marketing_link', UNDEFINED)
        user = context.get('user', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        # SOURCE LINE 5
        __M_writer(u'\n')
        # SOURCE LINE 6
        __M_writer(u'\n')
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        # SOURCE LINE 9
        if settings.MITX_FEATURES.get('ENABLE_FEEDBACK_SUBMISSION', False):
            # SOURCE LINE 10
            __M_writer(u'\n<div class="help-tab">\n  <a href="#help-modal" rel="leanModal">')
            # SOURCE LINE 12
            __M_writer(filters.decode.utf8(_("Help")))
            __M_writer(u'</a>\n</div>\n\n<section id="help-modal" class="modal">\n  <div class="inner-wrapper" id="help_wrapper">\n    <header>\n      <h2>')
            # SOURCE LINE 18
            __M_writer(filters.decode.utf8(_('{span_start}{platform_name}{span_end} Help').format(span_start='<span class="edx">', span_end='</span>', platform_name=settings.PLATFORM_NAME)))
            __M_writer(u'</h2>\n      <hr>\n    </header>\n\n')
            # SOURCE LINE 22

            discussion_link = get_discussion_link(course) if course else None
            
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['discussion_link'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 24
            __M_writer(u'\n\n')
            # SOURCE LINE 26
            if discussion_link:
                # SOURCE LINE 27
                __M_writer(u'    <p>')
                __M_writer(filters.decode.utf8(_('For <strong>questions on course lectures, homework, tools, or materials for this course</strong>, post in the {link_start}course discussion forum{link_end}.').format(
      link_start='<a href="{url}" target="_blank">'.format(url=discussion_link),
      link_end='</a>',
      )))
                # SOURCE LINE 30
                __M_writer(u'\n    </p>\n')
            # SOURCE LINE 33
            __M_writer(u'\n    <p>')
            # SOURCE LINE 34
            __M_writer(filters.decode.utf8(_('Have <strong>general questions about {platform_name}</strong>? You can find lots of helpful information in the {platform_name} {link_start}FAQ{link_end}.').format(
        link_start='<a href="{url}" target="_blank">'.format(
          url=marketing_link('FAQ')
        ),
        link_end='</a>',
        platform_name=settings.PLATFORM_NAME)))
            # SOURCE LINE 39
            __M_writer(u'\n      </p>\n\n    <p>')
            # SOURCE LINE 42
            __M_writer(filters.decode.utf8(_('Have a <strong>question about something specific</strong>? You can contact the {platform_name} general support team directly:').format(platform_name=settings.PLATFORM_NAME)))
            __M_writer(u'</p>\n    <hr>\n\n    <div class="help-buttons">\n      <a href="#" id="feedback_link_problem">')
            # SOURCE LINE 46
            __M_writer(filters.decode.utf8(_('Report a problem')))
            __M_writer(u'</a>\n      <a href="#" id="feedback_link_suggestion">')
            # SOURCE LINE 47
            __M_writer(filters.decode.utf8(_('Make a suggestion')))
            __M_writer(u'</a>\n      <a href="#" id="feedback_link_question">')
            # SOURCE LINE 48
            __M_writer(filters.decode.utf8(_('Ask a question')))
            __M_writer(u'</a>\n    </div>\n\n')
            # SOURCE LINE 52
            __M_writer(u'    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n\n  <div class="inner-wrapper" id="feedback_form_wrapper">\n    <header></header>\n\n    <form id="feedback_form" class="feedback_form" method="post" data-remote="true" action="/submit_feedback">\n      <div id="feedback_error" class="modal-form-error"></div>\n')
            # SOURCE LINE 64
            if not user.is_authenticated():
                # SOURCE LINE 65
                __M_writer(u'      <label data-field="name">')
                __M_writer(filters.decode.utf8(_('Name*')))
                __M_writer(u'</label>\n      <input name="name" type="text">\n      <label data-field="email">')
                # SOURCE LINE 67
                __M_writer(filters.decode.utf8(_('E-mail*')))
                __M_writer(u'</label>\n      <input name="email" type="text">\n')
            # SOURCE LINE 70
            __M_writer(u'      <label data-field="subject">')
            __M_writer(filters.decode.utf8(_('Briefly describe your issue*')))
            __M_writer(u'</label>\n      <input name="subject" type="text">\n      <label data-field="details">')
            # SOURCE LINE 72
            __M_writer(filters.decode.utf8(_('Tell us the details*')))
            __M_writer(u'\n<span class="tip">')
            # SOURCE LINE 73
            __M_writer(filters.decode.utf8(_('Include error messages, steps which lead to the issue, etc')))
            __M_writer(u'</span></label>\n      <textarea name="details"></textarea>\n      <input name="issue_type" type="hidden">\n')
            # SOURCE LINE 76
            if course:
                # SOURCE LINE 77
                __M_writer(u'      <input name="course_id" type="hidden" value="')
                __M_writer(filters.html_escape(filters.decode.utf8(course.id )))
                __M_writer(u'">\n')
            # SOURCE LINE 79
            __M_writer(u'      <div class="submit">\n        <input name="submit" type="submit" value="Submit">\n      </div>\n    </form>\n\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n\n  <div class="inner-wrapper" id="feedback_success_wrapper">\n    <header>\n      <h2>')
            # SOURCE LINE 93
            __M_writer(filters.decode.utf8(_('Thank You!')))
            __M_writer(u'</h2>\n      <hr>\n    </header>\n\n    ')
            # SOURCE LINE 97

            dst = datetime.now(pytz.utc).astimezone(pytz.timezone("America/New_York")).dst()
            if dst:
              open_time = "13:00"
              close_time = "21:00"
            else:
              open_time = "14:00"
              close_time = "22:00"
                
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['dst','open_time','close_time'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 105
            __M_writer(u'\n    <p>\n    ')
            # SOURCE LINE 107
            __M_writer(filters.decode.utf8(_(
        'Thank you for your inquiry or feedback.  We typically respond to a request '
        'within one business day (Monday to Friday, {open_time} UTC to {close_time} UTC.) In the meantime, please '
        'review our {link_start}detailed FAQs{link_end} where most questions have '
        'already been answered.'
    ).format(
        open_time=open_time,
        close_time=close_time,
        link_start='<a href="{}" target="_blank">'.format(marketing_link('FAQ')),
        link_end='</a>'
    )))
            # SOURCE LINE 117
            __M_writer(u'\n    </p>\n\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n\n<script type="text/javascript">\n(function() {\n    $(".help-tab").click(function() {\n        $(".field-error").removeClass("field-error");\n        $("#feedback_form")[0].reset();\n        $("#feedback_form input[type=\'submit\']").removeAttr("disabled");\n        $("#feedback_form_wrapper").css("display", "none");\n        $("#feedback_error").css("display", "none");\n        $("#feedback_success_wrapper").css("display", "none");\n        $("#help_wrapper").css("display", "block");\n    });\n    showFeedback = function(event, issue_type, title, subject_label, details_label) {\n        $("#help_wrapper").css("display", "none");\n        $("#feedback_form input[name=\'issue_type\']").val(issue_type);\n        $("#feedback_form_wrapper").css("display", "block");\n        $("#feedback_form_wrapper header").html("<h2>" + title + "</h2><hr>");\n        $("#feedback_form_wrapper label[data-field=\'subject\']").html(subject_label);\n        $("#feedback_form_wrapper label[data-field=\'details\']").html(details_label);\n        event.preventDefault();\n    };\n    $("#feedback_link_problem").click(function(event) {\n        showFeedback(\n            event,\n            gettext("problem"),\n            gettext("Report a Problem"),\n            gettext("Brief description of the problem*"),\n            gettext("Details of the problem you are encountering*") + "<span class=\'tip\'>" +\n              gettext("Include error messages, steps which lead to the issue, etc.") + "</span>"\n        );\n    });\n    $("#feedback_link_suggestion").click(function(event) {\n        showFeedback(\n            event,\n            gettext("suggestion"),\n            gettext("Make a Suggestion"),\n            gettext("Brief description of your suggestion*"),\n            gettext("Details*")\n        );\n    });\n    $("#feedback_link_question").click(function(event) {\n        showFeedback(\n            event,\n            gettext("question"),\n            gettext("Ask a Question"),\n            gettext("Brief summary of your question*"),\n            gettext("Details*")\n        );\n    });\n    $("#feedback_form").submit(function() {\n        $("input[type=\'submit\']", this).attr("disabled", "disabled");\n    });\n    $("#feedback_form").on("ajax:complete", function() {\n        $("input[type=\'submit\']", this).removeAttr("disabled");\n    });\n    $("#feedback_form").on("ajax:success", function(event, data, status, xhr) {\n        $("#feedback_form_wrapper").css("display", "none");\n        $("#feedback_success_wrapper").css("display", "block");\n    });\n    $("#feedback_form").on("ajax:error", function(event, xhr, status, error) {\n        $(".field-error").removeClass("field-error");\n        var responseData;\n        try {\n            responseData = jQuery.parseJSON(xhr.responseText);\n        } catch(err) {\n        }\n        if (responseData) {\n            $("[data-field=\'"+responseData.field+"\']").addClass("field-error");\n            $("#feedback_error").html(responseData.error).stop().css("display", "block");\n        } else {\n            // If no data (or malformed data) is returned, a server error occurred\n            htmlStr = gettext("An error has occurred.");\n')
            # SOURCE LINE 199
            if settings.FEEDBACK_SUBMISSION_EMAIL:
                # SOURCE LINE 200
                __M_writer(u'            htmlStr += " " + _.template(\n              gettext("Please {link_start}send us e-mail{link_end}."),\n              {link_start: \'<a href="#" id="feedback_email">\', link_end: \'</a>\'},\n              {interpolate: /\\{(.+?)\\}/g})\n')
                # SOURCE LINE 204
            else:
                # SOURCE LINE 205
                __M_writer(u'            // If no email is configured, we can\'t do much other than\n            // ask the user to try again later\n            htmlStr += gettext(" Please try again later.");\n')
            # SOURCE LINE 209
            __M_writer(u'            $("#feedback_error").html(htmlStr).stop().css("display", "block");\n')
            # SOURCE LINE 210
            if settings.FEEDBACK_SUBMISSION_EMAIL:
                # SOURCE LINE 211
                __M_writer(u'            $("#feedback_email").click(function(e) {\n                mailto = "mailto:" + "')
                # SOURCE LINE 212
                __M_writer(filters.decode.utf8(settings.FEEDBACK_SUBMISSION_EMAIL))
                __M_writer(u'" +\n                    "?subject=" + $("#feedback_form input[name=\'subject\']").val() +\n                    "&body=" + $("#feedback_form textarea[name=\'details\']").val();\n                window.open(mailto);\n                e.preventDefault();\n            });\n')
            # SOURCE LINE 219
            __M_writer(u'        }\n    });\n})(this)\n</script>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


