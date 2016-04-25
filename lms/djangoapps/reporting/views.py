from mitxmako.shortcuts import render_to_response


def reports_view(request):
    return render_to_response('reporting/reports.html')

