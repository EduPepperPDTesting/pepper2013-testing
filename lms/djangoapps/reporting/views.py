from mitxmako.shortcuts import render_to_response
from .models import Reports, Categories


def reports_view(request):
    reports = Reports.objects.select_related('author__first_name', 'author__last_name').all().order_by('order')
    categories = Categories.objects.all().order_by('order')
    data = []
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
        data.append({'id': category.id,
                     'name': category.name,
                     'reports': report_list})

    return render_to_response('reporting/reports.html', data)
