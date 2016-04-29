from mitxmako.shortcuts import render_to_response
from .models import Reports, Categories, Views, ViewRelationships, ViewColumns, ReportViews, ReportViewColumns, ReportFilters
from permissions.decorators import user_has_perms
from pepper_utilities.utils import get_request_array, render_json_response


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
    if report_id != 'none':
        try:
            report = Reports.objects.get(id=report_id)
            selected_views = ReportViews.objects.filter(report=report).order_by('order')
            view_columns = ViewColumns.objects.filter(view__in=selected_views.values_list('id', flat=True)).order_by(
                'view', 'name')
            selected_columns = ReportViewColumns.objects.filter(report=report)
            filters = ReportFilters.objects.filter(report=report).order_by('order')
            data.update({'report': report,
                         'view_columns': view_columns,
                         'selected_views': selected_views,
                         'selected_columns': selected_columns,
                         'filters': filters})
            action = 'edit'
        except:
            data = {'error_title': 'Report Not Found',
                    'error_message': 'No report found with this ID.',
                    'window_title': 'Report Not Found'}
            return render_to_response('error.html', data, status=404)
    else:
        action = 'new'
    data.update({'action': action})
    return render_to_response('reporting/edit-report.html', data)


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
