from mitxmako.shortcuts import render_to_response
from .models import Reports, Categories, Views, ViewRelationships, ViewColumns, ReportViews, ReportViewColumns, ReportFilters
from .models import reporting_store
from permissions.decorators import user_has_perms
from permissions.utils import check_access_level, check_user_perms
from django.contrib.auth.decorators import login_required
from pepper_utilities.utils import get_request_array, render_json_response
from math import floor
from django_future.csrf import ensure_csrf_cookie
from django.db import transaction
from django.db.models import Q, Max
import sys
import json
import time
from .aggregation_config import AggregationConfig
from student.views import study_time_format
from .treatment_filters import get_mongo_filters
from django.conf import settings
from threading import Thread
import gevent
from StringIO import StringIO
from datetime import datetime
from django.http import HttpResponse
from school_year import report_has_school_year, get_school_year_item, get_query_school_year

def postpone(function):
    """
    Decorator for processing in a separate thread through gevent.
    :param function: Function to apply this decorator to.
    :return: Decorator.
    """
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


@login_required
def reports_view(request):
    """
    View for the main reports page.
    :param request: Request object.
    :return: The Reports page.
    """
    levels = {'System': 0, 'State': 1, 'District': 2, 'School': 3}
    access_level = check_access_level(request.user, 'reporting', ['administer', 'create_reports', 'view'])

    # If this is user has System access, show all the reports, otherwise, only show reports above their access level.
    if access_level == 'System':
        reports = Reports.objects.select_related('author__first_name', 'author__last_name').all().order_by('order')
    else:
        qs = Q(access_level='System')
        if not access_level or levels[access_level] > 0:
            qs |= Q(access_level='State', access_id=request.user.profile.district.state.id)
        if not access_level or levels[access_level] > 1:
            qs |= Q(access_level='District', access_id=request.user.profile.district.id)
        if not access_level or levels[access_level] > 2:
            qs |= Q(access_level='School', access_id=request.user.profile.school.id)
        qs |= Q(author_id=request.user.id)
        reports = Reports.objects.select_related('author__first_name', 'author__last_name').filter(qs).order_by('order')
    categories = Categories.objects.all().order_by('order')

    admin_rights = check_user_perms(request.user, 'reporting', 'administer')
    create_rights = check_user_perms(request.user, 'reporting', 'create_reports')

    data = {'categories': list(),
            'admin_rights': admin_rights,
            'create_rights': create_rights,
            'access_level': access_level}

    # Add uncategorized (unpublished) reports for admins.
    if admin_rights or create_rights:
        report_list = list()
        qs = Q(category__isnull=True)
        ####Original logic
        '''
        if not admin_rights:
            if access_level == 'School':
                qs &= Q(access_level='School') & Q(access_id=request.user.profile.school.id)
            elif access_level == 'District':
                qs &= Q(access_level='District') & Q(access_id=request.user.profile.district.id)
            elif access_level == 'State':
                qs &= Q(access_level='State') & Q(access_id=request.user.profile.district.state.id)
        '''
        if not request.user.is_superuser:
            qs &= Q(author_id=request.user.id)
        category_reports = reports.filter(qs)
        for category_report in category_reports:
            report_list.append({'id': category_report.id,
                                'name': category_report.name,
                                'description': category_report.description,
                                'author': category_report.author.first_name + ' ' + category_report.author.last_name,
                                'access_level': category_report.access_level,
                                'created': category_report.created,
                                'modified': category_report.modified})
        data['categories'].append({'id': None,
                                   'name': 'Draft Reports',
                                   'reports': report_list})

    # Add the rest of the reports by category.
    for category in categories:
        report_list = list()
        category_reports = reports.filter(category=category)
        for category_report in category_reports:
            report_list.append({'id': category_report.id,
                                'name': category_report.name,
                                'description': category_report.description,
                                'author': category_report.author.first_name + ' ' + category_report.author.last_name,
                                'access_level': category_report.access_level,
                                'created': category_report.created,
                                'modified': category_report.modified})
        data['categories'].append({'id': category.id,
                                   'name': category.name,
                                   'reports': report_list})

    return render_to_response('reporting/reports.html', data)


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def category_save(request):
    """
    Save new categories added by the user.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    name = request.POST.get('name', False)
    if name:
        try:
            maximum_order = Categories.objects.all().aggregate(Max('order')).get('order__max')
            maximum_order = maximum_order if maximum_order is not None else 0
            category = Categories()
            category.name = name
            category.order = maximum_order + 1
            category.save()
        except Exception as e:
            data = {'success': False, 'error': '{0}'.format(e)}
            transaction.rollback()
        else:
            data = {'success': True, 'name': category.name, 'id': category.id}
            transaction.commit()
    else:
        data = {'success': False, 'error': 'No name submitted.'}

    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def category_delete(request):
    """
    Delete requested category.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    category_id = request.POST.get('category_id', False)
    if category_id:
        try:
            Categories.objects.get(id=category_id).delete()
        except Exception as e:
            data = {'success': False, 'error': '{0}'.format(e)}
            transaction.rollback()
        else:
            data = {'success': True}
            transaction.commit()
    else:
        data = {'success': False, 'error': 'No Category ID submitted.'}

    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def order_save(request):
    """
    Save the order of the categories and reports in the report view.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    order = json.loads(request.body)
    try:
        for ci, cat in enumerate(order):
            if cat['id'] != 'None':
                category = Categories.objects.get(id=cat['id'])
                category.order = ci
                category.save()
            else:
                category = None

            for ri, rep in enumerate(cat['reports']):
                report = Reports.objects.get(id=rep['id'])
                report.order = ri
                report.category = category
                report.save()
    except Exception as e:
        data = {'success': False, 'error': '{0}'.format(e)}
        transaction.rollback()
    else:
        data = {'success': True}
        transaction.commit()

    return render_json_response(data)


@user_has_perms('reporting', ['administer', 'create_reports'])
def report_edit(request, report_id):
    """
    View for editing reports.
    :param request: Request object.
    :param report_id: The ID of the report to be edited. 'new' if this is a new report.
    :return: Report editing page.
    """
    views = Views.objects.all().order_by('name')
    data = {'views': views}
    if report_id != 'new':
        try:
            report = Reports.objects.get(id=report_id)
            admin_rights = check_user_perms(request.user, 'reporting', 'administer')
            create_rights = check_user_perms(request.user, 'reporting', 'create_reports')
            access_level = check_access_level(request.user, 'reporting', 'create_reports')
            user_access_id = None
            if access_level == 'State':
                user_access_id = request.user.profile.district.state.id
            elif access_level == 'District':
                user_access_id = request.user.profile.district.id
            elif access_level == 'School':
                user_access_id = request.user.profile.school.id
            if admin_rights or (create_rights and
                                access_level == report.access_level and
                                user_access_id == report.access_id):
                selected_views = ReportViews.objects.filter(report=report).order_by('order').values_list('view__id', flat=True)
                selected_views_columns = ViewColumns.objects.filter(view__id__in=selected_views).order_by('view', 'name')
                selected_columns = ReportViewColumns.objects.filter(report=report).order_by('order').values_list('column__id', flat=True)
                filters = ReportFilters.objects.filter(report=report).order_by('order')
                second_column = int(floor(len(selected_views_columns) / 2))
                remainder = len(selected_views_columns) % 2
                first_column = second_column + remainder
                data.update({'report': report,
                             'view_columns': selected_views_columns,
                             'selected_views': selected_views,
                             'selected_columns': selected_columns,
                             'report_filters': filters,
                             'first_column': first_column})
                action = 'edit'
            else:
                raise Exception('Not allowed.')
        except:
            data = {'error_title': 'Report Not Found',
                    'error_message': '''No report found with this ID. If you believe this is in error, please contact
                        site support.''',
                    'window_title': 'Report Not Found'}
            return render_to_response('error.html', data, status=404)
    else:
        action = 'new'
    data.update({'action': action, 'possible_operators': ['=', '!=', '>', '<', '>=', '<=']})
    return render_to_response('reporting/edit-report.html', data)


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def report_save(request, report_id):
    """
    Save edited or new reports.
    :param request: Request object.
    :param report_id: The ID of the report to be edited. 'new' if this is a new report.
    :return: JSON reporting success or failure of the operation.
    """
    try:
        name = request.POST.get('report_name', '')
        description = request.POST.get('report_description', '')
        distinct = not request.POST.get('distinct-enable', False) == 'yes'
        views = get_request_array(request.POST, 'view')
        columns = get_request_array(request.POST, 'column')
        column_order = get_request_array(request.POST, 'selected-column')
        filter_conjunctions = get_request_array(request.POST, 'filter-conjunction')
        filter_columns = get_request_array(request.POST, 'filter-column')
        filter_operators = get_request_array(request.POST, 'filter-operator')
        filter_values = get_request_array(request.POST, 'filter-value')
        action = request.POST.get('action', '')

        report = False
        if action == 'new':
            report = Reports()
            report.author = request.user
        elif action == 'edit':
            report = Reports.objects.get(id=int(report_id))

        if report:
            access_level = check_access_level(request.user, 'reporting', ['administer', 'create_reports'])

            report.name = name
            report.description = description
            report.distinct = distinct
            report.access_level = access_level
            if access_level == 'State':
                report.access_id = request.user.profile.district.state.id
            elif access_level == 'District':
                report.access_id = request.user.profile.district.id
            elif access_level == 'School':
                report.access_id = request.user.profile.school.id
            report.save()           

            ReportViews.objects.filter(report=report).delete()
            for i, view in views.iteritems():
                report_view = ReportViews()
                report_view.report = report
                report_view.order = int(i)
                report_view.view = Views.objects.get(id=int(view))
                report_view.save()

            ReportViewColumns.objects.filter(report=report).delete()
            for i, column in columns.iteritems():
                report_column = ReportViewColumns()
                report_column.report = report
                report_column.column = ViewColumns.objects.get(id=int(column))
                report_column.order = column_order[column]
                report_column.save()

            ReportFilters.objects.filter(report=report).delete()
            for i, column in filter_columns.iteritems():
                report_filter = ReportFilters()
                report_filter.report = report
                report_filter.conjunction = filter_conjunctions[i] if int(i) > 0 else None
                report_filter.column = ViewColumns.objects.get(id=int(column))
                report_filter.value = filter_values[i].strip()
                report_filter.operator = filter_operators[i]
                report_filter.order = int(i)
                report_filter.save()
           
            rs = reporting_store()
            selected_columns = ReportViewColumns.objects.filter(report=report).order_by('order')            
            if report_has_school_year(selected_columns):                
                for item in get_school_year_item():
                    collection = get_cache_collection(request, report_id, item)
                    rs.del_collection(collection)

                collection = get_cache_collection(request, report_id, "all")
                rs.del_collection(collection)

            
            collection = get_cache_collection(request, report_id, "")
            rs.del_collection(collection)

        else:
            raise Exception('Report could not be located or created.')
    except Exception as e:
        transaction.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return render_json_response({'success': False, 'error': '{0} (Line# {1})'.format(e, exc_traceback.tb_lineno)})
    else:
        transaction.commit()
        return render_json_response({'success': True, 'report_id': report.id})


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def report_delete(request):
    """
    Delete requested report.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    report_id = request.POST.get('report_id', False)
    if report_id:
        try:
            report = Reports.objects.get(id=report_id)
            rid = report.id
            rname = report.name
            
            Reports.objects.get(id=report_id).delete()          

        except Exception as e:
            data = {'success': False, 'error': '{0}'.format(e)}
            transaction.rollback()
        else:
            data = {'success': True}
            transaction.commit()
    else:
        data = {'success': False, 'error': 'No Report ID given.'}

    return render_json_response(data)


