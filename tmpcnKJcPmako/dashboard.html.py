# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465229642.855865
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/dashboard.html'
_template_uri = 'dashboard.html'
_source_encoding = 'utf-8'
_exports = [u'js_extra', u'title']


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 2

from django.core.urlresolvers import reverse
from courseware.courses import course_image_url, get_course_about_section
from courseware.access import has_access
from certificates.models import CertificateStatuses
from xmodule.modulestore import MONGO_MODULESTORE_TYPE
from xmodule.modulestore.django import modulestore
from student.models import School,Cohort,District,SubjectArea,GradeLevel,YearsInEducation
from baseinfo.models import Enum


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 19
    ns = runtime.TemplateNamespace(u'static', context._clean_inheritance_tokens(), templateuri=u'static_content.html', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'static')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        csrf_token = context.get('csrf_token', UNDEFINED)
        courses_incomplated = context.get('courses_incomplated', UNDEFINED)
        request = context.get('request', UNDEFINED)
        float = context.get('float', UNDEFINED)
        static = _mako_get_namespace(context, 'static')
        alert_text = context.get('alert_text', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        message = context.get('message', UNDEFINED)
        def title():
            return render_title(context.locals_(__M_locals))
        errored_courses = context.get('errored_courses', UNDEFINED)
        def js_extra():
            return render_js_extra(context.locals_(__M_locals))
        alert_enabled = context.get('alert_enabled', UNDEFINED)
        havent_enroll = context.get('havent_enroll', UNDEFINED)
        len = context.get('len', UNDEFINED)
        exam_registrations = context.get('exam_registrations', UNDEFINED)
        staff_access = context.get('staff_access', UNDEFINED)
        cert_statuses = context.get('cert_statuses', UNDEFINED)
        course_optouts = context.get('course_optouts', UNDEFINED)
        marketing_link = context.get('marketing_link', UNDEFINED)
        settings = context.get('settings', UNDEFINED)
        list = context.get('list', UNDEFINED)
        show_courseware_links_for = context.get('show_courseware_links_for', UNDEFINED)
        curr_user = context.get('curr_user', UNDEFINED)
        external_auth_map = context.get('external_auth_map', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 11
        __M_writer(u'\n<!--@begin:Hide Dashboard button in this page-->\n<!--@date:2013-11-02-->\n<style type="text/css" media="screen">\n  #image_uploading{display:none;}\n</style>\n<!--@end-->\n')
        # SOURCE LINE 18
        __M_writer(u'\n')
        # SOURCE LINE 19
        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 20
        __M_writer(u'\n<!--@begin:Add new page style-->\n<!--@date:2013-11-02-->\n<style type="text/css" media="screen">\n #submit:hover,#submit_email_change:hover,#photo_submit:hover {\n   background:#6e8194;\n   transition-delay: 0s, 0s, 0s;\n   transition-duration: 0.25s, 0.25s, 0.25s;\n   transition-property:color, background,\u200b box-shadow;\n   transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n   transition-duration:0.25s,\u200b 0.25s,\u200b 0.25s;\n   color:#fff;\n }\n #submit,#submit_email_change,#photo_submit {\n   border-width:0;\n   background:#556370;\n   text-decoration: none;\n   padding-bottom: 7px;\n   padding-left: 10px;\n   padding-right: 10px;\n   padding-top: 7px;\n   border-bottom-left-radius: 2px;\n   border-bottom-right-radius: 2px;\n   cursor: pointer;\n   border-top-left-radius: 2px;\n   border-top-right-radius: 2px;\n   font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n   box-shadow: #949494 0px 2px 1px 0px;\n   color:#fff;\n   transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n }\n #submit:normal,,#submit_email_change:normal,#photo_submit:normal {\n   background:#126F9A;\n   text-decoration: none;\n   border-bottom-left-radius: 2px;\n   border-bottom-right-radius: 2px;\n   cursor: pointer;\n   border-top-left-radius: 2px;\n   border-top-right-radius: 2px;\n   font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n   box-shadow: rgb(10, 74, 103) 0px 2px 1px 0px;\n   color:#fff;\n   transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n }\n</style>\n<!--@end-->\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'js_extra'):
            context['self'].js_extra(**pageargs)
        

        # SOURCE LINE 376
        __M_writer(u'\n<section class="container dashboard" id="container_dashboard">\n')
        # SOURCE LINE 378
        if message and curr_user==request.user:
            # SOURCE LINE 379
            __M_writer(u'    <section class="dashboard-banner">\n      ')
            # SOURCE LINE 380
            __M_writer(filters.decode.utf8(message))
            __M_writer(u'\n    </section>\n')
        # SOURCE LINE 383
        __M_writer(u'  <section class="profile-sidebar">\n    <header class="profile">\n      <h1 class="user-name">')
        # SOURCE LINE 385
        __M_writer(filters.decode.utf8( curr_user.username ))
        __M_writer(u'</h1>\n    </header>\n    <section class="user-info">\n      <ul>\n        <li>\n<!--@begin:Profile\uff1ausername-->\n<!--@date:2013-11-02-->\n          <span class="title">\n            <div class="icon name-icon"></div><b>')
        # SOURCE LINE 393
        __M_writer(filters.decode.utf8(_("Name")))
        __M_writer(u':</b>\n            <span id="full_name_span" class="data" style="display:inline;margin-left:0;font-weight:normal;">')
        # SOURCE LINE 394
        __M_writer(filters.html_escape(filters.decode.utf8( curr_user.first_name )))
        __M_writer(u' ')
        __M_writer(filters.html_escape(filters.decode.utf8( curr_user.last_name )))
        __M_writer(u'</span>\n            \n\t\t\t<script>\n\t\t\t\tvar full_name = document.getElementById(\'full_name_span\').textContent;\n\t\t\t\tif(full_name.length>31)\n\t\t\t\t{\n\t\t\t\t\tdocument.getElementById(\'full_name_span\').textContent = full_name.substring(0,27)+" ...";\n\t\t\t\t}\n\t\t   </script>\n\t\t\t\n')
        # SOURCE LINE 404
        if curr_user==request.user:
            # SOURCE LINE 405
            __M_writer(u'            (<a href="#apply_name_change" rel="leanModal" class="edit-name">')
            __M_writer(filters.decode.utf8(_("edit")))
            __M_writer(u'</a>)\n')
        # SOURCE LINE 407
        __M_writer(u'<!--@end-->          \n        </li>\n<!--@begin:Profile\uff1auser photo-->\n<!--@date:2013-11-02-->\n        <li>\n          <span class="title"><div class="icon email-icon" style="background-image:url(/static/images/portal-icons/photo.png) !important;">\n            </div><b>')
        # SOURCE LINE 413
        __M_writer(filters.decode.utf8(_("User Photo")))
        __M_writer(u'</b>\n')
        # SOURCE LINE 414
        if curr_user==request.user:
            # SOURCE LINE 415
            __M_writer(u'            (<a href="#change_photo" rel="leanModal" class="edit-photo">')
            __M_writer(filters.decode.utf8(_("edit")))
            __M_writer(u'</a>)\n')
        # SOURCE LINE 417
        __M_writer(u'          </span> \n          <div style="text-align:center;margin-top:5px;">\n            <img src="')
        # SOURCE LINE 419
        __M_writer(filters.decode.utf8(reverse('user_photo',args=[curr_user.id])))
        __M_writer(u'" style="" alt="photo" />\n          </div>\n        </li>\n<!--@end-->\n        <!-- <li> -->\n        <!--   <span class="title"><div class="icon email-icon"></div>')
        # SOURCE LINE 424
        __M_writer(filters.decode.utf8(_("Email")))
        __M_writer(u' -->\n        <!--     %if curr_user==request.user: -->\n        <!--     % if external_auth_map is None or \'shib\' not in external_auth_map.external_domain: -->\n        <!--     <\\!-- (<a href="#change_email" rel="leanModal" class="edit-email">')
        # SOURCE LINE 427
        __M_writer(filters.decode.utf8(_("edit")))
        __M_writer(u'</a>) -\\-> -->\n        <!--     % endif -->\n        <!--     %endif -->\n        <!--   </span> <span class="data">')
        # SOURCE LINE 430
        __M_writer(filters.html_escape(filters.decode.utf8( curr_user.email )))
        __M_writer(u'</span> -->\n        <!-- </li> -->\n')
        # SOURCE LINE 432
        if curr_user==request.user and not request.session.get('idp'):
            # SOURCE LINE 433
            if external_auth_map is None or 'shib' not in external_auth_map.external_domain:
                # SOURCE LINE 434
                __M_writer(u'        <li>\n          <span class="title"><a href="#password_reset_complete" rel="leanModal" id="pwd_reset_button">')
                # SOURCE LINE 435
                __M_writer(filters.decode.utf8(_("Reset Password")))
                __M_writer(u'</a></span>\n          <form id="password_reset_form" method="post" data-remote="true" action="')
                # SOURCE LINE 436
                __M_writer(filters.decode.utf8(reverse('password_reset')))
                __M_writer(u'">\n            <input id="id_email" type="hidden" name="email" maxlength="75" value="')
                # SOURCE LINE 437
                __M_writer(filters.decode.utf8(curr_user.email))
                __M_writer(u'" />\n            <!-- <input type="submit" id="pwd_reset_button" value="')
                # SOURCE LINE 438
                __M_writer(filters.decode.utf8(_('Reset Password')))
                __M_writer(u'" /> -->\n          </form>\n        </li>\n')
        # SOURCE LINE 443
        __M_writer(u'        \n<!-------------------------------- My Pepper Stats------------------------------------->\n    <li>\n      <span class="title">\n         <div style="font-family: \'Open Sans\';font-size:12px;">\n            <div class="" style="padding:0 0 5px 0;"> \n              <b style="font-size:14px;color:#000">My Pepper Stats:</b>\n            </div>\n            <div style="line-height:30px;"><b>All Course Time:</b>\n           <span id="all_course_time" style="display:inline;"></span>\n           </div>\n           <div style="line-height:30px;"><b>Collaboration Time:</b>\n           <span id="collaboration_time" style="display:inline;"></span>\n           </div>\n           <!-- hide totle adjustment time -->\n           <!--\n           <div style="line-height:30px;"><b>Adjusted Total Time:</b>\n            <span id="totle_adjustment_time" style="display:inline;"></span>\n           </div>\n           -->\n           <div style="line-height:30px;"><b>Total Time:</b>\n            <span id="total_time_in_pepper" style="display:inline;"></span>\n           </div>\n         </div>\n      </span>\n    </li>\n<!-------------------------------------------------------------------------------------->\n\t\t<li>\n          <span class="title">\n\t\t  <div style="font-family: \'Open Sans\';font-size:12px;">\n            <div class="" style="padding:0 0 5px 0;"> \n              <b style="font-size:14px;color:#000">My Profile:</b>\n            </div>\n\t\t\t<div style="line-height:30px;"><b>State:</b>\n')
        # SOURCE LINE 477
        if curr_user.profile.district_id:
            # SOURCE LINE 478
            __M_writer(u'\t\t\t  ')
            __M_writer(filters.decode.utf8(curr_user.profile.district.state.name))
            __M_writer(u'\n')
        # SOURCE LINE 480
        __M_writer(u'\t\t\t</div>\n\t\t\t<div style="line-height:30px;"><b>District:</b>\n')
        # SOURCE LINE 482
        if curr_user.profile.district_id:
            # SOURCE LINE 483
            __M_writer(u'\t\t\t  <br>')
            __M_writer(filters.decode.utf8(curr_user.profile.district.name))
            __M_writer(u'\n')
        # SOURCE LINE 485
        __M_writer(u'\t\t\t</div>\n\t\t\t<div style="line-height:30px;"><b>School:</b>\n')
        # SOURCE LINE 487
        if curr_user.profile.school_id:
            # SOURCE LINE 488
            __M_writer(u'\t\t\t  <br>')
            __M_writer(filters.decode.utf8(curr_user.profile.school.name))
            __M_writer(u'\n')
        # SOURCE LINE 490
        if curr_user==request.user:
            # SOURCE LINE 491
            __M_writer(u'\t\t\t  (<a href="#change_school" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 493
        __M_writer(u'\t\t\t</div>\n\t\t\t<div style="line-height:30px;"><b>Grade Level:</b>\n              ')
        # SOURCE LINE 495
        gn=list() 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['gn'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n')
        # SOURCE LINE 496
        if curr_user.profile.grade_level_id:
            # SOURCE LINE 497
            __M_writer(u'              <br>\n')
            # SOURCE LINE 498
            for i,c in enumerate(curr_user.profile.grade_level_id.split(',')):
                # SOURCE LINE 499
                if len(c)>0:
                    # SOURCE LINE 500
                    __M_writer(u'\t\t\t  ')
                    gn.append(GradeLevel.objects.get(id=c).name) 
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
                    __M_writer(u'\n')
        # SOURCE LINE 504
        __M_writer(u'              ')
        __M_writer(filters.decode.utf8(", ".join(gn)))
        __M_writer(u'\n')
        # SOURCE LINE 505
        if curr_user==request.user:
            # SOURCE LINE 506
            __M_writer(u'\t\t\t  (<a href="#change_grade_level" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 508
        __M_writer(u'\t\t\t</div>\n\t\t\t<div style="line-height:30px;"><b>Major Subject Area:</b>\n')
        # SOURCE LINE 510
        if curr_user.profile.major_subject_area_id:
            # SOURCE LINE 511
            __M_writer(u'              <br>\n\t\t\t  ')
            # SOURCE LINE 512
            __M_writer(filters.decode.utf8(SubjectArea.objects.get(id=curr_user.profile.major_subject_area_id).name))
            __M_writer(u'\n')
        # SOURCE LINE 514
        if curr_user==request.user:
            # SOURCE LINE 515
            __M_writer(u'\t\t\t  (<a href="#change_major_subject_area" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 517
        __M_writer(u'\t\t\t</div>\n\t\t\t<div style="line-height:30px;"><b>Number of Years in Education:</b>\n')
        # SOURCE LINE 519
        if curr_user.profile.years_in_education_id:
            # SOURCE LINE 520
            __M_writer(u'\t\t\t  ')
            __M_writer(filters.decode.utf8(YearsInEducation.objects.get(id=curr_user.profile.years_in_education_id).name))
            __M_writer(u'\n')
        # SOURCE LINE 522
        if curr_user==request.user:
            # SOURCE LINE 523
            __M_writer(u'              (<a href="#change_years_in_education" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 525
        __M_writer(u'\t\t\t</div>\n\n            <div style="padding:15px 0 5px 0;"> \n              <b style="font-size:14px;color:#000;">My Learners\' Profile:</b>\n            </div>\n            \n\t\t\t<div style="line-height:30px;">\n              <b>Free/Reduced Lunch:</b>\n')
        # SOURCE LINE 533
        if curr_user.profile.percent_lunch:
            # SOURCE LINE 534
            __M_writer(u'\t\t\t  ')
            __M_writer(filters.decode.utf8(Enum.objects.get(name='percent_lunch',value=curr_user.profile.percent_lunch).content))
            __M_writer(u'\n')
        # SOURCE LINE 536
        if curr_user==request.user:
            # SOURCE LINE 537
            __M_writer(u'              (<a href="#change_percent_lunch" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 539
        __M_writer(u'\t\t\t</div>\n            <div style="line-height:30px;">\n              <b>IEPs:</b>\n')
        # SOURCE LINE 542
        if curr_user.profile.percent_iep:
            # SOURCE LINE 543
            __M_writer(u'\t\t\t  ')
            __M_writer(filters.decode.utf8(Enum.objects.get(name='percent_iep',value=curr_user.profile.percent_iep).content))
            __M_writer(u'\n')
        # SOURCE LINE 545
        if curr_user==request.user:
            # SOURCE LINE 546
            __M_writer(u'              (<a href="#change_percent_iep" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 548
        __M_writer(u'\t\t\t</div>\n            <div style="line-height:30px;">\n              <b>English Learners:</b>\n')
        # SOURCE LINE 551
        if curr_user.profile.percent_eng_learner:
            # SOURCE LINE 552
            __M_writer(u'\t\t\t  ')
            __M_writer(filters.decode.utf8(Enum.objects.get(name='percent_eng_learner',value=curr_user.profile.percent_eng_learner).content))
            __M_writer(u'\n')
        # SOURCE LINE 554
        if curr_user==request.user:
            # SOURCE LINE 555
            __M_writer(u'              (<a href="#change_percent_eng_learner" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 557
        __M_writer(u'\t\t\t</div>\n            </span>\n\t\t</li>\n        <li>\n          <span class="title">\n          <div style="font-family: \'Open Sans\';font-size:12px;">\n            <b style="color:#000;font-size:14px;">Bio:</b>\n')
        # SOURCE LINE 564
        if curr_user==request.user:
            # SOURCE LINE 565
            __M_writer(u'            (<a href="#change_bio" rel="leanModal">edit</a>)\n')
        # SOURCE LINE 567
        __M_writer(u'<pre style="padding:0;margin-top:10px;">\n')
        # SOURCE LINE 568
        if curr_user.profile.bio:
            # SOURCE LINE 569
            __M_writer(filters.decode.utf8(curr_user.profile.bio))
            __M_writer(u'\n')
            # SOURCE LINE 570
        else:
            # SOURCE LINE 571
            __M_writer(u'Add info that you would like to share about yourself here:  \n')
        # SOURCE LINE 573
        __M_writer(u'</pre>\n          </div>\n          </span>\n        </li>\n<!--@end-->        \n      </ul>\n<!--@begin: Remove some profile info-->\n<!--@date:2013-11-02-->  \n         <!-- <div style="width:180px">  <span>City:Aptos</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:180px"><span>State:Ca</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:180px"><span>Zip:96003</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:180px"><span>Address:(none)</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:180px"><span>Phone:(none)</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div><p/></div> -->\n         <!-- <div style="width:180px"><span>District:Really big</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:220px"><span>School:Ver Little School</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:240px"><span>Role tale in school:Teacher</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n         <!-- <div style="width:230px"><span>Focus Grade(s)4,5,and 6</span>  <span style="float:right;padding-right:0px;">(<a href="" class="">edit</a>)</span></div> -->\n       </div>\n<!--@end-->      \n    </section>\n  </section>\n<!--@begin:The styles used only in Dashboard-->\n<!--@date:2013-11-02-->\n<style type="text/css" media="screen">\n  a.btnx:hover {\n  background: linear-gradient(#1e8bbe, #0e72a1); \n  transition-delay: 0s, 0s, 0s;\n  transition-duration: 0.25s, 0.25s, 0.25s;\n  transition-property:color, background,\u200b box-shadow;\n  transition-timing-function:\n  cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  transition-duration:0.25s,\u200b 0.25s,\u200b 0.25s;\n  text-decoration:none;\n  }\n  a.btnx {\n  background-clip: padding-box;\n  border:1ps solid rgb(13, 114, 162);\n  background-color:rgb(29, 157, 217);\n  background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #1d9dd9), color-stop(100%, #0e7cb0));\n  background-image: -webkit-linear-gradient(#1d9dd9, #0e7cb0);\n  background-image: linear-gradient(#1d9dd9, #0e7cb0);\n  border: 1px solid #0d72a2;\n  box-shadow: inset 0 1px 0 0 #61b8e1;\n  text-decoration: none;\n  padding:6px 32px 7px 32px;\n  line-height:26px;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n  border-top-left-radius: 3px;\n  border-top-right-radius: 3px;\n  cursor: pointer;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  color:#fff;\n  transition-timing-function: cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n  a.btnx:normal {\n  background-color:#126F9A;\n  text-decoration: none;\n  border-bottom-left-radius: 2px;\n  border-bottom-right-radius: 2px;\n  cursor: pointer;\n  border-top-left-radius: 2px;\n  border-top-right-radius: 2px;\n  font-family: \'Open Sans\',Verdana,Geneva,sans-serif;\n  color:#fff;\n  transition-timing-function:cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1), cubic-bezier(0.42, 0, 0.58, 1);\n  }\n</style>\n<!--@end-->\n<!--@begin:Add lastnew in Dashboard-->\n<!--@date:2013-11-02-->\n<section class="my-courses">\n  <header style="width:886px;height:246px;margin:auto;position:relative;border-bottom:none;margin-bottom:30px;">\n    <div style="position:absolute;background:url(')
        # SOURCE LINE 647
        __M_writer(filters.decode.utf8(static.url('images/p15.png')))
        __M_writer(u');width:886px;height:246px;">\n      <a href="http://www.pepperpcg.blogspot.com" target="_blank" style="margin:170px 0 0 227px;position:absolute;" class="btnx dashboard-btn1">')
        # SOURCE LINE 648
        __M_writer(filters.decode.utf8(_('Latest News')))
        __M_writer(u'</a>\n    </div>\n  </header>\n</section>\n<!--@end-->\n\n<!--@begin:Add alert in Dashboard page-->\n<!--@date:2016-04-12-->\n')
        # SOURCE LINE 656
        if alert_enabled == "enabled" and alert_text != "":
            # SOURCE LINE 657
            __M_writer(u'<section class="my-courses">\n<div id="con_alert" style="width:879px;margin:auto;position:relative;margin-bottom:30px;border:2px solid #900;">\n  <div style="width:829px;background-color:#FFC651;font-weight:bold;color:#900;padding:25px;line-height:20px;">\n      ')
            # SOURCE LINE 660
            __M_writer(filters.decode.utf8(alert_text))
            __M_writer(u'\n  </div>\n</div>\n</section>\n')
        # SOURCE LINE 665
        __M_writer(u'<!--@end-->\n\n')
        # SOURCE LINE 667
        if curr_user==request.user:
            # SOURCE LINE 668
            if havent_enroll > 0:
                # SOURCE LINE 669
                __M_writer(u'<section class="my-courses" style="padding:20px 0 20px 0;text-align:right;" >\n  <a href="/more_courses_available" class="btnx dashboard-btn1">\n    ')
                # SOURCE LINE 671
                __M_writer(filters.decode.utf8(havent_enroll))
                __M_writer(u' More Course(s) Available For You\n  </a>\n</section>\n')
        # SOURCE LINE 676
        __M_writer(u'\n<section class="my-courses" style="" >\n    <header>\n      <h2>')
        # SOURCE LINE 679
        __M_writer(filters.decode.utf8(_("Current Courses")))
        __M_writer(u'</h2>\n    </header>\n')
        # SOURCE LINE 681
        if len(courses_incomplated) > 0:
            # SOURCE LINE 682
            __M_writer(u'<!--@begin:Change the disply of the courses list in Dashboard-->\n<!--@date:2013-11-02-->    \n')
            # SOURCE LINE 684
            for i,course in enumerate(courses_incomplated):
                # SOURCE LINE 685
                __M_writer(u'    ')

                border_overide='';
                if i==len(courses_incomplated)-1:
                  border_overide="border-bottom:3px solid #0098C9"
                
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['border_overide'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 689
                __M_writer(u'\n        <article class="my-course" style="')
                # SOURCE LINE 690
                __M_writer(filters.decode.utf8(border_overide))
                __M_writer(u'" >\n          ')
                # SOURCE LINE 691

                course_target = reverse('courseware', args=[course.id])
                          
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['course_target'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 693
                __M_writer(u'\n')
                # SOURCE LINE 694
                if course.id in show_courseware_links_for:
                    # SOURCE LINE 695
                    if curr_user==request.user:
                        # SOURCE LINE 696
                        __M_writer(u'            <a href="')
                        __M_writer(filters.decode.utf8(course_target))
                        __M_writer(u'" class="cover">\n')
                        # SOURCE LINE 697
                    else:
                        # SOURCE LINE 698
                        __M_writer(u'            <a href="" class="cover" style="cursor:default;" onclick="return false;">\n')
                    # SOURCE LINE 700
                    __M_writer(u'              <img src="')
                    __M_writer(filters.decode.utf8(course_image_url(course)))
                    __M_writer(u'" style="width:200px;height:104px;" alt="')
                    __M_writer(filters.html_escape(filters.decode.utf8(_('{course_number} {course_name} Cover Image').format(course_number=course.number, course_name=course.display_name_with_default) )))
                    __M_writer(u'" />\n            </a>\n<!--@end-->          \n')
                    # SOURCE LINE 703
                else:
                    # SOURCE LINE 704
                    __M_writer(u'            <div class="cover">\n              <img src="')
                    # SOURCE LINE 705
                    __M_writer(filters.decode.utf8(course_image_url(course)))
                    __M_writer(u'" alt="')
                    __M_writer(filters.html_escape(filters.decode.utf8(_('{course_number} {course_name} Cover Image').format(course_number=course.number, course_name=course.display_name_with_default) )))
                    __M_writer(u'" />\n            </div>\n')
                # SOURCE LINE 708
                __M_writer(u'          <section class="info">\n            <hgroup>\n<!--@begin:Change the display of current courses in Dashboard-->\n<!--@date:2013-11-02-->                 \n              <p class="date-block">\n                ')
                # SOURCE LINE 713
                __M_writer(filters.decode.utf8(_("Enrollment date - {end_date:%B %d,%Y}").format(end_date=course.student_enrollment_date)))
                __M_writer(u'\n')
                # SOURCE LINE 714
                if curr_user==request.user:
                    # SOURCE LINE 715
                    __M_writer(u'                  <a href="#unenroll-modal" class="unenroll" style="font-size:13px;margin:2px 0px 0px 10px" rel="leanModal" data-course-id="')
                    __M_writer(filters.decode.utf8(course.id))
                    __M_writer(u'" data-course-number="')
                    __M_writer(filters.decode.utf8(course.number))
                    __M_writer(u'">')
                    __M_writer(filters.decode.utf8(_('Unregister')))
                    __M_writer(u'</a>\n')
                # SOURCE LINE 717
                __M_writer(u'              </p>\n')
                # SOURCE LINE 718
                if False:
                    # SOURCE LINE 719
                    __M_writer(u'              <p class="date-block">\n')
                    # SOURCE LINE 720
                    if course.has_ended():
                        # SOURCE LINE 721
                        __M_writer(u'              ')
                        __M_writer(filters.decode.utf8(_("Course Completed - {end_date}").format(end_date=course.end_date_text)))
                        __M_writer(u'\n')
                        # SOURCE LINE 722
                    elif course.has_started():
                        # SOURCE LINE 723
                        __M_writer(u'              ')
                        __M_writer(filters.decode.utf8(_("Course Started - {start_date}").format(start_date=course.start_date_text)))
                        __M_writer(u'\n')
                        # SOURCE LINE 724
                    else:   # hasn't started yet
                        # SOURCE LINE 725
                        __M_writer(u'              ')
                        __M_writer(filters.decode.utf8(_("Course Starts - {start_date}").format(start_date=course.start_date_text)))
                        __M_writer(u'\n')
                    # SOURCE LINE 727
                    __M_writer(u'              </p>\n')
                # SOURCE LINE 729
                __M_writer(u'<!--@end-->      \n              <h2 class="university">')
                # SOURCE LINE 730
                __M_writer(filters.decode.utf8(get_course_about_section(course, 'university')))
                __M_writer(u'</h2>\n              <h3>\n')
                # SOURCE LINE 732
                if course.id in show_courseware_links_for:
                    # SOURCE LINE 733
                    if curr_user==request.user:
                        # SOURCE LINE 734
                        __M_writer(u'                  <a href="')
                        __M_writer(filters.decode.utf8(course_target))
                        __M_writer(u'">')
                        __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                        __M_writer(u' ')
                        __M_writer(filters.decode.utf8(course.display_name_with_default))
                        __M_writer(u'</a>\n')
                        # SOURCE LINE 735
                    else:
                        # SOURCE LINE 736
                        __M_writer(u'                  <a href="" style="cursor:default;" onclick="return false;" course_number="')
                        __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                        __M_writer(u'">')
                        __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                        __M_writer(u' ')
                        __M_writer(filters.decode.utf8(course.display_name_with_default))
                        __M_writer(u'</a>\n')
                    # SOURCE LINE 738
                else:
                    # SOURCE LINE 739
                    __M_writer(u'                  <span>')
                    __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                    __M_writer(u' ')
                    __M_writer(filters.decode.utf8(course.display_name_with_default))
                    __M_writer(u'</span>\n')
                # SOURCE LINE 741
                __M_writer(u'              </h3>\n            </hgroup>\n            ')
                # SOURCE LINE 743

                testcenter_exam_info = course.current_test_center_exam
                registration = exam_registrations.get(course.id)
                testcenter_register_target = reverse('begin_exam_registration', args=[course.id])
                            
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['testcenter_register_target','testcenter_exam_info','registration'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 747
                __M_writer(u'\n')
                # SOURCE LINE 748
                if testcenter_exam_info is not None:
                    # SOURCE LINE 749
                    if registration is None and testcenter_exam_info.is_registering():
                        # SOURCE LINE 750
                        __M_writer(u'                <div class="message message-status is-shown exam-register">\n                  <a href="')
                        # SOURCE LINE 751
                        __M_writer(filters.decode.utf8(testcenter_register_target))
                        __M_writer(u'" class="button exam-button" id="exam_register_button">')
                        __M_writer(filters.decode.utf8(_("Register for Pearson exam")))
                        __M_writer(u'</a>\n                  <p class="message-copy">')
                        # SOURCE LINE 752
                        __M_writer(filters.decode.utf8(_("Registration for the Pearson exam is now open and will close on {end_date}").format(end_date="<strong>{}</strong>".format(testcenter_exam_info.registration_end_date_text))))
                        __M_writer(u'</p>\n                </div>\n')
                    # SOURCE LINE 755
                    __M_writer(u'                <!-- display a registration for a current exam, even if the registration period is over -->\n')
                    # SOURCE LINE 756
                    if registration is not None:
                        # SOURCE LINE 757
                        if registration.is_accepted:
                            # SOURCE LINE 758
                            __M_writer(u'                <div class="message message-status is-shown exam-schedule">\n                   <a href="')
                            # SOURCE LINE 759
                            __M_writer(filters.decode.utf8(registration.registration_signup_url))
                            __M_writer(u'" class="button exam-button">')
                            __M_writer(filters.decode.utf8(_("Schedule Pearson exam")))
                            __M_writer(u'</a>\n                   <p class="exam-registration-number">')
                            # SOURCE LINE 760
                            __M_writer(filters.decode.utf8(_("{link_start}Registration{link_end} number: {number}").format(
                      link_start='<a href="{url}" id="exam_register_link">'.format(url=testcenter_register_target),
                      link_end='</a>',
                      number=registration.client_candidate_id,
                    )))
                            # SOURCE LINE 764
                            __M_writer(u'</p>\n                   <p class="message-copy">')
                            # SOURCE LINE 765
                            __M_writer(filters.decode.utf8(_("Write this down! You'll need it to schedule your exam.")))
                            __M_writer(u'</p>\n                </div>\n')
                        # SOURCE LINE 768
                        if  registration.is_rejected:
                            # SOURCE LINE 769
                            __M_writer(u'                <div class="message message-status is-shown exam-schedule">\n                  <p class="message-copy">\n                    <strong>')
                            # SOURCE LINE 771
                            __M_writer(filters.decode.utf8(_("Your registration for the Pearson exam has been rejected. Please {link_start}see your registration status details{link_end}.").format(
                      link_start='<a href="{url}" id="exam_register_link">'.format(url=testcenter_register_target),
                      link_end='</a>')))
                            # SOURCE LINE 773
                            __M_writer(u'</strong>\n                    ')
                            # SOURCE LINE 774
                            __M_writer(filters.decode.utf8(_("Otherwise {link_start}contact edX at {email}{link_end} for further help.").format(
                      link_start='<a class="contact-link" href="mailto:{email}?subject=Pearson VUE Exam - {about} {number}">'.format(email="exam-help@edx.org", about=get_course_about_section(course, 'university'), number=course.display_number_with_default),
                      link_end='</a>',
                      email="exam-help@edx.org",
                     )))
                            # SOURCE LINE 778
                            __M_writer(u'\n                </div>\n')
                        # SOURCE LINE 781
                        if not registration.is_accepted and not registration.is_rejected:
                            # SOURCE LINE 782
                            __M_writer(u'\t            <div class="message message-status is-shown">\n                  <p class="message-copy"><strong>')
                            # SOURCE LINE 783
                            __M_writer(filters.decode.utf8(_("Your {link_start}registration for the Pearson exam{link_end} is pending.").format(link_start='<a href="{url}" id="exam_register_link">'.format(url=testcenter_register_target), link_end='</a>')))
                            __M_writer(u'</strong>\n                  ')
                            # SOURCE LINE 784
                            __M_writer(filters.decode.utf8(_("Within a few days, you should see a confirmation number here, which can be used to schedule your exam.")))
                            __M_writer(u'\n                  </p>\n                </div>\n')
                # SOURCE LINE 790
                __M_writer(u'            ')

                cert_status = cert_statuses.get(course.id)
                
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['cert_status'] if __M_key in __M_locals_builtin_stored]))
                # SOURCE LINE 792
                __M_writer(u'\n')
                # SOURCE LINE 793
                if course.has_ended() and cert_status:
                    # SOURCE LINE 794
                    __M_writer(u'                ')

                    if cert_status['status'] == 'generating':
                        status_css_class = 'course-status-certrendering'
                    elif cert_status['status'] == 'ready':
                        status_css_class = 'course-status-certavailable'
                    elif cert_status['status'] == 'notpassing':
                        status_css_class = 'course-status-certnotavailable'
                    else:
                        status_css_class = 'course-status-processing'
                    
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['status_css_class'] if __M_key in __M_locals_builtin_stored]))
                    # SOURCE LINE 803
                    __M_writer(u'\n                <div class="message message-status ')
                    # SOURCE LINE 804
                    __M_writer(filters.decode.utf8(status_css_class))
                    __M_writer(u' is-shown">\n')
                    # SOURCE LINE 805
                    if cert_status['status'] == 'processing':
                        # SOURCE LINE 806
                        __M_writer(u'                      <p class="message-copy">')
                        __M_writer(filters.decode.utf8(_("Final course details are being wrapped up at this time. Your final standing will be available shortly.")))
                        __M_writer(u'</p>\n')
                        # SOURCE LINE 807
                    elif cert_status['status'] in ('generating', 'ready', 'notpassing', 'restricted'):
                        # SOURCE LINE 808
                        __M_writer(u'                      <p class="message-copy">')
                        __M_writer(filters.decode.utf8(_("Your final grade:")))
                        __M_writer(u'\n                      <span class="grade-value">')
                        # SOURCE LINE 809
                        __M_writer(filters.decode.utf8("{0:.0f}%".format(float(cert_status['grade'])*100)))
                        __M_writer(u'</span>.\n')
                        # SOURCE LINE 810
                        if cert_status['status'] == 'notpassing':
                            # SOURCE LINE 811
                            __M_writer(u'                         ')
                            __M_writer(filters.decode.utf8(_("Grade required for a certificate:")))
                            __M_writer(u' <span class="grade-value">\n                           ')
                            # SOURCE LINE 812
                            __M_writer(filters.decode.utf8("{0:.0f}%".format(float(course.lowest_passing_grade)*100)))
                            __M_writer(u'</span>.\n')
                            # SOURCE LINE 813
                        elif cert_status['status'] == 'restricted':
                            # SOURCE LINE 814
                            __M_writer(u'                          <p class="message-copy">\n                          ')
                            # SOURCE LINE 815
                            __M_writer(filters.decode.utf8(_("Your certificate is being held pending confirmation that the issuance of your certificate is in compliance with strict U.S. embargoes on Iran, Cuba, Syria and Sudan. If you think our system has mistakenly identified you as being connected with one of those countries, please let us know by contacting {email}.").format(email='<a class="contact-link" href="mailto:{email}">{email}</a>.'.format(email=settings.CONTACT_EMAIL))))
                            __M_writer(u'\n                          </p>\n')
                        # SOURCE LINE 818
                        __M_writer(u'                      </p>\n')
                    # SOURCE LINE 820
                    if cert_status['show_disabled_download_button'] or cert_status['show_download_url'] or cert_status['show_survey_button']:
                        # SOURCE LINE 821
                        __M_writer(u'                  <ul class="actions">\n')
                        # SOURCE LINE 822
                        if cert_status['show_disabled_download_button']:
                            # SOURCE LINE 823
                            __M_writer(u'                      <li class="action"><span class="disabled">\n                          ')
                            # SOURCE LINE 824
                            __M_writer(filters.decode.utf8(_("Your Certificate is Generating")))
                            __M_writer(u'</span></li>\n')
                            # SOURCE LINE 825
                        elif cert_status['show_download_url']:
                            # SOURCE LINE 826
                            __M_writer(u'                      <li class="action">\n                      <a class="btn" href="')
                            # SOURCE LINE 827
                            __M_writer(filters.decode.utf8(cert_status['download_url']))
                            __M_writer(u'"\n                         title="')
                            # SOURCE LINE 828
                            __M_writer(filters.decode.utf8(_('This link will open/download a PDF document')))
                            __M_writer(u'">\n                         Download Your PDF Certificate</a></li>\n')
                        # SOURCE LINE 831
                        if cert_status['show_survey_button']:
                            # SOURCE LINE 832
                            __M_writer(u'                      <li class="action"><a class="cta" href="')
                            __M_writer(filters.decode.utf8(cert_status['survey_url']))
                            __M_writer(u'">\n                             ')
                            # SOURCE LINE 833
                            __M_writer(filters.decode.utf8(_('Complete our course feedback survey')))
                            __M_writer(u'</a></li>\n')
                        # SOURCE LINE 835
                        __M_writer(u'                  </ul>\n')
                    # SOURCE LINE 837
                    __M_writer(u'                </div>\n')
                # SOURCE LINE 839
                __M_writer(u'            <link rel="stylesheet" href="/static/tmp-resource/css/main.css" type="text/css" media="screen" />\n')
                # SOURCE LINE 840
                if course.id in show_courseware_links_for:
                    # SOURCE LINE 841
                    if curr_user==request.user:              
                        # SOURCE LINE 842
                        __M_writer(u'\t\t\t<a href="')
                        __M_writer(filters.decode.utf8(reverse('portfolio_about_me',args=[course.id])))
                        __M_writer(u'" class="enter-course dashboard-btn1">')
                        __M_writer(filters.decode.utf8(_('View Portfolio')))
                        __M_writer(u'</a>\n')
                        # SOURCE LINE 843
                    else:
                        # SOURCE LINE 844
                        __M_writer(u'            <a href="javascript:void(0)" class="enter-course dashboard-btn1 portfolio-btn" link="')
                        __M_writer(filters.decode.utf8(reverse('portfolio_about_me',args=[course.id,curr_user.id])))
                        __M_writer(u'">')
                        __M_writer(filters.decode.utf8(_('View Portfolio')))
                        __M_writer(u'</a>\n')
                    # SOURCE LINE 846
                    if curr_user==request.user:      
                        # SOURCE LINE 847
                        __M_writer(u'            <a href="')
                        __M_writer(filters.decode.utf8(course_target))
                        __M_writer(u'" class="enter-course dashboard-btn2" style="margin-left:10px;">')
                        __M_writer(filters.decode.utf8(_('View Course')))
                        __M_writer(u'</a>\n')
                # SOURCE LINE 850
                if curr_user==request.user:
                    # SOURCE LINE 851
                    if settings.MITX_FEATURES['ENABLE_INSTRUCTOR_EMAIL'] and modulestore().get_modulestore_type(course.id) == MONGO_MODULESTORE_TYPE:
                        # SOURCE LINE 852
                        __M_writer(u'\t      <!-- Only show the Email Settings link/modal if this course has bulk email feature enabled -->\n               <!-- hide email settings -->\n              <!--\n              <a href="#email-settings-modal" class="email-settings" rel="leanModal" data-course-id="')
                        # SOURCE LINE 855
                        __M_writer(filters.decode.utf8(course.id))
                        __M_writer(u'" data-course-number="')
                        __M_writer(filters.decode.utf8(course.number))
                        __M_writer(u'" data-optout="')
                        __M_writer(filters.decode.utf8(course.id in course_optouts))
                        __M_writer(u'">')
                        __M_writer(filters.decode.utf8(_('Email Settings')))
                        __M_writer(u'</a>\n              -->\n')
                        # SOURCE LINE 857
                        if course.hide_timer == False:
                            # SOURCE LINE 858
                            if course.show_external_timer == False:
                                # SOURCE LINE 859
                                __M_writer(u'                  <div class="course-time" time_type="course" course_id="')
                                __M_writer(filters.decode.utf8(course.id))
                                __M_writer(u'">Course Time: <span></span></div>\n')
                                # SOURCE LINE 860
                            else:
                                # SOURCE LINE 861
                                __M_writer(u'                  <div class="course-time" time_type="external" course_id="')
                                __M_writer(filters.decode.utf8(course.id))
                                __M_writer(u'">External Time: <span></span></div>\n')
                # SOURCE LINE 866
                __M_writer(u'          </section>\n        </article>\n')
            # SOURCE LINE 869
        else:
            # SOURCE LINE 870
            __M_writer(u'      <section class="empty-dashboard-message">\n')
            # SOURCE LINE 871
            if curr_user==request.user:
                # SOURCE LINE 872
                __M_writer(u'        <p>')
                __M_writer(filters.decode.utf8(_("Looks like you haven't registered for any courses yet.")))
                __M_writer(u'</p>\n        <a href="')
                # SOURCE LINE 873
                __M_writer(filters.decode.utf8(marketing_link('COURSES')))
                __M_writer(u'">\n            ')
                # SOURCE LINE 874
                __M_writer(filters.decode.utf8(_("Find courses now!")))
                __M_writer(u'\n        </a>\n')
            # SOURCE LINE 877
            __M_writer(u'      </section>\n')
        # SOURCE LINE 879
        if staff_access and len(errored_courses) > 0:
            # SOURCE LINE 880
            __M_writer(u'      <div id="course-errors">\n        <h2>')
            # SOURCE LINE 881
            __M_writer(filters.decode.utf8(_("Course-loading errors")))
            __M_writer(u'</h2>\n')
            # SOURCE LINE 882
            for course_dir, errors in errored_courses.items():
                # SOURCE LINE 883
                __M_writer(u'         <h3>')
                __M_writer(filters.html_escape(filters.decode.utf8(course_dir )))
                __M_writer(u'</h3>\n             <ul>\n')
                # SOURCE LINE 885
                for (msg, err) in errors:
                    # SOURCE LINE 886
                    __M_writer(u'               <li>')
                    __M_writer(filters.decode.utf8(msg))
                    __M_writer(u'\n                 <ul><li><pre>')
                    # SOURCE LINE 887
                    __M_writer(filters.decode.utf8(err))
                    __M_writer(u'</pre></li></ul>\n               </li>\n')
                # SOURCE LINE 890
                __M_writer(u'             </ul>\n')
        # SOURCE LINE 893
        __M_writer(u'<!--@begin:Shown completed course list-->\n<!--@date:2013-11-02-->\n          <header>\n            <h2>')
        # SOURCE LINE 896
        __M_writer(filters.decode.utf8(_("Completed Courses")))
        __M_writer(u'</h2>\n          </header>\n          ')
        # SOURCE LINE 898
        runtime._include_file(context, u'completed_courses.html', _template_uri)
        __M_writer(u'\n<!--@end-->\n</section>\n</section>\n<!--@begin:Chagne the table with new profile fields-->\n<!--@date:2013-11-02-->\n<section id="change_photo" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 907
        __M_writer(filters.decode.utf8(_('Add Profile Picture').format(course_number='<span id="email_settings_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_photo_form" method="post" enctype="multipart/form-data" action="upload_photo">\n      <!--@begin:Shown completed course list-->\n      <!--@date:2013-11-24-->\n      <div id="change_photo_error" class="modal-form-error"> </div>\n      <!--@end-->\n      <fieldset>\n        <div class="input-group">\n          <label>\n            <div style="border:5px solid #999;width:110px;height:110px;text-align:center;">\n              <img src="')
        # SOURCE LINE 919
        __M_writer(filters.decode.utf8(reverse('user_photo')))
        __M_writer(u'" style="" alt="photo" />\n            </div>\n          </label>\n          <label style="margin:20px 0;display:block;">\n            <input type="file" name="photo" id="id_photo" value="Choose a file" />\n          </label>\n          <label>\n            The image will be automatically scaled to fit within 110x110 pixels.\n          </label>  \n          <div id="image_uploading" style="text-align:center;">\n            <img src="/static/images/ora-loading.gif" style=""/> \n          </div>              \n        </div>\n      </fieldset>\n\t  <input type="hidden" name="csrfmiddlewaretoken" value="')
        # SOURCE LINE 933
        __M_writer(filters.decode.utf8(csrf_token))
        __M_writer(u'"/>\n      <div class="submit">\n        <input type="submit" class="btnx" id="photo_submit" value="Upload" />\n      </div>          \n    </form>\n    <div class="close-modal" id="change_photo_close">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="change_school" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 948
        __M_writer(filters.decode.utf8(_('Change My School').format(course_number='<span id="email_settings_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_school_form" method="post">\n      <fieldset>\n        <div class="input-group">\n            <label>School:</label>\n            <label style="margin:20px 0;display:block;">\n              <select name="school_id" style="width:100%" autocomplete="off">\n')
        # SOURCE LINE 957
        if curr_user.profile.district_id:
            # SOURCE LINE 958
            for item in School.objects.filter(district_id=curr_user.profile.district.id).order_by("name"):
                # SOURCE LINE 959
                __M_writer(u'                <option value="')
                __M_writer(filters.decode.utf8(item.id))
                __M_writer(u'">')
                __M_writer(filters.decode.utf8(item.name))
                __M_writer(u'</option>\n')
        # SOURCE LINE 962
        __M_writer(u'              </select>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>\n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<link rel="stylesheet" href="/static/tmp-resource/css/main.css" type="text/css" media="screen" />\n<section id="change_grade_level" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 981
        __M_writer(filters.decode.utf8(_('Change My Grade Level').format(course_number='<span id="email_settings_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_grade_level_form" method="post">\n      <fieldset>\n        <label id="">\n          Grade Level-Check all that apply:\n        </label>\n        <div class="input-group">\n          <label style="margin:20px 0;display:block;">\n            <input id="grade_level_id" type="hidden" name="grade_level_id" value="" autocomplete="off"/>\n')
        # SOURCE LINE 992
        for item in GradeLevel.objects.all():
            # SOURCE LINE 993
            __M_writer(u'            <span class="level">\n              <a href="#" id="grade_btn')
            # SOURCE LINE 994
            __M_writer(filters.decode.utf8(item.id))
            __M_writer(u'" class="btn_grade_level" onclick="click_grade_btn(')
            __M_writer(filters.decode.utf8(item.id))
            __M_writer(u');return false">\n                ')
            # SOURCE LINE 995
            __M_writer(filters.decode.utf8(item.name))
            __M_writer(u'\n              </a>\n            </span>\n')
        # SOURCE LINE 999
        __M_writer(u'            <br style="clear:both;"/>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="change_major_subject_area" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1017
        __M_writer(filters.decode.utf8(_('Change My Subject Area').format(course_number='<span id="email_settings_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_major_subject_area_form" method="post">\n      <fieldset>\n        <div class="input-group">\n          <label style="margin:20px 0;display:block;">\n            <select id="major_subject_area_id" name="major_subject_area_id" style="width:100%" autocomplete="off">\n')
        # SOURCE LINE 1025
        for item in SubjectArea.objects.all().order_by('so'):
            # SOURCE LINE 1026
            __M_writer(u'              <option value="')
            __M_writer(filters.decode.utf8(item.id))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(item.name))
            __M_writer(u'</option>\n')
        # SOURCE LINE 1028
        __M_writer(u'            </select>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="change_years_in_education" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1046
        __M_writer(filters.decode.utf8(_('Change Number of Years in Education').format()))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_years_in_education_form" method="post">\n      <fieldset>\n        <div class="input-group">\n          <label style="margin:20px 0;display:block;">\n            <select id="years_in_education_id" name="years_in_education_id" style="width:100%" autocomplete="off">\n')
        # SOURCE LINE 1054
        for item in YearsInEducation.objects.all():
            # SOURCE LINE 1055
            __M_writer(u'              <option value="')
            __M_writer(filters.decode.utf8(item.id))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(item.name))
            __M_writer(u'</option>\n')
        # SOURCE LINE 1057
        __M_writer(u'            </select>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<!-- percent_lunch form -->\n<section id="change_percent_lunch" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1076
        __M_writer(filters.decode.utf8(_('Change Free/Reduced Lunch').format()))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_percent_lunch_form" method="post">\n      <fieldset>\n        <div class="input-group">\n          <label style="margin:20px 0;display:block;">\n            <select id="percent_lunch" name="percent_lunch" style="width:100%" autocomplete="off">\n')
        # SOURCE LINE 1084
        for item in Enum.objects.filter(name="percent_lunch").order_by("odr"):
            # SOURCE LINE 1085
            __M_writer(u'              <option value="')
            __M_writer(filters.decode.utf8(item.value))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(item.content))
            __M_writer(u'</option>\n')
        # SOURCE LINE 1087
        __M_writer(u'            </select>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<!-- change_percent_iep form -->\n<section id="change_percent_iep" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1106
        __M_writer(filters.decode.utf8(_('Change IEPs').format()))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_percent_iep_form" method="post">\n      <fieldset>\n        <div class="input-group">\n          <label style="margin:20px 0;display:block;">\n            <select id="percent_iep" name="percent_iep" style="width:100%" autocomplete="off">\n')
        # SOURCE LINE 1114
        for item in Enum.objects.filter(name="percent_iep").order_by("odr"):
            # SOURCE LINE 1115
            __M_writer(u'              <option value="')
            __M_writer(filters.decode.utf8(item.value))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(item.content))
            __M_writer(u'</option>\n')
        # SOURCE LINE 1117
        __M_writer(u'            </select>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<!-- percent_eng_learner form -->\n<section id="change_percent_eng_learner" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1136
        __M_writer(filters.decode.utf8(_('Change English Learners').format()))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_percent_eng_learner_form" method="post">\n      <fieldset>\n        <div class="input-group">\n          <label style="margin:20px 0;display:block;">\n            <select id="percent_eng_learner" name="percent_eng_learner" style="width:100%" autocomplete="off">\n')
        # SOURCE LINE 1144
        for item in Enum.objects.filter(name="percent_lunch").order_by("odr"):
            # SOURCE LINE 1145
            __M_writer(u'              <option value="')
            __M_writer(filters.decode.utf8(item.value))
            __M_writer(u'">')
            __M_writer(filters.decode.utf8(item.content))
            __M_writer(u'</option>\n')
        # SOURCE LINE 1147
        __M_writer(u'            </select>\n          </label>\n        </div>\n      </fieldset>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="change_bio" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1165
        __M_writer(filters.decode.utf8(_('Change My BIO').format(course_number='<span id="email_settings_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="change_bio_form" method="post">\n      <fieldset>\n        <div class="input-group">\n          <label>\n            <textarea maxlength="255" id="txBio" name="bio" rows="" cols="" tabindex=""  style="width:100%;height:100%;height:300px;resize:none;">')
        # SOURCE LINE 1172
        __M_writer(filters.decode.utf8(curr_user.profile.bio))
        __M_writer(u'</textarea>\n          </label>\n          <section style="color:black;">\n            Maximum to 255 Characters <span></span>\n          </section>\n        </div>\n      </fieldset>\n      <script type="text/javascript">\n        var txBio=document.getElementById(\'txBio\');\n        txBio.oninput=function(){\n          $(this).parent().next("section").find("span").html(255-this.value.length)\n        }\n        txBio.oninput()\n      </script>\n      <div class="submit">\n        <input type="submit" class="btnx" id="submit" value="Save Changes" />\n      </div>          \n    </form>\n    <div class="close-modal">\n      <div class="inner" id="change_bio_close">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n  <!--@end-->\n</section>\n<section id="email-settings-modal" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1201
        __M_writer(filters.decode.utf8(_('Email Settings for {course_number}').format(course_number='<span id="email_settings_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <form id="email_settings_form" method="post">\n      <input name="course_id" id="email_settings_course_id" type="hidden" />\n      <label>')
        # SOURCE LINE 1206
        __M_writer(filters.decode.utf8(_("Receive course emails")))
        __M_writer(u' <input type="checkbox" id="receive_emails" name="receive_emails" /></label>\n      <div class="submit">\n<!--@begin:Chagne the button bolor in Email Settings table-->\n<!--@date:2013-11-02-->\n        <input type="submit" class="btnx" id="submit" value="Save Settings" />\n<!--@end-->        \n      </div>\n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="unenroll-modal" class="modal unenroll-modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1224
        __M_writer(filters.decode.utf8(_('Are you sure you want to unregister from {course_number}?').format(course_number='<span id="unenroll_course_number"></span>')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <div id="unenroll_error" class="modal-form-error"></div>\n    <form id="unenroll_form" method="post" data-remote="true" action="')
        # SOURCE LINE 1228
        __M_writer(filters.decode.utf8(reverse('change_enrollment')))
        __M_writer(u'">\n      <input name="course_id" id="unenroll_course_id" type="hidden" />\n      <input name="enrollment_action" type="hidden" value="unenroll" />\n      <div class="submit">\n        <input id="submit" name="submit" type="submit" value="Unregister" />\n      </div>\n    </form>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="password_reset_complete" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1245
        __M_writer(filters.decode.utf8(_('Password Reset Email Sent')))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <div>\n      <form> <!-- Here for styling reasons -->\n        <section>\n          <p>')
        # SOURCE LINE 1251
        __M_writer(filters.decode.utf8(_('An email has been sent to {email}. Follow the link in the email to change your password.').format(email=curr_user.email)))
        __M_writer(u'</p>\n        </section>\n      </form>\n    </div>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<section id="change_email" class="modal">\n  <div class="inner-wrapper">\n    <header>\n<!--@begin:Change the title of email table-->\n<!--@date:2013-11-02-->            \n      <h2><span id="change_email_title">')
        # SOURCE LINE 1267
        __M_writer(filters.decode.utf8(_("Change My Email")))
        __M_writer(u'</span></h2>\n<!--@end-->\n      <hr/>\n    </header>\n    <div id="change_email_body">\n      <form id="change_email_form">\n        <div id="change_email_error" class="modal-form-error"> </div>\n        <fieldset>\n          <div class="input-group">\n<!--@begin:Change the email table-->\n<!--@date:2013-11-02-->            \n            <label>')
        # SOURCE LINE 1278
        __M_writer(filters.decode.utf8(_('Please edit your email below:')))
        __M_writer(u'</label>\n            <input id="new_email_field" type="email" value="')
        # SOURCE LINE 1279
        __M_writer(filters.decode.utf8(curr_user.email))
        __M_writer(u'" />\n            <!-- <label>')
        # SOURCE LINE 1280
        __M_writer(filters.decode.utf8(_('Please confirm your password:')))
        __M_writer(u'</label> -->\n            <!-- <input id="new_email_password" value="" type="password" /> -->\n          </div>\n          <!-- <section> -->\n          <!--   <p>')
        # SOURCE LINE 1284
        __M_writer(filters.decode.utf8(_('We will send a confirmation to both {email} and your new email as part of the process.').format(email=curr_user.email)))
        __M_writer(u'</p> -->\n          <!-- </section> -->\n<!--@end-->          \n          <div class="submit">\n            <input type="submit" id="submit_email_change" value="')
        # SOURCE LINE 1288
        __M_writer(filters.decode.utf8(_('Change Email')))
        __M_writer(u'"/>\n          </div>\n        </fieldset>\n      </form>\n    </div>\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n<!--@begin:User photo upload table-->\n<!--@date:2013-11-02-->\n<!----\n<section id="apply_picture_change" class="modal">\n  <div class="inner-wrapper">\n    <div class="close-modal">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n    <header>\n      <h2>Picture uploading</h2>\n      <hr/>\n    </header>\n    <div id="">\n      <form method="" id="" action="">\n       <fieldset>\n          <div class="input-group">\n            <label>Please choose a file.</label>\n            <input type="file" name="file" value="" />\n          </div>\n          <div class="submit">\n            <input type="submit" id="submit" value="Upload now">\n          </div>\n        </fieldset>\n      </form>\n    </div>\n  </div>\n</section>\n-->\n<!--@end-->\n<section id="apply_name_change" class="modal">\n  <div class="inner-wrapper">\n    <header>\n      <h2>')
        # SOURCE LINE 1334
        __M_writer(filters.decode.utf8(_("Change your name")))
        __M_writer(u'</h2>\n      <hr/>\n    </header>\n    <div id="change_name_body">\n      <form id="change_name_form">\n        <div id="change_name_error" class="modal-form-error"> </div>\n        <p>')
        # SOURCE LINE 1340
        __M_writer(filters.decode.utf8(_("To uphold the credibility of {platform} certificates, all name changes will be logged and recorded.").format(platform=settings.PLATFORM_NAME)))
        __M_writer(u'</p>\n        <br/>\n        <fieldset>\n          <div class="input-group">\n            <label>')
        # SOURCE LINE 1344
        __M_writer(filters.decode.utf8(_("Enter your desired full name, as it will appear on the {platform} certificates:").format(platform=settings.PLATFORM_NAME)))
        __M_writer(u'</label>\n<!--@begin:Username change table-->\n<!--@date:2013-11-02-->            \n            <br/><br/>\n            <label style="font-style:normal;color:#666;font-size:16px;font-family:\'open sans\'">First Name</label>\n            <input id="new_first_name_field" value="')
        # SOURCE LINE 1349
        __M_writer(filters.decode.utf8(curr_user.first_name))
        __M_writer(u'" type="text" autocomplete="off" maxlength="30"/>\n            <label style="font-style:normal;color:#666;font-size:16px;font-family:\'open sans\'">Last Name</label>\n            <input id="new_last_name_field" value="')
        # SOURCE LINE 1351
        __M_writer(filters.decode.utf8(curr_user.last_name))
        __M_writer(u'" type="text" autocomplete="off" maxlength="30"/>\n<!--@end-->\n            <label>')
        # SOURCE LINE 1353
        __M_writer(filters.decode.utf8(_("Reason for name change:")))
        __M_writer(u'</label>\n            <textarea id="name_rationale_field" value=""></textarea>\n          </div>\n          <div class="submit">\n            <input type="submit" id="submit" value="')
        # SOURCE LINE 1357
        __M_writer(filters.decode.utf8(_('Change My Name')))
        __M_writer(u'">\n          </div>\n        </fieldset>\n      </form>\n    </div>\n    <div class="close-modal" id="change_name_close">\n      <div class="inner">\n        <p>&#10005;</p>\n      </div>\n    </div>\n  </div>\n</section>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js_extra(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def js_extra():
            return render_js_extra(context)
        request = context.get('request', UNDEFINED)
        curr_user = context.get('curr_user', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 66
        __M_writer(u'\n<script type="text/javascript">\n  /*@begin:Click the round button in grade_level table*/\n  /*@date:2013-11-02*/\n  function click_grade_btn(i){\n    var vals={}\n    $.each($("#grade_level_id").val().split(","),function(i,v){\n      if(v)vals[v]=1;\n    });\n    var link=document.getElementById("grade_btn"+i);\n    if($(link).hasClass("btn_grade_level_active")){\n      $(link).removeClass("btn_grade_level_active");\n      vals[i]=\'\';\n    }else{\n      $(link).addClass("btn_grade_level_active");\n      vals[i]=1;\n    }\n    var arVals=[];\n    $.each(vals,function(i,v){\n      if(v)arVals.push(i)\n    });\n    arVals.sort(function(a,b){return parseInt(a)-parseInt(b)});\n    $("#grade_level_id").val(arVals.join());\n  }\n  /*@end*/\n  (function() {\n    $(".email-settings").click(function(event) {\n      $("#email_settings_course_id").val( $(event.target).data("course-id") );\n      $("#email_settings_course_number").text( $(event.target).data("course-number") );\n      if($(event.target).data("optout") == "False") {\n        $("#receive_emails").prop(\'checked\', true);\n      }\n    });\n    $(".unenroll").click(function(event) {\n      $("#unenroll_course_id").val( $(event.target).data("course-id") );\n      $("#unenroll_course_number").text( $(event.target).data("course-number") );\n    });\n    $(\'#unenroll_form\').on(\'ajax:complete\', function(event, xhr) {\n      if(xhr.status == 200) {\n        location.href = "')
        # SOURCE LINE 105
        __M_writer(filters.decode.utf8(reverse('dashboard')))
        __M_writer(u'";\n      } else if (xhr.status == 403) {\n        location.href = "')
        # SOURCE LINE 107
        __M_writer(filters.decode.utf8(reverse('signin_user')))
        __M_writer(u'?course_id=" +\n          $("#unenroll_course_id").val() + "&enrollment_action=unenroll";\n      } else {\n        $(\'#unenroll_error\').html(\n          xhr.responseText ? xhr.responseText : "An error occurred. Please try again later."\n        ).stop().css("display", "block");\n      }\n    });\n    $(\'#pwd_reset_button\').click(function() {\n      $.post(\'')
        # SOURCE LINE 116
        __M_writer(filters.decode.utf8(reverse("password_reset")))
        __M_writer(u'\',\n             {"email"  : $(\'#id_email\').val()},\n             function(data){\n               //$("#password_reset_complete_link").click();\n             });\n      return false;\n    });\n    $("#change_email_form").submit(function(){\n      var new_email = $(\'#new_email_field\').val();\n      /*@begin:Do not need to confirm passowrd when changing email*/\n      /*@date:2013-11-02*/\n      //var new_password = $(\'#new_email_password\').val();\n      $.post(\'')
        # SOURCE LINE 128
        __M_writer(filters.decode.utf8(reverse("change_email")))
        __M_writer(u'\',\n             {"new_email" : new_email, "password" : ""},\n             /*@end*/\n             function(data) {\n               if (data.success) {\n                 $("#change_email_title").html("Please verify your new email");\n                 $("#change_email_form").html("<p>You\'ll receive a confirmation in your " +\n                                              "in-box. Please click the link in the " +\n                                              "email to confirm the email change.</p>");\n                 $("#change_email_form").html("<p>')
        # SOURCE LINE 137
        __M_writer(filters.decode.utf8(_('You\'ll receive a confirmation in your in-box. Please click the link in the email to confirm the email change.')))
        __M_writer(u'</p>");\n               } else {\n                 $("#change_email_error").html(data.error).stop().css("display", "block");\n               }\n             });\n      return false;\n    });\n    $("#change_name_form").submit(function(){\n      /*@begin:Change the name to two fileds*/\n      /*@date:2013-11-02*/\n      var new_first_name = $(\'#new_first_name_field\').val();\n      var new_last_name = $(\'#new_last_name_field\').val();\n      var rationale = $(\'#name_rationale_field\').val();\n      $.post(\'')
        # SOURCE LINE 150
        __M_writer(filters.decode.utf8(reverse("change_name")))
        __M_writer(u'\',\n             {"new_first_name":new_first_name, "new_last_name":new_last_name,"rationale":rationale},\n             /*@end*/\n             function(data) {\n               if(data.success) {\n                 location.reload();\n                 // $("#change_name_body").html("<p>Name changed.</p>");\n               } else {\n                 $("#change_name_error").html(data.error).stop().css("display", "block");\n               }\n             });\n      return false;\n    });\n<!--@begin:Process the newly added fields in dashboard-->\n<!--@date:2013-11-02-->\n     $("#change_school_form").find("select[name=\'school_id\']").val(\'')
        # SOURCE LINE 165
        __M_writer(filters.decode.utf8(curr_user.profile.school_id))
        __M_writer(u'\')\n    $("#change_school_form").submit(function(){\n      var school_id = $(this.school_id).val();\n      $.post(\'')
        # SOURCE LINE 168
        __M_writer(filters.decode.utf8(reverse("change_school")))
        __M_writer(u'\',\n             {"school_id":school_id},\n             function(data) {\n               if(data.success) {\n                 location.reload();\n               } else {\n                 $("#change_school_error").html(data.error).stop().css("display", "block");\n               }\n             });\n       return false;\n    });\n    $.each( \'')
        # SOURCE LINE 179
        __M_writer(filters.decode.utf8(curr_user.profile.grade_level_id))
        __M_writer(u'\'.split(\',\') ,function(i,v){\n      if($.trim(v))\n        click_grade_btn(v);\n    });\n    $("#change_grade_level_form").submit(function(){\n      var grade_level_id = $(this.grade_level_id).val();\n      $.post(\'')
        # SOURCE LINE 185
        __M_writer(filters.decode.utf8(reverse("change_grade_level")))
        __M_writer(u'\',\n             {"grade_level_id":grade_level_id},\n             function(data) {\n               if(data.success) {\n                 location.reload();\n               } else {\n                 $("#change_grade_level_error").html(data.error).stop().css("display", "block");\n               }\n             });\n      return false;\n    });\n    // change_percent_lunch submit\n    $("#change_percent_lunch_form").find("select[name=\'percent_lunch\']").val(\'')
        # SOURCE LINE 197
        __M_writer(filters.decode.utf8(curr_user.profile.percent_lunch))
        __M_writer(u'\')\n      $("#change_percent_lunch_form").submit(function(){\n        var percent_lunch = $(this.percent_lunch).val();\n        $.post(\'')
        # SOURCE LINE 200
        __M_writer(filters.decode.utf8(reverse("change_percent_lunch")))
        __M_writer(u'\',\n               {"percent_lunch":percent_lunch},\n               function(data) {\n                 if(data.success) {\n                   location.reload();\n                 } else {\n                   $("#change_percent_lunch_error").html(data.error).stop().css("display", "block");\n                 }\n               });\n        return false;\n      });\n    // change_percent_iep submit\n    $("#change_percent_iep_form").find("select[name=\'percent_iep\']").val(\'')
        # SOURCE LINE 212
        __M_writer(filters.decode.utf8(curr_user.profile.percent_iep))
        __M_writer(u'\')\n      $("#change_percent_iep_form").submit(function(){\n        var percent_iep = $(this.percent_iep).val();\n        $.post(\'')
        # SOURCE LINE 215
        __M_writer(filters.decode.utf8(reverse("change_percent_iep")))
        __M_writer(u'\',\n               {"percent_iep":percent_iep},\n               function(data) {\n                 if(data.success) {\n                   location.reload();\n                 } else {\n                   $("#change_percent_iep_error").html(data.error).stop().css("display", "block");\n                 }\n               });\n        return false;\n      });\n    // change_percent_eng_learner submit\n    $("#change_percent_eng_learner_form").find("select[name=\'percent_eng_learner\']").val(\'')
        # SOURCE LINE 227
        __M_writer(filters.decode.utf8(curr_user.profile.percent_eng_learner))
        __M_writer(u'\')\n      $("#change_percent_eng_learner_form").submit(function(){\n        var percent_eng_learner = $(this.percent_eng_learner).val();\n        $.post(\'')
        # SOURCE LINE 230
        __M_writer(filters.decode.utf8(reverse("change_percent_eng_learner")))
        __M_writer(u'\',\n               {"percent_eng_learner":percent_eng_learner},\n               function(data) {\n                 if(data.success) {\n                   location.reload();\n                 } else {\n                   $("#change_percent_eng_learner_error").html(data.error).stop().css("display", "block");\n                 }\n               });\n        return false;\n      });\n    $("#change_major_subject_area_form").find("select[name=\'major_subject_area_id\']").val(\'')
        # SOURCE LINE 241
        __M_writer(filters.decode.utf8(curr_user.profile.major_subject_area_id))
        __M_writer(u'\')\n      $("#change_major_subject_area_form").submit(function(){\n        var major_subject_area_id = $(this.major_subject_area_id).val();\n        $.post(\'')
        # SOURCE LINE 244
        __M_writer(filters.decode.utf8(reverse("change_major_subject_area")))
        __M_writer(u'\',\n               {"major_subject_area_id":major_subject_area_id},\n               function(data) {\n                 if(data.success) {\n                   location.reload();\n                 } else {\n                   $("#change_major_subject_area_error").html(data.error).stop().css("display", "block");\n                 }\n               });\n        return false;\n      });\n    $("#change_years_in_education_form").find("select[name=\'years_in_education_id\']").val(\'')
        # SOURCE LINE 255
        __M_writer(filters.decode.utf8(curr_user.profile.years_in_education_id))
        __M_writer(u'\')\n      $("#change_years_in_education_form").submit(function(){\n        var years_in_education_id = $(this.years_in_education_id).val();\n        $.post(\'')
        # SOURCE LINE 258
        __M_writer(filters.decode.utf8(reverse("change_years_in_education")))
        __M_writer(u'\',\n               {"years_in_education_id":years_in_education_id},\n               function(data) {\n                 if(data.success) {\n                   location.reload();\n                 } else {\n                   $("#change_years_in_education_error").html(data.error).stop().css("display", "block");\n                 }\n               });\n        return false;\n      });\n    $("#change_bio_form").submit(function(){\n      var bio = $(this.bio).val();\n      $.post(\'')
        # SOURCE LINE 271
        __M_writer(filters.decode.utf8(reverse("change_bio")))
        __M_writer(u'\',\n             {"bio":bio},\n             function(data) {\n               if(data.success) {\n                 location.reload();\n               } else {\n                 $("#change_bio_error").html(data.error).stop().css("display", "block");\n               }\n             });\n      return false;\n    });\n    <!--@end-->\n    $("#email_settings_form").submit(function(){\n      $.ajax({\n        type: "POST",\n        url: \'')
        # SOURCE LINE 286
        __M_writer(filters.decode.utf8(reverse("change_email_settings")))
        __M_writer(u'\',\n        data: $(this).serializeArray(),\n        success: function(data) {\n          if(data.success) {\n            location.href = "')
        # SOURCE LINE 290
        __M_writer(filters.decode.utf8(reverse('dashboard')))
        __M_writer(u'";\n          }\n        },\n        error: function(xhr, textStatus, error) {\n          if (xhr.status == 403) {\n            location.href = "')
        # SOURCE LINE 295
        __M_writer(filters.decode.utf8(reverse('signin_user')))
        __M_writer(u'";          \n          }\n        }\n      });\n      return false;\n    });\n  })(this)\n  $("#change_photo_form").submit(function(){\n    var AllowImgFileSize=512;\n    var AllowImgWidth=1024;\n    var AllowImgHeight=768; \n    var fileImg = document.getElementById("id_photo"); \n    <!--check file choose-->\n    if (fileImg.value=="")\n    {\n      $("#change_photo_error").html("Update your avatar by uploading an image from your computer.").stop().css("display", "block");\n      fileImg.focus();\n      return false;\n    }\n    <!------------------------------------------>\n    <!--check file type-->\n    var fileImg_url=fileImg.value.toLowerCase();\n    var fileImg_ext=fileImg_url.substring(fileImg_url.length-3,fileImg_url.length);\n    if (fileImg_ext!="jpg" && fileImg_ext!="peg" && fileImg_ext!="png")\n    {\n      $("#change_photo_error").html("We accept image only in JPG or PNG.").stop().css("display", "block");\n      //fileImg.select()\n      //document.execCommand("Delete");\n      fileImg.focus();\n      return false;\n    }\n    <!------------------------------------------>\n    <!--check file size(less than 2m)-->\n    var file_size =  fileImg.files[0].size;\n    if (file_size>2048*1024)\n    {\n      $("#change_photo_error").html("The file size CANNOT exceed 2MB (2048 KB).").stop().css("display", "block");\n      fileImg.focus();\n      return false;\n    }\n    <!------------------------------------------>\n    document.getElementById("photo_submit").disabled = true;\n    $(\'#image_uploading\').show(); \n    $(\'#change_photo_form\').submit(); \n    });\n<!--@begin:clear form content and error information when close the sub page-->\n<!--@date:2013-12-05--> \n    $("#change_name_close").click(function(){\n      $(\'#change_name_error\').hide();\n    });\n    $("#change_photo_close").click(function(){\n      $(\'#change_photo_error\').hide();\n      $(\'#id_photo\')[0].value = "";\n    });\n    $("#change_bio_close").click(function(){\n      $(\'#id_bio\')[0].value = "";\n    });\n    $("#container_dashboard").click(function(){\n      $(\'#change_name_error\').hide();\n      $(\'#change_photo_error\').hide();\n      $(\'#id_photo\')[0].value = "";\n      $(\'#id_bio\')[0].value = "";\n    });\n<!--@end-->\n  //-----------------------------------------------\n  $(".portfolio-btn").click(function(){\n    var curr_user={};\n    var interviewer={};\n    //var course_number=$(this).parent().find("a").eq(0).text().split(\' \')[0];\n    var course_number=$(this).parent().find("a").attr("course_number");\n    interviewer.id="')
        # SOURCE LINE 365
        __M_writer(filters.decode.utf8(request.user.id))
        __M_writer(u'";\n    interviewer.name="')
        # SOURCE LINE 366
        __M_writer(filters.decode.utf8(request.user.username))
        __M_writer(u'";\n    interviewer.fullname="')
        # SOURCE LINE 367
        __M_writer(filters.decode.utf8(request.user.first_name))
        __M_writer(u' ')
        __M_writer(filters.decode.utf8(request.user.last_name))
        __M_writer(u'";\n    curr_user.id="')
        # SOURCE LINE 368
        __M_writer(filters.decode.utf8(curr_user.id))
        __M_writer(u'";\n    var datainfo={\'info\':JSON.stringify({\'user_id\':curr_user.id,\'interviewer_id\':interviewer.id,\'interviewer_name\':interviewer.name,\n                                         \'interviewer_fullname\':interviewer.fullname,\'type\':\'view_portfolio\',\n                                         \'course_number\':course_number,\'date\':(new Date()).toISOString(),\'activate\':\'false\'})};\n    var url = $(this).attr("link");\n    $.post("')
        # SOURCE LINE 373
        __M_writer(filters.decode.utf8(reverse('save_interactive_update')))
        __M_writer(u'",datainfo,function(){window.open(url,\'_self\');});\n   })\n  </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        curr_user = context.get('curr_user', UNDEFINED)
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 20
        __M_writer(u'<title>')
        __M_writer(filters.decode.utf8(_("Dashboard - {username}".format(username=curr_user.username))))
        __M_writer(u'</title>')
        return ''
    finally:
        context.caller_stack._pop_frame()


