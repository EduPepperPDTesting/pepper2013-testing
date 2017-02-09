from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from administration.models import PepRegTraining, PepRegStudent
from student.models import UserProfile, People, State, District
from django.contrib.auth.models import User
from .models import TrainingUsers
from administration.pepconn import get_post_array
from django.db.models import Q
from people.views import get_pager
from view_counter.models import view_counter_store
#from notification import send_notification


def index(request):
    return render_to_response('trainings/trainings.html', {})

@login_required
def training_registration(request, training_id):
    training = PepRegTraining.objects.get(id=training_id) #TrainingTrainings
    return render_to_response('training/training_registration.html', {"training": training}) #register_unregister_students


@login_required
def training_join(request, training_id):
    """
    Registering student

    :param request:
    :return:
    """
    training = PepRegTraining.objects.get(id=training_id)

    for user_id in request.POST.get("user_ids", "").split(","):
        if not user_id.isdigit():
            continue
        try:
            user = User.objects.get(id=int(user_id))

            mems = TrainingUsers.objects.filter(user=user, training=training)

            if not mems.exists():
                tu = TrainingUsers(user=user, training=training)
                tu.save()

                pepmems = PepRegStudent.objects.filter(student=user, training=training)

                if not pepmems.exists():
                    prs = PepRegStudent(student=user, training=training, user_create=request.user, user_modify=request.user, student_status="Registered")
                    prs.save()

        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': "{0}".format(e)}), content_type="application/json")


    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required
def training_leave(request, training_id):
    """
    Unegistering student

    :param request:
    :return:
    """

    training = PepRegTraining.objects.get(id=training_id)

    for user_id in request.POST.get("user_ids", "").split(","):
        if not user_id.isdigit():
            continue
        try:
            user = User.objects.get(id=int(user_id))

            mems = TrainingUsers.objects.filter(user=user, training=training)

            if mems.exists():
                mems.delete()

                pepmems = PepRegStudent.objects.filter(student=user, training=training, student_status="Registered")

                if pepmems.exists():
                    pepmems.delete()

        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': "{0}".format(e)}), content_type="application/json")

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


@login_required
def get_add_user_rows(request, training_id):
    """
    Builds the rows for display in the students to be registered for training.
    :param request: User request
    :return: Table rows for the student table
    """

    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['user__email', '__icontains', 'str'],
               1: ['user__username', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['user__last_name', '__iexact', 'str'],
               4: ['user__profile__district__state__name', '__iexact', 'str'],
               5: ['user__profile__district__name', '__iexact', 'str'],
               6: ['user__profile__cohort__code', '__icontains', 'str'],
               7: ['user__profile__school__name', '__icontains', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 8)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size

    if filters.get('8'):
        filters['all'] = filters['8']
        del filters['8']

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

    members = TrainingUsers.objects.filter(training=training_id).values_list('user', flat=True) #user_id

    users = users.exclude(user__in=members)

    if not request.user.is_superuser:
        users = users.filter(user__profile__district=request.user.profile.district)

    # Add the row data to the list of rows.
    rows = list()
    count = users.count()
    for item in users[start:end]:
        row = list()

        row.append(str(item.user.email))

        row.append(str(item.user.username))
        row.append(str(item.user.first_name))
        row.append(str(item.user.last_name))

        try:
            user_school = item.user.profile.school.name
        except:
            user_school = ""
        try:
            user_district = str(item.user.profile.district.name)
            user_district_state = str(item.user.profile.district.state.name)
        except:
            user_district = ""
            user_district_state = ""
        try:
            user_cohort = str(item.user.profile.cohort.code)
        except:
            user_cohort = ""

        row.append(str(user_district_state))
        row.append(str(user_district))
        row.append(str(user_cohort))
        row.append(str(user_school))

        row.append('<input class="select_box" type="checkbox" name="id" value="' + str(item.user.id) + '"/>')

        rows.append(row)

    # The number of results is the first value in the return JSON
    json_out = [count]

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")


@login_required
def get_remove_user_rows(request, training_id):
    """
    Builds the rows for display in the students to be unregistered from training.
    :param request: User request
    :return: Table rows for the student table
    """
    # Defines the columns in the table. Key is the column #, value is a list made up of the column selector, the type of
    # selection, and the type of data in the column (or False to ignore this column in filters).
    columns = {0: ['user__email', '__icontains', 'str'],
               1: ['user__username', '__icontains', 'str'],
               2: ['user__first_name', '__icontains', 'str'],
               3: ['user__last_name', '__iexact', 'str'],
               4: ['user__profile__district__state__name', '__iexact', 'str'],
               5: ['user__profile__district__name', '__iexact', 'str'],
               6: ['user__profile__cohort__code', '__icontains', 'str'],
               7: ['user__profile__school__name', '__icontains', 'str']}
    # Parse the sort data passed in.
    sorts = get_post_array(request.GET, 'col')
    # Parse the filter data passed in.
    filters = get_post_array(request.GET, 'fcol', 8)
    # Get the page number and number of rows per page, and calculate the start and end of the query.
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    start = page * size
    end = start + size - 1

    if filters.get('8'):
        filters['all'] = filters['8']
        del filters['8']

    # Get the sort arguments if any.
    order = build_sorts(columns, sorts)

    # If the were filers passed in, get the arguments to filter by and add them to the query.
    if len(filters):
        args, kwargs = build_filters(columns, filters)
        # If there was a search for all, add the Q arguments.
        if args:
            users = TrainingUsers.objects.prefetch_related().filter(args, **kwargs).order_by(*order)
        else:
            users = TrainingUsers.objects.prefetch_related().filter(**kwargs).order_by(*order)
    # If there are no filters, just select all.
    else:
        users = TrainingUsers.objects.prefetch_related().all().order_by(*order)

    users = users.filter(training=training_id)

    # The number of results is the first value in the return JSON
    count = users.count()
    json_out = [count]

    # Add the row data to the list of rows.
    rows = list()
    for item in users[start:end]:
        row = list()

        row.append(str(item.user.email))

        row.append(str(item.user.username))
        row.append(str(item.user.first_name))
        row.append(str(item.user.last_name))

        try:
            user_school = item.user.profile.school.name
        except:
            user_school = ""
        try:
            user_district = str(item.user.profile.district.name)
            user_district_state = str(item.user.profile.district.state.name)
        except:
            user_district = ""
            user_district_state = ""
        try:
            user_cohort = str(item.user.profile.cohort.code)
        except:
            user_cohort = ""

        row.append(str(user_district_state))
        row.append(str(user_district))
        row.append(str(user_cohort))
        row.append(str(user_school))

        row.append('<input class="select_box" type="checkbox" name="id" value="' + str(item.user.id) + '"/>')
        rows.append(row)

    # The list of rows is the second value in the return JSON.
    json_out.append(rows)

    return HttpResponse(json.dumps(json_out), content_type="application/json")

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