@login_required
def report_view(request, report_id):
    """
    View for viewing reports.
    :param request: Request object.
    :param report_id: The ID of the report to be edited.
    :return: The Report page.
    """
    school_year = ""
    try:
        allowed = False
        report = Reports.objects.get(id=report_id)
        selected_columns = ReportViewColumns.objects.filter(report=report).order_by('order')

        if report.access_level == 'System':
            allowed = True
        elif report.access_level == 'State' and request.user.profile.district.state.id == report.access_id:
            allowed = True
        elif report.access_level == 'District' and request.user.profile.district.id == report.access_id:
            allowed = True
        elif report.access_level == 'School' and request.user.profile.school.id == report.access_id:
            allowed = True
        elif request.user.is_superuser:
            allowed = True
        if allowed:
            school_year = request.GET.get('school_year', '')
            if school_year:
                school_year = str(school_year).replace("-","_")

            rs = reporting_store()
            collection = get_cache_collection(request, report_id, school_year)

            stats = int(rs.get_collection_stats(collection)['ok'])
            if(not(stats)):
                rs.del_collection(collection)
                selected_view = ReportViews.objects.filter(report=report)[0]
                report_filters = ReportFilters.objects.filter(report=report).order_by('order')

                columns = []
                filters = []
                for col in selected_columns:
                    columns.append(col)
                for f in report_filters:
                    filters.append(f)

                create_report_collection(request, report, selected_view, columns, filters, report_id)

            view_id = ReportViews.objects.filter(report=report)[0].view_id;
            pd_planner_id = Views.objects.filter(name='PD Planner')[0].id;
            school_year_item = []
            if (report_has_school_year(selected_columns)) or (view_id == pd_planner_id):
                school_year_item = get_school_year_item()
        else:
            raise Exception('Not allowed.')
    except:
        data = {'error_title': 'Report Not Found',
                'error_message': '''No report found with this ID. If you believe this is in error, please contact
                        site support.''',
                'window_title': 'Report Not Found'}
        return render_to_response('error.html', data, status=404)

    data = {'report': report,
            'school_year': school_year,
            'display_columns': selected_columns,
            'school_year_item': school_year_item}
    return render_to_response('reporting/view-report.html', data)


