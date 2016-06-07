# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224884.435245
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/communities/community_edit.html'
_template_uri = 'communities/community_edit.html'
_source_encoding = 'utf-8'
_exports = [u'title']


# SOURCE LINE 1

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from file_uploader.utils import get_file_url
from administration.configuration import has_hangout_perms
from student.models import State,District


# SOURCE LINE 8
navbar_show_extended=False 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 10
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'../static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'../main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        csrf_token = context.get('csrf_token', UNDEFINED)
        hangout = context.get('hangout', UNDEFINED)
        name = context.get('name', UNDEFINED)
        district = context.get('district', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        facilitator = context.get('facilitator', UNDEFINED)
        request = context.get('request', UNDEFINED)
        user_type = context.get('user_type', UNDEFINED)
        private = context.get('private', UNDEFINED)
        community_id = context.get('community_id', UNDEFINED)
        courses = context.get('courses', UNDEFINED)
        state = context.get('state', UNDEFINED)
        courses_drop = context.get('courses_drop', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        logo = context.get('logo', UNDEFINED)
        motto = context.get('motto', UNDEFINED)
        resources = context.get('resources', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n')
        # SOURCE LINE 8
        __M_writer(u'\n')
        # SOURCE LINE 9
        __M_writer(u'\n')
        # SOURCE LINE 10
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 11
        __M_writer(u'\n<link rel="stylesheet" type="text/css"  href="/static/css/communities.css"/>\n\n<style type="text/css" media="screen">\n    #page-nav,#page-footer{width:1180px;}\n    #btn-logged-user{display:none;}\n    .form-select{font-size:14px !important;width:180px;}\n    .image-link-style{\n        border-radius: 6px;\n        -moz-border-radius: 6px;\n        -webkit-border-radius: 6px;\n        display: block;\n        float: left;\n        margin: 30px;\n    }\n    .image-bottom-style{\n        border-radius: 0 0 6px 6px;\n        -moz-border-radius: 0 0 6px 6px;\n        -webkit-border-radius: 0 0 6px 6px;\n        display: block;\n    }\n    .card-link{\n        display: table-cell;\n        width: 240px;\n        height: 60px;\n        vertical-align: middle;\n        padding: 0 17px;\n        font-size: 22px;\n        background: rgba(18,111,154,0.95);\n        text-decoration: none!important;\n    }\n    .card-link span{\n        color: #FFFFFF;\n    }\n    .community-form {\n        margin: 0 auto;\n        width: 900px;\n        padding: 20px;\n    }\n    #community-name,\n    #community-hangouts,\n    #community-logo,\n    #community-facilitator,\n    #community-state,\n    #community-district {\n        display: block;\n        float: left;\n        margin: 0 40px 20px 0;\n        text-align: left;\n        position: relative;\n    }\n    .community-form label {\n        cursor: default !important;\n    }\n    #community-logo .remove {\n        display: block;\n        background: #fff center url(/static/images/moderator-delete-icon.png) no-repeat;\n        width: 12px;\n        height: 11px;\n        border: solid 1px #ddd;\n        border-radius: 1px;\n        position: absolute;\n        top: 1.25em;\n        right: 2px;\n    }\n    #community-name input, #community-facilitator input {\n        display: block;\n        width: 500px;\n    }\n    #community-logo input,\n    #community-state select,\n    #community-district select {\n        display: block;\n    }\n    #community-name,\n    #community-motto,\n    #community-courses,\n    #community-resources {\n        clear: both;\n        display: block;\n        text-align: left;\n        margin-bottom: 20px;\n    }\n    #community-motto input {\n        display: block;\n        width: 860px;\n    }\n    #community-state {\n        float: left;\n    }\n    #community-private {\n        display: block;\n        float: right;\n        text-align: left;\n        clear: both;\n    }\n    #community-private input {\n        margin-left: 10px;\n    }\n    #community-hangouts div {\n        line-height: 2.5em;\n    }\n    #community-hangouts input {\n        width: 500px;\n    }\n    #community-courses span, #community-resources span, #community-logo span {\n        display: block;\n    }\n    #community-courses input, #community-courses select, #community-resources input, .resource-logo-label {\n        display: block;\n        float: left;\n        margin: 0 20px 20px 0;\n    }\n    .resource-link, .resource-name {\n        width: 220px;\n    }\n    #community-form-buttons {\n        clear: both;\n        margin: 0 auto;\n        padding-top: 20px;\n        text-align: right;\n    }\n    #community-cancel {\n        float: left;\n    }\n    #community-resources .add, #community-courses .add {\n        padding: 0 6px;\n    }\n    #community-resources .minus, #community-courses .minus {\n        padding: 0 8px;\n    }\n    .community-course, .community-resource, #community-state {\n        clear: both;\n    }\n    .community-logo-thumb {\n        float: left;\n        width: 150px;\n        margin-right: 10px;\n    }\n    .community-resource-logo-wrap {\n        float: left;\n        width: 150px;\n        margin-right: 10px;\n        position: relative;\n    }\n    .community-resource-logo-wrap .remove {\n        display: block;\n        background: #fff center url(/static/images/moderator-delete-icon.png) no-repeat;\n        width: 12px;\n        height: 11px;\n        border: solid 1px #ddd;\n        border-radius: 1px;\n        position: absolute;\n        top: -2px;\n        right: -2px;\n    }\n    .community-error-box {\n        border-color: red !important;\n    }\n    .about-field {\n        color: #999;\n        font-size: 80%;\n        display: inline !important;\n    }\n</style>\n<section class="community-form" style="text-align:center;background:#F5F5F5;">\n    <form action="')
        # SOURCE LINE 177
        __M_writer(filters.decode.utf8(reverse('community_edit_process')))
        __M_writer(u'" method="post" enctype="multipart/form-data" id="community-edit-form">\n        <label id="community-name"><span>Community Name:</span><input type="text" name="name" value="')
        # SOURCE LINE 178
        __M_writer(filters.decode.utf8(name))
        __M_writer(u'" placeholder="The name of the community"></label>\n')
        # SOURCE LINE 179
        if logo != '':
            # SOURCE LINE 180
            __M_writer(u'            <label id="community-logo"><span>Logo:</span><img class="community-logo-thumb" src="')
            __M_writer(filters.decode.utf8(logo))
            __M_writer(u'"><input type="hidden" name="logo" value="')
            __M_writer(filters.decode.utf8(logo))
            __M_writer(u'"><a href="#" class="remove"></a></label>\n')
            # SOURCE LINE 181
        else:
            # SOURCE LINE 182
            __M_writer(u'            <label id="community-logo"><span>Logo <span class="about-field">(380px X 260px or larger for best results)</span>:</span><input type="file" name="logo"></label>\n')
        # SOURCE LINE 184
        __M_writer(u'        <label id="community-motto"><span>Description (Motto):</span><input type="text" name="motto" value="')
        __M_writer(filters.decode.utf8(motto))
        __M_writer(u'" placeholder="A description or motto for this community"></label>\n        <label id="community-facilitator"><span>Facilitator:</span><input type="text" name="facilitator" value="')
        # SOURCE LINE 185
        __M_writer(filters.decode.utf8(facilitator))
        __M_writer(u'" placeholder="The email of the user who will administer this community"></label>\n')
        # SOURCE LINE 186
        if user_type == 'super':
            # SOURCE LINE 187
            __M_writer(u'            <label id="community-state"><span>Select State:</span>\n                <select id="state-dropdown" name="state-dropdown"></select>\n            </label>\n            <label id="community-district"><span>Select District:</span>\n                <select id="district-dropdown" name="district-dropdown"></select>\n            </label>\n')
            # SOURCE LINE 193
        else:
            # SOURCE LINE 194
            __M_writer(u'            <label id="community-state"><span>Select State:</span>\n                <select id="state-dropdown" name="state-dropdown" disabled></select>\n            </label>\n            <label id="community-district"><span>Select District:</span>\n                <select id="district-dropdown" name="district-dropdown" disabled></select>\n            </label>\n')
        # SOURCE LINE 201
        if private:
            # SOURCE LINE 202
            __M_writer(u'            <label id="community-private"><span>Private Group:</span><input type="checkbox" name="private" value="1" checked="checked"></label>\n')
            # SOURCE LINE 203
        else:
            # SOURCE LINE 204
            __M_writer(u'            <label id="community-private"><span>Private Group:</span><input type="checkbox" name="private" value="1"></label>\n')
        # SOURCE LINE 206
        if has_hangout_perms(request.user):
            # SOURCE LINE 207
            __M_writer(u'            <label id="community-hangouts"><span>Hangouts Setup:</span>\n                <div>\n                    <span>1. </span><a href="http://hangouts.google.com/start" target="_blank">Start Hangout</a>&nbsp;&nbsp;&nbsp;\n                    <span>2. </span><input type="text" name="hangout" value="')
            # SOURCE LINE 210
            __M_writer(filters.decode.utf8(hangout))
            __M_writer(u'" placeholder="Copy/Paste Hangout URL Here">\n                </div>\n            </label>\n')
        # SOURCE LINE 214
        __M_writer(u'        <label id="community-courses"><span>Courses:</span>\n')
        # SOURCE LINE 215
        for idx, course in enumerate(courses):
            # SOURCE LINE 216
            __M_writer(u'            <div class="community-course">\n                <select name="course[')
            # SOURCE LINE 217
            __M_writer(filters.decode.utf8(idx))
            __M_writer(u']">\n                    <option value="">Select a Course</option>\n')
            # SOURCE LINE 219
            for course_option in courses_drop:
                # SOURCE LINE 220
                if course == course_option['id']:
                    # SOURCE LINE 221
                    __M_writer(u'                            <option value="')
                    __M_writer(filters.decode.utf8(course_option['id']))
                    __M_writer(u'" selected="selected">')
                    __M_writer(filters.decode.utf8(course_option['number']))
                    __M_writer(u' | ')
                    __M_writer(filters.decode.utf8(course_option['name']))
                    __M_writer(u'</option>\n')
                    # SOURCE LINE 222
                else:
                    # SOURCE LINE 223
                    __M_writer(u'                            <option value="')
                    __M_writer(filters.decode.utf8(course_option['id']))
                    __M_writer(u'">')
                    __M_writer(filters.decode.utf8(course_option['number']))
                    __M_writer(u' | ')
                    __M_writer(filters.decode.utf8(course_option['name']))
                    __M_writer(u'</option>\n')
            # SOURCE LINE 226
            __M_writer(u'                </select>\n                <input type="button" class="add operation" value="+" onclick="newCourse()">\n            </div>\n')
        # SOURCE LINE 230
        __M_writer(u'        </label>\n        <label id="community-resources"><span>Resources:</span>\n')
        # SOURCE LINE 232
        for idx, resource in enumerate(resources):
            # SOURCE LINE 233
            __M_writer(u'            <div class="community-resource">\n                <input class="resource-name" type="text" name="resource_name[')
            # SOURCE LINE 234
            __M_writer(filters.decode.utf8(idx))
            __M_writer(u']" value="')
            __M_writer(filters.decode.utf8(resource['name']))
            __M_writer(u'" placeholder="Resource name">\n                <input class="resource-link" type="text" name="resource_link[')
            # SOURCE LINE 235
            __M_writer(filters.decode.utf8(idx))
            __M_writer(u']" value="')
            __M_writer(filters.decode.utf8(resource['link']))
            __M_writer(u'" placeholder="Resource link">\n                <label><div class="resource-logo-label">Logo:</div>\n')
            # SOURCE LINE 237
            if resource['logo']:
                # SOURCE LINE 238
                __M_writer(u'                    <div class="community-resource-logo-wrap">\n                        <img src="')
                # SOURCE LINE 239
                __M_writer(filters.decode.utf8(get_file_url(resource['logo'])))
                __M_writer(u'" class="community-logo-thumb">\n                        <input class="community-resource-logo" type="hidden" name="resource_logo[')
                # SOURCE LINE 240
                __M_writer(filters.decode.utf8(idx))
                __M_writer(u']" value="')
                __M_writer(filters.decode.utf8(resource['logo'].id))
                __M_writer(u'">\n                        <a href="#" class="remove"></a>\n                    </div>\n')
                # SOURCE LINE 243
            else:
                # SOURCE LINE 244
                __M_writer(u'                    <input class="resource-logo" type="file" name="resource_logo[')
                __M_writer(filters.decode.utf8(idx))
                __M_writer(u']">\n')
            # SOURCE LINE 246
            __M_writer(u'                </label>\n                <input type="button" class="add operation" value="+" onclick="newResource()">\n            </div>\n')
        # SOURCE LINE 250
        __M_writer(u'        </label>\n        <input type="hidden" value="')
        # SOURCE LINE 251
        __M_writer(filters.decode.utf8(community_id))
        __M_writer(u'" name="community_id">\n        <input type="hidden" name="csrfmiddlewaretoken" value="')
        # SOURCE LINE 252
        __M_writer(filters.decode.utf8(csrf_token))
        __M_writer(u'"/>\n        <div id="community-form-buttons">\n            <input id="community-cancel" type="button" value="Cancel">\n            <input id="community-submit" type="submit" value="Submit" name="submit">\n        </div>\n    </form>\n</section>\n<script type="text/javascript">\n    function newCourse() {\n        var course_num = $(\'.community-course\').length;\n        $(\'.community-course\').each(function(index) {\n            $(this).find(\'.operation\').replaceWith(\'<input type="button" class="minus operation" value="-" onclick="removeCourse(\' + index + \')">\');\n        });\n        var entry = \'<div class="community-course"><select name="course[\' + course_num + \']"><option value="">Select a Course</option>\';\n')
        # SOURCE LINE 266
        for course_option in courses_drop:
            # SOURCE LINE 267
            __M_writer(u'            entry += \'<option value="')
            __M_writer(filters.decode.utf8(course_option['id']))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(course_option['number']))
            __M_writer(u' | ')
            __M_writer(filters.decode.utf8(course_option['name'].replace("'", r"\'")))
            __M_writer(u"</option>';\n")
        # SOURCE LINE 269
        __M_writer(u'        entry += \'</select><input type="button" class="add operation" value="+" onclick="newCourse()"></div>\';\n        $(\'#community-courses\').append(entry);\n    }\n    function newResource() {\n        var resource_num = $(\'.community-resource\').length;\n        $(\'.community-resource\').each(function(index) {\n            $(this).find(\'.operation\').replaceWith(\'<input type="button" class="minus operation" value="-" onclick="removeResource(\' + index + \')">\');\n        });\n        var entry = \'<div class="community-resource">\';\n        entry += \'<input class="resource-name" type="text" name="resource_name[\' + resource_num + \']" value="" placeholder="Resource name">\';\n        entry += \'<input class="resource-link" type="text" name="resource_link[\' + resource_num + \']" value="" placeholder="Resource link">\';\n        entry += \'<label><div class="resource-logo-label">Logo:</div><input  class="resource-logo" type="file" name="resource_logo[\' + resource_num + \']"></label>\';\n        entry += \'<input type="button" class="add operation" value="+" onclick="newResource()">\';\n        $(\'#community-resources\').append(entry);\n    }\n    function removeCourse(index) {\n        $(\'.community-course\').each(function(i) {\n            if (i == index) {\n                $(this).remove();\n            } else {\n                var num = 0;\n                if (i < index) {\n                    num = i;\n                }\n                if (i > index) {\n                    num = i - 1;\n                }\n                $(this).children(\'select\').attr(\'name\', \'course[\' + num + \']\');\n            }\n        });\n        $(\'.community-course .minus\').each(function(index) {\n            $(this).replaceWith(\'<input type="button" class="minus operation" value="-" onclick="removeCourse(\' + index + \')">\');\n        });\n    }\n    function removeResource(index) {\n        $(\'.community-resource\').each(function(i) {\n            if (i == index) {\n                $(this).remove();\n            } else {\n                var num = 0;\n                if (i < index) {\n                    num = i;\n                }\n                if (i > index) {\n                    num = i - 1;\n                }\n                $(this).children(\'.resource-link\').attr(\'name\', \'resource_link[\' + num + \']\');\n                $(this).children(\'.resource-name\').attr(\'name\', \'resource_name[\' + num + \']\');\n                $(this).children(\'.resource-logo\').attr(\'name\', \'resource_logo[\' + num + \']\');\n            }\n        });\n        $(\'.community-resource .minus\').each(function(index) {\n            $(this).replaceWith(\'<input type="button" class="minus operation" value="-" onclick="removeResource(\' + index + \')">\');\n        });\n    }\n    function checkUser(email) {\n        var valid = true;\n        $.ajax({\n            url: "')
        # SOURCE LINE 327
        __M_writer(filters.decode.utf8(reverse('community_check_user')))
        __M_writer(u'",\n            type: \'GET\',\n            async: false,\n            data: {email: email},\n            success: function(data) {\n                valid = data.Valid;\n            }\n        });\n        return valid;\n    }\n    var state_id = \'')
        # SOURCE LINE 337
        __M_writer(filters.decode.utf8(state))
        __M_writer(u"';\n    var district_id = '")
        # SOURCE LINE 338
        __M_writer(filters.decode.utf8(district))
        __M_writer(u"';\n    $(document).ready(function() {\n        $.get('")
        # SOURCE LINE 340
        __M_writer(filters.decode.utf8(reverse('pepper_utilities_drop_states')))
        __M_writer(u'\', function (data) {\n            // Build the options.\n            var options = \'<option value=""></option>\';\n            $.each(data, function (index, object) {\n                options += \'<option value="\' + object.id+ \'"\';\n                if (object.id == state_id) {\n                    options += \' selected\';\n                }\n                options += \'>\' + object.name + \'</option>\';\n            });\n            // Add them to the state dropdown.\n            $(\'#state-dropdown\').append(options);\n            $("#state-dropdown").change(function () {\n                if ($(this).val()) {\n                    // Clear the current district and school options since the state changed.\n                    $(\'#district-dropdown option\').remove();\n                    // Get the allowed Districts\n                    $.get(\'')
        # SOURCE LINE 357
        __M_writer(filters.decode.utf8(reverse('pepper_utilities_drop_districts')))
        __M_writer(u'\', {state: $(this).val()}, function (data) {\n                        var content = \'<option value=""></option>\';\n                        $.each(data, function (index, object) {\n                            content += \'<option value="\' + object.id + \'"\';\n                            if (object.id == district_id) {\n                                content += \' selected\';\n                            }\n                            content += \'>\' + object.name + \'</option>\';\n                        });\n                        // Add it to the form.\n                        $(\'#district-dropdown\').append(content);\n                    });\n                }\n            });\n            if (state_id) {\n                $("#state-dropdown").trigger(\'change\');\n            }\n        });\n        $(\'#community-logo .remove\').click(function() {\n            var content = \'<label id="community-logo"><span>Logo <span class="about-field">(380px X 260px or larger for best results)</span>:</span><input type="file" name="logo"></label>\';\n            $(\'#community-logo\').replaceWith(content);\n        });\n        $(\'.community-resource .remove\').click(function() {\n            var name = $(this).siblings(\'.community-resource-logo\').attr(\'name\');\n            var content = \'<input class="resource-logo" type="file" name="\' + name + \'">\';\n            $(this).parent(\'.community-resource-logo-wrap\').replaceWith(content);\n        });\n        $(\'#community-cancel\').click(function() {\n')
        # SOURCE LINE 385
        if community_id == 'new':
            # SOURCE LINE 386
            __M_writer(u'                window.location.href = "')
            __M_writer(filters.decode.utf8(reverse('communities')))
            __M_writer(u'";\n')
            # SOURCE LINE 387
        else:
            # SOURCE LINE 388
            __M_writer(u'                window.location.href = "')
            __M_writer(filters.decode.utf8(reverse('community_view', args=[community_id])))
            __M_writer(u'";\n')
        # SOURCE LINE 390
        __M_writer(u"        });\n        $('#community-edit-form').submit(function() {\n            $('.community-error-box').removeClass('community-error-box');\n            var valid = true;\n            var errors = ['The following errors occurred:\\n'];\n            if (!/[A-Za-z]/.test($('#community-name input').val())) {\n                valid = false;\n                errors.push('Name is required.');\n                $('#community-name input').addClass('community-error-box');\n            }\n            if (!/^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*$/.test($('#community-facilitator input').val())) {\n                valid = false;\n                errors.push('Valid facilitator email is required.');\n                $('#community-facilitator input').addClass('community-error-box');\n            } else if (!checkUser($('#community-facilitator input').val())) {\n                valid = false;\n                errors.push('This email is not currently in our system.');\n                $('#community-facilitator input').addClass('community-error-box');\n            }\n            if (!valid) {\n                var error = errors.join('\\n');\n                alert(error);\n            }\n            return valid;\n        });\n    });\n</script>")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 11
        __M_writer(u'<title>Communities</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


