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
    return render_to_response('d_certificate.html', {'course':t_course,'completed_time': t_time_fin})

@ensure_csrf_cookie
@cache_if_anonymous
def download_certificate_demo(request):
     return render_to_response('d_certificate_demo.html', {})
#@end