@login_required
def report_get_rows(request):
    """
    Gets the rows for the tablesorter table.
    :param request: Request object.
    :return: Tablesorter table rows.
    """
    sorts = get_request_array(request.GET, 'col')
    filters = get_request_array(request.GET, 'fcol')
    page = int(request.GET['page'])
    size = int(request.GET['size'])
    report_id = request.GET['report_id']
    school_year = request.GET.get('school_year', '')
    start = page * size
    rows = []
    report = Reports.objects.get(id=report_id)
    selected_columns = ReportViewColumns.objects.filter(report=report).order_by('order')
    sorts, filters = build_sorts_and_filters(selected_columns, sorts, filters)
    rs = reporting_store()
    collection = get_cache_collection(request, report_id, school_year)
    data = rs.get_page(collection, start, size, filters, sorts)
    total = rs.get_count(collection, filters)

    for d in data:
        row = []
        for col in selected_columns:
            try:
                row.append(data_format(col.column, d))
            except Exception as e:
                row.append('')
        row.append('')
        rows.append(row)
    return render_json_response({'total': total, 'rows': rows})


def build_sorts_and_filters(columns, sorts, filters):
    """
    Builds the sorts and filters for mongo based on the input params from tablesorter.
    :param columns: The columns on which to act.
    :param sorts: The sorts from tablesorter.
    :param filters: the filters from tablesorter
    :return: Sorts and filters for mongo.
    """
    column = []
    data_type = {}
    custom_filter = {}
    int_type = ['int', 'time']
    for i, col in enumerate(columns):
        column.append(col.column.column)
        data_type[col.column.column] = col.column.data_type
        custom_filter[col.column.column] = col.column.custom_filter

    order = ['$natural', 1, 0]
    for col, sort in sorts.iteritems():
        pre = 1
        if bool(int(sort)):
            pre = -1
        if data_type[column[int(col)]] in int_type:
            order = [column[int(col)], pre, 1]
        else:
            order = [column[int(col)], pre, 0]

    filter = {}
    for col, f in filters.iteritems():
        if custom_filter[column[int(col)]] > 0:
            filter[column[int(col)]] = f
        else:
            reg = {'$regex': '.*' + f + '.*', '$options': 'i'}
            filter[column[int(col)]] = reg
    return order, filter


