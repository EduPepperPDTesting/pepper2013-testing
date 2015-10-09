from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators import csrf
import django_comment_client.utils as utils
from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location
from dashboard.models import *
from models import *
import time
import datetime
import logging
log = logging.getLogger("tracking")


def record_time(request):
    user_id = str(request.POST.get('user_id'))
    rts = recordTimeStore()
    info = request.POST
    if info['type'] == 'course_page':
        rts = recordTimeStore()
        if info['prev_vertical_id'] != '':
            returnInfo = rts.set_item('end_time', info['time'], user_id, info['prev_vertical_id'], info['prev_time'])
            if returnInfo['updatedExisting']:
                setPageTime(rts, info, user_id)
        rts.insert_item({'user_id': user_id, 'vertical_id': info['new_vertical_id'], 'start_time': info['time'], 'location': info['location']})
    else:
        returnInfo = rts.set_item('end_time', info['time'], user_id, info['prev_vertical_id'], info['prev_time'])
        if returnInfo['updatedExisting']:
            setPageTime(rts, info, user_id)
    return utils.JsonResponse({})


def setPageTime(rts, info, user_id):
    item = rts.get_item(user_id, info['prev_vertical_id'], info['prev_time'])
    time_delta = getTimeDelta(item['start_time'], item['end_time'])
    rdata = rts.get_page_item(item['user_id'], item['vertical_id'])
    if rdata is not None:
        rts.set_page_item({'user_id': user_id, 'vertical_id': item['vertical_id'], 'time': time_delta}, rdata)
    else:
        course, chapter, sequ, vertical, position = getCourseInfo(item['location'], item['vertical_id'])
        course_name = course.display_coursenumber + ' ' + course.display_name
        vertical_name = get_vertical_name(sequ, vertical, position)
        sort_key = get_sort_key(vertical_name)
        rts.set_page_item({'user_id': user_id, 'vertical_id': item['vertical_id'], 'time': time_delta, 'location': item['location'],
                          'course_name': course_name, 'vertical_name': vertical_name, 'sort_key': sort_key}, rdata)


def getTimeDelta(start, end):
    format = '%Y-%m-%dT%H:%M:%S.%fZ'
    start_struct = time.strptime(start, format)
    end_struct = time.strptime(end, format)
    start_time = datetime.datetime(*start_struct[:6])
    end_time = datetime.datetime(*end_struct[:6])
    return (end_time - start_time).seconds


def getCourseInfo(location, vertical_id):
    locationList = location.split('/')
    location_head = ['i4x', locationList[0], locationList[1]]
    course = modulestore().get_item(Location(location_head + ['course', locationList[2]]))
    chapter = modulestore().get_item(Location(location_head + ['chapter', locationList[4]]))
    sequ = modulestore().get_item(Location(location_head + ['sequential', locationList[5]]))
    vertical = modulestore().get_item(vertical_id)
    return course, chapter, sequ, vertical, locationList[6]


def get_sequ_num(str):
    l = str.split("\t")
    if len(l) > 1:
        return list[0]
    else:
        l = str.split(" ")
        return l[0]


def get_vertical_name(sequ, vertical, position):
    sequ_num = get_sequ_num(sequ.display_name)
    if sequ_num.find(".") >= 0:
        return sequ_num + '.' + position + ': ' + vertical.display_name
    else:
        return vertical.display_name


def get_sort_key(name):
    num = name.split(":")[0]
    r = 0
    modulus = 1000000
    if num.find(".") >= 0:
        digital_arr = num.split(".")
        for i in range(len(digital_arr)):
            modulus = modulus / 100
            try:
                r += int(digital_arr[i]) * modulus
            except:
                return r
        return r
    else:
        return name


def create_report(request, user_id=None):
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = request.user
    context = {
        'curr_user': user}
    return render_to_response('study_time.html', context)


def get_study_time_range(request):
    rts = recordTimeStore()
    user_id = str(request.user.id)
    count = rts.get_page_total(user_id)
    info = rts.return_page_items(user_id, int(request.POST.get('skip')), int(request.POST.get('limit')))
    return utils.JsonResponse({'results': info, 'count': count})


def get_course_time(request):
    rts = recordTimeStore()
    user_id = str(request.POST.get('user_id'))
    time = rts.get_course_time(user_id, request.POST.get('course_id'), request.POST.get('type'))
    return utils.JsonResponse({'time': time})


def save_course_time(request):
    rts = recordTimeStore()
    user_id = str(request.POST.get('user_id'))
    rts.set_course_time(user_id, request.POST.get('course_id'), request.POST.get('type'), request.POST.get('time'))
    return utils.JsonResponse({})
