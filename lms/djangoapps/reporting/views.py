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


@login_required
def reports_view(request):
    levels = {'System': 0, 'State': 1, 'District': 2, 'School': 3}
    access_level = check_access_level(request.user, 'reporting', ['administer', 'create_reports', 'view_reports'])
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
        reports = Reports.objects.select_related('author__first_name', 'author__last_name').filter(qs).order_by('order')
    categories = Categories.objects.all().order_by('order')

    data = {'categories': list()}

    # Add uncategorized (unpublished) reports for admins.
    if check_user_perms(request.user, 'reporting', ['administer', 'create_reports']):
        report_list = list()
        category_reports = reports.filter(category__isnull=True)
        for category_report in category_reports:
            report_list.append({'id': category_report.id,
                                'name': category_report.name,
                                'description': category_report.description,
                                'author': category_report.author.first_name + ' ' + category_report.author.last_name,
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
            data = {'success': True, 'name': category.name}
            transaction.commit()
    else:
        data = {'success': False, 'error': 'No name submitted.'}

    return render_json_response(data)


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def order_save(request):
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
    views = Views.objects.all().order_by('name')
    data = {'views': views}
    if report_id != 'new':
        try:
            report = Reports.objects.get(id=report_id)
            selected_views = ReportViews.objects.filter(report=report).order_by('order').values_list('view__id', flat=True)
            selected_views_columns = ViewColumns.objects.filter(view__id__in=selected_views).order_by('view', 'name')
            selected_columns = ReportViewColumns.objects.filter(report=report).values_list('column__id', flat=True)
            filters = ReportFilters.objects.filter(report=report).order_by('order')
            third_column = int(floor(len(selected_views_columns) / 3))
            remainder = len(selected_views_columns) % 3
            first_column = third_column + 1 if remainder > 0 else third_column
            second_column = first_column * 2 if remainder > 1 else first_column * 2 - 1
            data.update({'report': report,
                         'view_columns': selected_views_columns,
                         'selected_views': selected_views,
                         'selected_columns': selected_columns,
                         'report_filters': filters,
                         'first_column': first_column,
                         'second_column': second_column})
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
    #raise Exception('{0}'.format(data))
    return render_to_response('reporting/edit-report.html', data)


@ensure_csrf_cookie
@user_has_perms('reporting', ['administer', 'create_reports'])
@transaction.commit_manually
def report_save(request, report_id):
    try:
        name = request.POST.get('report_name', '')
        description = request.POST.get('report_description', '')
        views = get_request_array(request.POST, 'view')
        columns = get_request_array(request.POST, 'column')
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
                report_column.save()

            ReportFilters.objects.filter(report=report).delete()
            for i, column in filter_columns.iteritems():
                report_filter = ReportFilters()
                report_filter.report = report
                report_filter.conjunction = filter_conjunctions[i] if int(i) > 0 else None
                report_filter.column = ViewColumns.objects.get(id=int(column))
                report_filter.value = filter_values[i]
                report_filter.operator = filter_operators[i]
                report_filter.order = int(i)
                report_filter.save()
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
    report_id = request.POST.get('report_id', False)
    if report_id:
        try:
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


@user_has_perms('reporting')
def report_view(request, report_id):
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


@user_has_perms('reporting', 'administer')
def views_edit_update(request):
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
                                        'source': column.column})
    else:
        data = {'success': False}

    return render_json_response(data)


@user_has_perms('reporting', 'administer')
def relationship_data(request):
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
    view_name = request.POST.get('view_name', '')
    view_description = request.POST.get('view_description', '')
    view_source = request.POST.get('view_source', '')
    column_names = get_request_array(request.POST, 'column_name')
    column_descriptions = get_request_array(request.POST, 'column_description')
    column_sources = get_request_array(request.POST, 'column_source')
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
                ViewColumns.objects.filter(view=view).delete()
            for i, column_name in column_names.iteritems():
                column = ViewColumns()
                column.name = column_name
                column.description = column_descriptions[i]
                column.column = column_sources[i]
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


@user_has_perms('reporting', 'administer')
def views_list(request):
    views = Views.objects.all().order_by('name')
    view_list = dict()
    for view in views:
        view_list.update({view.id: view.name})

    return render_json_response(view_list)


@user_has_perms('reporting', 'administer')
def view_columns_list(request):
    view = request.GET.get('view', False)

    reporting = reporting_store()
    view_column_list = reporting.get_columns(view)

    return render_json_response(view_column_list)