def get_cache_collection(request, report_id, school_year=""):
    """
    Returns the name of the aggregate collection.
    :param request: Request object.
    :return: aggregate collection name.
    """

    return 'tmp_collection_' + str(request.user.id) + '_' + str(report_id) + school_year


@postpone
def create_report_collection(request, report, selected_view, columns, filters, report_id):
    """
    Creates aggregate collections in Mongo in a background process.
    :param request: Request object from the report view.
    :param selected_view: The view off of which to build the aggregate collection.
    :param columns: The columns to show in the aggregate collection.
    :param filters: The filters to use in the aggregate collection.
    """
    gevent.sleep(0)
    aggregate_config = AggregationConfig[selected_view.view.collection]
    aggregate_query = aggregate_query_format(request, aggregate_config['query'], report, columns, filters, report_id)
    rs = reporting_store()
    rs.get_aggregate(aggregate_config['collection'], aggregate_query, report.distinct)


def aggregate_query_format(request, query, report, columns, filters, report_id, out=True):
    """
    Does some formatting to the query for mongo.
    :param request: The request object from upstream.
    :param query: Mongo query.
    :param columns: The columns to show in the aggregate collection.
    :param filters: The filters to use in the aggregate collection.
    :param out: Whether to generate aggregate collection.
    :return: The formatted query.
    """
    
    school_year = request.GET.get('school_year', '')
    if school_year:
        school_year = str(school_year).replace("-","_")

    query = query_ref_variable(query, request, report, columns, filters)
    query = query.replace('\n', '').replace('\r', '')
    if out:
        query += ',{"$out":"' + get_cache_collection(request, report_id, school_year) + '"}'
    query = eval(query)
    return query


