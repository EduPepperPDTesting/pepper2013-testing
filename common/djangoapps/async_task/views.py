from models import AsyncTask
from django.http import HttpResponse
import json


def ajax_get_async_task(request):
    task = AsyncTask.objects.get(id=request.REQUEST.get('id'))

    seconds = (task.update_time - task.create_time).seconds

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    r = {'id': task.id,
         'title': task.title,
         'last_message': task.last_message,
         'status': task.status,
         'task_running_time': "%d:%02d:%02d" % (h, m, s)
         }

    return HttpResponse(json.dumps(r), content_type="application/json")

