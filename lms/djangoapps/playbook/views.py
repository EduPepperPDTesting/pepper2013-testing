from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from mitxmako.shortcuts import render_to_response, render_to_string
import json

from playbook.models import Play, Category, PlaybookTags

import logging
log = logging.getLogger("tracking")

@login_required
def playbook(request):
    categories = Category.objects.all()

    return render_to_response('playbook/playbook.html', {'categories': categories})

@login_required
def create_new_play(request):
    if request.method == 'POST':
        creator = request.user
        title = request.POST.get('title')
        category = Category.objects.get(pk=int(request.POST.get('category')))
        duration = int(request.POST.get('duration'))
        tip = request.POST.get('tip')
        tags = request.POST.get('tags')
        
        new_play = Play(title=title, category=category, duration=duration, tip=tip, creator=creator)
        new_play.save()
        if tags != '':
            for tag in tags.split(','):
                try:
                    playbook_tag = PlaybookTags.objects.get(name=tag)
                except PlaybookTags.DoesNotExist:
                    playbook_tag = PlaybookTags.objects.create(name=tag, creator=creator)
                new_play.tags.add(playbook_tag)

    return redirect(reverse('playbook'))

@login_required
def edit_play(request):
    if request.method == 'POST':
        modifier = request.user
        play = Play.objects.get(pk=request.POST.get('play_id'))
        title = request.POST.get('title')
        category = Category.objects.get(pk=int(request.POST.get('category')))
        duration = int(request.POST.get('duration'))
        tip = request.POST.get('tip')
        tags = request.POST.get('tags')
        play.modifier = modifier
        play.title = title
        play.category = category
        play.duration = duration
        play.tip = tip
        play.tags.clear()
        if tags != '':
            for tag in tags.split(','):
                try:
                    playbook_tag = PlaybookTags.objects.get(name=tag)
                except PlaybookTags.DoesNotExist:
                    playbook_tag = PlaybookTags.objects.create(name=tag, creator=modifier)
                play.tags.add(playbook_tag)
        play.save()

    return redirect(reverse('play_detail', args=[play.pk]))

def get_plays(request):
    """ for debug """
    if request.GET.get('category') == '-1':
        plays = Play.objects.all()
        play_list = []
        for play in plays:
            p = {}
            p['title'] = play.title
            play_list.append(p)
        return HttpResponse(json.dumps({'plays':play_list}))

def get_play_list(request):
    play_list_fragment = ''
    category_id = int(request.GET.get('category'))

    if category_id == -1:
        plays = Play.objects.all()
    else:
        plays = Play.objects.get(category=category_id)

    for play in plays:
        data = {}
        data['play_id'] = play.pk
        data['title'] = play.title
        data['step_nums'] = 0
        data['category_name'] = play.category.name
        data['created_time'] = play.created_time
        data['creator'] = play.creator.profile.getFullname();
        play_list_fragment += render_to_string('playbook/play-list-in-tenant-fragment.html', data)

    return HttpResponse(play_list_fragment)

@login_required
def create_new_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            category = Category.objects.get(name=name)
            return render_to_response('playbook/create_category.html', {'created': 'False'})
        except Category.DoesNotExist:
            creator = request.user
            new_category = Category(name=name, creator=creator)
            new_category.save()
            return render_to_response('playbook/create_category.html', {'created': 'True'})
    if request.method == 'GET':
        return render_to_response('playbook/create_category.html', {'created': 'False'})
        
@login_required
def play_detail(request, play_pk):

    play = Play.objects.get(pk=play_pk)

    categories = Category.objects.all()
    tag_list = []
    for tag in play.tags.all():
        tag_list.append(tag.name)
    tags = ','.join(tag_list)

    data = {'play': play, 'categories': categories, 'tags': tags}

    return render_to_response('playbook/play_detail.html', data)