def query_ref_variable(query, request, report, columns, filters):
    """
    Replace the placeholders.
    :param query: Mongo query
    :param request: Request object.
    :param columns: The columns to show in the report.
    :param filters: The filters to use in the report.
    :return: The replaced query.
    """
    domain = get_query_user_domain(request.user)
    school_year = get_query_school_year(request, report, columns)
    distinct = get_query_distinct(report.distinct, columns)
    columns = get_query_display_columns(columns)
    filters = get_query_filters(filters)
    pd_domain, pd_user_domain = get_query_pd_domain(request.user)
    return query.replace('{user_domain}', domain)\
        .replace('{display_columns}', columns)\
        .replace('{filters}', filters)\
        .replace('{distinct}', distinct)\
        .replace('{school_year}', school_year)\
        .replace('{pd_domain}', pd_domain)\
        .replace('{pd_user_domain}', pd_user_domain)\
        .replace(',,', ',')


def get_query_user_domain(user):
    """
    Get the user's domain (permissions).
    :param user: The user object.
    :return: Mongo query
    """
    domain = '{"$match":{"user_id":' + str(user.id) + '}},'
    if check_user_perms(user, 'reporting', ['view', 'administer']):
        level = check_access_level(user, 'reporting', ['view', 'administer'])
        if level == 'System':
            domain = ''
        elif level == 'State':
            domain = '{"$match":{"state_id":' + str(user.profile.district.state.id) + '}},'
        elif level == 'District':
            domain = '{"$match":{"district_id":' + str(user.profile.district.id) + '}},'
        elif level == 'School':
            domain = '{"$match":{"school_id":' + str(user.profile.school.id) + '}},'
    return domain

def get_query_pd_domain(user):
    """
    Get the pd domain (permissions).
    :param user: The user object.
    :return: Mongo query
    """
    domain = '{"$match":{"district_id":' + str(user.profile.district.id) + '}},'
    pd_user_domain_tmp = '{"$match":{"#domain#":#value#}},'
    if check_user_perms(user, 'reporting', ['view', 'administer']):
        level = check_access_level(user, 'reporting', ['view', 'administer'])
        if level == 'System':
            domain = ''
            pd_user_domain = ''
        elif level == 'State':
            domain = '{"$match":{"state_id":' + str(user.profile.district.state.id) + '}},'
            pd_user_domain = ''
        elif level == 'District':
            pd_user_domain = ''
        elif level == 'School':
            pd_user_domain = pd_user_domain_tmp.replace('#domain#', 'school_id').replace('#value#', str(user.profile.school.id))
    else:
        pd_user_domain = pd_user_domain_tmp.replace('#domain#', 'user_id').replace('#value#', str(user.id))
    return domain, pd_user_domain


def get_query_display_columns(columns):
    """
    Get the columns shown in the report.
    :param columns: The columns shown in the report.
    :return: Mongo query.
    """
    column_str = ''
    for col in columns:
        if col.column.data_type == 'int':
            column_str += '"' + col.column.column + '":{"$substr":["$' + col.column.column + '", 0,-1]},'
        else:
            column_str += '"' + col.column.column + '":1,'
    if column_str != '':
        return ',{"$project": {' + column_str[:-1] + '}}'
    else:
        return column_str


