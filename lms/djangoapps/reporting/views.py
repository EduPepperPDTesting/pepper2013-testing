from mitxmako.shortcuts import render_to_response
from .models import Reports, Categories, Views, ViewRelationships, ViewColumns, ReportViews, ReportViewColumns, ReportFilters
from permissions.decorators import user_has_perms
from pepper_utilities.utils import get_request_array, render_json_response
from math import floor
from django_future.csrf import ensure_csrf_cookie


@user_has_perms('reporting')
def reports_view(request):
    reports = Reports.objects.select_related('author__first_name', 'author__last_name').all().order_by('order')
    categories = Categories.objects.all().order_by('order')
    report_list = []
    category_reports = reports.filter(category__isnull=True)
    for category_report in category_reports:
        report_list.append({'id': category_report.id,
                            'name': category_report.name,
                            'description': category_report.description,
                            'author': category_report.author.first_name + ' ' + category_report.author.last_name,
                            'created': category_report.created,
                            'modified': category_report.modified})
    data = {'categories': [{'id': None,
                            'name': 'Draft Reports',
                            'reports': report_list}]}
    for category in categories:
        report_list = []
        category_reports = reports.filter(category=category)
        for category_report in category_reports:
            report_list.append({'id': category_report.id,
                                'name': category_report.name,
                                'description': category_report.description,
                                'author': category_report.author.first_name + ' ' + category_report.author.last_name,
                                'created': category_report.created,
                                'modified': category_report.modified})
        data['categories'].append({'id': category.id,
                                   'name': category.name,
                                   'reports': report_list})

    return render_to_response('reporting/reports.html', data)


@user_has_perms('reporting', 'administer')
def report_edit(request, report_id):
    views = Views.objects.all().order_by('name')
    data = {'views': views}
    if report_id != 'new':
        try:
            report = Reports.objects.get(id=report_id)
            selected_views = ReportViews.objects.filter(report=report).order_by('order')
            view_columns = ViewColumns.objects.filter(view__in=selected_views.values_list('id', flat=True)).order_by(
                'view', 'name')
            selected_columns = ReportViewColumns.objects.filter(report=report)
            filters = ReportFilters.objects.filter(report=report).order_by('order')
            third_column = floor(len(view_columns) / 3)
            remainder = len(view_columns) % 3
            first_column = third_column + 1 if remainder > 0 else third_column
            second_column = third_column + 1 if remainder > 1 else third_column
            s = selected_columns.values_list('id', flat=True)
            x = 0
            data.update({'report': report,
                         'view_columns': view_columns,
                         'selected_views': selected_views,
                         'selected_columns': selected_columns,
                         'report_filters': filters,
                         'first_column': first_column,
                         'second_column': second_column,
                         'third_column': third_column})
            action = 'edit'
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
@user_has_perms('reporting', 'administer')
def report_save(request):
    name = request.POST.get('report_name', '')
    description = request.POST.get('report_description', '')
    views = get_request_array(request.POST, 'view')
    columns = get_request_array(request.POST, 'column')
    filter_conjunctions = get_request_array(request.POST, 'filter-conjunction')
    filter_views = get_request_array(request.POST, 'filter-view')
    filter_operators = get_request_array(request.POST, 'filter-operator')
    filter_values = get_request_array(request.POST, 'filter-value')
    action = request.POST.get('action', '')
    report_id = request.POST.get('report_id', '')

    report = False
    if action == 'new':
        report = Reports()
        report.author = request.user
    elif action == 'edit':
        report = Reports.object.get(id=report_id)

    if report:
        report.name = name
        report.description = description
        report.save()

        ReportViews.objects.filter(report=report).delete()
        for i, view in views:
            report_view = ReportViews()
            report_view.report = report
            report_view.order = int(i)
            report_view.view = Views.objects.get(id=view)
            report_view.save()

        ReportViewColumns.objects.filter(report=report).delete()
        for i, column in columns:
            report_column = ReportViewColumns()
            report_column.report = report
            report_column.column = ViewColumns.objects.get(id=column)
            report_column.save()

        ReportFilters.objects.filter(report=report)
        for i, filter in filter_views:
            report_filter = ReportFilters()
            report_filter.report = report
            report_filter.conjunction = filter_conjunctions[i] if int(i) > 0 else None
            report_filter.view = Views.objects.get(id=filter)
            report_filter.value = filter_values[i]
            report_filter.operator = filter_operators[i]
            report_filter.save()
    else:
        pass


@user_has_perms('reporting')
def report_view(request):
    # TODO: Add the code to show the actual report itself.
    pass


@user_has_perms('reporting', 'administer')
def related_views(request):
    relationships = ViewRelationships.objects.select_related().filter(left=request.GET.get('view_id')).order_by('name')
    data = []
    for relationship in relationships:
        data.append({'id': relationship.right.id, 'name': relationship.right.name})
    return render_json_response(data)


@user_has_perms('reporting', 'administer')
def view_columns(request):
    views = get_request_array(request.GET, 'view')
    columns = ViewColumns.objects.select_related().filter(view__in=views.values()).order_by('view', 'name')
    data = []
    for column in columns:
        data.append({'id': column.id,
                     'name': column.view.name + '.' + column.name,
                     'description': column.description})
    return render_json_response(data)
