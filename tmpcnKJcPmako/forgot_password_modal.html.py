# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229564.574592
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/forgot_password_modal.html'
_template_uri = u'forgot_password_modal.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 3
from django.core.urlresolvers import reverse 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n<!--@begin:Add new page style-->\n<!--@date:2013-11-02-->\n<style>\n  #forgot-password-modal #password-reset .form-actions button[type="submit"]:hover {\n  background:#6e8194;\n  transition-delay: 0s, 0s, 0s;\n  transition-duration: 0.25s, 0.25s, 0.25s;\n  transition-property:color, background,\u200b box-shadow;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  transition-duration:0.25s,\u200b 0.25s,\u200b 0.25s;\n  color:#fff;\n  }\n  #forgot-password-modal #password-reset .form-actions button[type="submit"] {\n  background-color:#556370;\n  text-decoration: none;\n  padding-bottom: 7px;\n  padding-left: 10px;\n  padding-right: 10px;\n  padding-top: 7px;\n  border-bottom-left-radius: 2px;\n  border-bottom-right-radius: 2px;\n  cursor: pointer;\n  border-top-left-radius: 2px;\n  border-top-right-radius: 2px;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  box-shadow: #949494 0px 2px 1px 0px;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n  #forgot-password-modal #password-reset .form-actions button[type="submit"]:normal {\n  background-color:#126F9A;\n  text-decoration: none;\n  border-bottom-left-radius: 2px;\n  border-bottom-right-radius: 2px;\n  cursor: pointer;\n  border-top-left-radius: 2px;\n  border-top-right-radius: 2px;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  box-shadow: rgb(10, 74, 103) 0px 2px 1px 0px;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n</style>\n<!--@end-->\n\n\n<section id="forgot-password-modal" class="modal forgot-password-modal">\n  <div class="inner-wrapper">\n    <div id="password-reset">\n      <header>\n        <h2>')
        # SOURCE LINE 55
        __M_writer(filters.decode.utf8(_("Password Reset")))
        __M_writer(u'</h2>\n      </header>\n\n      <div class="instructions">\n        <p>')
        # SOURCE LINE 59
        __M_writer(filters.decode.utf8(_("Please enter your e-mail address below, and we will e-mail instructions for setting a new password.")))
        __M_writer(u'</p>\n      </div>\n\n      <form id="pwd_reset_form" action="')
        # SOURCE LINE 62
        __M_writer(filters.decode.utf8(reverse('password_reset')))
        __M_writer(u'" method="post" data-remote="true">\n        <fieldset class="group group-form group-form-requiredinformation">\n          <legend class="is-hidden">')
        # SOURCE LINE 64
        __M_writer(filters.decode.utf8(_("Required Information")))
        __M_writer(u'</legend>\n\n          <ol class="list-input">\n<!--@begin:Change the table style-->\n<!--@date:2013-11-02-->\n            <li class="field text" id="field-email">\n              <label for="pwd_reset_email" style="font-weight:bold;">')
        # SOURCE LINE 70
        __M_writer(filters.decode.utf8(_("Your E-mail Address")))
        __M_writer(u'</label>\n              <input style="font-size:12px;" id="pwd_reset_email" type="email" name="email" value="" placeholder="example: username@domain.com" />\n\t\t\t  <span class="tip tip-input" style="font-size:13px;">')
        # SOURCE LINE 72
        __M_writer(filters.decode.utf8(_("This is the email address you used to register with {platform}").format(platform=settings.PLATFORM_NAME)))
        __M_writer(u'.</span>\n<!--@end-->                          \n            </li>\n          </ol>\n        </fieldset>\n\n        <div class="form-actions">\n<!--@begin:Change the text in the submit button-->\n<!--@date:2013-11-02-->          \n          <button name="submit" type="submit" id="pwd_reset_button" class="action action-primary action-update">')
        # SOURCE LINE 81
        __M_writer(filters.decode.utf8(_("Reset Password")))
        __M_writer(u'</button>\n<!--@end-->           \n        </div>\n      </form>\n    </div>\n\n    <a href="#" class="close-modal" title="Close Modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </a>\n  </div>\n</section>\n\n<script type="text/javascript">\n  (function() {\n   $(document).delegate(\'#pwd_reset_form\', \'ajax:success\', function(data, json, xhr) {\n     if(json.success) {\n       $("#password-reset").html(json.value);\n     } else {\n       $(\'#pwd_error\').remove()\n       $(\'#pwd_reset_form\').prepend(\'<div id="pwd_error" class="modal-form-error">\'+json.error+\'</div>\');\n       $(\'#pwd_error\').stop().css("display", "block");\n     }\n   });\n   // removing close link\'s default behavior\n   $(\'#login-modal .close-modal\').click(function(e) {\n    e.preventDefault();\n   });\n  })(this)\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