def get_query_filters(filters):
    """
    Get the filters in the report.
    :param filters: The filters to use in the report.
    :return: Mongo query.
    """
    filter_str = ''
    if len(filters) > 0:
        for filter in filters:
            conjunction = '##'
            value = filter.value
            if filter.conjunction is not None:
                conjunction += filter.conjunction.lower() + '##'
            if filter.value.isdigit() is False:
                value = "'" + filter.value + "'"
            filter_str += conjunction + filter.column.column + filter.operator + value
        sql = get_mongo_filters(filter_str[2:])
        return ',{"$match":' + sql + '}'
    return filter_str


def get_query_distinct(is_distinct, columns):
    """
    Get the distinct filtering in the report.
    :param is_distinct: Whether distinct or not.
    :param columns: The columns shown in the report.
    :return: Mongo query.
    """
    distinct = ''
    column_str = ''
    if len(columns) > 0 and is_distinct:
        distinct = {'$group': {'_id': {}}}
        for col in columns:
            field = col.column.column
            field_value = '$' + col.column.column
            distinct['$group']['_id'][field] = field_value
            distinct['$group'][field] = {'$push': field_value}
            column_str += "'" + field + "':{'$arrayElemAt': ['" + field_value + "', 0]},"
        return ',' + str(distinct) + ',{"$project":{' + column_str[:-1] + '}}'
    return distinct


def data_format(col, data, is_excel=False):
    """
    Report data format.
    :param col: The columns shown in the report.
    :param data: Each row of data in the report.
    :param is_excel: If this is True, then the operation of object is Excel.
    :return: The formatted data.
    """
    if col.data_type == 'time':
        return study_time_format(data[col.column])
    if col.data_type == 'url':
        if is_excel:
            return settings.LMS_BASE + data[col.column]
        else:
            return '<a href="{0}" target="_blank">Link</a>'.format(data[col.column])
    if col.data_type == 'date':
        return time.strftime('%m-%d-%Y', time.strptime(data[col.column], '%Y-%m-%d'))
    return data[col.column]


@login_required
def report_download_excel(request, report_id):
    """
    View for serving an Excel version of the report.
    :param request: Request object.
    :param report_id: The ID of the requested report.
    :return: The Excel document.
    """
    import xlsxwriter
    output = StringIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
    worksheet = workbook.add_worksheet()
    report = Reports.objects.get(id=report_id)
    columns = ReportViewColumns.objects.filter(report=report).order_by('order')    
    school_year = request.GET.get('school_year', '')

    for i, k in enumerate(columns):
        worksheet.write(0, i, k.column.name)
    row = 1
    rs = reporting_store()
    rs.set_collection(get_cache_collection(request, report_id, school_year))
    results = rs.collection.find()
    for p in results:
        for i, k in enumerate(columns):
            try:
                p[k.column.column] = data_format(k.column, p, True)
            except:
                p[k.column.column] = ''

            worksheet.write(row, i, p[k.column.column])
        row += 1
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = datetime.now().strftime('attachment; filename=report-%Y-%m-%d-%H-%M-%S.xlsx')
    workbook.close()
    response.write(output.getvalue())
    return response


@login_required
def report_get_progress(request, report_id):
    """
    Checks the status of the collection creation progress.
    :param request: Request object.
    :return: JSON representation of the status.
    """    
    school_year = request.GET.get('school_year', '')
    rs = reporting_store()
    collection = get_cache_collection(request, report_id, school_year)
    stats = int(rs.get_collection_stats(collection)['ok'])
    return render_json_response({'success': stats, 'collection':collection})


def report_get_custom_filters(request, report_id):
    """
    Return the options of custom filters.
    :param request: Request object.
    :param Report object.
    """
    data = []
    school_year = request.GET.get('school_year', '')
    rs = reporting_store()
    collection = get_cache_collection(request, report_id, school_year)
    rs.set_collection(collection)
    report = Reports.objects.get(id=report_id)
    selected_columns = ReportViewColumns.objects.filter(report=report, column__custom_filter=1).order_by('order')
    for col in selected_columns:
        result = rs.collection.distinct(col.column.column)
        data.append({
            'items': sorted(result, cmp=None, key=None, reverse=True),
            'index': col.order
        })
    return render_json_response({'data': data})


