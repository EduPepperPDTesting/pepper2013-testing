# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465218642.316619
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/login.html'
_template_uri = 'login.html'
_source_encoding = 'utf-8'
_exports = [u'js_extra', u'title']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 7
from django.core.urlresolvers import reverse 

# SOURCE LINE 8
from django.utils.translation import ugettext as _ 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 5
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        course_id = context.get('course_id', UNDEFINED)
        def js_extra():
            return render_js_extra(context.locals_(__M_locals))
        settings = context.get('settings', UNDEFINED)
        enrollment_action = context.get('enrollment_action', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n\n')
        # SOURCE LINE 7
        __M_writer(u'\n')
        # SOURCE LINE 8
        __M_writer(u'\n<!--@begin:New added page style-->\n<!--@date:2013-11-02-->\n<link rel="stylesheet" type="text/css"  href="/static/tmp-resource/css/ppd-general01.css"/>\n<style>\n  #submit:hover {\n  background:#6e8194;\n  transition-delay: 0s, 0s, 0s;\n  transition-duration: 0.25s, 0.25s, 0.25s;\n  transition-property:color, background,\u200b box-shadow;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  transition-duration:0.25s,\u200b 0.25s,\u200b 0.25s;\n  color:#fff;\n  }\n  #submit {\n  background-color:#556370;\n  text-decoration: none;\n  padding-bottom: 7px;\n  padding-left: 10px;\n  padding-right: 10px;\n  padding-top: 7px;\n  border-bottom-left-radius: 2px;\n  border-bottom-right-radius: 2px;\n  cursor: pointer;\n  border-top-left-radius: 2px;\n  border-top-right-radius: 2px;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  box-shadow: #949494 0px 2px 1px 0px;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n  #submit:normal {\n  background-color:#126F9A;\n  text-decoration: none;\n  border-bottom-left-radius: 2px;\n  border-bottom-right-radius: 2px;\n  cursor: pointer;\n  border-top-left-radius: 2px;\n  border-top-right-radius: 2px;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  box-shadow: rgb(10, 74, 103) 0px 2px 1px 0px;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n</style>\n<!--@end-->\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 55
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'js_extra'):
            context['self'].js_extra(**pageargs)
        

        # SOURCE LINE 171
        __M_writer(u'\n<div style="width:960px;margin:0 auto;">\n<section class="introduction">\n\t<!--@begin:use new image name(ppd-...); modify the style-->\n\t<!--@date:2013-11-02-->\n\t<div style="margin:0 auto;width:960px;height:195px;background:url(/static/images/ppd-register-banner.jpg);border-bottom:1px solid #000;">\n\t<!--@end-->\n\n\t\t<!--@begin:use html text to replace the text on the picture; add code(class="_...") to modify font style-->\n\t\t<!--@date:2013-11-02-->\n\t\t<div style="width:580px;float:left">\n\t\t\t<div class="_banner_whatis_title_font">\n\t\t\t\tPLEASE LOG IN\n\t\t\t\t<div class="_banner_whatis_title_content_font">\n\t\t\t\t\tto access your account and courses\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t\t<!--@end-->\n\t</div>\n</section>\n\n<section class="login container">\n  <section role="main" class="content">\n    <form role="form" id="login-form" method="post" data-remote="true" action="/login_ajax" novalidate>\n\n      <!-- status messages -->\n      <div role="alert" class="status message">\n        <h3 class="message-title">')
        # SOURCE LINE 199
        __M_writer(filters.decode.utf8(_("We're Sorry, {platform_name} accounts are unavailable currently").format(platform_name=settings.PLATFORM_NAME)))
        __M_writer(u'</h3>\n        <p class="message-copy">Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>\n      </div>\n\n      <div role="alert" class="status message submission-error" tabindex="-1">\n        <h3 class="message-title">')
        # SOURCE LINE 204
        __M_writer(filters.decode.utf8(_("The following errors occured while logging you in:")))
        __M_writer(u' </h3>\n        <ul class="message-copy">\n          <li>')
        # SOURCE LINE 206
        __M_writer(filters.decode.utf8(_("Your email or password is incorrect")))
        __M_writer(u'</li>\n        </ul>\n      </div>\n\n      <p class="instructions sr">\n        ')
        # SOURCE LINE 211
        __M_writer(filters.decode.utf8(_('Please provide the following information to log into your {platform_name} account. Required fields are noted by <strong class="indicator">bold text and an asterisk (*)</strong>.').format(platform_name=settings.PLATFORM_NAME)))
        __M_writer(u'\n      </p>\n\n      <fieldset class="group group-form group-form-requiredinformation">\n        <legend class="sr">')
        # SOURCE LINE 215
        __M_writer(filters.decode.utf8(_('Required Information')))
        __M_writer(u'</legend>\n\n        <ol class="list-input">\n<!--@begin:Change the form-->\n<!--@date:2013-11-02-->\n          <li class="field text" id="field-email">\n            <label for="email" style="font-weight:bold;">')
        # SOURCE LINE 221
        __M_writer(filters.decode.utf8(_('E-mail')))
        __M_writer(u'</label>\n            <input class="" id="email" type="email" name="email" value="" placeholder="example: username@domain.com" required aria-required="true" />\n          </li>\n          <li class="field password" id="field-password">\n            <label for="password" style="font-weight:bold;">')
        # SOURCE LINE 225
        __M_writer(filters.decode.utf8(_('Password')))
        __M_writer(u'</label>\n            <input id="password" type="password" name="password" value="" required aria-required="true" />\n            <span class="tip tip-input">\n              <a href="#forgot-password-modal" rel="leanModal" class="blue pwd-reset action action-forgotpw">')
        # SOURCE LINE 228
        __M_writer(filters.decode.utf8(_('Forgot password?')))
        __M_writer(u'</a>\n<!--@end-->\n            </span>\n          </li>\n        </ol>\n      </fieldset>\n\n      <fieldset class="group group-form group-form-secondary group-form-accountpreferences">\n        <legend class="sr">')
        # SOURCE LINE 236
        __M_writer(filters.decode.utf8(_('Account Preferences')))
        __M_writer(u'</legend>\n\n        <ol class="list-input">\n<!--@begin:Change the font of Remember me\n<!--@date:2013-11-02-->\n          <li class="field checkbox" id="field-remember">\n            <input id="remember-yes" type="checkbox" name="remember" value="true" />\n            <label for="remember-yes" style="font-weight:bold;">')
        # SOURCE LINE 243
        __M_writer(filters.decode.utf8(_('Remember me')))
        __M_writer(u'</label>\n<!--@end-->\n          </li>\n        </ol>\n      </fieldset>\n\n')
        # SOURCE LINE 249
        if course_id and enrollment_action:
            # SOURCE LINE 250
            __M_writer(u'      <input type="hidden" name="enrollment_action" value="')
            __M_writer(filters.html_escape(filters.decode.utf8(enrollment_action )))
            __M_writer(u'" />\n      <input type="hidden" name="course_id" value="')
            # SOURCE LINE 251
            __M_writer(filters.html_escape(filters.decode.utf8(course_id )))
            __M_writer(u'" />\n')
        # SOURCE LINE 253
        __M_writer(u'\n      <div class="form-actions">\n        <button name="submit" type="submit" id="submit" class="action action-primary action-update"></button>\n      </div>\n\n    </form>\n  </section>\n\n  <aside role="complementary">\n    <header>\n      <h2 class="sr">')
        # SOURCE LINE 263
        __M_writer(filters.decode.utf8(_("Helpful Information")))
        __M_writer(u'</h2>\n    </header>\n\n')
        # SOURCE LINE 266
        if settings.MITX_FEATURES.get('AUTH_USE_OPENID'):
            # SOURCE LINE 267
            __M_writer(u'    <!-- <div class="cta cta-login-options-openid">\n      <h3>')
            # SOURCE LINE 268
            __M_writer(filters.decode.utf8(_("Login via OpenID")))
            __M_writer(u'</h3>\n      <p>')
            # SOURCE LINE 269
            __M_writer(filters.decode.utf8(_('You can now start learning with {platform_name} by logging in with your <a rel="external" href="http://openid.net/">OpenID account</a>.').format(platform_name=settings.PLATFORM_NAME)))
            __M_writer(u'</p>\n      <a class="action action-login-openid" href="#">')
            # SOURCE LINE 270
            __M_writer(filters.decode.utf8(_("Login via OpenID")))
            __M_writer(u'</a>\n    </div> -->\n')
        # SOURCE LINE 273
        __M_writer(u'\n    <div class="cta cta-help" style="line-height:25px;color:#666;">\n<!--@begin:delete the text-->\n<!--@date:2013-11-15-->\n\t<!--\n      <h3 style="font-size:16px;color:#3461ad;">Not yet a member of pepper?<br>There are two ways to join.</h3><br>\n\t -->\n<!--@end-->\n\n      <!--@begin:Removed for now and will implement when e-transaction works-->\n      <!--@date:2013-11-02-->\n      <!--\n      To sign up your teachers please<br> contact\n      <a href="mailto:info@pepperpd.com" class="blue-underline" style="text-decoration:underline !important;">info@pepperpd.com</a><br><br>\n      To sign up as an individual,<br> please\n      <a href="" class="blue-underline" style="text-decoration:underline !important;">Click Here</a>\n      -->\n      <!--@end-->\n    </div>\n  </aside>\n  </section>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js_extra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def js_extra():
            return render_js_extra(context)
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 57
        __M_writer(u'\n  <script type="text/javascript">\n    $(function() {\n\n      var view_name = \'view-login\';\n\n      // adding js class for styling with accessibility in mind\n      $(\'body\').addClass(\'js\').addClass(view_name);\n\n      // new window/tab opening\n      $(\'a[rel="external"], a[class="new-vp"]\')\n      .click( function() {\n      window.open( $(this).attr(\'href\') );\n      return false;\n      });\n\n      // form field label styling on focus\n      $("form :input").focus(function() {\n        $("label[for=\'" + this.id + "\']").parent().addClass("is-focused");\n      }).blur(function() {\n        $("label").parent().removeClass("is-focused");\n      });\n    });\n\n    (function() {\n        var urlParams = {};\n        var searchString = window.location.search.substring(1);\n        if (searchString !== undefined) {\n            var pairs = searchString.split(\'&\');\n            for (var i = 0; i < pairs.length; i++) {\n                var values = pairs[i].split(\'=\');\n                urlParams[values[0]] = values[1] === undefined ? false : decodeURIComponent(values[1]);\n            }\n        }\n\n        if (localStorage.pepperpd_login_email)\n        {\n            $("#email").val(localStorage.pepperpd_login_email);\n        }\n        toggleSubmitButton(true);\n\n        $(\'#login-form\').on(\'submit\', function() {\n            toggleSubmitButton(false);\n        });\n\n        $(\'#login-form\').on(\'ajax:error\', function() {\n            toggleSubmitButton(true);\n        });\n\n        $(\'#login-form\').on(\'ajax:success\', function(event, json, xhr) {\n            if (json.success) {\n                if ($(\'#remember-yes\').attr("checked"))\n                {\n                    localStorage.pepperpd_login_email=$("#email").val();\n                }\n\n                if (urlParams[\'next\'] !== undefined && !isExternal(urlParams[\'next\']) && urlParams[\'next\'].match(/^course.+courseware/)) {\n                    var next = urlParams[\'next\'];\n                    if (next.substring(0,1) != \'/\') {\n                        next = \'/\' + next;\n                    }\n                  location.href = next;\n                } else if (urlParams[\'next\'] !== undefined && !isExternal(urlParams[\'next\']) && urlParams[\'next\'].match(/^\\/sso\\/idp\\/auth/)) {\n                   location.href = urlParams[\'next\'];\n                }  else {\n                    location.href = "')
        # SOURCE LINE 122
        __M_writer(filters.decode.utf8(reverse('dashboard')))
        __M_writer(u'";\n                }\n\n            } else {\n                toggleSubmitButton(true);\n                $(\'.message.submission-error\').addClass(\'is-shown\').focus();\n                $(\'.message.submission-error .message-copy\').html(json.value);\n            }\n        });\n    })(this);\n\n    function toggleSubmitButton(enable) {\n      var $submitButton = $(\'form .form-actions #submit\');\n\n\n      if(enable) {\n        $submitButton.\n          removeClass(\'is-disabled\').\n          removeProp(\'disabled\').\n\n          <!--@begin:modify LogIn -> Log In-->\n          <!--@date:2013-11-02-->\n          html("')
        # SOURCE LINE 144
        __M_writer(filters.decode.utf8(_('Log In').format(platform_name=settings.PLATFORM_NAME)))
        __M_writer(u" <span class='orn-plus'>&</span> ")
        __M_writer(filters.decode.utf8(_('Access My Courses')))
        __M_writer(u'");\n          <!--@end-->\n      } else {\n        $submitButton.\n          addClass(\'is-disabled\').\n          prop(\'disabled\', true).\n          html(gettext(\'Processing your account information &hellip;\'));\n      }\n\n    }\n\n//------------- Clear time storage-------------------//\n\n    function clearTimeSessionStorage(){\n      var user_id = sessionStorage.getItem(\'user_id\');\n      if(user_id != null){\n        sessionStorage.removeItem(user_id + \'_course_id\');\n        sessionStorage.removeItem(user_id + \'_vertical_id\');\n        sessionStorage.removeItem(user_id + \'_type\');\n        sessionStorage.removeItem(user_id + \'_time\');\n        sessionStorage.removeItem(\'user_id\');\n      }\n    }\n\n    clearTimeSessionStorage();\n\n  </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        settings = context.get('settings', UNDEFINED)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 55
        __M_writer(u'<title>')
        __M_writer(filters.decode.utf8(_("Log into your {platform_name} Account").format(platform_name=settings.PLATFORM_NAME)))
        __M_writer(u'</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


