from django.contrib.auth.decorators import login_required
import logging
from certificates.models import GeneratedCertificate
from certificates.models import CertificateStatuses as status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

#@begin:View certificate page use
#@date:2013-11-28
from django.shortcuts import redirect
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response, render_to_string
from mitxmako.shortcuts import marketing_link
from util.cache import cache_if_anonymous
#@end

from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)
from courseware.model_data import FieldDataCache
import datetime

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics,ttfonts
import os
from io import BytesIO
import urllib
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.cache import cache_control
from administration.models import Author,CertificateAssociationType,Certificate

import cStringIO as StringIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from cgi import escape

logger = logging.getLogger(__name__)

@csrf_exempt
def update_certificate(request):
    """
    Will update GeneratedCertificate for a new certificate or
    modify an existing certificate entry.

    See models.py for a state diagram of certificate states

    This view should only ever be accessed by the xqueue server
    """

    if request.method == "POST":

        xqueue_body = json.loads(request.POST.get('xqueue_body'))
        xqueue_header = json.loads(request.POST.get('xqueue_header'))

        try:
            cert = GeneratedCertificate.objects.get(
                   user__username=xqueue_body['username'],
                   course_id=xqueue_body['course_id'],
                   key=xqueue_header['lms_key'])

        except GeneratedCertificate.DoesNotExist:
            logger.critical('Unable to lookup certificate\n'
                         'xqueue_body: {0}\n'
                         'xqueue_header: {1}'.format(
                                      xqueue_body, xqueue_header))

            return HttpResponse(json.dumps({
                            'return_code': 1,
                            'content': 'unable to lookup key'}),
                             mimetype='application/json')

        if 'error' in xqueue_body:
            cert.status = status.error
            if 'error_reason' in xqueue_body:

                # Hopefully we will record a meaningful error
                # here if something bad happened during the
                # certificate generation process
                #
                # example:
                #  (aamorm BerkeleyX/CS169.1x/2012_Fall)
                #  <class 'simples3.bucket.S3Error'>:
                #  HTTP error (reason=error(32, 'Broken pipe'), filename=None) :
                #  certificate_agent.py:175


                cert.error_reason = xqueue_body['error_reason']
        else:
            if cert.status in [status.generating, status.regenerating]:
                cert.download_uuid = xqueue_body['download_uuid']
                cert.verify_uuid = xqueue_body['verify_uuid']
                cert.download_url = xqueue_body['url']
                cert.status = status.downloadable
            elif cert.status in [status.deleting]:
                cert.status = status.deleted
            else:
                logger.critical('Invalid state for cert update: {0}'.format(
                    cert.status))
                return HttpResponse(json.dumps({
                            'return_code': 1,
                            'content': 'invalid cert status'}),
                             mimetype='application/json')
        cert.save()
        return HttpResponse(json.dumps({'return_code': 0}),
                             mimetype='application/json')

#@begin:View certificate page
#@date:2013-11-28
def course_from_id(course_id):
    """Return the CourseDescriptor corresponding to this course_id"""
    course_loc = CourseDescriptor.id_to_location(course_id)
    return modulestore().get_instance(course_id, course_loc)
'''
@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def download_certificate(request,course_id,completed_time):
    certificate_type=[['WestEd','PCG Education','A.L.L.','Understanding Language Initiative at Stanford'],['CT Core Standards']]
    user_id = request.user.id
    user_course = get_course_with_access(user_id, course_id, 'load')
    t_time = ""
    t_y = ""
    t_m = ""
    t_d = ""
    changdu = len(completed_time)
    if changdu > 9:
        t_time = completed_time.split('-')
        t_y = int(t_time[0])
        t_m = int(t_time[1])
        t_d = int(t_time[2])
    c_completed_time = datetime.date(t_y,t_m,t_d).strftime("%B %d, %Y ")

####### Ancestor

    user_id_temp = user_id + 15
    temp1 = '821bf6753e09qx4'
    temp2 = '103md94e157wf62a9'
    user_id_string = '%d' %user_id_temp
    pdf_filename = temp1 + user_id_string + temp2 + '.pdf'

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"' #directly download pdf
    buffer = BytesIO()
    # Create the PDF object, using the BytesIO object as its "file." Paper size = 'A4'
    c = canvas.Canvas(buffer,pagesize=(841.89,595.27))
    for i in range(len(certificate_type)):
        if user_course.display_organization in certificate_type[i]:
            if i==0:
                pdf=draw_certificate_default(request,user_course,c_completed_time,buffer,c)
            else:
                pdf=draw_certificate_CT(buffer,c)
    response.write(pdf)
    return response
'''
@login_required
def course_credits(request):
     return render_to_response('course_credits.html', {})

