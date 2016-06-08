
from .models import ReportViews
from .models import reporting_store

school_year_collection = ['UserView', 'UserCourseView']


def report_has_school_year(columns):
    for col in columns:
        if col.column.data_type == 'time':
            return True
    return False


def get_school_year_item():
    data = []
    rs = reporting_store()
    rs.set_collection(school_year_collection[0])
    result = rs.collection.group({'school_year': 1}, {}, {}, 'function(obj,prev){}')
    for item in result:
        data.append(item['school_year'])
    return sorted(data, cmp=None, key=None, reverse=True)


def get_query_school_year(request, report, columns):
    selected_view = ReportViews.objects.filter(report=report)[0]
    if report_has_school_year(columns):
        school_year_item = request.GET.get('school_year', 'all')
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
        return ''