@user_has_perms('reporting', ['administer', 'create_reports'])
def related_views(request):
    """
    Gets the views related to the selected view.
    :param request: Request object.
    :return: JSON list of related views.
    """
    relationships = ViewRelationships.objects.select_related().filter(left=request.GET.get('view_id')).order_by('right__name')
    data = []
    for relationship in relationships:
        data.append({'id': relationship.right.id, 'name': relationship.right.name})
    return render_json_response(data)


@user_has_perms('reporting', ['administer', 'create_reports'])
def view_columns(request):
    """
    Gets a list of the columns in the selected view.
    :param request: Request object
    :return: JSON list of columns in the selected view.
    """
    views = get_request_array(request.GET, 'view')
    columns = ViewColumns.objects.select_related().filter(view__in=views.values()).order_by('view', 'name')
    data = []
    for column in columns:
        data.append({'id': column.id,
                     'type': column.data_type,
                     'name': column.view.name + '.' + column.name,
                     'description': column.description})
    return render_json_response(data)


@user_has_perms('reporting', 'administer')
def views_edit_update(request):
    """
    Update info for the view and relationship tables in the view editor.
    :param request: Request object.
    :return: JSON list of views and relationships.
    """
    views = Views.objects.all().order_by('name')
    columns = ViewColumns.objects.all().order_by('name')
    relationships = ViewRelationships.objects.select_related().all()

    view_list = list()
    for view in views:
        view_list.append({'name': view.name,
                           'description': view.description,
                           'id': view.id,
                           'columns': ', '.join(columns.filter(view=view).values_list('name', flat=True))})

    relationship_list = list()
    for relationship in relationships:
        relationship_list.append({'relationship': '{0} -> {1}'.format(relationship.left.view.name,
                                                                      relationship.right.view.name),
                                  'columns': '{0}.{1} = {2}.{3}'.format(relationship.left.view.name,
                                                                        relationship.left.name,
                                                                        relationship.right.view.name,
                                                                        relationship.right.name),
                                  'id': relationship.id})

    data = {'views': view_list,
            'relationships': relationship_list}
    return render_json_response(data)


@user_has_perms('reporting', 'administer')
def view_data(request):
    """
    Gets the view data for the editing form.
    :param request: Request object.
    :return: JSON representation of the view data.
    """
    view_id = request.GET.get('view_id', False)
    if view_id:
        try:
            view = Views.objects.get(id=view_id)
            columns = ViewColumns.objects.filter(view=view)
        except Exception as e:
            data = {'success': False}
        else:
            data = {'success': True,
                    'id': view.id,
                    'name': view.name,
                    'description': view.description,
                    'source': view.collection,
                    'columns': list()}
            for column in columns:
                data['columns'].append({'id': column.id,
                                        'name': column.name,
                                        'description': column.description,
                                        'source': column.column,
                                        'type': column.data_type,
                                        'custom_filter': column.custom_filter})
    else:
        data = {'success': False}

    return render_json_response(data)


@user_has_perms('reporting', 'administer')
def relationship_data(request):
    """
    Gets the view relationship data for the editing form.
    :param request: Request object.
    :return: JSON representation of the relationship data.
    """
    relationship_id = request.GET.get('relationship_id', False)
    if relationship_id:
        try:
            relationship = ViewRelationships.objects.select_related().get(id=relationship_id)
        except Exception as e:
            data = {'success': False}
        else:
            data = {'success': True,
                    'id': relationship.id,
                    'left_view': relationship.left.view.id,
                    'right_view': relationship.right.view.id,
                    'left_column': relationship.left.id,
                    'right_column': relationship.right.id}
    else:
        data = {'success': False}

    return render_json_response(data)


@user_has_perms('reporting', 'administer')
def views_edit(request):
    """
    The view for the view editing page.
    :param request: Request object.
    :return: The view edit page.
    """
    views = Views.objects.all().order_by('name')
    columns = ViewColumns.objects.all().order_by('name')
    relationships = ViewRelationships.objects.select_related().all()

    data = {'views': views,
            'columns': columns,
            'relationships': relationships}
    return render_to_response('reporting/edit-views.html', data)