@ensure_csrf_cookie
@cache_if_anonymous
def download_certificate_demo(request):
     return render_to_response('d_certificate_demo.html', {})
#@end
'''
def draw_certificate_default(request, user_course, c_completed_time, buffer, c):
    first_name = request.user.first_name
    last_name = request.user.last_name
    c_course_name = user_course.display_name_with_default
    c_user_name = first_name + ' ' +last_name
    c_organization = ''
    c_estimated_effort = ''
    c_course_full_name = user_course.display_number_with_default + " " + c_course_name #course name
    fontpath = '/home/tahoe/edx_all/edx-platform/lms/static/fonts'
    imagepath = '/home/tahoe/edx_all/edx-platform/lms/static/images/certificate'
    pdfmetrics.registerFont(ttfonts.TTFont('Open Sans',os.path.join(fontpath, 'OpenSans-Regular-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('OpenSans_i',os.path.join(fontpath, 'OpenSans-Italic-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('OpenSans_b',os.path.join(fontpath, 'OpenSans-Bold-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('Nunito',os.path.join(fontpath, 'Nunito-Regular.ttf')))
    fontsize_completedtime = 15
    fontsize_maincontent = 20
    fontsize_username = 45
    fontsize_coursename = 25
    fontsize_effort = 21

    if user_course.display_number_with_default == "PEP101x":
        c_organization = 'PCG Education'
        c.drawImage(imagepath+"/certificate_pcg.jpg",0,0, width=841.89,height=595.27,mask=None)
        c_estimated_effort = user_course.certificates_estimated_effort
    else:
        c_organization = 'WestEd'
        c.drawImage(imagepath+"/certificate_wested.jpg",0,0, width=841.89,height=595.27,mask=None)
        c_estimated_effort = user_course.certificates_estimated_effort

    c.drawImage(imagepath+"/qianzi.jpg",360,50, width=None,height=None,mask=None)
    #c.drawImage(imagepath+"/pcgeducationdown_logo.jpg",590,75, width=None,height=None,mask=None)

    c.setFillColorRGB(0.5,0.5,0.5)
    c.setFont("Open Sans", 25)
    c.drawString(642,490,"CERTIFICATE")
    c.setFont("OpenSans_i", fontsize_completedtime)
    c.drawString(652,468,c_completed_time)

    c.setFont("Open Sans", fontsize_maincontent)
    c.drawString(50,400,'This is to certify that')

    c.drawString(50,313,'Successfully completed')

    c.drawString(50,230,'a course of study offered by ')
    c.setFont("OpenSans_b", fontsize_maincontent)
    c.drawString(315,230,c_organization)

    if user_course.display_number_with_default == "PEP101x":
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(460,230,', a partner in ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(584,230,'Pepper')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(655,230,', an online')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(50,205,'learning initiative for ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(247,205,'Common Core Specialists')
    else:
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(389,230,', a partner in ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(514,230,'Pepper')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(585,230,', an online learning')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(50,205,'initiative for ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(165,205,'Common Core Specialists')

    c.setFont("Open Sans", fontsize_effort)
    c.drawString(50,50,'Estimated Effort: ' + c_estimated_effort)

    c.setFillColorRGB(0,0.5,0.85)
    if len(c_user_name)<=25:
        fontsize_username = 45
        c.setFont("Nunito", fontsize_username)
        c.drawString(50,348,c_user_name)
    elif len(c_user_name)<=40:
        fontsize_username = 37
        c.setFont("Nunito", fontsize_username)
        c.drawString(50,352,c_user_name)
    else:
        fontsize_username = 24
        c.setFont("Nunito", fontsize_username)
        c.drawString(50,356,c_user_name)
    c.setFont("Nunito", fontsize_coursename)
    c.drawString(50,270,c_course_full_name)

    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
'''
def draw_certificate_default(request, user_course, c_completed_time, buffer, c):
    first_name = request.user.first_name
    last_name = request.user.last_name
    c_course_name = user_course.display_name_with_default
    c_user_name = first_name + ' ' +last_name
    c_organization = ''
    c_estimated_effort = ''
    c_course_full_name = user_course.display_number_with_default + " " + c_course_name #course name
    fontpath = '/home/tahoe/edx_all/edx-platform/lms/static/fonts'
    imagepath = '/home/tahoe/edx_all/edx-platform/lms/static/images/certificate'
    pdfmetrics.registerFont(ttfonts.TTFont('Open Sans',os.path.join(fontpath, 'OpenSans-Regular-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('OpenSans_i',os.path.join(fontpath, 'OpenSans-Italic-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('OpenSans_b',os.path.join(fontpath, 'OpenSans-Bold-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('Nunito',os.path.join(fontpath, 'Nunito-Regular.ttf')))
    fontsize_completedtime = 15
    fontsize_maincontent = 20
    fontsize_username = 45
    fontsize_coursename = 25
    fontsize_effort = 21

    if user_course.display_organization == "PCG Education":
        c_organization = 'PCG Education'
        c.drawImage(imagepath+"/certificate_pcg.jpg",0,0, width=841.89,height=595.27,mask=None)
        c_estimated_effort = user_course.certificates_estimated_effort
    elif user_course.display_organization=='WestEd':
        c_organization = 'WestEd'
        c.drawImage(imagepath+"/certificate_wested.jpg",0,0, width=841.89,height=595.27,mask=None)
        c_estimated_effort = user_course.certificates_estimated_effort
    elif user_course.display_organization=='A.L.L.':
        c_organization = 'Accelerated Literacy Learning'
        c.drawImage(imagepath+"/certificate_A.L.L.jpg",0,0, width=841.89,height=595.27,mask=None)
        c_estimated_effort = user_course.certificates_estimated_effort
    elif user_course.display_organization=='Understanding Language Initiative at Stanford':
        c_organization = 'Understanding Language Initiative at Stanford'
        c.drawImage(imagepath+"/certificate_ULStanford.jpg",0,0, width=841.89,height=595.27,mask=None)
        c_estimated_effort = user_course.certificates_estimated_effort

    c.drawImage(imagepath+"/qianzi.jpg",360,50, width=None,height=None,mask=None)
    #c.drawImage(imagepath+"/pcgeducationdown_logo.jpg",590,75, width=None,height=None,mask=None)

    c.setFillColorRGB(0.5,0.5,0.5)
    c.setFont("Open Sans", 25)
    c.drawString(642,490,"CERTIFICATE")
    c.setFont("OpenSans_i", fontsize_completedtime)
    c.drawString(652,468,c_completed_time)

    c.setFont("Open Sans", fontsize_maincontent)
    c.drawString(50,400,'This is to certify that')

    c.drawString(50,313,'Successfully completed')


    if user_course.display_organization == "PCG Education":
        c.drawString(50,230,'a course of study offered by ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(315,230,c_organization)
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(460,230,', a partner in ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(584,230,'Pepper')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(655,230,', an online')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(50,205,'learning community.')
    elif user_course.display_organization=='WestEd':
        c.drawString(50,230,'a course of study offered by ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(315,230,c_organization)
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(389,230,', a partner in ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(514,230,'Pepper')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(585,230,', an online learning')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(50,205,'initiative for ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(165,205,'Common Core Specialists')
    elif user_course.display_organization=='A.L.L.':
        c.drawString(50,230,'a course of study offered by ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(315,230,c_organization)
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(613,230,', a partner in ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(737,230,'Pepper')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(807,230,',')
        c.drawString(50,205,'an online')
        c.setFont("Open Sans", fontsize_maincontent)
        c.drawString(144,205,'learning community.')
    elif user_course.display_organization=='Understanding Language Initiative at Stanford':
        c.drawString(50,230,'a course which is part of Pepper, an online learning community. Content for this ')
        c.drawString(50,205,'course was created by the ')
        c.setFont("OpenSans_b", fontsize_maincontent)
        c.drawString(302,205,c_organization)
        c.drawString(50,180,"University.")
    c.setFont("Open Sans", fontsize_effort)
    c.drawString(50,50,'Estimated Effort: ' + c_estimated_effort)

    c.setFillColorRGB(0,0.5,0.85)
    if len(c_user_name)<=25:
        fontsize_username = 45
        c.setFont("Nunito", fontsize_username)
        c.drawString(50,348,c_user_name)
    elif len(c_user_name)<=40:
        fontsize_username = 37
        c.setFont("Nunito", fontsize_username)
        c.drawString(50,352,c_user_name)
    else:
        fontsize_username = 24
        c.setFont("Nunito", fontsize_username)
        c.drawString(50,356,c_user_name)
    c.setFont("Nunito", fontsize_coursename)
    c.drawString(50,270,c_course_full_name)

    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def draw_certificate_CT(buffer, c):
    fontpath = '/home/tahoe/edx_all/edx-platform/lms/static/fonts'
    imagepath = '/home/tahoe/edx_all/edx-platform/lms/static/images/certificate'
    pdfmetrics.registerFont(ttfonts.TTFont('Nunito',os.path.join(fontpath, 'Nunito-Regular.ttf')))
    c.drawImage(imagepath+"/blank_certificate.jpg",0,0, width=841.89,height=595.27,mask=None)
    fontsize = 40
    c.setFillColorRGB(0,0.5,0.85)
    c.setFont("Nunito",fontsize )
    c.drawString(50,328,'Thank you for completing this module!')
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
    
# new certificate------------------------------------------------
@ensure_csrf_cookie
@cache_if_anonymous
def certificate_preview(request):
    return render_to_response('certificate_preview.html', {})

def getCertificateBlob(request,organization):
    certificate = Certificate.objects.filter(association_type__name='School',association=request.user.profile.school_id)
    if len(certificate) > 0:
        return certificate[0].certificate_blob
    certificate = Certificate.objects.filter(association_type__name='District',association=request.user.profile.district.id)
    if len(certificate) > 0:
        return certificate[0].certificate_blob
    author = Author.objects.filter(name=organization)
    if len(author) > 0:
        certificate = Certificate.objects.filter(association_type__name='Author',association=author[0].id)
        if len(certificate) > 0:
            return certificate[0].certificate_blob
    return ''


@login_required
@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def download_certificate(request, course_id, completed_time):
    user_id = request.user.id
    user_course = get_course_with_access(user_id, course_id, 'load')
    first_name = request.user.first_name
    last_name = request.user.last_name

    course_name = user_course.display_name_with_default
    # user_name = first_name + ' ' + last_name
    course_full_name = user_course.display_number_with_default + " " + course_name
    estimated_effort = user_course.certificates_estimated_effort
    completed_time = datetime.datetime.strptime(completed_time, '%Y-%m-%d').strftime('%B %d, %Y ')
    blob = urllib.unquote(getCertificateBlob(request, user_course.display_organization).decode('utf8').encode('utf8'))
    output_error = ''
    try:
        blob = blob.format(
            firstname=first_name,
            lastname=last_name,
            coursename=course_name,
            coursenumber=course_full_name,
            date=completed_time,
            hours=estimated_effort)
    except KeyError, e:
        output_error = 'The placeholder {0} does not exist.'.format(str(e))
    # return render_to_response('download_certificate.html', {'content': blob, 'outputError': output_error})

    context_dict = {
        'content': blob,
        'outputError': output_error,
    }

    html = render_to_string('download_certificate.html', context_dict)
    result = StringIO.StringIO()
    pdf = pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")), result, encoding="UTF-8")
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('There was an error when generating your certificate: <pre>%s</pre>' % escape(html))

