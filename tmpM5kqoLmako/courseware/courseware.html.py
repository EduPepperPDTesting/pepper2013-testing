# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223109.695444
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/courseware.html'
_template_uri = 'courseware/courseware.html'
_source_encoding = 'utf-8'
_exports = [u'headextra', u'header_extras', u'js_extra', u'bodyclass', u'title']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 2
from courseware.courses import course_author_image_url 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'/static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def bodyclass():
            return render_bodyclass(context.locals_(__M_locals))
        def title():
            return render_title(context.locals_(__M_locals))
        timer_navigation_return_url = context.get('timer_navigation_return_url', UNDEFINED)
        accordion = context.get('accordion', UNDEFINED)
        content = context.get('content', UNDEFINED)
        course = context.get('course', UNDEFINED)
        def js_extra():
            return render_js_extra(context.locals_(__M_locals))
        timer_expiration_duration = context.get('timer_expiration_duration', UNDEFINED)
        static = _mako_get_namespace(context, 'static')
        chat = context.get('chat', UNDEFINED)
        def headextra():
            return render_headextra(context.locals_(__M_locals))
        def header_extras():
            return render_header_extras(context.locals_(__M_locals))
        show_chat = context.get('show_chat', UNDEFINED)
        time_expired_redirect_url = context.get('time_expired_redirect_url', UNDEFINED)
        staff_access = context.get('staff_access', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'bodyclass'):
            context['self'].bodyclass(**pageargs)
        

        # SOURCE LINE 5
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 6
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'headextra'):
            context['self'].headextra(**pageargs)
        

        # SOURCE LINE 18
        __M_writer(u'\n\n<style type="text/css" media="screen">\n  [class^="icon-"], [class*=" icon-"] {font-family: "FontAwesome" !important;}\n  .course_author_image_div{border-bottom-style:solid;border-bottom-width:1px;border-bottom-color:#aaa;}\n</style>\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header_extras'):
            context['self'].header_extras(**pageargs)
        

        # SOURCE LINE 30
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'js_extra'):
            context['self'].js_extra(**pageargs)
        

        # SOURCE LINE 264
        __M_writer(u'\n\n')
        # SOURCE LINE 266
        if timer_expiration_duration:
            # SOURCE LINE 267
            __M_writer(u'<div class="timer-main">\n  <div id="timer_wrapper">\n')
            # SOURCE LINE 269
            if timer_navigation_return_url:
                # SOURCE LINE 270
                __M_writer(u'    <a href="')
                __M_writer(filters.decode.utf8(timer_navigation_return_url))
                __M_writer(u'" class="timer_return_url">')
                __M_writer(filters.decode.utf8(_("Return to Exam")))
                __M_writer(u'</a>\n')
            # SOURCE LINE 272
            __M_writer(u'    <div class="timer_label">Time Remaining:</div> <div id="exam_timer" class="timer_value">&nbsp;</div>\n  </div>\n</div>\n')
        # SOURCE LINE 276
        __M_writer(u'\n\n')
        # SOURCE LINE 278
        if accordion:
            # SOURCE LINE 279
            __M_writer(u' ')
            runtime._include_file(context, u'/courseware/course_navigation.html', _template_uri, active_page='courseware')
            __M_writer(u'\n')
        # SOURCE LINE 281
        __M_writer(u' \n<section class="container">\n  <div class="course-wrapper">\n<!--@begin:Change the color of the left index in My course-->\n<!--@date:2013-11-02-->\n<style type="text/css" media="screen">\n  #accordion a{color:#366092}\n</style>\n<!--@end-->    \n\n\n')
        # SOURCE LINE 292
        if accordion:
            # SOURCE LINE 293
            __M_writer(u'    <section aria-label="')
            __M_writer(filters.decode.utf8(_('Course Navigation')))
            __M_writer(u'" class="course-index">\n      <header id="open_close_accordion">\n        <a href="#">')
            # SOURCE LINE 295
            __M_writer(filters.decode.utf8(_("close")))
            __M_writer(u'</a>\n      </header>\n      <div class="course_author_image_div">\n        <img src="')
            # SOURCE LINE 298
            __M_writer(filters.decode.utf8(course_author_image_url(course)))
            __M_writer(u'" width="100%" alt=""/>\n      </div>\n      <div id="accordion" style="display: none">\n        <nav>\n          ')
            # SOURCE LINE 302
            __M_writer(filters.decode.utf8(accordion))
            __M_writer(u'\n        </nav>\n      </div>\n    </section>\n')
        # SOURCE LINE 307
        __M_writer(u'\n    <section class="course-content">\n')
        # SOURCE LINE 309
        if course.hide_timer == False:
            # SOURCE LINE 310
            if course.show_external_timer == False:
                # SOURCE LINE 311
                __M_writer(u'        <div class="course_timer"></div>\n')
                # SOURCE LINE 312
            else:
                # SOURCE LINE 313
                __M_writer(u'        <div class="external_timer"></div>\n')
        # SOURCE LINE 316
        __M_writer(u'      ')
        __M_writer(filters.decode.utf8(content))
        __M_writer(u'\n    </section>\n  </div>\n</section>\n\n')
        # SOURCE LINE 321
        if show_chat:
            # SOURCE LINE 322
            __M_writer(u'  <div id="chat-wrapper">\n    <div id="chat-toggle" class="closed">\n      <span id="chat-open">Open Chat <em class="icon-chevron-up"></em></span>\n      <span id="chat-close">Close Chat <em class="icon-chevron-down"></em></span>\n    </div>\n    <div id="chat-block">\n')
            # SOURCE LINE 329
            __M_writer(u'      <div id="candy"></div>\n    </div>\n  </div>\n')
        # SOURCE LINE 333
        __M_writer(u'\n')
        # SOURCE LINE 334
        if course.show_calculator:
            # SOURCE LINE 335
            __M_writer(u'    <div class="calc-main">\n        <a aria-label="')
            # SOURCE LINE 336
            __M_writer(filters.decode.utf8(_('Open Calculator')))
            __M_writer(u'" href="#" class="calc">')
            __M_writer(filters.decode.utf8(_("Calculator")))
            __M_writer(u'</a>\n\n        <div id="calculator_wrapper">\n            <form id="calculator">\n                <div class="input-wrapper">\n                    <input type="text" id="calculator_input" title="Calculator Input Field" />\n\n                    <div class="help-wrapper">\n                        <a href="#">')
            # SOURCE LINE 344
            __M_writer(filters.decode.utf8(_("Hints")))
            __M_writer(u'</a>\n                        <dl class="help">\n                            <dt>')
            # SOURCE LINE 346
            __M_writer(filters.decode.utf8(_("Suffixes:")))
            __M_writer(u'</dt>\n                            <dd> %kMGTcmunp</dd>\n                            <dt>')
            # SOURCE LINE 348
            __M_writer(filters.decode.utf8(_("Operations:")))
            __M_writer(u'</dt>\n                            <dd>^ * / + - ()</dd>\n                            <dt>')
            # SOURCE LINE 350
            __M_writer(filters.decode.utf8(_("Functions:")))
            __M_writer(u'</dt>\n                            <dd>sin, cos, tan, sqrt, log10, log2, ln, arccos, arcsin, arctan, abs </dd>\n                            <dt>')
            # SOURCE LINE 352
            __M_writer(filters.decode.utf8(_("Constants")))
            __M_writer(u'</dt>\n                            <dd>e, pi</dd>\n\n                            <!-- Students won\'t know what parallel means at this time.  Complex numbers aren\'t well tested in the courseware, so we would prefer to not expose them.  If you read the comments in the source, feel free to use them. If you run into a bug, please let us know. But we can\'t officially support them right now.\n\n                            <dt>Unsupported:</dt> <dd>||, j </dd>  -->\n                        </dl>\n                    </div>\n                </div>\n                <input id="calculator_button" type="submit" title="Calculate" value="="/>\n                <input type="text" id="calculator_output" title="Calculator Output Field" readonly />\n            </form>\n\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headextra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def headextra():
            return render_headextra(context)
        static = _mako_get_namespace(context, 'static')
        show_chat = context.get('show_chat', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 8
        __M_writer(u'\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 9
            __M_writer(filters.decode.utf8(static.css(group=u'course')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n  ')
        # SOURCE LINE 10
        runtime._include_file(context, u'../discussion/_js_head_dependencies.html', _template_uri)
        __M_writer(u'\n')
        # SOURCE LINE 11
        if show_chat:
            # SOURCE LINE 12
            __M_writer(u'    <link rel="stylesheet" href="')
            __M_writer(filters.decode.utf8(static.url('css/vendor/ui-lightness/jquery-ui-1.8.22.custom.css')))
            __M_writer(u'" />\n')
            # SOURCE LINE 16
            __M_writer(u'    <link rel="stylesheet" href="')
            __M_writer(filters.decode.utf8(static.url('candy_res/candy_full.css')))
            __M_writer(u'" />\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header_extras(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def header_extras():
            return render_header_extras(context)
        static = _mako_get_namespace(context, 'static')
        __M_writer = context.writer()
        # SOURCE LINE 24
        __M_writer(u'\n')
        # SOURCE LINE 25
        for template_name in ["image-modal"]:
            # SOURCE LINE 26
            __M_writer(u'<script type="text/template" id="')
            __M_writer(filters.decode.utf8(template_name))
            __M_writer(u'-tpl">\n    ')
            def ccall(caller):
                def body():
                    __M_writer = context.writer()
                    return ''
                return [body]
            context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
            try:
                # SOURCE LINE 27
                __M_writer(filters.decode.utf8(static.include(path=u'js/' + (template_name) + u'.underscore')))
            finally:
                context.caller_stack.nextcaller = None
            __M_writer(u'\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js_extra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        timer_expiration_duration = context.get('timer_expiration_duration', UNDEFINED)
        time_expired_redirect_url = context.get('time_expired_redirect_url', UNDEFINED)
        course = context.get('course', UNDEFINED)
        def js_extra():
            return render_js_extra(context)
        static = _mako_get_namespace(context, 'static')
        chat = context.get('chat', UNDEFINED)
        show_chat = context.get('show_chat', UNDEFINED)
        staff_access = context.get('staff_access', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 31
        __M_writer(u'\n  <script type="text/javascript" src="')
        # SOURCE LINE 32
        __M_writer(filters.decode.utf8(static.url('js/vendor/jquery.scrollTo-1.4.2-min.js')))
        __M_writer(u'"></script>\n  <script type="text/javascript" src="')
        # SOURCE LINE 33
        __M_writer(filters.decode.utf8(static.url('js/vendor/flot/jquery.flot.js')))
        __M_writer(u'"></script>\n\n')
        # SOURCE LINE 36
        __M_writer(u'  <script type="text/javascript" src="')
        __M_writer(filters.decode.utf8(static.url('js/vendor/codemirror-compressed.js')))
        __M_writer(u'"></script>\n  <script type="text/javascript" src="')
        # SOURCE LINE 37
        __M_writer(filters.decode.utf8(static.url('js/my_chunks.js')))
        __M_writer(u'"></script>\n\n')
        # SOURCE LINE 43
        __M_writer(u' \n<!--@begin:Load and initialize ORA editor-->\n<!--@date:2013-11-02-->\n\n<script type="text/javascript">\n  \n</script>\n  <script type="text/javascript" src="')
        # SOURCE LINE 50
        __M_writer(filters.decode.utf8(static.url('js/vendor/tiny_mce/tiny_mce.js')))
        __M_writer(u'"></script>\n  <script type="text/javascript">\n    tinymce.baseURL=\'/static/js/vendor/tiny_mce\'\n    var tinyMCE_init_sate=0;\n    var switch_content_page=0;\n    \n    tinymce.baseURL=\'/static/js/vendor/tiny_mce\'\n    \n    function tinyMCE_init()\n    {\n        if(!tinyMCE_init_sate){\n\n          tinyMCE.init({\n          // General options\n          mode : "textareas",\n          editor_selector : "mceEditor",\n          theme : "advanced",\n          plugins : "contextmenu,paste,style,advimage,table,fullscreen,spellchecker",\n          spellchecker_languages : "+English=en",\n          // Theme options\n          theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect",\n          theme_advanced_buttons2 : "outdent,indent,blockquote,|,undo,redo,link,unlink,|,forecolor,backcolor,sub,sup,|,fullscreen,spellchecker",\n          theme_advanced_buttons3 : "tablecontrols,|,image",\n          theme_advanced_toolbar_location : "top",\n          theme_advanced_toolbar_align : "left",\n          theme_advanced_statusbar_location : "",\n          theme_advanced_resizing : false,\n          popup_css: \'/static/js/vendor/tiny_mce/themes/advanced/skins/default/dialog.css\',\n            setup : function(ed) {\n              ed.onInit.add(function(ed, evt) {\n                tinyMCE.execCommand(\'mceSpellCheck\');\n                if (document.documentElement.scrollTop==0){\n                  document.body.scrollTop = 0\n                }\n                else{\n                  document.documentElement.scrollTop = 0\n                }\n                \n              });\n            }\n            });\n          tinyMCE_init_sate=1;\n      }\n    }\n    function tinyMCE_class_init(name)\n    {   \n        tinyMCE.init({\n        // General options\n        mode : "textareas",\n        editor_selector : name,\n        theme : "advanced",\n        plugins : "contextmenu,paste,style,advimage,table,fullscreen,spellchecker",\n        spellchecker_languages : "+English=en",\n        // Theme options\n        theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect",\n        theme_advanced_buttons2 : "outdent,indent,blockquote,|,undo,redo,link,unlink,|,forecolor,backcolor,sub,sup,|,fullscreen,spellchecker",\n        theme_advanced_buttons3 : "tablecontrols,|,image",\n        theme_advanced_toolbar_location : "top",\n        theme_advanced_toolbar_align : "left",\n        theme_advanced_statusbar_location : "",\n        theme_advanced_resizing : false,\n        popup_css: \'/static/js/vendor/tiny_mce/themes/advanced/skins/default/dialog.css\',\n          setup : function(ed) {\n              ed.onInit.add(function(ed, evt) {\n                tinyMCE.execCommand(\'mceSpellCheck\');\n                if (document.documentElement.scrollTop==0){\n                  document.body.scrollTop = 0\n                }\n                else{\n                  document.documentElement.scrollTop = 0\n                }\n                \n              });\n            }\n          });\n    }\n     function tinyMCE_sate(val)\n    {\n      tinyMCE_init_sate=val;\n    }\n    function set_tinyMCE_switchPage(val)\n    {\n      switch_content_page=val;\n    }\n    function get_tinyMCE_switchPage()\n    {\n      return switch_content_page;\n    }\n  </script>\n  <!--@end-->\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 140
            __M_writer(filters.decode.utf8(static.js(group=u'courseware')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n  ')
        def ccall(caller):
            def body():
                __M_writer = context.writer()
                return ''
            return [body]
        context.caller_stack.nextcaller = runtime.Namespace('caller', context, callables=ccall(__M_caller))
        try:
            # SOURCE LINE 141
            __M_writer(filters.decode.utf8(static.js(group=u'discussion')))
        finally:
            context.caller_stack.nextcaller = None
        __M_writer(u'\n\n  ')
        # SOURCE LINE 143
        runtime._include_file(context, u'../discussion/_js_body_dependencies.html', _template_uri)
        __M_writer(u'\n')
        # SOURCE LINE 144
        if staff_access:
            # SOURCE LINE 145
            __M_writer(u'    ')
            runtime._include_file(context, u'xqa_interface.html', _template_uri)
            __M_writer(u'\n')
        # SOURCE LINE 147
        __M_writer(u'\n  <!-- TODO: http://docs.jquery.com/Plugins/Validation -->\n  <script type="text/javascript">\n/*@begin:Change the following to be comments as loading youtub slows down the page loading in China*/\n/*@date:2013-11-02*/    \n    //document.write(\'\\x3Cscript type="text/javascript" src="\' +\n        //document.location.protocol + \'//www.youtube.com/iframe_api">\\x3C/script>\');\n/*@end*/\n  </script>\n\n  <script type="text/javascript">\n    var $$course_id = "')
        # SOURCE LINE 158
        __M_writer(filters.decode.utf8(course.id))
        __M_writer(u'";\n\n    $(function(){\n        $(".ui-accordion-header a, .ui-accordion-content .subtitle").each(function() {\n          var elemText = $(this).text().replace(/^\\s+|\\s+$/g,\'\'); // Strip leading and trailing whitespace\n          var wordArray = elemText.split(" ");\n          var finalTitle = "";\n          if (wordArray.length > 0) {\n            for (i=0;i<=wordArray.length-1;i++) {\n              finalTitle += wordArray[i];\n              if (i == (wordArray.length-2)) {\n                finalTitle += "&nbsp;";\n              } else if (i == (wordArray.length-1)) {\n                // Do nothing\n              } else {\n                finalTitle += " ";\n              }\n            }\n          }\n          $(this).html(finalTitle);\n        });\n      });\n  </script>\n\n')
        # SOURCE LINE 182
        if timer_expiration_duration:
            # SOURCE LINE 183
            __M_writer(u'  <script type="text/javascript">\n    var timer = {\n      timer_inst : null,\n      end_time : null,\n      get_remaining_secs : function(endTime) {\n        var currentTime = new Date();\n        var remaining_secs = Math.floor((endTime - currentTime)/1000);\n        return remaining_secs;\n      },\n      get_time_string : function() {\n        function pretty_time_string(num) {\n          return ( num < 10 ? "0" : "" ) + num;\n        }\n        // count down in terms of hours, minutes, and seconds:\n        var hours = pretty_time_string(Math.floor(remaining_secs / 3600));\n        remaining_secs = remaining_secs % 3600;\n        var minutes = pretty_time_string(Math.floor(remaining_secs / 60));\n        remaining_secs = remaining_secs % 60;\n        var seconds = pretty_time_string(Math.floor(remaining_secs));\n\n        var remainingTimeString = hours + ":" + minutes + ":" + seconds;\n        return remainingTimeString;\n      },\n      update_time : function(self) {\n        remaining_secs = self.get_remaining_secs(self.end_time);\n        if (remaining_secs <= 0) {\n          self.end(self);\n        }\n        $(\'#exam_timer\').text(self.get_time_string(remaining_secs));\n      },\n      start : function() { var that = this;\n        // set the end time when the template is rendered.\n        // This value should be UTC time as number of milliseconds since epoch.\n        this.end_time = new Date((new Date()).getTime() + ')
            # SOURCE LINE 216
            __M_writer(filters.decode.utf8(timer_expiration_duration))
            __M_writer(u');\n        this.timer_inst = setInterval(function(){ that.update_time(that); }, 1000);\n      },\n      end : function(self) {\n        clearInterval(self.timer_inst);\n        // redirect to specified URL:\n        window.location = "')
            # SOURCE LINE 222
            __M_writer(filters.decode.utf8(time_expired_redirect_url))
            __M_writer(u'";\n      }\n    }\n    // start timer right away:\n    timer.start();\n  </script>\n')
        # SOURCE LINE 229
        __M_writer(u'\n')
        # SOURCE LINE 230
        if show_chat:
            # SOURCE LINE 231
            __M_writer(u'  <script type="text/javascript" src="')
            __M_writer(filters.decode.utf8(static.url('js/vendor/candy_libs/libs.min.js')))
            __M_writer(u'"></script>\n  <script type="text/javascript" src="')
            # SOURCE LINE 232
            __M_writer(filters.decode.utf8(static.url('js/vendor/candy.min.js')))
            __M_writer(u'"></script>\n\n  <script type="text/javascript">\n    // initialize the Candy.js plugin\n    $(document).ready(function() {\n      Candy.init("http://')
            # SOURCE LINE 237
            __M_writer(filters.decode.utf8(chat['domain']))
            __M_writer(u':5280/http-bind/", {\n        core: { debug: true, autojoin: ["')
            # SOURCE LINE 238
            __M_writer(filters.decode.utf8(chat['room']))
            __M_writer(u'@conference.')
            __M_writer(filters.decode.utf8(chat['domain']))
            __M_writer(u'"] },\n        view: { resources: "')
            # SOURCE LINE 239
            __M_writer(filters.decode.utf8(static.url('candy_res/')))
            __M_writer(u'"}\n      });\n      Candy.Core.connect("')
            # SOURCE LINE 241
            __M_writer(filters.decode.utf8(chat['username']))
            __M_writer(u'", "')
            __M_writer(filters.decode.utf8(chat['password']))
            __M_writer(u'");\n\n      // show/hide the chat widget\n      $(\'#chat-toggle\').click(function() {\n        var toggle = $(this);\n        if (toggle.hasClass(\'closed\')) {\n          $(\'#chat-block\').show().animate({height: \'400px\'}, \'slow\', function() {\n            $(\'#chat-open\').hide();\n            $(\'#chat-close\').show();\n          });\n        } else {\n          $(\'#chat-block\').animate({height: \'0px\'}, \'slow\', function() {\n            $(\'#chat-open\').show();\n            $(\'#chat-close\').hide();\n            $(this).hide(); // do this at the very end\n          });\n        }\n        toggle.toggleClass(\'closed\');\n      });\n    });\n  </script>\n')
        # SOURCE LINE 263
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bodyclass(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        course = context.get('course', UNDEFINED)
        def bodyclass():
            return render_bodyclass(context)
        __M_writer = context.writer()
        # SOURCE LINE 5
        __M_writer(u'courseware ')
        __M_writer(filters.decode.utf8(course.css_class))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        course = context.get('course', UNDEFINED)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'<title course_number="')
        __M_writer(filters.decode.utf8(course.display_number_with_default))
        __M_writer(u'">')
        __M_writer(filters.html_escape(filters.decode.utf8(_("{course_number} Course").format(course_number=course.display_number_with_default) )))
        __M_writer(u'</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