@ensure_csrf_cookie
@user_has_perms('reporting', 'administer')
@transaction.commit_manually
def view_add(request):
    """
    Handles the creation/saving of views.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    view_name = request.POST.get('view_name', '')
    view_description = request.POST.get('view_description', '')
    view_source = request.POST.get('view_source', '')
    column_names = get_request_array(request.POST, 'column_name')
    column_descriptions = get_request_array(request.POST, 'column_description')
    column_sources = get_request_array(request.POST, 'column_source')
    column_types = get_request_array(request.POST, 'column_type')
    column_ids = get_request_array(request.POST, 'column_id')
    column_custom_filter = get_request_array(request.POST, 'column_custom_filter')
    view_id = request.POST.get('view_id', False)

    error = list()

    try:
        if view_id:
            view = Views.objects.get(id=view_id)
        else:
            view = Views()
        view.name = view_name
        view.description = view_description
        view.collection = view_source
        view.save()
    except Exception as e:
        error.append('View Error: {0}'.format(e))
        transaction.rollback()
    else:
        transaction.commit()
        try:
            if view_id:
                columns = [int(i) for i in column_ids.values()]
                ViewColumns.objects.filter(view=view).exclude(id__in=columns).delete()
            for i, column_name in column_names.iteritems():
                column_id = column_ids.get(i, False)
                if column_id:
                    column = ViewColumns.objects.get(id=int(column_id))
                else:
                    column = ViewColumns()
                column.name = column_name
                column.description = column_descriptions[i]
                column.column = column_sources[i]
                column.data_type = column_types[i]
                column.custom_filter = column_custom_filter[i]
                column.view = view
                column.save()
        except Exception as e:
            error.append('Column Error: {0}'.format(e))
            transaction.rollback()
        else:
            transaction.commit()

    if len(error):
        data = {'success': False, 'error': ' '.join(error)}
    else:
        data = {'success': True}

    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('reporting', 'administer')
@transaction.commit_manually
def relationship_add(request):
    """
    Handles the creation/saving of view relationships.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    left_column = request.POST.get('left_column', '')
    right_column = request.POST.get('right_column', '')
    relationship_id = request.POST.get('relationship_id', False)

    try:
        if relationship_id:
            relationship = ViewRelationships.objects.get(id=relationship_id)
        else:
            relationship = ViewRelationships()
        relationship.left = ViewColumns.objects.get(id=left_column)
        relationship.right = ViewColumns.objects.get(id=right_column)
        relationship.save()
    except Exception as e:
        data = {'success': False, 'error': '{0}'.format(e)}
        transaction.rollback()
    else:
        data = {'success': True}
        transaction.commit()

    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('reporting', 'administer')
@transaction.commit_manually
def views_delete(request):
    """
    Deletes selected view.
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    view_ids = get_request_array(request.POST, 'view_id')
    try:
        Views.objects.filter(id__in=view_ids.values()).delete()
        data = {'success': True}
    except Exception as e:
        data = {'success': False, 'error': '{0}'.format(e)}
        transaction.rollback()
    else:
        transaction.commit()
    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('reporting', 'administer')
@transaction.commit_manually
def relationships_delete(request):
    """
    Deletes selected view relationship
    :param request: Request object.
    :return: JSON reporting success or failure of the operation.
    """
    relationship_ids = get_request_array(request.POST, 'relationship_id')
    try:
        ViewRelationships.objects.filter(id__in=relationship_ids.values()).delete()
        data = {'success': True}
    except Exception as e:
        data = {'success': False, 'error': '{0}'.format(e)}
        transaction.rollback()
    else:
        transaction.commit()
    return render_json_response(data)


@user_has_perms('reporting', ['administer', 'create_reports'])
def views_list(request):
    """
    Gets a list o available views.
    :param request: Request object.
    :return: JSON list of views.
    """
    views = Views.objects.all().order_by('name')
    view_list = dict()
    for view in views:
        view_list.update({view.id: view.name})

    return render_json_response(view_list)


# TODO: Test this at some point to see if it works as expected.
# @user_has_perms('reporting', ['administer', 'create_reports'])
# def view_columns_list(request):
#     """
#     Gets a list of columns for the selected collection.
#     :param request: Request object.
#     :return: JSON list of columns.
#     """
#     view = request.GET.get('view', False)
#
#     reporting = reporting_store()
#     view_column_list = reporting.get_columns(view)
#
#     return render_json_response(view_column_list)
