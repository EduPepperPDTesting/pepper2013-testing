from mitxmako.shortcuts import render_to_response
from .models import Reports, Categories, Views
from permissions.decorators import user_has_perms


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
        except:
            data = {'error_title': 'Report Not Found',
                    'error_message': 'No report found with this ID.',
                    'window_title': 'Report Not Found'}
            return render_to_response('error.html', data, status=404)
    else:
        report = 'none'
    data.update({'report': report})
    return render_to_response('reporting/new-report.html', data)


@user_has_perms('reporting')
def report_view(request):
    # TODO: Add the code to show the actual report itself.
    pass


@user_has_perms('reporting', 'administer')
def related_views(request):
    # TODO: Add the code to return the views related to the passed view.
    pass
