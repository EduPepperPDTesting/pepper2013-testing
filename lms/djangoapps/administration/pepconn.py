from django.conf import settings
from django.template import Context
from django.core.urlresolvers import reverse
from django_future.csrf import ensure_csrf_cookie
from mitxmako.shortcuts import render_to_response, render_to_string, marketing_link
from pepper_utilities.utils import render_json_response

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from student.models import User, UserProfile, Registration, CourseEnrollmentAllowed
from pepper_utilities.utils import random_mark
import json
import logging
import csv
import urllib2

# import multiprocessing
from multiprocessing import Process, Queue, Pipe
from django.core.validators import validate_email, validate_slug, ValidationError

from .models import CustomEmail, CustomEmailLog, ImportTask, ImportTaskLog, EmailTask, EmailTaskLog, FilterFavorite

import gevent
from django import db
from django.db import IntegrityError

from StringIO import StringIO
from student.models import Transaction, District, Cohort, School, State
from mail import send_html_mail
from datetime import datetime, timedelta
from pytz import UTC

from mako.template import Template
import mitxmako

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.db.models import F

log = logging.getLogger("tracking")
USER_CSV_COLS = ('email', 'state_name', 'district_name',)
DISTRICT_CSV_COLS = ('id', 'name', 'state')
SCHOOL_CSV_COLS = ('name', 'id', 'state', 'district_id')

# from gevent import monkey


def attstr(obj, attr):
    r = obj
    try:
        for a in attr.split("."):
            r = getattr(r, a)
    except:
        r = ""

    if r is None:
        r = ""
    return r


def render_from_string(template_string, dictionary, context=None, namespace='main'):
    context_instance = Context(dictionary)
    # add dictionary to context_instance
    context_instance.update(dictionary or {})
    # collapse context_instance to a single dictionary for mako
    context_dictionary = {}
    context_instance['settings'] = settings
    context_instance['MITX_ROOT_URL'] = settings.MITX_ROOT_URL
    context_instance['marketing_link'] = marketing_link

    # In various testing contexts, there might not be a current request context.
    if mitxmako.middleware.requestcontext is not None:
        for d in mitxmako.middleware.requestcontext:
            context_dictionary.update(d)
    for d in context_instance:
        context_dictionary.update(d)
    if context:
        context_dictionary.update(context)
    # fetch and render template
    raw_template = Template(template_string)
    return raw_template.render_unicode(**context_dictionary)


def paging(all, size, page):
    try:
        page = int(page)
    except Exception:
        page = 1
    try:
        size = int(size)
    except Exception:
        size = 1
    paginator = Paginator(all, size)
    if page < 1:
        page = 1
    if page > paginator.num_pages:
        page = paginator.num_pages
    data = paginator.page(page)
    return data


def postpone(function):
    def decorator(*args, **kwargs):
        p = Process(target=function, args=args, kwargs=kwargs)
        p.daemon = True
        p.start()
    return decorator


@login_required
@user_passes_test(lambda u: u.is_superuser)
def main(request):
    # from django.contrib.sessions.models import Session
    states = State.objects.all().order_by('name')
    districts = District.objects.all().order_by('name')
    schools = School.objects.all().order_by('name')
    data = {
        'states': list(),
        'districts': list(),
        'schools': list()
    }
    for item in states:
        data['states'].append({'id': item.id, 'name': item.name.replace('"', r'\"')})
    for item in districts:
        data['districts'].append({'id': item.id, 'name': item.name.replace('"', r'\"'), 'parent_id': item.state.id})
    for item in schools:
        data['schools'].append({'id': item.id, 'name': item.name.replace('"', r'\"'), 'parent_id': item.district_id})

    return render_to_response('administration/pepconn.html', data)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cohort_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        if request.POST.get('id'):
            d = Cohort(request.POST['id'])
        else:
            d = Cohort()
        d.code = request.POST['code']
        d.licences = int(request.POST['licences'])
        d.term_months = int(request.POST['term_months'])
        d.start_date = request.POST['start_date']
        d.district_id = int(request.POST['district_id'])
        d.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def build_filters(columns, filters):
    """
    Builds the filters for the PepConn report data
    :param columns: the columns in this table
    :param filters: the filters requested
    :return: the arguments to pass to filter()
    """
    kwargs = dict()
    args = None
    # Iterate through the filters.
    for column, value in filters.iteritems():
        # For the numerical columns, just filter that column by the passed value.
        if not column == 'all':
            c = int(column)
            # If the column is an integer value, convert the search term.
            out_value = value
            if columns[c][2] == 'int' and value.isdigit():
                out_value = int(value)
            # Build the actual kwargs to pass to filer(). in this case, we need the column selector ([0]) as well as the
            # type of selection to make ([1] - '__iexact').
            kwargs[columns[c][0] + columns[c][1]] = out_value
        # If this is a search for all, we need to do an OR search, so we build one with Q objects.
        else:
            args_list = list()
            for key, data in columns.iteritems():
                # [2] holds the column type (int, str, or False to ignore).
                if data[2]:
                    # If the column is an integer value, convert the search term (as long as the string is only digits).
                    out_value = value
                    if data[2] == 'int':
                        if value.isdigit():
                            out_value = int(value)
                        else:
                            out_value = None
                    if out_value is not None:
                        # Create the Q object and add it to the list.
                        args_list.append(Q(**{data[0] + data[1]: out_value}))
            # Start the list with the first object, then add the rest with ORs.
            args = args_list.pop()
            for item in args_list:
                args |= item

    return args, kwargs


