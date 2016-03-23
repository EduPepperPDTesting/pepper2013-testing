from student.models import State, District, School, Cohort, User
from django.http import HttpResponse
import json


def drop_states(request):
    r = list()
    data = State.objects.all().order_by('name')
    for item in data:
        r.append({'id': item.id, 'name': item.name})
    return HttpResponse(json.dumps(r), content_type='application/json')


def drop_districts(request):
    r = list()
    state = request.GET.get('state', False)
    if state:
        data = District.objects.filter(state=state).order_by('name')
    else:
        data = District.objects.all().order_by('name')

    for item in data:
        r.append({'id': item.id, 'name': item.name, 'code': item.code})
    return HttpResponse(json.dumps(r), content_type='application/json')


def drop_schools(request):
    r = list()
    district = request.GET.get('district', False)
    if district:
        data = School.objects.filter(district=district).order_by('name')
    else:
        data = School.objects.all().order_by('name')

    for item in data:
        r.append({'id': item.id, 'name': item.name})
    return HttpResponse(json.dumps(r), content_type='application/json')


def drop_cohorts(request):
    r = list()
    district = request.GET.get('district', False)
    state = request.GET.get('state', False)
    if district:
        data = Cohort.objects.filter(district=district).order_by('code')
    elif state:
        data = Cohort.objects.filter(district__state=state).order_by('code')
    else:
        data = Cohort.objects.all().order_by('code')

    for item in data:
        r.append({'id': item.id, 'code': item.code})
    return HttpResponse(json.dumps(r), content_type='application/json')


def user_email_completion(request):
    r = list()
    lookup = request.GET.get('q', False)
    if lookup:
        data = User.objects.filter(email_icontains=lookup)
        for item in data:
            r.append(item.email)
    return HttpResponse(json.dumps(r), content_type='application/json')
