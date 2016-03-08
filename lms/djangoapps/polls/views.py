from mitxmako.shortcuts import render_to_response
from django.http import HttpResponse
from .models import poll_store
from datetime import datetime
from django.utils import timezone
import json
import urllib2
from math import floor


def poll_form_view(request, poll_type=None):
    if poll_type:
        return render_to_response('polls/' + poll_type + '_form.html')


def poll_form_submit(request, poll_type):
    try:
        poll_id = request.POST.get('poll_id')
        question = request.POST.get('question')
        answers = get_post_array(request.POST, 'answers')
        expiration = request.POST.get('expiration', '')
        expiration_object = None
        if expiration:
            expiration_object = datetime.strptime(expiration, '%m/%d/%Y')
        poll_connect = poll_store()
        poll_connect.set_poll(poll_type, poll_id, question, answers, expiration_object)
        response = {'Success': True}
    except Exception as e:
        response = {'Success': False, 'Error': 'Error: {0}'.format(e)}

    return HttpResponse(json.dumps(response), content_type='application/json')


def vote_calc(poll_dict, poll_type, poll_id):
    poll_connect = poll_store()
    votes = dict()
    total = 0
    for idx, answer in poll_dict['answers'].iteritems():
        votes.update({idx: {'count': poll_connect.get_answers(poll_type, poll_id, idx).count()}})
        total += votes[idx]['count']

    for key, vote in votes.iteritems():
        vote.update({'percent': floor((vote['count'] / total) * 100) if total else 0})

    return votes


def poll_data(poll_type, poll_id, user_id):
    poll_connect = poll_store()
    poll_dict = poll_connect.get_poll(poll_type, poll_id)
    user_answered = poll_connect.user_answered(poll_type, poll_id, user_id)

    votes = vote_calc(poll_dict, poll_type, poll_id)

    if poll_dict['expiration'] > timezone.now():
        expired = False
    else:
        expired = True

    data = {'question': poll_dict['question'],
            'answers': poll_dict['answers'],
            'expiration': poll_dict['expiration'],
            'expired': expired,
            'user_answered': user_answered,
            'votes': votes,
            'poll_type': poll_dict['type'],
            'poll_id': poll_dict['identifier'],
            }
    return data


def poll_view(request, poll_type, poll_id):
    data = poll_data(poll_type, poll_id, request.user.id)
    return render_to_response('polls/' + poll_type + '_poll.html', data)


def poll_vote(request):
    try:
        poll_type = request.POST.get('poll_type')
        poll_id = request.POST.get('poll_id')
        vote = request.POST.get('vote')

        poll_connect = poll_store()

        poll_connect.set_answer(poll_type, poll_id, request.user.id, vote)

        poll_dict = poll_connect.get_poll(poll_type, poll_id)

        votes = vote_calc(poll_dict, poll_type, poll_id)

        response = {'Success': True, 'Votes': votes, 'Answers': poll_dict['answers']}
    except Exception as e:
        response = {'Success': False, 'Error': 'Error: {0}'.format(e)}

    return HttpResponse(json.dumps(response), content_type='application/json')


def get_post_array(post, name):
    """
    Gets array values from a POST.
    """
    output = dict()
    for key in post.keys():
        value = urllib2.unquote(post.get(key))
        if key.startswith(name + '[') and not value == 'undefined':
            start = key.find('[')
            i = key[start + 1:-1]
            output.update({i: value})
    return output