def build_sorts(columns, sorts):
    """
    Builds the sorts for the PepConn report data
    :param columns: the columns in this table
    :param sorts: the sorts requested
    :return: the arguments to pass to order_by()
    """
    order = list()
    # Iterate through the passed sorts.
    for column, sort in sorts.iteritems():
        # Default to an ASC search, but if the sort is 1, change it to DESC by adding a -.
        pre = ''
        if bool(int(sort)):
            pre = '-'
        # We just need the column selector out of the columns, not the type.
        order.append(pre + columns[int(column)][0])
    return order


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_user_rows(request):
    """
    Builds the rows for display in the PepConn Users report.
    :param request: User request
    :return: Table rows for the user table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['user_id', '', 'int'],
               1: ['user__last_name', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['school__name', '__iexact', 'str'],
               4: ['district__name', '__iexact', 'str'],
               5: ['cohort__code', '__icontains', 'str'],
               6: ['district__state__name', '__iexact', 'str'],
               7: ['user__email', '__icontains', 'str'],
               8: ['sso_type', '__icontains', 'str'],
               9: ['sso_idp', '__icontains', 'str'],
               10: ['subscription_status', '__iexact', 'str'],
               12: ['user__date_joined', '__icontains', False]}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 12)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        args, kwargs = build_filters(columns, filters)
        # If there was a search for all, add the Q arguments.
        if args:
            users = UserProfile.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            users = UserProfile.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        users = UserProfile.objects.prefetch_related().all().order_by(*order)
    # The number of results is the first value in the return JSON
    count = users.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in users[start:end]:
        row = list()
        row.append(int(item.user.id))
        row.append(str(item.user.last_name))
        row.append(str(item.user.first_name))

        try:
            user_school = item.school.name
        except:
            user_school = ""
        try:
            user_district = str(item.district.name)
            user_district_state = str(item.district.state.name)
        except:
            user_district = ""
            user_district_state = ""
        try:
            user_cohort = str(item.cohort.code)
        except:
            user_cohort = ""

        row.append(str(user_school))
        row.append(str(user_district))
        row.append(str(user_cohort))
        row.append(str(user_district_state))
        row.append(str(item.user.email))
        row.append(str(item.sso_type))
        row.append(str(item.sso_idp))
        row.append(str(item.subscription_status))
        try:
            activation_key = str(Registration.objects.get(user_id=item.user_id).activation_key)
        except:
            activation_key = ''
        row.append('<a href="/register/' + activation_key + '" target="_blank">Activation Link</a>')
        row.append(str(item.user.date_joined))
        row.append('<input class="user_select_box" type="checkbox" name="id" value="' + str(item.user.id) + '"/><img onclick = "editUserData('+str(item.id)+')" id = "editUser" data-id = "'+str(item.id)+'" src="/static/images/pencil_edit.png" class = "edit_icon"></td>')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_school_rows(request):
    """
    Builds the rows for display in the PepConn Schools report.
    :param request: User request
    :return: Table rows for the user table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['code', '__icontains', 'str'],
               1: ['name', '__icontains', 'str'],
               2: ['district__name', '__iexact', 'str'],
               3: ['district__code', '__icontains', 'str'],
               4: ['district__state__name', '__iexact', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 5)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        # If there was a search for all, add the Q arguments.
        args, kwargs = build_filters(columns, filters)
        if args:
            schools = School.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            schools = School.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        schools = School.objects.prefetch_related().all().order_by(*order)
    # The number of results is the first value in the return JSON
    count = schools.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in schools[start:end]:
        row = list()
        row.append(str(item.code))
        row.append(str(item.name))
        try:
            district_state = item.district.state.name
        except:
            district_state = ""
        try:
            district_name = item.district.name
        except:
            district_name = ""
        try:
            district_id = item.district.code
        except:
            district_id = ""
        row.append(str(district_name))
        row.append(str(district_id))
        row.append(str(district_state))
        row.append('<input type="checkbox" name="id" class="school_select_box" value="' + str(item.id) + '"/><img onclick = "editSchoolsData('+str(item.id)+')" id = "editSchool" data-id = "'+str(item.id)+'" src="/static/images/pencil_edit.png" class = "edit_icon">')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_district_rows(request):
    """
    Builds the rows for display in the PepConn Districts report.
    :param request: User request
    :return: Table rows for the user table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['code', '__icontains', 'str'],
               1: ['name', '__icontains', 'str'],
               2: ['state__name', '__iexact', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 3)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        # If there was a search for all, add the Q arguments.
        args, kwargs = build_filters(columns, filters)
        if args:
            districts = District.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            districts = District.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        districts = District.objects.prefetch_related().all().order_by(*order)
    # The number of results is the first value in the return JSON
    count = districts.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in districts[start:end]:
        row = list()
        row.append(str(item.code))
        row.append(str(item.name))
        row.append(str(item.state.name))
        row.append('<input type="checkbox" name="id" class="district_select_box" value="' + str(item.id) + '"/><img onclick="editDistrictsInfo('+str(item.id)+')" id = "editDistrict" data-id = "'+str(item.id)+'" src="/static/images/pencil_edit.png" class = "edit_icon">')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")


def district_get_info(request):
    district = request.POST.get('id')
    row = District.objects.get(id=district)
    code = row.code
    name = row.name
    j = json.dumps({'code': code, 'name': name})
    return HttpResponse(j, content_type="application/json")


def school_get_info(request):
    school_id = request.POST.get('id')
    school = School.objects.prefetch_related().get(id=school_id)
    code = "<h2>Edit School Form</h2>Code:<input type = 'text' id = 'schoolCodeValue' value = '"+str(school.code)+"'></input><br><br>"
    code += "Name:<input type = 'text' id = 'schoolNameValue' value = '"+str(school.name)+"'></input><br><br>"
    state = school.district.state
    code += "District:<select type = 'search' id = 'schoolDistrictValue'>"
    for item in District.objects.filter(state_id=state):
        code += "<option value = '"+str(item.id)+"'>"+str(item.name)+"</option>"
    code += "</select><br><br>"
    code += "<button data-id = '"+str(school.id)+"' onclick = 'submitSchoolEdit()' type = 'submit' id = 'submitSchoolEditButton'>Submit</button>"
    code += "<p id = 'schoolEditMessage'></p>"
    j = json.dumps({'code':code})
    return HttpResponse(j, content_type="application/json")


def cohort_get_info(request):
    cohort_id = request.POST.get('id')
    cohort = Cohort.objects.prefetch_related().get(id=cohort_id)
    code = "<h2>Edit Cohort Form</h2>Code:<input type = 'text' id = 'cohortCodeValue' value = '"+str(cohort.code)+"'></input><br><br>"
    code += "Licences:<input type = 'text' id = 'cohortLicenceValue' value = '"+str(cohort.licences)+"'></input><br><br>"
    code += "Term Months:<input type = 'text' id = 'cohortTermValue' value = '"+str(cohort.term_months)+"'></input><br><br>"
    code += "District:<select type = 'search' id = 'cohortDistrictValue'>"
    try:
        state=cohort.district.state
        for item in District.objects.filter(state_id=state):
            code += "<option value = '"+str(item.id)+"'>"+str(item.name)+"</option>"
        code += "</select><br><br>"
    except:
        for item in District.objects.all():
            code += "<option value = '"+str(item.id)+"'>"+str(item.name)+"</option>"
        code += "</select><br><br>"
    code += "<button data-id = '"+str(cohort.id)+"' onclick = 'submitCohortEdit()' type = 'submit' id = 'submitCohortEditButton'>Submit</button>"
    code += "<p id = 'cohortEditMessage'></p>"
    j = json.dumps({'code':code})
    return HttpResponse(j, content_type="application/json")


def user_get_info(request):
    user_id = request.POST.get('id')
    profile = UserProfile.objects.prefetch_related().get(id=user_id)
    code = "<h2>Edit User Form</h2>First Name:<input type = 'text' id = 'userFirstValue' value = '"+str(profile.user.first_name)+"'></input><br><br>"
    code += "Last Name:<input type = 'text' id = 'userLastValue' value = '"+str(profile.user.last_name)+"'></input><br><br>"
    try:
        state = profile.district.state
        code += "District:<select type = 'search' id = 'userDistrictValue'><option value = ''></option>"
        for item in District.objects.filter(state_id=state.id):
            try:
                if profile.district == item:
                    code += "<option value = '"+str(item.id)+"' selected>"+str(item.name)+"</option>"
                else:
                    code += "<option value = '"+str(item.id)+"'>"+str(item.name)+"</option>"
            except:
                code += "<option value = '"+str(item.id)+"'>"+str(item.name)+"</option>"
        code += "</select><br><br>"
        code += "Cohort:<select type = 'search' id = 'userCohortValue'><option value = ''></option>"

        for item in Cohort.objects.all():
            try:
                if profile.cohort == item:
                    code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"' selected>"+str(item.code)+"</option>"
                else:
                    code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"'>"+str(item.code)+"</option>"
            except Exception as ex:
                    try:
                        code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"'>"+str(item.code)+"</option>"
                    except:
                        code += "<option value = '"+str(item.id)+"' data-district='-1'>"+str(item.code)+"</option>"

        code += "</select><br><br>TEST"
        code += "School:<select type = 'search' id = 'userSchoolValue'><option value = ''></option>"
        for item in School.objects.filter(district__state_id=state):
            try:
                if profile.school_id == item.id:
                    code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"' selected>"+str(item.name)+"</option>"
                else:
                    code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"' >"+str(item.name)+"</option>"
            except:
                code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"'>"+str(item.name)+"</option>"
        code += "</select><br><br>"
    except:
        code += "District:<select type = 'search' id = 'userDistrictValue'><option value = ''></option>"
        for item in District.objects.all():
            code += "<option value = '"+str(item.id)+"'>"+str(item.name)+"</option>"
        code += "</select><br><br>"
        code += "School:<select type = 'search' id = 'userSchoolValue'><option value = ''></option>"
        for item in School.objects.all():
            code += "<option value = '"+str(item.id)+"' data-district='"+str(item.district.id)+"'>"+str(item.name)+"</option>"
        code += "</select><br><br>"
    code += "<button data-id = '"+str(profile.id)+"' onclick = 'submitUserEdit()' type = 'submit' id = 'submitUserEditButton'>Submit</button>"
    code += "<p id = 'userEditMessage'></p>"
    j = json.dumps({'code':code})
    return HttpResponse(j, content_type="application/json")


def user_edit_info(request):
    user_id = request.POST.get('id')
    profile = UserProfile.objects.prefetch_related().get(id=user_id)
    profile.user.first_name = request.POST.get('first')
    profile.user.last_name = request.POST.get('last')
    profile.district_id = request.POST.get('district')
    profile.cohort_id = request.POST.get('cohort')
    profile.school_id = request.POST.get('school')
    profile.user.save()
    profile.save()
    j = json.dumps({'success': 'true', 'error':'none', 'data':'hello, here is the name '+str(profile.user.first_name)})
    return HttpResponse(j, content_type="application/json")


def cohort_edit_info(request):
    cohort_id = request.POST.get('id')
    cohort = Cohort.objects.get(id=cohort_id)
    cohort.code = request.POST.get('code')
    cohort.licences = request.POST.get('licences')
    cohort.term_months=request.POST.get('term')
    cohort.district_id=request.POST.get('district')
    cohort.save()
    j = json.dumps({'success': 'true', 'error':'none'})
    return HttpResponse(j, content_type="application/json")


def school_edit_info(request):
    school_id = request.POST.get('id')
    row = School.objects.prefetch_related().get(id=school_id)
    row.code = request.POST.get('code')
    row.name = request.POST.get('name')
    row.district_id = request.POST.get('district')
    row.save()
    j = json.dumps({'success': 'true', 'error':'none'})
    return HttpResponse(j, content_type="application/json")


def district_edit_info(request):
    district = request.POST.get('id')
    row = District.objects.get(id=district)
    row.code = request.POST.get('code')
    row.name = request.POST.get('name')
    row.save()
    j = json.dumps({'success': 'true', 'error':'none'})
    return HttpResponse(j, content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_cohort_rows(request):
    """
    Builds the rows for display in the PepConn Cohorts report.
    :param request: User request
    :return: Table rows for the user table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['code', '__icontains', 'str'],
               1: ['licenses', '', 'int'],
               2: ['term_months', '', 'int'],
               3: ['start_date', '__icontains', False],
               4: ['district__name', '__iexact', 'str'],
               5: ['district__code', '__iexact', 'str'],
               6: ['district__state__name', '__iexact', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 7)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        # If there was a search for all, add the Q arguments.
        args, kwargs = build_filters(columns, filters)
        if args:
            cohorts = Cohort.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            cohorts = Cohort.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        cohorts = Cohort.objects.prefetch_related().all().order_by(*order)
    # The number of results is the first value in the return JSON
    count = cohorts.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in cohorts[start:end]:
        row = list()
        row.append(str(item.code))
        row.append(str(item.licences))
        row.append(str(item.term_months))
        row.append(str('{d:%Y-%m-%d}'.format(d=item.start_date)))
        try:
            district_name = item.district.name
        except:
            district_name = ""
        try:
            district_code = item.district.code
        except:
            district_code = ""
        try:
            district_state = item.district.state.name
        except:
            district_state = ""
        row.append(str(district_name))
        row.append(str(district_code))
        row.append(str(district_state))
        row.append('<input type="checkbox" name="id" class="cohort_select_box" value="' + str(item.id) + '"/><img onclick = "editCohortData('+str(item.id)+')" id = "editCohort" data-id = "'+str(item.id)+'" src="/static/images/pencil_edit.png" class = "edit_icon">')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")


