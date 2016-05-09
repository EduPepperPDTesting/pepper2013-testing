from student.models import State, District, School, Cohort, User
from .utils import render_json_response


def drop_states(request):
    r = list()
    access_level = request.GET.get('access_level', 'System')
    if access_level:
        if access_level == 'System':
            data = State.objects.all().order_by('name')
        else:
            data = State.objects.filter(id=request.user.profile.district.state.id)
        for item in data:
            r.append({'id': item.id, 'name': item.name})
    return render_json_response(r)


def drop_districts(request):
    r = list()
    access_level = request.GET.get('access_level', 'System')
    if access_level:
        if access_level == 'System':
            state = request.GET.get('state', False)
        else:
            state = request.user.profile.district.state.id

        district = False
        if access_level == 'District' or access_level == 'School':
            district = request.user.profile.district.id

        if district:
            data = District.objects.filter(id=district)
        elif state:
            data = District.objects.filter(state=state).order_by('name')
        else:
            data = District.objects.all().order_by('name')

        for item in data:
            r.append({'id': item.id, 'name': item.name, 'code': item.code})
    return render_json_response(r)


def drop_schools(request):
    r = list()
    access_level = request.GET.get('access_level', 'System')
    if access_level:
        if access_level == 'System' or access_level == 'State':
            district = request.GET.get('district', False)
        else:
            district = request.user.profile.district.id

        school = False
        if access_level == 'School':
            school = request.user.profile.school.id

        if school:
            data = School.objects.filter(id=school)
        elif district:
            data = School.objects.filter(district=district).order_by('name')
        else:
            data = School.objects.all().order_by('name')

        for item in data:
            r.append({'id': item.id, 'name': item.name})
    return render_json_response(r)


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
    return render_json_response(r)


def user_email_completion(request):
    r = list()
    lookup = request.GET.get('q', False)
    if lookup:
        data = User.objects.filter(email__istartswith=lookup)
        for item in data:
            r.append(item.email)
    return render_json_response(r)


def user_email_exists(request):
    exists = False
    lookup = request.GET.get('email', False)
    if lookup:
        exists = User.objects.filter(email=lookup).exists()
    return render_json_response(exists)

