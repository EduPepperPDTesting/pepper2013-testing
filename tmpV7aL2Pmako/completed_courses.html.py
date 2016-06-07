# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465224092.281572
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/completed_courses.html'
_template_uri = u'completed_courses.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 3

from django.core.urlresolvers import reverse
from courseware.courses import course_image_url, get_course_about_section
from courseware.access import has_access
from certificates.models import CertificateStatuses
from xmodule.modulestore import MONGO_MODULESTORE_TYPE
from xmodule.modulestore.django import modulestore


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        cert_statuses = context.get('cert_statuses', UNDEFINED)
        settings = context.get('settings', UNDEFINED)
        external_times = context.get('external_times', UNDEFINED)
        float = context.get('float', UNDEFINED)
        request = context.get('request', UNDEFINED)
        show_courseware_links_for = context.get('show_courseware_links_for', UNDEFINED)
        exam_registrations = context.get('exam_registrations', UNDEFINED)
        curr_user = context.get('curr_user', UNDEFINED)
        course_times = context.get('course_times', UNDEFINED)
        courses_complated = context.get('courses_complated', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 10
        __M_writer(u'\n\n<!--@begin:information of user who have no COMPLETED COURSES-->\n<!--@date:2013-12-13-->\n')
        # SOURCE LINE 14
        if not courses_complated:
            # SOURCE LINE 15
            __M_writer(u'   <section class="empty-dashboard-message">\n        <p>')
            # SOURCE LINE 16
            __M_writer(filters.decode.utf8(_("You haven’t completed any course yet.")))
            __M_writer(u'</p>\n   </section>\n')
        # SOURCE LINE 19
        __M_writer(u'<!--@end-->\n\n')
        # SOURCE LINE 21
        for course in courses_complated:
            # SOURCE LINE 22
            __M_writer(u'        <article class="my-course">\n          ')
            # SOURCE LINE 23

            course_target = reverse('courseware', args=[course.id])
                      
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['course_target'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 25
            __M_writer(u'\n')
            # SOURCE LINE 26
            if course.id in show_courseware_links_for:
                # SOURCE LINE 27
                if curr_user==request.user:
                    # SOURCE LINE 28
                    __M_writer(u'            <a href="')
                    __M_writer(filters.decode.utf8(course_target))
                    __M_writer(u'" class="cover">\n')
                    # SOURCE LINE 29
                else:
                    # SOURCE LINE 30
                    __M_writer(u'            <a href="" class="cover" style="cursor:default;" onclick="return false;">\n')
                # SOURCE LINE 32
                __M_writer(u'              <img src="')
                __M_writer(filters.decode.utf8(course_image_url(course)))
                __M_writer(u'" style="width:200px;height:104px;" alt="')
                __M_writer(filters.html_escape(filters.decode.utf8(_('{course_number} {course_name} Cover Image').format(course_number=course.number, course_name=course.display_name_with_default) )))
                __M_writer(u'" />\n            </a>\n')
                # SOURCE LINE 34
            else:
                # SOURCE LINE 35
                __M_writer(u'            <div class="cover">\n              <img src="')
                # SOURCE LINE 36
                __M_writer(filters.decode.utf8(course_image_url(course)))
                __M_writer(u'" alt="')
                __M_writer(filters.html_escape(filters.decode.utf8(_('{course_number} {course_name} Cover Image').format(course_number=course.number, course_name=course.display_name_with_default) )))
                __M_writer(u'" />\n            </div>\n')
            # SOURCE LINE 39
            __M_writer(u'          <section class="info">\n            <hgroup>\n              <p class="date-block">\n                ')
            # SOURCE LINE 42
            __M_writer(filters.decode.utf8(_("Course Completed - {end_date:%B %d,%Y}").format(end_date=course.student_enrollment_date)))
            __M_writer(u'\n              </p>\n              <h2 class="university">')
            # SOURCE LINE 44
            __M_writer(filters.decode.utf8(get_course_about_section(course, 'university')))
            __M_writer(u'</h2>\n              <h3>\n')
            # SOURCE LINE 46
            if course.id in show_courseware_links_for:
                # SOURCE LINE 47
                if curr_user==request.user:
                    # SOURCE LINE 48
                    __M_writer(u'                  <a href="')
                    __M_writer(filters.decode.utf8(course_target))
                    __M_writer(u'">')
                    __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                    __M_writer(u' ')
                    __M_writer(filters.decode.utf8(course.display_name_with_default))
                    __M_writer(u'</a>\n')
                    # SOURCE LINE 49
                else:
                    # SOURCE LINE 50
                    __M_writer(u'                  <a href="" style="cursor:default;" onclick="return false;" course_number="')
                    __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                    __M_writer(u'">')
                    __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                    __M_writer(u' ')
                    __M_writer(filters.decode.utf8(course.display_name_with_default))
                    __M_writer(u'</a>\n')
                # SOURCE LINE 52
            else:
                # SOURCE LINE 53
                __M_writer(u'                  <span>')
                __M_writer(filters.html_escape(filters.decode.utf8(course.display_number_with_default )))
                __M_writer(u' ')
                __M_writer(filters.decode.utf8(course.display_name_with_default))
                __M_writer(u'</span>\n')
            # SOURCE LINE 55
            __M_writer(u'              </h3>\n            </hgroup>\n            ')
            # SOURCE LINE 57

            testcenter_exam_info = course.current_test_center_exam
            registration = exam_registrations.get(course.id)
            testcenter_register_target = reverse('begin_exam_registration', args=[course.id])
                        
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['testcenter_register_target','testcenter_exam_info','registration'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 61
            __M_writer(u'\n')
            # SOURCE LINE 62
            if testcenter_exam_info is not None:
                # SOURCE LINE 63
                if registration is None and testcenter_exam_info.is_registering():
                    # SOURCE LINE 64
                    __M_writer(u'                <div class="message message-status is-shown exam-register">\n                  <a href="')
                    # SOURCE LINE 65
                    __M_writer(filters.decode.utf8(testcenter_register_target))
                    __M_writer(u'" class="button exam-button" id="exam_register_button">')
                    __M_writer(filters.decode.utf8(_("Register for Pearson exam")))
                    __M_writer(u'</a>\n                  <p class="message-copy">')
                    # SOURCE LINE 66
                    __M_writer(filters.decode.utf8(_("Registration for the Pearson exam is now open and will close on {end_date}").format(end_date="<strong>{}</strong>".format(testcenter_exam_info.registration_end_date_text))))
                    __M_writer(u'</p>\n                </div>\n')
                # SOURCE LINE 69
                __M_writer(u'                <!-- display a registration for a current exam, even if the registration period is over -->\n')
                # SOURCE LINE 70
                if registration is not None:
                    # SOURCE LINE 71
                    if registration.is_accepted:
                        # SOURCE LINE 72
                        __M_writer(u'                <div class="message message-status is-shown exam-schedule">\n                   <a href="')
                        # SOURCE LINE 73
                        __M_writer(filters.decode.utf8(registration.registration_signup_url))
                        __M_writer(u'" class="button exam-button">')
                        __M_writer(filters.decode.utf8(_("Schedule Pearson exam")))
                        __M_writer(u'</a>\n                   <p class="exam-registration-number">')
                        # SOURCE LINE 74
                        __M_writer(filters.decode.utf8(_("{link_start}Registration{link_end} number: {number}").format(
                      link_start='<a href="{url}" id="exam_register_link">'.format(url=testcenter_register_target),
                      link_end='</a>',
                      number=registration.client_candidate_id,
                    )))
                        # SOURCE LINE 78
                        __M_writer(u'</p>\n                   <p class="message-copy">')
                        # SOURCE LINE 79
                        __M_writer(filters.decode.utf8(_("Write this down! You'll need it to schedule your exam.")))
                        __M_writer(u'</p>\n                </div>\n')
                    # SOURCE LINE 82
                    if  registration.is_rejected:
                        # SOURCE LINE 83
                        __M_writer(u'                <div class="message message-status is-shown exam-schedule">\n                  <p class="message-copy">\n                    <strong>')
                        # SOURCE LINE 85
                        __M_writer(filters.decode.utf8(_("Your registration for the Pearson exam has been rejected. Please {link_start}see your registration status details{link_end}.").format(
                      link_start='<a href="{url}" id="exam_register_link">'.format(url=testcenter_register_target),
                      link_end='</a>')))
                        # SOURCE LINE 87
                        __M_writer(u'</strong>\n                    ')
                        # SOURCE LINE 88
                        __M_writer(filters.decode.utf8(_("Otherwise {link_start}contact edX at {email}{link_end} for further help.").format(
                      link_start='<a class="contact-link" href="mailto:{email}?subject=Pearson VUE Exam - {about} {number}">'.format(email="exam-help@edx.org", about=get_course_about_section(course, 'university'), number=course.display_number_with_default),
                      link_end='</a>',
                      email="exam-help@edx.org",
                     )))
                        # SOURCE LINE 92
                        __M_writer(u'\n                </div>\n')
                    # SOURCE LINE 95
                    if not registration.is_accepted and not registration.is_rejected:
                        # SOURCE LINE 96
                        __M_writer(u'\t            <div class="message message-status is-shown">\n                  <p class="message-copy"><strong>')
                        # SOURCE LINE 97
                        __M_writer(filters.decode.utf8(_("Your {link_start}registration for the Pearson exam{link_end} is pending.").format(link_start='<a href="{url}" id="exam_register_link">'.format(url=testcenter_register_target), link_end='</a>')))
                        __M_writer(u'</strong>\n                  ')
                        # SOURCE LINE 98
                        __M_writer(filters.decode.utf8(_("Within a few days, you should see a confirmation number here, which can be used to schedule your exam.")))
                        __M_writer(u'\n                  </p>\n                </div>\n')
            # SOURCE LINE 104
            __M_writer(u'            ')

            cert_status = cert_statuses.get(course.id)
            
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['cert_status'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 106
            __M_writer(u'\n')
            # SOURCE LINE 107
            if course.has_ended() and cert_status:
                # SOURCE LINE 108
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
                # SOURCE LINE 117
                __M_writer(u'\n                <div class="message message-status ')
                # SOURCE LINE 118
                __M_writer(filters.decode.utf8(status_css_class))
                __M_writer(u' is-shown">\n')
                # SOURCE LINE 119
                if cert_status['status'] == 'processing':
                    # SOURCE LINE 120
                    __M_writer(u'                      <p class="message-copy">')
                    __M_writer(filters.decode.utf8(_("Final course details are being wrapped up at this time. Your final standing will be available shortly.")))
                    __M_writer(u'</p>\n')
                    # SOURCE LINE 121
                elif cert_status['status'] in ('generating', 'ready', 'notpassing', 'restricted'):
                    # SOURCE LINE 122
                    __M_writer(u'                      <p class="message-copy">')
                    __M_writer(filters.decode.utf8(_("Your final grade:")))
                    __M_writer(u'\n                      <span class="grade-value">')
                    # SOURCE LINE 123
                    __M_writer(filters.decode.utf8("{0:.0f}%".format(float(cert_status['grade'])*100)))
                    __M_writer(u'</span>.\n')
                    # SOURCE LINE 124
                    if cert_status['status'] == 'notpassing':
                        # SOURCE LINE 125
                        __M_writer(u'                         ')
                        __M_writer(filters.decode.utf8(_("Grade required for a certificate:")))
                        __M_writer(u' <span class="grade-value">\n                           ')
                        # SOURCE LINE 126
                        __M_writer(filters.decode.utf8("{0:.0f}%".format(float(course.lowest_passing_grade)*100)))
                        __M_writer(u'</span>.\n')
                        # SOURCE LINE 127
                    elif cert_status['status'] == 'restricted':
                        # SOURCE LINE 128
                        __M_writer(u'                          <p class="message-copy">\n                          ')
                        # SOURCE LINE 129
                        __M_writer(filters.decode.utf8(_("Your certificate is being held pending confirmation that the issuance of your certificate is in compliance with strict U.S. embargoes on Iran, Cuba, Syria and Sudan. If you think our system has mistakenly identified you as being connected with one of those countries, please let us know by contacting {email}.").format(email='<a class="contact-link" href="mailto:{email}">{email}</a>.'.format(email=settings.CONTACT_EMAIL))))
                        __M_writer(u'\n                          </p>\n')
                    # SOURCE LINE 132
                    __M_writer(u'                      </p>\n')
                # SOURCE LINE 134
                if cert_status['show_disabled_download_button'] or cert_status['show_download_url'] or cert_status['show_survey_button']:
                    # SOURCE LINE 135
                    __M_writer(u'                  <ul class="actions">\n')
                    # SOURCE LINE 136
                    if cert_status['show_disabled_download_button']:
                        # SOURCE LINE 137
                        __M_writer(u'                      <li class="action"><span class="disabled">\n                          ')
                        # SOURCE LINE 138
                        __M_writer(filters.decode.utf8(_("Your Certificate is Generating")))
                        __M_writer(u'</span></li>\n')
                        # SOURCE LINE 139
                    elif cert_status['show_download_url']:
                        # SOURCE LINE 140
                        if curr_user==request.user:      
                            # SOURCE LINE 141
                            __M_writer(u'                      <li class="action">\n                      <a class="btn" href="')
                            # SOURCE LINE 142
                            __M_writer(filters.decode.utf8(cert_status['download_url']))
                            __M_writer(u'"\n                         title="')
                            # SOURCE LINE 143
                            __M_writer(filters.decode.utf8(_('This link will open/download a PDF document')))
                            __M_writer(u'">\n                         Download Your PDF Certificate</a>\n                      </li>\n')
                    # SOURCE LINE 148
                    if cert_status['show_survey_button']:
                        # SOURCE LINE 149
                        __M_writer(u'                      <li class="action"><a class="cta" href="')
                        __M_writer(filters.decode.utf8(cert_status['survey_url']))
                        __M_writer(u'">\n                             ')
                        # SOURCE LINE 150
                        __M_writer(filters.decode.utf8(_('Complete our course feedback survey')))
                        __M_writer(u'</a></li>\n')
                    # SOURCE LINE 152
                    __M_writer(u'                  </ul>\n')
                # SOURCE LINE 154
                __M_writer(u'                </div>\n')
            # SOURCE LINE 156
            __M_writer(u'                <link rel="stylesheet" href="/static/tmp-resource/css/main.css" type="text/css" media="screen" />\n\n')
            # SOURCE LINE 158
            if course.id in show_courseware_links_for:
                # SOURCE LINE 159
                if curr_user==request.user:              
                    # SOURCE LINE 160
                    __M_writer(u'\t\t\t\t<a href="')
                    __M_writer(filters.decode.utf8(reverse('portfolio_about_me',args=[course.id])))
                    __M_writer(u'" class="enter-course dashboard-btn1">')
                    __M_writer(filters.decode.utf8(_('View Portfolio')))
                    __M_writer(u'</a>\n')
                    # SOURCE LINE 161
                else:
                    # SOURCE LINE 162
                    __M_writer(u'                <a href="javascript:void(0)" class="enter-course dashboard-btn1 portfolio-btn" link="')
                    __M_writer(filters.decode.utf8(reverse('portfolio_about_me',args=[course.id,curr_user.id])))
                    __M_writer(u'">')
                    __M_writer(filters.decode.utf8(_('View Portfolio')))
                    __M_writer(u'</a>\n')
                # SOURCE LINE 164
                __M_writer(u'\n')
                # SOURCE LINE 165
                if curr_user==request.user:      
                    # SOURCE LINE 166
                    __M_writer(u'                <a href="')
                    __M_writer(filters.decode.utf8(course_target))
                    __M_writer(u'" class="enter-course dashboard-btn2" style="margin-left:10px;">')
                    __M_writer(filters.decode.utf8(_('View Course')))
                    __M_writer(u'</a>\n')
            # SOURCE LINE 169
            __M_writer(u'\n')
            # SOURCE LINE 170
            if settings.MITX_FEATURES['ENABLE_INSTRUCTOR_EMAIL'] and modulestore().get_modulestore_type(course.id) == MONGO_MODULESTORE_TYPE:
                # SOURCE LINE 171
                __M_writer(u'  \t      <!-- Only show the Email Settings link/modal if this course has bulk email feature enabled -->\n')
                # SOURCE LINE 172
                if curr_user==request.user:      
                    # SOURCE LINE 173
                    __M_writer(u'              <a href="')
                    __M_writer(filters.decode.utf8(reverse('download_certificate',args=[course.id,("{end_date:%Y-%m-%d}").format(end_date=course.student_enrollment_date)])))
                    __M_writer(u'" target="blank" class="enter-course dashboard-btn1" style="margin-left:10px;float:right;">')
                    __M_writer(filters.decode.utf8(_('Download Your PDF Certificate')))
                    __M_writer(u'</a>\n')
                    # SOURCE LINE 174
                    if course.hide_timer == False:
                        # SOURCE LINE 175
                        if course.show_external_timer == False:
                            # SOURCE LINE 176
                            __M_writer(u'                  <div class="course-time-completed" time_type="course" course_id="')
                            __M_writer(filters.decode.utf8(course.id))
                            __M_writer(u'">Course Time: <span>')
                            __M_writer(filters.decode.utf8(course_times[course.id]))
                            __M_writer(u'</span></div>\n')
                            # SOURCE LINE 177
                        else:
                            # SOURCE LINE 178
                            __M_writer(u'                  <div class="course-time-completed" time_type="external" course_id="')
                            __M_writer(filters.decode.utf8(course.id))
                            __M_writer(u'">External Time: <span>')
                            __M_writer(filters.decode.utf8(external_times[course.id]))
                            __M_writer(u'<span></div>\n')
            # SOURCE LINE 183
            __M_writer(u'            </section>\n          </article>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


