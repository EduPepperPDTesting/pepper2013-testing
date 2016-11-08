from django import db
from mail import send_html_mail
from mitxmako.shortcuts import render_to_response
from xmodule.modulestore.django import modulestore
from courseware.courses import (get_courses, get_course_with_access, get_course_by_id,
                                get_courses_by_university, sort_by_announcement, sort_by_custom)
from courseware.access import has_access
from student.models import UserTestGroup, CourseEnrollment, UserProfile, Registration, District, State, School
from django.core.urlresolvers import reverse
from django.conf import settings
import json
from student.models import User, UserProfile
from django.http import HttpResponse, HttpResponseForbidden
from pepper_utilities.utils import random_mark
from xmodule.course_module import CourseDescriptor


def course_list(request):
    email = request.GET.get("email", "")
    try:
        UserProfile.objects.get(user__email=email, subscription_status='Imported')
    except:
        email = ""
    filterDic = {'_id.category': 'course', 'metadata.paypal_purchase_link': {"$ne": "", "$exists": True}}  # {"$nin": ("", None)}
    items = modulestore().collection.find(filterDic)
    courses = modulestore()._load_items(list(items), 0)
    return render_to_response("shopping/course_list.html", {'courses': courses, 'email': email})


def registered_for_course(course, user):
    """
    Return True if user is registered for course, else False
    """
    if user is None:
        return False
    if user.is_authenticated():
        return CourseEnrollment.is_enrolled(user, course.id)
    else:
        return False


def course_info(request, course_id):
    course = get_course_with_access(request.user, course_id, 'see_exists')
    registered = registered_for_course(course, request.user)

    if has_access(request.user, course, 'load'):
        course_target = reverse('info', args=[course.id])
    else:
        course_target = reverse('about_course', args=[course.id])

    show_courseware_link = (has_access(request.user, course, 'load') or
                            settings.MITX_FEATURES.get('ENABLE_LMS_MIGRATION'))

    return render_to_response('shopping/course_info.html',
                              {'course': course,
                               'registered': registered,
                               'course_target': course_target,
                               'show_courseware_link': show_courseware_link})


def valid_discount_code(request):
    discount_code = request.POST.get("discount_code")
    course_id = request.POST.get("course_id")

    try:
        course_loc = CourseDescriptor.id_to_location(course_id)
        course = modulestore().get_instance(course_id, course_loc)
        json_out = {'success': True,
                    'matched': discount_code == course.paypal_discount_code,
                    'discount_link': course.paypal_discount_link}
    except Exception as e:
        json_out = {'success': False, 'message': '%s' % e}

    return HttpResponse(json.dumps(json_out), content_type="application/json")


def enroll_post(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    dist_org = request.POST.get('dist_org')
    dist_org_website = request.POST.get('dist_org_website')
    state_id = int(request.POST.get('state_id'))
    country = request.POST.get('country')

    try:
        user = User.objects.get(email=email)
        json_out = {'success': True, 'user_exists': True}
        return HttpResponse(json.dumps(json_out), content_type="application/json")
    except:
        username = random_mark(20)
        user = User(username=username, email=email, is_active=False)

    try:
        state = State.objects.get(id=state_id)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(username)
        user.save()

        registration = Registration()
        registration.register(user)

        profile = UserProfile(user=user)
        profile.district = District.objects.get(name="Pepper Network " + state.name, state=state)
        profile.school = School.objects.get(name="Member", district=profile.district)
        profile.state_id = state
        profile.subscription_status = "Imported"
        profile.save()

        subject = "PayPal Course Purchase Order (%s)" % user.username
        body = """Username: %s <br>
        First Name: %s <br>
        Last Name: %s <br>
        Email: %s <br>
        Phone Number: %s <br>
        School District/Organization: %s <br>
        School District/Organization Website: %s <br>
        State: %s <br>
        Country: %s
        """ % (username, first_name, last_name, email, phone, dist_org, dist_org_website, state.name, country)

        send_html_mail(subject, body, settings.SUPPORT_EMAIL, ["peppersupport@pcgus.com"])
        
        db.transaction.commit()
        json_out = {'success': True, 'user_exists': False}
    except Exception as e:
        db.transaction.rollback()
        json_out = {'success': False, "message": "%s" % e}

    return HttpResponse(json.dumps(json_out), content_type="application/json")
