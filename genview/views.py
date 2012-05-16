from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import randint, shuffle, random, seed
from snag.genview import models
from sys import *

# Home page
def home(request):
    # about
    about = ['un', 'dos', 'tres']

    # gen
    gen = []
    for alels in range(1, 33):
        gen.append(alels)
    shuffle(gen)

    # auth
    if request.user.is_authenticated():
        auth = "<p>User is authenticated as: <b>"+request.user.username+"</b></p>"

    else:
        auth = "<p>User is anonymous</p>"

    #about = models.Page.objects.get(id=1)
    #pics_list = models.Pic.objects.order_by('-id')[:49]
    ##r = randint(0, (len(pics_list)-1))
    ##pic_random = pics_list[r]
    return render_to_response('home.html', {'home': home, 'about': about, 'gen': gen, 'auth': auth})

# Test page: javascript timing test
def testpage(request):
    if request.user.is_authenticated():
        auth = "<p>User is authenticated</p>"
    else:
        auth = "<p>User is anonymous</p>"

    return render_to_response('testpage.html', {'testpage': testpage, 'auth': auth})

def profile(request):

    if request.user.is_authenticated():
        auth = "<p>User profile.</p>"
        auth += "<p>Hello {{ user.username }}. User is authenticated</p>"
    else:
        auth = "<p>User is anonymous</p>"

    #about = models.Page.objects.get(id=1)
    #pics_list = models.Pic.objects.order_by('-id')[:49]
    ##r = randint(0, (len(pics_list)-1))
    ##pic_random = pics_list[r]
    return render_to_response('profile.html', {'auth': auth })


'''
# Conversations
def conversations_list(request):
    about = models.Page.objects.get(id=1)
    conversations_list = models.Conversation.objects.order_by('-date')
    ##pics_in_conversation = get_list_or_404(models.Pic.objects.order_by('-conversation'))
    paginator = Paginator(conversations_list, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        conversations_list_pag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        conversations_list_pag = paginator.page(paginator.num_pages)
    return render_to_response('latest_conversations.html', {'about': about, 'conversations_list': conversations_list, 'conversations_list_pag': conversations_list_pag })

def conversation_item(request, conversation_id):
    conversation_item = get_object_or_404(models.Conversation, pk=conversation_id)
    return render_to_response('conversation_item.html', { 'conversation_item' : conversation_item })
    #parts = get_list_or_404(models.Participant, conversation=conversation_id)
    #return render_to_response('conversation_item.html', { 'parts': parts, 'conversation_item' : conversation_item,})

# Participants
def participants_list(request):
    participants_list = models.Participant.objects.order_by('-last_name')
    paginator = Paginator(participants_list, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        participants_list_pag = paginator.page(page)
    except (EmptyPage, InvalidPage):
        participants_list_pag = paginator.page(paginator.num_pages)

    return render_to_response('participants_list.html', {'participants_list': participants_list, 'participants_list_pag': participants_list_pag})

def participant_item(request, participant_id):
    participant_item = get_object_or_404(models.Participant, pk=participant_id)
    in_conversations = get_list_or_404(models.Conversation.objects.order_by('-date'), participants=participant_id)
    #in_conversations =''
    return render_to_response('participant_item.html', {'participant_item': participant_item, 'in_conversations': in_conversations })

'''
