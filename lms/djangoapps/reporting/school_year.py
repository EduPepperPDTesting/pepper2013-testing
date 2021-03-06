
from .models import ReportViews
from .models import reporting_store

school_year_collection = ['UserView', 'UserCourseView', 'PDPlannerView']


def report_has_school_year(columns):
    for col in columns:
        if col.column.data_type == 'time' or col.column.data_type == 'clk':
            return True
    return False


def get_school_year_item():
    rs = reporting_store()
    rs.set_collection(school_year_collection[0])
    result = rs.collection.distinct('school_year')
    return sorted(result, cmp=None, key=None, reverse=True)


def get_default_school_year_item(school_year_item):
    if school_year_item == '':
        rs = reporting_store()
        rs.set_collection(school_year_collection[0])
        result = list(rs.collection.find({'school_year': 'current'}))
        if result:
            school_year_item = 'current'
        else:
            school_year_item = 'all'
    return school_year_item


def get_query_school_year(request, report, columns):
    selected_view = ReportViews.objects.filter(report=report)[0]
    if report_has_school_year(columns):
        school_year_item = request.GET.get('school_year', '')
        school_year_item = get_default_school_year_item(school_year_item)
        if selected_view.view.collection in school_year_collection:
            if school_year_item != 'all':
                return '{"$match":{"school_year":"' + school_year_item + '"}},'
            else:
                return ''
        else:
            if school_year_item != 'all':
                return str(["$$item.school_year", school_year_item])
            else:
                return str([1, 1])
    else:
        if selected_view.view.collection in school_year_collection:
            return '{"$match":{"school_year":"current"}},'
        else:
            return str(["$$item.school_year", "current"])