###############################################
#            District Data Import             #
###############################################

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_district_submit(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        r = csv.reader(file, dialect=csv.excel)
        r1 = []
        r1.extend(r)

        task = ImportTask()
        task.filename = file.name
        task.total_lines = len(r1)
        task.user = request.user
        task.save()
        db.transaction.commit()

        from django.db import connection
        connection.close()

        do_import_district(task, r1, request)

        return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")


def import_district_progress(request):
    try:
        task = ImportTask.objects.get(id=request.POST.get('taskId'))
        j = json.dumps({'task': task.filename, 'percent': '%.2f' % (task.process_lines*100/task.total_lines)})
    except Exception as e:
        j = json.dumps({'task': 'no', 'percent': 100})
    return HttpResponse(j, content_type="application/json")


def validate_district_cvs_line(line):
    # check field count
    n = 0
    for item in line:
        if len(item.strip()):
            n += 1
    if n != len(DISTRICT_CSV_COLS):
        raise Exception("Wrong column count %s" % n)

    name = line[DISTRICT_CSV_COLS.index('name')]
    code = line[DISTRICT_CSV_COLS.index('id')]

    if len(District.objects.filter(name=name, code=code)) > 0:
        raise Exception("A district named '{name}' already exists".format(name=name))


@postpone
def do_import_district(task, csv_lines, request):
    gevent.sleep(0)

    count_success = 0

    for i, line in enumerate(csv_lines):
        tasklog = ImportTaskLog()
        tasklog.create_date = datetime.now(UTC)
        tasklog.line = i + 1
        tasklog.task = task
        tasklog.import_data = line
        try:
            task.process_lines = i + 1

            id = line[DISTRICT_CSV_COLS.index('id')]
            name = line[DISTRICT_CSV_COLS.index('name')]
            state_name = line[DISTRICT_CSV_COLS.index('state')]

            validate_district_cvs_line(line)

            state = State.objects.get(name=state_name).id

            district = District()
            district.code = id
            district.name = name
            district.state_id = state
            district.save()

            tasklog.error = 'ok'
        except Exception as e:
            db.transaction.rollback()
            tasklog.error = "%s" % e
            log.debug("import error: %s" %e)
        finally:
            count_success += 1
            task.success_lines = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            tasklog.save()
            db.transaction.commit()

    email_results(task, request.user.email)


def import_district_tasks(request):
    tasks = []
    timeout = datetime.now(UTC) - timedelta(minute=5)
    for t in ImportTask.objects.filter(Q(task_read__exact=0) & Q(user__exact=request.user)).order_by("-id"):
        task = {"type": "import", "id": t.id, "filename": t.filename, "progress": t.process_lines*100/t.total_lines, "error": False}
        if t.update_time <= timeout and t.process_lines < t.total_lines:
            task['error'] = True
        tasks.append(task)

    for t in EmailTask.objects.filter(Q(task_read__exact=0) & Q(user__exact=request.user)).order_by("-id"):
        task = {"type": "email", "id": t.id, "total": t.total_emails, "progress": t.process_emails*100/t.total_emails, "error": False}
        if t.update_time <= timeout and t.process_emails < t.total_emails:
            task['error'] = True
        tasks.append(task)

    return HttpResponse(json.dumps({'success': True, 'tasks': tasks}), content_type="application/json")


def single_district_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        #state = State.objects.get(name=request.POST['state']).id
        district = District()
        district.code = request.POST['id']
        district.name = request.POST['name']
        district.state_id = request.POST['state']
        district.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


##############################################
#             School Data Import             #
##############################################

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_school_submit(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        r = csv.reader(file, dialect=csv.excel)
        r1 = []
        r1.extend(r)

        task = ImportTask()
        task.filename = file.name
        task.total_lines = len(r1)
        task.user = request.user
        task.save()
        db.transaction.commit()

        from django.db import connection
        connection.close()

        do_import_school(task, r1, request)

        return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")


def import_school_progress(request):
    try:
        task = ImportTask.objects.get(id=request.POST.get('taskId'))
        j = json.dumps({'task': task.filename, 'percent': '%.2f' % (task.process_lines*100/task.total_lines)})
    except Exception as e:
        j = json.dumps({'task': 'no', 'percent': 100})
    return HttpResponse(j, content_type="application/json")


def validate_school_cvs_line(line, district):
    name = line[SCHOOL_CSV_COLS.index('name')]
    id = line[SCHOOL_CSV_COLS.index('id')]
    n = 0
    for item in line:
        if len(item.strip()):
            n += 1
    if n != len(SCHOOL_CSV_COLS):
        raise Exception("Wrong column count")
    if len(School.objects.filter(name=name, district=district)) > 0:
        raise Exception("A school named '{name}' already exists in the district".format(name=name))
    if len(School.objects.filter(code=id)) > 0:
        raise Exception("A school with code '{code}' already exists.")


@postpone
def do_import_school(task, csv_lines, request):
    gevent.sleep(0)

    count_success = 0

    for i, line in enumerate(csv_lines):
        tasklog = ImportTaskLog()
        tasklog.create_date = datetime.now(UTC)
        tasklog.line = i + 1
        tasklog.task = task
        tasklog.import_data = line

        try:
            task.process_lines = i + 1

            name = line[SCHOOL_CSV_COLS.index('name')]
            id = line[SCHOOL_CSV_COLS.index('id')]
            state = line[SCHOOL_CSV_COLS.index('state')]
            district_id = line[SCHOOL_CSV_COLS.index('district_id')]
            district_object = District.objects.get(code=district_id)

            validate_school_cvs_line(line, district_object)

            school = School()
            school.name = name
            school.code = id
            school.district = district_object
            school.save()

            tasklog.error = 'ok'
        except Exception as e:
            db.transaction.rollback()
            tasklog.error = "%s" % e
            log.debug("import error: %s" %e)
        finally:
            count_success += 1
            task.success_lines = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            tasklog.save()
            db.transaction.commit()

    email_results(task, request.user.email)


def import_school_tasks(request):
    tasks = []
    timeout = datetime.now(UTC) - timedelta(minute=5)
    for t in ImportTask.objects.filter(Q(task_read__exact=0) & Q(user__exact=request.user)).order_by("-id"):
        task = {"type": "import", "id": t.id, "filename": t.filename, "progress": t.process_lines*100/t.total_lines, "error": False}
        if t.update_time <= timeout and t.process_lines < t.total_lines:
            task['error'] = True
        tasks.append(task)

    for t in EmailTask.objects.filter(Q(task_read__exact=0) & Q(user__exact=request.user)).order_by("-id"):
        task = {"type": "email", "id": t.id, "total": t.total_emails, "progress": t.process_emails*100/t.total_emails, "error": False}
        if t.update_time <= timeout and t.process_emails < t.total_emails:
            task['error'] = True
        tasks.append(task)

    return HttpResponse(json.dumps({'success': True, 'tasks': tasks}), content_type="application/json")


def single_school_submit(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        if len(School.objects.filter(name=request.POST['name'], district__id=request.POST['district_id'])) > 0:
            raise Exception("A school named '{name}' already exists in the district".format(name=name))
        if len(School.objects.filter(code=request.POST['id'])) > 0:
            raise Exception("A school with code '{request.POST[\'id\']}' already exists.")
        school = School()
        school.name = request.POST['name']
        school.code = request.POST['id']
        district_id = request.POST['district_id']
        district_object = District.objects.get(id=district_id)
        school.district = district_object
        school.save()
    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


#* -------------- User Data Import -------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_user_submit(request):
    # monkey.patch_all(socket=False)
    
    if request.method == 'POST':
        # district_id=request.POST.get("district")
        # school_id=request.POST.get("school")

        # output_pipe,input_pipe=multiprocessing.Pipe()
        # request.session['task']=''

        #** readlines from csv
        #output = StringIO(newline=None)
        file = request.FILES.get('file')
        #output.write(unicode(file.read()))
        #r = csv.reader(output.getvalue(), dialect=csv.excel)
        r = csv.reader(file, dialect=csv.excel)
        rl = []
        rl.extend(r)

        #** create task
        task = ImportTask()
        task.filename = file.name
        task.total_lines = len(rl)
        task.user = request.user
        task.save()
        db.transaction.commit()

        #** close connection before import
        # http://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
        from django.db import connection 
        connection.close()

        #** begin import
        do_import_user(task, rl, request)
        
        return HttpResponse(json.dumps({'success': True, 'taskId': task.id}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")


def import_user_progress(request):
    try:
        task = ImportTask.objects.get(id=request.POST.get('taskId'))
        j = json.dumps({'task': task.filename, 'percent': '%.2f' % (task.process_lines*100/task.total_lines)})
    except Exception as e:
        j = json.dumps({'task': 'no', 'percent': 100})
    return HttpResponse(j, content_type="application/json")


@postpone
def do_import_user(task, csv_lines, request):
    gevent.sleep(0)

    # district_id=request.POST.get("district")
    # school_id=request.POST.get("school")

    #** import into district
    # district=District.objects.get(id=district_id)
    
    send_registration_email = request.POST.get('send_registration_email') == 'true'

    #** ==================== importing
    count_success = 0
    
    for i, line in enumerate(csv_lines):
        tasklog = ImportTaskLog()
        tasklog.create_date = datetime.now(UTC)
        tasklog.line = i + 1
        tasklog.task = task
        tasklog.import_data = line
        try:
            #** record processed count
            task.process_lines = i + 1

            email = line[USER_CSV_COLS.index('email')]
            state_name = line[USER_CSV_COLS.index('state_name')]
            district_name = line[USER_CSV_COLS.index('district_name')]
            
            #** generating origin username
            username = random_mark(20)

            #** create log
            tasklog.username = username
            tasklog.error = "ok"
              
            validate_user_cvs_line(line)

            state = State.objects.get(name=state_name)
            district = District.objects.get(state=state, name=district_name)

            #** user
            user = User(username=username, email=email, is_active=False)
            user.set_password(username)
            user.save()

            #** registration
            registration = Registration()
            registration.register(user)

            #** profile
            profile = UserProfile(user=user)
            profile.district = district
            profile.subscription_status = "Imported"

            #** course enroll
            if district.code == "3968593":
                cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='Edu2000/EDU101/2014_EDU_Jan', email=email)
            else:
                cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG_Education/PEP101.1/S2016', email=email)
            cea.is_active = True
            cea.auto_enroll = True
            cea.save()

            #** send activation email if required
            if send_registration_email:
                try:
                    profile.subscription_status = "Unregistered"
                    reg = Registration.objects.get(user=user)
                    props = {'key': reg.activation_key, 'district': district.name, 'email': email}

                    use_custom = request.POST.get("customize_email")
                    if use_custom == 'true':
                        custom_email = request.POST.get("custom_email_001")
                        custom_email_subject = request.POST.get("custom_email_subject")
                        subject = render_from_string(custom_email_subject, props)
                        body = render_from_string(custom_email, props)
                    else:
                        subject = render_to_string('emails/activation_email_subject.txt', props)
                        body = render_to_string('emails/activation_email.txt', props)

                    subject = ''.join(subject.splitlines())
                    send_html_mail(subject, body, settings.SUPPORT_EMAIL, [email])


                except Exception as e:
                    raise Exception("Failed to send registration email %s" % e)

            # Save the profile after we know everything has been set correctly.
            profile.save()

        except Exception as e:
            db.transaction.rollback()
            tasklog.error = "%s" % e
            log.debug("import error: %s" % e)

        finally:
            count_success += 1
            task.success_lines = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            tasklog.save()
            db.transaction.commit()

    email_results(task, request.user.email)


def email_results(task, email):
    tasklogs = ImportTaskLog.objects.filter(task=task).exclude(error='ok')
    if len(tasklogs):
        FIELDS = ["line", "username", "import_data", "create_date", "error"]
        TITLES = ["Line", "Username", "Import Data", "Create Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row = {"line": d.line,
                   "username": d.username,
                   "import_data": d.import_data,
                   "create_date": d.create_date,
                   "error": d.error
                   }
            writer.writerow(row)
        output.seek(0)
        attach = [{'filename': 'log.csv', 'mimetype': 'text/csv', 'data': output.read()}]
        send_html_mail("User Data Import Report",
                       "Report of importing %s, see attachment." % task.filename,

                       settings.SUPPORT_EMAIL, [email], attach)
        output.close()


def validate_user_cvs_line(line):
    #** check field count
    n = 0
    for item in line:
        if len(item.strip()):
            n += 1
    if n != len(USER_CSV_COLS):
        raise Exception("Wrong fields count")

    #** email
    email = line[USER_CSV_COLS.index('email')]
    validate_email(email)

    #** check user exists
    if len(User.objects.filter(email=email)) > 0:
        raise Exception("An account with the Email '{email}' already exists".format(email=email))


def import_user_tasks(request):
    tasks = []
    timeout = datetime.now(UTC) - timedelta(minutes=5)
    for t in ImportTask.objects.filter(Q(task_read__exact=0) & Q(user__exact=request.user)).order_by("-id"):
        task = {"type": "import", "id": t.id, "filename": t.filename, "progress": t.process_lines*100/t.total_lines, "error": False}
        if t.update_time <= timeout and t.process_lines < t.total_lines:
            task['error'] = True
        tasks.append(task)

    for t in EmailTask.objects.filter(Q(task_read__exact=0) & Q(user__exact=request.user)).order_by("-id"):
        task = {"type": "email", "id": t.id, "total": t.total_emails, "progress": t.process_emails*100/t.total_emails, "error": False}
        if t.update_time <= timeout and t.process_emails < t.total_emails:
            task['error'] = True
        tasks.append(task)
     
    return HttpResponse(json.dumps({'success': True, 'tasks': tasks}), content_type="application/json")


def single_user_submit(request):

    send_registration_email = request.POST.get('send_registration_email') == 'true'
    message = "Message Begin: Email? " + str(send_registration_email)
    if not request.user.is_authenticated:
        raise Http404
    try:
        email = request.POST['email']
        district_id = request.POST['district']
        username = random_mark(20)
        user = User(username=username, email=email, is_active=False)
        user.set_password(username)
        user.save()

        district = District.objects.get(id=district_id)

        message += "  email? "+email+"   district? "+str(district)

        #** registration
        registration = Registration()
        registration.register(user)

        #** profile
        profile = UserProfile(user=user)
        profile.district = district
        profile.subscription_status = "Imported"

        #** course enroll
        if district.code == "3968593":
            cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='Edu2000/EDU101/2014_EDU_Jan', email=email)
        else:
            cea, _ = CourseEnrollmentAllowed.objects.get_or_create(course_id='PCG_Education/PEP101.1/S2016', email=email)
        cea.is_active = True
        cea.auto_enroll = True
        cea.save()

        #** send activation email if required
        if send_registration_email:
            try:
                profile.subscription_status = "Unregistered"
                reg = Registration.objects.get(user=user)
                props = {'key': reg.activation_key, 'district': district.name, 'email': email}

                use_custom = request.POST.get("customize_email")
                if use_custom == 'true':
                    custom_email = request.POST.get("custom_email_003")
                    custom_email_subject = request.POST.get("custom_email_subject")
                    subject = render_from_string(custom_email_subject, props)
                    body = render_from_string(custom_email, props)
                else:
                    subject = render_to_string('emails/activation_email_subject.txt', props)
                    body = render_to_string('emails/activation_email.txt', props)

                subject = ''.join(subject.splitlines())
                send_html_mail(subject, body, settings.SUPPORT_EMAIL, [email])


            except Exception as e:
                raise Exception("Failed to send registration email %s" % e)

        # Save profile now that we have everything set.
        profile.save()

    except Exception as e:
        db.transaction.rollback()
        return HttpResponse(json.dumps({'success': False, 'error': '%s' % e, "message": message}),
                            content_type="application/json")

    return HttpResponse(json.dumps({'success': True, "message": message}), content_type="application/json")


def task_close(request):
    try:
        type = request.POST.get('taskType')
        if type == 'import':
            task = ImportTask.objects.get(id=request.POST.get('taskId'))
        elif type == 'email':
            task = EmailTask.objects.get(id=request.POST.get('taskId'))
        else:
            raise Exception("Bad Input")
        task.task_read = 1
        task.save()
        db.transaction.commit()
        j = json.dumps({"success": True})
    except Exception as e:
        j = json.dumps({"success": False})

    return HttpResponse(j, content_type="application/json")


def add_to_sso(request):
    try:
        change = UserProfile.objects.get(user_id=int(request.POST.get('id')))
        change.sso_idp = str(request.POST.get('sso'))
        change.sso_type = str(request.POST.get('ssotype'))
        change.save()
        message = "success"
    except Exception as e:
        db.transaction.rollback()
        message = "Error: " + str(e)

    j = json.dumps({"message": message})
    return HttpResponse(j, content_type="application/json")


def add_to_cohort(request):
    try:
        change = UserProfile.objects.get(user_id=int(request.POST.get('id')))
        change.cohort_id = int(request.POST.get('cohort'))
        change.save()
        message = "success"
    except Exception as e:
        db.transaction.rollback()
        message = "Error: " + e

    j = json.dumps({"message": message})
    return HttpResponse(j, content_type="application/json")


def remove_from_cohort(request):
    message = {'success': True}
    id = request.POST.get("id")
    try:
        user = UserProfile.objects.get(user_id=id)
        user.cohort_id = 0
        user.save()
    except Exception as e:
        db.transaction.rollback()
        message = e
    j = json.dumps({"message": message})
    return HttpResponse(j, content_type="application/json")


#* -------------- Dropdown List -------------

def drop_states(request):
    r = list()
    data = State.objects.all()
    data = data.order_by("name")
    for item in data:
        r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_districts(request):
    r = list()
    if request.GET.get('state'):
        data = District.objects.all()
        data = data.filter(state=request.GET.get('state'))
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_schools(request):
    r = list()
    if request.GET.get('district'):
        data = School.objects.all()
        data = data.filter(district=request.GET.get('district'))
        data = data.order_by("name")
        for item in data:
            r.append({"id": item.id, "name": item.name})
    return HttpResponse(json.dumps(r), content_type="application/json")


def drop_cohorts(request):
    data = Cohort.objects.all()
    if request.GET.get('district'):
        data = data.filter(district=request.GET.get('district'))
    elif request.GET.get('state'):
        data = data.filter(district__state=request.GET.get('state'))
    r = list()
    for item in data:
        r.append({"id": item.id, "code": item.code})
    return HttpResponse(json.dumps(r), content_type="application/json")


def registration_table(request):
    data = UserProfile.objects.all().select_related('User')

    data = UserProfile.objects.all()
    data = registration_filter_user(request.GET, data)

    if request.GET.get('sortField', None):
        if request.GET.get('sortOrder') == 'desc':
            data = data.order_by("-" + request.GET.get('sortField'))
        else:
            data = data.order_by(request.GET.get('sortField'))
    
    page = request.GET.get('page')
    size = request.GET.get('size')
    data = paging(data, size, page)

    rows = []
    pagingInfo = {'page': data.number, 'pages': data.paginator.num_pages, 'total': data.paginator.count}

    for p in data:
        date = p.activate_date.strftime('%b-%d-%y %H:%M:%S') if p.activate_date else ''
        
        rows.append({'id': p.user.id,
                     'user__email': p.user.email,
                     'user__first_name': p.user.first_name,
                     'user__last_name': p.user.last_name,
                     'district': p.district.name if p.district_id else '',
                     'activate_date': date,
                     "subscription_status": p.subscription_status
                     })

    return HttpResponse(json.dumps({'rows': rows, 'paging': pagingInfo}), content_type="application/json")


#* -------------- Favorite Filter -------------

@login_required
@user_passes_test(lambda u: u.is_superuser)    
def favorite_filter_load(request):
    favs = []
    
    # favs=[{'id':1,'name':'Alabama','filter':{'state':1,'district':34,'school':1406}}]

    for ff in FilterFavorite.objects.filter(user=request.user).order_by('name'):
        favs.append({'id': ff.id,
                     'name': ff.name,
                     'filter': ff.filter_json
                     })
    
    return HttpResponse(json.dumps(favs), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def favorite_filter_save(request):
    name = request.GET.get('name')
    FilterFavorite.objects.filter(name=name).delete()
    ff = FilterFavorite()
    ff.user = request.user
    ff.name = name
    ff.filter_json = request.GET.get('filter')
    ff.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def favorite_filter_delete(request):
    FilterFavorite.objects.filter(id=request.GET.get('id')).delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


#* -------------- Registration -------------

def registration_filter_user(vars, data):
    if vars.get('state', None):
        data = data.filter(Q(district__state_id=vars.get('state')))
    if vars.get('district', None):
        data = data.filter(Q(district_id=vars.get('district')))
    if vars.get('school', None):
        data = data.filter(Q(school_id=vars.get('school')))
    return data


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration_send_email(request):
    message = ""
    message = str(request.POST.get('ids'))
    ids=[]
    if request.POST.get('ids'):
        message = request.POST.get("sending custom")
        ids = [int(s) for s in request.POST.get('ids').split(',') if s.isdigit()]
    else:
        data = UserProfile.objects.all()
        data = registration_filter_user(request.POST, data)
        ids = data.values_list('user_id', flat=True)

    task = EmailTask()
    task.total_emails = len(ids)
    task.user = request.user
    task.save()
    
    do_send_registration_email(task, ids, request)
    return HttpResponse(json.dumps({'success': True, 'taskId': task.id, 'message': message}), content_type="application/json")


@postpone
def do_send_registration_email(task, user_ids, request):
    gevent.sleep(0)

    count_success = 0
    for i, user_id in enumerate(user_ids):
        #** create log
        tasklog = EmailTaskLog()
        tasklog.task = task
        tasklog.send_date = datetime.now(UTC)
        tasklog.username = ''
        tasklog.email = ''
        tasklog.district_name = ''
        try:
            user = User.objects.get(id=user_id)
            profile = UserProfile.objects.get(user=user)
            profile.subscription_status = 'Unregistered'

            #** record processed count
            task.process_emails = i + 1

            tasklog.username = user.username
            tasklog.email = user.email
            tasklog.district_name = user.profile.district.name
            tasklog.error = "ok"
            
            reg = Registration.objects.get(user=user)

            props = {'key': reg.activation_key, 'district': user.profile.district.name, 'email': user.email}

            use_custom = request.POST.get("customize_email")
            if use_custom == 'true':
                custom_email = request.POST.get("custom_email_002")
                custom_email_subject = request.POST.get("custom_email_subject")
                subject = render_from_string(custom_email_subject, props)
                body = render_from_string(custom_email, props)
            else:
                subject = render_to_string('emails/activation_email_subject.txt', props)
                body = render_to_string('emails/activation_email.txt', props)
            
            subject = ''.join(subject.splitlines())

            send_html_mail(subject, body, settings.SUPPORT_EMAIL, [user.email])

        except Exception as e:
            db.transaction.rollback()
            tasklog.error = "%s" % e
        finally:
            count_success += 1
            task.success_emails = count_success
            task.update_time = datetime.now(UTC)
            task.save()
            tasklog.save()
            profile.save()
            db.transaction.commit()

    #** post process

    tasklogs = EmailTaskLog.objects.filter(task=task).exclude(error='ok')

    if len(tasklogs):
        FIELDS = ["username", "email", "district", "send_date", "error"]
        TITLES = ["Username", "Email", "District", "Send Date", "Error"]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writerow(dict(zip(FIELDS, TITLES)))
        for d in tasklogs:
            row = {"username": d.username,
                   "email": d.email,
                   "district": d.district_name,
                   "send_date": d.send_date,
                   "error": d.error
                   }
            writer.writerow(row)
        output.seek(0)
        attach = [{'filename': 'log.csv', 'mimetype': 'text/csv', 'data': output.read()}]
        send_html_mail("Sending Registration Email Report",
                       "Report of sending registration email, see attachment.",
                       settings.SUPPORT_EMAIL, [request.user.email], attach)

        output.close()


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_custom_email(request):
    try:
        email = CustomEmail.objects.get(id=request.POST.get("id"))
    except Exception as e:
        return render_json_response({'success': True, 'message': e.message})

    return render_json_response({'success': True, 'message': email.email_content})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@ensure_csrf_cookie
def save_custom_email(request):
    op = request.POST.get('op')
    if op == 'update':
        try:
            email = CustomEmail.objects.get(id=request.POST.get('id'))
            email.email_content = request.POST.get('message')
            email.save()
            email_log = CustomEmailLog()
            email_log.email_name = email.name
            email_log.user = request.user
            email_log.operation = 'update'
            email_log.save()
            return render_json_response({'success': True, 'op': 'updated'})
        except Exception as e:
            return render_json_response({'success': False, 'error': '{0}'.format(e)})
    else:
        try:
            email = CustomEmail()
            email.email_content = request.POST.get('message')
            email.user = request.user
            email.name = request.POST.get('name')
            if op == 'public':
                email.system = 1
                email.private = 0
            elif op == 'private':
                email.system = 0
                email.private = 1
            elif op == 'organization':
                email.system = 0
                email.private = 0
            else:
                raise Exception('No operation selected')
            try:
                email.district = District.objects.get(id=request.POST.get('district'))
            except:
                pass
            try:
                email.school = School.objects.get(id=request.POST.get('school'))
            except:
                pass
            try:
                email.state = State.objects.get(id=request.POST.get('state'))
            except:
                pass
            email.save()
            return render_json_response({'success': True, 'op': 'saved'})
        except IntegrityError as e:
            return render_json_response({'success': False, 'error': 'duplicate'})
        except Exception as e:
            return render_json_response({'success': False, 'error': '{0}'.format(e)})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@ensure_csrf_cookie
def delete_custom_email(request):
    try:
        email = CustomEmail.objects.get(id=request.POST.get('id', False))
        email_log = CustomEmailLog()
        email_log.email_name = email.name
        email_log.user = request.user
        email_log.operation = 'delete'
        email_log.save()
        email.delete()
        return render_json_response({'success': True})
    except Exception as e:
        return render_json_response({'success': False, 'error': '{0}'.format(e)})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_custom_email_list(request):
    data = list()

    private = request.GET.get('private', False)
    public = request.GET.get('public', False)
    state = request.GET.get('state', False)
    district = request.GET.get('district', False)
    school = request.GET.get('school', False)
    query = dict()
    if private:
        query.update({'private': True})
    if public:
        query.update({'system': True})
    if state:
        query.update({'state': state})
    if district:
        query.update({'district': district})
    if school:
        query.update({'school': school})

    for i in CustomEmail.objects.filter(**query).order_by('name'):
        data.append({
            'id': i.id,
            'name': i.name,
        })
    return render_json_response(data)


def registration_email_progress(request):
    try:
        task = EmailTask.objects.get(id=request.POST.get('taskId'))
        message = {'percent': '%.2f' % (task.process_emails * 100 / task.total_emails)}
    except Exception as e:
        message = {'percent': 100}
    return HttpResponse(json.dumps(message), content_type="application/json")


def registration_invite_count(request):
    data = UserProfile.objects.all().select_related('User')
    data = registration_filter_user(request.POST, data)
            
    count = data.filter(subscription_status='Imported').count()
    return HttpResponse(json.dumps({'success': True, 'count': count}), content_type="application/json")


def registration_modify_user_status(request):
    message = {'success': True}
    for id in request.POST.get("ids").split(","): 
        user = User.objects.get(id=id)
        profile = UserProfile.objects.get(user_id=id)
        try:
            if request.POST['subscription_status'] == 'Registered':
                user.is_active = True
            else:
                user.is_active = False
            user.save()
            profile.subscription_status = request.POST['subscription_status']
            profile.save()
        except Exception as e:
            db.transaction.rollback()
            message = {'success': False}
            break
            
    return HttpResponse(json.dumps(message), content_type="application/json")


def registration_delete_users(request):
    message = {'success': True}
    ids = request.POST.get("ids").split(",")
    try:
        User.objects.filter(id__in=ids).delete()
        UserProfile.objects.filter(user_id__in=ids).delete()
        db.transaction.commit()
    except Exception as e:
        db.transaction.rollback()
        message = {'success': False, 'error': '%s' % (e)}
    return HttpResponse(json.dumps(message), content_type="application/json")    


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration_download_csv(request):
    FIELDS = ['user_id', "activate_link", "first_name", "last_name", "username", "email",
              "district", "cohort", "school", "invite_date", "activate_date", "subscription_status"]
    
    TITLES = ["User ID", "Activate Link", "First Name", "Last Name", "Username", "Email",
              "District", "Cohort", "School", "Invite Date", "Activate Date", "Status"]

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    
    writer.writerow(dict(zip(FIELDS, TITLES)))

    data = UserProfile.objects.all()
    data = registration_filter_user(request.POST, data)

    domain = "http://" + request.META['HTTP_HOST']

    for d in data:
        key, link = "", ""
        if Registration.objects.filter(user_id=d.user_id).count():
            key = Registration.objects.get(user_id=d.user_id).activation_key

        if key:
            link = domain + reverse('register_user', args=[key])

        writer.writerow({
            "user_id":attstr(d, "user_id"),
            "activate_link": link,
            "first_name": attstr(d, "user.first_name"),
            "last_name": attstr(d, "user.last_name"),
            "username": attstr(d, "user.username"),
            "email": attstr(d, "user.email"),
            "district": attstr(d, "district.name"),
            "cohort": attstr(d, "cohort.code"),
            "school": attstr(d, "school.name"),
            "invite_date": attstr(d, "invite_date"),
            "activate_date": attstr(d, "activate_date"),
            "subscription_status": attstr(d, "subscription_status")
            })

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.csv')
    output.seek(0)
    response.write(output.read())
    output.close()
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def registration_download_excel(request):
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    
    FIELDS = ['user_id', "activate_link", "first_name", "last_name", "username", "email",
              "_district", "_cohort", "_school", "_invite_date", "_activate_date", "subscription_status"]
    
    TITLES = ["User ID", "Activate Link", "First Name", "Last Name", "Username", "Email",
              "District", "Cohort", "School", "Invite Date", "Activate Date", "Status"]
    
    for i, k in enumerate(TITLES):
        worksheet.write(0, i, k)
    row = 1

    data = UserProfile.objects.all()
    data = registration_filter_user(request.POST, data)
    
    domain = "http://" + request.META['HTTP_HOST']
    for d in data:
        if Registration.objects.filter(user_id=d.user_id).count():
            key = Registration.objects.get(user_id=d.user_id).activation_key
        else:
            key = None
        d.activate_link = ""
        d.username = attstr(d, "user.username")
        d.first_name = attstr(d, "user.first_name")
        d.last_name = attstr(d, "user.last_name")
        d._school = attstr(d, "school.name")
        d._cohort = attstr(d, "cohort.code")
        d._district = attstr(d, "district.name")
        d.email = attstr(d, "user.email")
        d._invite_date = "%s" % attstr(d, "invite_date")
        d._activate_date = "%s" % attstr(d, "activate_date")
        
        for i, k in enumerate(FIELDS):
            if k == "activate_link" and key:
                d.activate_link = domain + reverse('register_user', args=[key])
                worksheet.write_url(row, i, getattr(d, k), None, key)
            else:
                worksheet.write(row, i, getattr(d, k))

        row += 1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.now().strftime('attachment; filename=users-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())    
    return response


def get_post_array(post, name, max=None):
    """
    Gets array values from a POST.
    """
    output = dict()
    for key in post.keys():
        value = urllib2.unquote(post.get(key))
        if key.startswith(name + '[') and not value == 'undefined':
            start = key.find('[')
            i = key[start + 1:-1]
            if max and int(i) > max:
                i = 'all'
            output.update({i: value})
    return output
