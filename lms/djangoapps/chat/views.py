from mitxmako.shortcuts import render_to_response
from courseware.courses import (get_courses, get_course_with_access,
                                get_courses_by_university, sort_by_announcement)

from django.contrib.auth.decorators import login_required

@login_required
def index(request,course_id):
    course=get_course_with_access(request.user, course_id, 'load')
    return render_to_response('chat/people.html', {'course': course})
