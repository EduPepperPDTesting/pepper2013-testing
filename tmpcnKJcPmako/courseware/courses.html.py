# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465231834.973463
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/courseware/courses.html'
_template_uri = 'courseware/courses.html'
_source_encoding = 'utf-8'
_exports = [u'title']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 2

from django.core.urlresolvers import reverse
from courseware.courses import course_image_url, get_course_about_section
from courseware.access import has_access
from certificates.models import CertificateStatuses
from xmodule.modulestore import MONGO_MODULESTORE_TYPE
from xmodule.modulestore.django import modulestore
from student.models import State,District,Transaction,Cohort,School,SubjectArea,GradeLevel,YearsInEducation
from baseinfo.models import Enum


# SOURCE LINE 12
navbar_show_extended=False 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 14
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'../static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'../main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        districts = context.get('districts', UNDEFINED)
        states_keys = context.get('states_keys', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        request = context.get('request', UNDEFINED)
        len = context.get('len', UNDEFINED)
        states = context.get('states', UNDEFINED)
        courses = context.get('courses', UNDEFINED)
        link = context.get('link', UNDEFINED)
        districts_keys = context.get('districts_keys', UNDEFINED)
        collections = context.get('collections', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 11
        __M_writer(u'\n')
        # SOURCE LINE 12
        __M_writer(u'\n')
        # SOURCE LINE 13
        __M_writer(u'\n')
        # SOURCE LINE 14
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 15
        __M_writer(u'\n\n<link rel="stylesheet" type="text/css"  href="/static/tmp-resource/css/ppd-general01.css"/>\n\n<style type="text/css" media="screen">\n    #btn-logged-user {\n        display:none;\n    }\n    .form-select {\n        font-size:14px !important;\n        width:180px;}\n    .image-link-style {\n        border-radius: 6px 6px 6px 6px;\n        -moz-border-radius: 6px 6px 6px 6px;\n        -webkit-border-radius: 6px 6px 6px 6px;\n        display: block;\n        float: left;\n        margin: 30px;\n    }\n    .image-bottom-style {\n        border-radius: 0 0 6px 6px;\n        -moz-border-radius: 0 0 6px 6px;\n        -webkit-border-radius: 0 0 6px 6px;\n        display: block;\n    }\n    .card-link {\n        display: table-cell;\n        width: 240px;\n        height: 60px;\n        vertical-align: middle;\n        padding: 0 17px;\n        font-size: 22px;\n        background: rgba(18,111,154,0.95);\n        text-decoration: none!important;\n    }\n    .card-link span {\n        color: #FFFFFF;\n    }\n    .grade_title {\n        float: left;\n        width: 920px;\n        height: 20px;\n        background-color: #fff;\n        text-align: left;\n        padding-left: 40px;\n        color: #666;\n        font-size: 16px;\n        font-weight: bold;\n        font-family: "Open Sans",Verdana,Geneva,sans-serif;\n        padding-top: 4px;\n        padding-bottom: 2px;\n    }\n    a.btnx:hover {\n        background: #638194;\n        transition-delay: 0s, 0s, 0s;\n        transition-duration: 0.25s, 0.25s, 0.25s;\n        transition-property:color, background,\u200bbox-shadow;\n        transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n        color:#fff;\n    }\n    a.btnx {\n        background-color: #556370;\n        padding-bottom: 2px !important;\n        padding-left: 10px;\n        padding-right: 10px;\n        padding-top: 2px !important;\n        text-decoration: none !important;\n        cursor: pointer;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        color:#fff;\n        transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n    }\n    a.btnx:normal {\n        background-color:#126F9A;\n        text-decoration: none;\n        cursor: pointer;\n        font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n        color:#fff;\n        transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n    }\n</style>\n<script>\n    function fsubmit(){\n        $("#course_list_form").submit();\n    }\n</script>\n<section class="find-courses" style="text-align:center;background:#F5F5F5;">\n    <!--@begin:use new image name(ppd-...); use (background:url..) replace <img src=...>-->\n    <!--@date:2013-11-02-->\n    <div style="margin:0 auto;width:960px;height:195px;background:url(/static/images/ppd-courses-banner.jpg);border-bottom:1px solid #000;">\n        <!--@end-->\n\n        <!--@begin:use html text to replace the text on the picture; add code(class="_...") to modify font style-->\n        <!--@date:2013-11-02-->\n        <div class="_banner_whatis_title_font">\n            PROFESSIONAL\n            <br/>\n            LEARNING CENTER\n            <div class="_banner_whatis_title_content_font">\n                build and enhance your community of practice\n            </div>\n        </div>\n        <!--@end-->\n    </div>\n\n    <section style="margin:auto;text-align:center;width:960px;background:#E6F5FC;">\n        <form method="" id="course_list_form" action="')
        # SOURCE LINE 121
        __M_writer(filters.decode.utf8(reverse('course_list')))
        __M_writer(u'">\n            <div style="padding:20px;color:#666;display:inline-block;">\n                <!--\n      <span style="color:#3468A1;font-family: \'Open Sans\';">COURSE (')
        # SOURCE LINE 124
        __M_writer(filters.decode.utf8(len(courses)))
        __M_writer(u')</span> &nbsp;&nbsp;&nbsp;&nbsp;\n    -->\n                <a href="/courses-list?subject_id=all&grade_id=all&author_id=all&op=find" style="color:#666">all</a> |\n                <a href="/courses-list?subject_id=all&grade_id=all&author_id=all&credit=1&op=find" style="color:#666">credit</a> |\n                <a href="/courses-list?subject_id=all&grade_id=all&author_id=all&is_new=1&op=find" style="color:#666">new</a>\n            </div>\n            <div style="display:inline-block;padding:0 1em 0 0;">\n                <select name="subject_id" class="form-select">\n                    <option value="all">All Subjects</option>\n                    <option value="AR">Assessments and Reporting</option>\n                    <option value="DC">Digital Citizenship</option>\n                    <option value="ELA">English Language Arts</option>\n                    <option value="ELL">English Language Learners</option>\n                    <option value="MA">Mathematics</option>\n                    <option value="PEP">Pepper</option>\n                    <option value="POW">Pepper\'s Online Workshops!</option>\n                    <option value="SC">Science</option>\n                    <option value="SE">Special Education</option>\n                    <option value="TECH">Technology</option>\n                    <option value="WR">Writing and Poetry</option>\n                </select>\n            </div>\n            <div style="display:inline-block;padding:0 1em 0 0;">\n                <select name="grade_id" class="form-select">\n                    <option value="all">All Grades</option>\n                    <option value="PreK-3">PreK-3</option>\n                    <option value="K-5">K-5</option>\n                    <option value="6-8">6-8</option>\n                    <option value="9-12">9-12</option>\n                    <option value="K-12">K-12</option>\n                </select>\n            </div>\n            <div style="display:inline-block;padding:0 1em 0 0;">\n                <select name="author_id" class="form-select">\n                    <option value="all">All Authors</option>\n                    <option value="A.L.L.">Accelerated Literacy Learning (A.L.L.)</option>\n                    <option value="PCG Education">PCG Education</option>\n                    <option value="Understanding Language Initiative at Stanford">Understanding Language Initiative at Stanford</option>\n                    <option value="WestEd">WestEd</option>\n                </select>\n                <!--<input type="submit" id="edit-submit" name="op" value="find">-->\n            </div>\n            <a href="javascript:;" class="btnx" onClick="fsubmit();">Find</a>\n')
        # SOURCE LINE 167
        if link:
            # SOURCE LINE 168
            __M_writer(u'                <input type="hidden" name="origin" value="courses"/>\n')
            # SOURCE LINE 169
            if request.user.is_authenticated():
                # SOURCE LINE 170
                __M_writer(u'                    <div>\n                        <table style="margin-left:236px;">\n                            <tr>\n                                <td>\n')
                # SOURCE LINE 174
                if len(states_keys) > 0:
                    # SOURCE LINE 175
                    __M_writer(u'                                        <div style="display:inline-block;padding:0 1em 0 0;margin-bottom:5px;">\n                                            <select name="state" class="form-select">\n                                                <option value="__NONE__">Select State</option>\n')
                    # SOURCE LINE 178
                    for state in states_keys:
                        # SOURCE LINE 179
                        __M_writer(u'                                                    <option value="')
                        __M_writer(filters.decode.utf8(state))
                        __M_writer(u'">')
                        __M_writer(filters.decode.utf8(state))
                        __M_writer(u'</option>\n')
                    # SOURCE LINE 181
                    __M_writer(u'                                            </select>\n                                        </div>\n')
                    # SOURCE LINE 183
                else:
                    # SOURCE LINE 184
                    __M_writer(u'                                        <div style="display:inline-block;padding:0 1em 0 0;margin-bottom:5px;">\n                                            <select name="state" class="form-select">\n                                                <option value="__NONE__">Select State</option>\n')
                    # SOURCE LINE 187
                    for item in State.objects.all().order_by('name'):
                        # SOURCE LINE 188
                        if request.GET.get('state')== "%s" % item.id:
                            # SOURCE LINE 189
                            __M_writer(u'                                                        <option value="')
                            __M_writer(filters.decode.utf8(item.name))
                            __M_writer(u'" selected>')
                            __M_writer(filters.decode.utf8(item.name))
                            __M_writer(u'</option>\n')
                            # SOURCE LINE 190
                        else:
                            # SOURCE LINE 191
                            __M_writer(u'                                                        <option value="')
                            __M_writer(filters.decode.utf8(item.name))
                            __M_writer(u'">')
                            __M_writer(filters.decode.utf8(item.name))
                            __M_writer(u'</option>\n')
                    # SOURCE LINE 194
                    __M_writer(u'                                            </select>\n                                        </div>\n')
                # SOURCE LINE 197
                __M_writer(u'                                </td>\n                                <td>\n')
                # SOURCE LINE 199
                if len(districts_keys) > 0:
                    # SOURCE LINE 200
                    __M_writer(u'                                        <div style="display:inline-block;margin-left:1px;">\n                                            <select name="district" class="form-select" id="district_list_normal_user">\n                                                <option value="__NONE__">Select District</option>\n')
                    # SOURCE LINE 203
                    for district in districts_keys:
                        # SOURCE LINE 204
                        __M_writer(u'                                                    <option value="')
                        __M_writer(filters.decode.utf8(district['id']))
                        __M_writer(u'">')
                        __M_writer(filters.decode.utf8(district['name']))
                        __M_writer(u'</option>\n')
                    # SOURCE LINE 206
                    __M_writer(u'                                            </select>\n                                        </div>\n')
                    # SOURCE LINE 208
                else:
                    # SOURCE LINE 209
                    __M_writer(u'                                        <div style="display:inline-block;margin-left:1px;">\n                                            <select name="district" class="form-select" id="district_list">\n                                                <option value="__NONE__">Select District</option>\n                                            </select>\n                                        </div>\n')
                # SOURCE LINE 215
                __M_writer(u'                                </td>\n                            </tr>\n                        </table>\n                    </div>\n')
        # SOURCE LINE 221
        __M_writer(u'            <script type="text/javascript">\n                var form=$("#course_list_form");\n                form.find("select[name=subject_id]").val("')
        # SOURCE LINE 223
        __M_writer(filters.decode.utf8(request.GET.get('subject_id','')))
        __M_writer(u'");\n                form.find("select[name=grade_id]").val("')
        # SOURCE LINE 224
        __M_writer(filters.decode.utf8(request.GET.get('grade_id','')))
        __M_writer(u'");\n                form.find("select[name=author_id]").val("')
        # SOURCE LINE 225
        __M_writer(filters.decode.utf8(request.GET.get('author_id','')))
        __M_writer(u'");\n            </script>\n        </form>\n    </section>\n\n    <section style="margin:auto;width:960px;background:#E4E4E4;">\n        <section class="courses" style="padding-top:5px!important;">\n            <div class="courses-listing">\n')
        # SOURCE LINE 233
        if link:
            # SOURCE LINE 234
            __M_writer(u'                    <div style="padding-left:25px;">\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/Mathematics.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=MA&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>Mathematics</span></a>\n                        </div>\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/English_Language_Arts.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=ELA&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>English Language Arts</span></a>\n                        </div>\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/Science.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <!--<a href="#show_course_prompt" rel="leanModal" class="card-link image-bottom-style"><span>Science</span></a>-->\n                            <a href="/courses-list?subject_id=SC&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>Science</span></a>\n                        </div>\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/Special_Education.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=SE&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>Special Education</span></a>\n                        </div>\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/Writing_and_Poetry.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=WR&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>Writing and Poetry</span></a>\n                        </div>\n\n')
            # SOURCE LINE 257
            if collections > 0:
                # SOURCE LINE 258
                __M_writer(u'\n                            <!--------Custom Content Collection-------->\n\n                            <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/collection/custom_content_collection.jpg);background-size:100% 100%;">\n                                <div style="height:100px;"></div>\n                                <a href="')
                # SOURCE LINE 263
                __M_writer(filters.decode.utf8(reverse('courses_collections')))
                __M_writer(u'" class="card-link image-bottom-style"><span>Leadership</span></a>\n                            </div>\n\n')
            # SOURCE LINE 267
            __M_writer(u'\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/English_Language_Learners.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=ELL&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>English Language Learners</span></a>\n                        </div>\n\n')
            # SOURCE LINE 273
            if request.user.is_authenticated() and len(states) > 0:
                # SOURCE LINE 274
                __M_writer(u'\n                            <!--------State Content Collection-------->\n\n                            <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/state/state_content_collection.jpg);background-size:100% 100%;">\n                                <div style="height:100px;"></div>\n                                <a href="/courses/states?state=')
                # SOURCE LINE 279
                __M_writer(filters.decode.utf8(request.user.profile.district.state.name))
                __M_writer(u'" class="card-link image-bottom-style"><span>State Content Collections</span></a>\n                            </div>\n\n')
            # SOURCE LINE 283
            if request.user.is_authenticated() and len(districts) > 0:
                # SOURCE LINE 284
                __M_writer(u'\n                            <!--------District Content Collection-------->\n\n                            <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/district/district_content_collection.jpg);background-size:100% 100%;">\n                                <div style="height:100px;"></div>\n                                <a href="/courses/districts?district=')
                # SOURCE LINE 289
                __M_writer(filters.decode.utf8(request.user.profile.district.code))
                __M_writer(u'" class="card-link image-bottom-style"><span>District Content Collections</span></a>\n                            </div>\n\n')
            # SOURCE LINE 293
            __M_writer(u'                        <!--------20160218 add-------->\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/Pepper_Online_Workshop.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=POW&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>Pepper\'s Online Workshops</span></a>\n                        </div>\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/DC-digital_citiznship_tile.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=DC&grade_id=all&author_id=all&op=find" class="card-link image-bottom-style"><span>Digital Citizenship</span></a>\n                        </div>\n                        <div class="image-link-style" style="width:240px;height:150px;background-image: url(/static/images/Just_Released.jpg);background-size:100% 100%;">\n                            <div style="height:100px;"></div>\n                            <a href="/courses-list?subject_id=all&grade_id=all&author_id=all&is_new=1&op=find" class="card-link image-bottom-style"><span>Just Released!</span></a>\n                        </div>\n                    </div>\n')
            # SOURCE LINE 307
        else:
            # SOURCE LINE 308
            if len(courses)>4:
                # SOURCE LINE 309
                if len(courses[4])>0:
                    # SOURCE LINE 310
                    __M_writer(u'                            <div class="grade_title">PreK-3 Courses</div>\n')
                # SOURCE LINE 312
                for course in courses[4]:
                    # SOURCE LINE 313
                    for c in course:
                        # SOURCE LINE 314
                        __M_writer(u'                            ')
                        runtime._include_file(context, u'../course.html', _template_uri, course=c)
                        __M_writer(u'\n')
                    # SOURCE LINE 316
                    __M_writer(u'                            <div style="float:left;width:900px;"></div>\n')
            # SOURCE LINE 319
            if len(courses)>0:
                # SOURCE LINE 320
                if len(courses[0])>0:
                    # SOURCE LINE 321
                    __M_writer(u'                            <div class="grade_title">K-5 Courses</div>\n')
                # SOURCE LINE 323
                for course in courses[0]:
                    # SOURCE LINE 324
                    for c in course:
                        # SOURCE LINE 325
                        __M_writer(u'                            ')
                        runtime._include_file(context, u'../course.html', _template_uri, course=c)
                        __M_writer(u'\n')
                    # SOURCE LINE 327
                    __M_writer(u'                            <div style="float:left;width:900px;"></div>\n')
            # SOURCE LINE 330
            if len(courses)>1:
                # SOURCE LINE 331
                if len(courses[1])>0:
                    # SOURCE LINE 332
                    __M_writer(u'                            <div class="grade_title">6-8 Courses</div>\n')
                # SOURCE LINE 334
                for course in courses[1]:
                    # SOURCE LINE 335
                    for c in course:
                        # SOURCE LINE 336
                        __M_writer(u'                            ')
                        runtime._include_file(context, u'../course.html', _template_uri, course=c)
                        __M_writer(u'\n')
                    # SOURCE LINE 338
                    __M_writer(u'                            <div style="float:left;width:900px;"></div>\n')
            # SOURCE LINE 341
            if len(courses)>2:
                # SOURCE LINE 342
                if len(courses[2])>0:
                    # SOURCE LINE 343
                    __M_writer(u'                            <div class="grade_title">9-12 Courses</div>\n')
                # SOURCE LINE 345
                for course in courses[2]:
                    # SOURCE LINE 346
                    for c in course:
                        # SOURCE LINE 347
                        __M_writer(u'                            ')
                        runtime._include_file(context, u'../course.html', _template_uri, course=c)
                        __M_writer(u'\n')
                    # SOURCE LINE 349
                    __M_writer(u'                            <div style="float:left;width:900px;"></div>\n')
            # SOURCE LINE 352
            if len(courses)>3:
                # SOURCE LINE 353
                if len(courses[3])>0:
                    # SOURCE LINE 354
                    __M_writer(u'                            <div class="grade_title">K-12 Courses</div>\n')
                # SOURCE LINE 356
                for course in courses[3]:
                    # SOURCE LINE 357
                    for c in course:
                        # SOURCE LINE 358
                        __M_writer(u'                            ')
                        runtime._include_file(context, u'../course.html', _template_uri, course=c)
                        __M_writer(u'\n')
                    # SOURCE LINE 360
                    __M_writer(u'                            <div style="float:left;width:900px;"></div>\n')
        # SOURCE LINE 364
        __M_writer(u'            </div>\n        </section>\n    </section>\n</section>\n\n<section id="show_course_prompt" class="modal" style="width:640px;">\n    <div class="inner-wrapper" style="width:629px;height:322px;background-image: url(/static/images/pepper_course_prompt.png);background-size:100% 100%;">\n        <div class="close-modal" id="course_prompt_close">\n            <div class="inner">\n                <p>&#10005;</p>\n            </div>\n        </div>\n    </div>\n</section>\n')
        # SOURCE LINE 378
        if link:
            # SOURCE LINE 379
            if len(states_keys) > 0:
                # SOURCE LINE 380
                __M_writer(u'<script type="text/javascript">\nvar form=$("#course_list_form");\nvar state="')
                # SOURCE LINE 382
                __M_writer(filters.decode.utf8(request.GET.get('state','__NONE__')))
                __M_writer(u'";\nvar district_id="')
                # SOURCE LINE 383
                __M_writer(filters.decode.utf8(request.GET.get('district','__NONE__')))
                __M_writer(u'";\nform.find("select[name=state]").val("__NONE__");\n$("#district_list_normal_user").val("__NONE__");\n\n$("#district_list_normal_user").css("width","auto");\n</script>\n')
                # SOURCE LINE 389
            else:
                # SOURCE LINE 390
                __M_writer(u'<script type="text/javascript">\nvar form=$("#course_list_form");\nvar state="')
                # SOURCE LINE 392
                __M_writer(filters.decode.utf8(request.GET.get('state','__NONE__')))
                __M_writer(u'";\nvar district_id="')
                # SOURCE LINE 393
                __M_writer(filters.decode.utf8(request.GET.get('district','__NONE__')))
                __M_writer(u'";\nform.find("select[name=state]").val("__NONE__");\n$("#district_list").val("__NONE__");\n\nif(state=="__NONE__"){\n    $("#district_list").css("width","182px");\n}\nelse{\n    $("#district_list").css("width","auto");\n}\n\n//form.find("select[name=state]").val(state);\n//dropDistrict(form,state,function(){$(this).val(district_id)});\n\nform.find("select[name=state]").change(function(a){\n    var state = $(this).val();\n    dropDistrict(form,state,district_id);\n    if(state=="__NONE__"){\n        $("#district_list").css("width","182px");\n    }\n    else{\n        $("#district_list").css("width","auto");\n    }\n});\n\nfunction dropDistrict(form,state,callback,no_code){\n  $.get(\'/courseware/drop_districts\',{state_name:state},function(r){\n      if((typeof r) == \'string\'){\n        r=$.parseJSON(r)\n      }\n      var html="";\n      var drop=form.find("select[name=district]");\n      clearOption(drop)\n      for(k in r){\n        d=r[k];\n        html+="<option value=\'" + d.code+"\'>" + d.name + "</option>";\n\n      }\n      drop.append(html)\n      if(callback instanceof Function){\n        callback.apply(drop[0]);\n      }\n  });\n}\nfunction clearOption(drop){\n  drop.find("option").filter(\n    function(){\n      return this.getAttribute("value")!="" && this.getAttribute("value")!="__NONE__"\n    }\n  ).remove()\n}\n</script>\n')
        # SOURCE LINE 447
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 15
        __M_writer(u'<title>')
        __M_writer(filters.decode.utf8(_("Courses")))
        __M_writer(u'</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


