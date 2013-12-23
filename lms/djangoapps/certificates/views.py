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
from mitxmako.shortcuts import render_to_response
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

def download_certificate(request,course_id,completed_time):
    t_user = request.user.id
    t_course = get_course_with_access(t_user, course_id, 'load')
    t_coursename = t_course.display_name_with_default
    first_name = request.user.profile.first_name
    last_name = request.user.profile.last_name

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
    t_time_fin = datetime.date(t_y,t_m,t_d).strftime("%B %d, %Y ")

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    buffer = BytesIO()
    # Create the PDF object, using the BytesIO object as its "file."
    c = canvas.Canvas(buffer,pagesize=(841.89,595.27))


    fontpath = '/home/tahoe/edx_all/edx-platform/lms/static/fonts'
    imagepath = '/home/tahoe/edx_all/edx-platform/lms/static/images/certificate'
    pdfmetrics.registerFont(ttfonts.TTFont('Open Sans',os.path.join(fontpath, 'OpenSans-Regular-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('OpenSans_i',os.path.join(fontpath, 'OpenSans-Italic-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('OpenSans_b',os.path.join(fontpath, 'OpenSans-Bold-webfont.ttf')))
    pdfmetrics.registerFont(ttfonts.TTFont('Nunito',os.path.join(fontpath, 'Nunito-Regular.ttf')))

    fontsize_completedtime = 15
    fontsize_maincontent = 20
    fontsize_username = 45
    fontsize_coursename = 28
    fontsize_effort = 21

    completed_time = t_time_fin
    user_name = first_name + ' ' +last_name
    course_name = t_coursename
    organization = ''
    estimated_effort = ''

    if t_course.display_number_with_default == "PEP101x":
        organization = 'PCG Education'
        c.drawImage(imagepath+"/zs_bg_pcg.jpg",0,0, width=841.89,height=595.27,mask=None)
        estimated_effort = '1 hours'
    else:
        organization = 'WestEd'
        c.drawImage(imagepath+"/zs_bg.jpg",0,0, width=841.89,height=595.27,mask=None)
        estimated_effort = '15 hours'

    c.drawImage(imagepath+"/qianzi.jpg",360,50, width=None,height=None,mask=None)
    c.drawImage(imagepath+"/pcg_logo_r.jpg",590,75, width=None,height=None,mask=None)

    c.setFillColorRGB(0.5,0.5,0.5)
    c.setFont("OpenSans_i", fontsize_completedtime)
    c.drawString(652,468,completed_time)

    c.setFont("Open Sans", fontsize_maincontent)
    c.drawString(50,400,'This is to certify that')

    c.drawString(50,313,'Successfully completed')

    c.drawString(50,230,'a course of study offered by ')
    c.setFont("OpenSans_b", fontsize_maincontent)
    c.drawString(315,230,organization)

    if t_course.display_number_with_default == "PEP101x":
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
    c.drawString(50,50,'Estimated Effort: ' + estimated_effort)

    c.setFillColorRGB(0,0.5,0.85)
    c.setFont("Nunito", fontsize_username)
    c.drawString(50,348,user_name)
    c.setFont("Nunito", fontsize_coursename)
    c.drawString(50,270,course_name)

    c.showPage()
    c.save()
    
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def course_credits(request):
     return render_to_response('course_credits.html', {})

@ensure_csrf_cookie
@cache_if_anonymous
def download_certificate_demo(request):
     return render_to_response('d_certificate_demo.html', {})
#@end