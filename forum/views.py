from os import cpu_count
from django.contrib.auth.password_validation import password_changed
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.defaulttags import register
from django.core.exceptions import PermissionDenied

from Ageforum.settings import ROOT_URLCONF

from forum.forms import DiscussionCreateForm, MessageCreateForm

from .models import Discussion, Message, Response, Vote

# routes
INDEX_ROUTE = '/'
# templates urls
INDEX_TEMPLATE = 'forum/index.html'
DISCUSSION_CREATE_TEMPLATE = 'forum/discussion_create.html'
RESPONSE_CREATE_TEMPLATE = 'forum/response_create.html'
DISCUSSION_DETAIL_TEMPLATE = 'forum/discussion_detail.html'


def index(request):
    """
    Show all discussions
    """
    discussion_list = Discussion.objects.order_by('date_publication')
    context = {
        'discussion_list': discussion_list,
    }
    return render(request, INDEX_TEMPLATE, context)


def discussion_create(request):
    """
    Show form to create a discussion when GET and create a discussion when POST. Otherwise, if user is not logged in redirects to index page
    """
    if not request.user.id:
        raise PermissionDenied()
    if request.method == 'GET':
        form = DiscussionCreateForm()
        context = {
            'form': form
        }
        return render(request, DISCUSSION_CREATE_TEMPLATE, context)
    elif request.method == 'POST':
        form = DiscussionCreateForm(data=request.POST)
        if form.is_valid():
            discussion = Discussion()
            discussion.user = request.user
            discussion.title = form.cleaned_data['title']
            discussion.text = form.cleaned_data['text']
            discussion.save()
            return HttpResponseRedirect(INDEX_ROUTE + str(discussion.id))
    else:
        raise PermissionDenied()


def response_create(request, discussion_id):
    """
    Show form to create a response when GET and create a response when POST
    """
    if not request.user.id:
        raise PermissionDenied()
    if request.method == 'GET':
        form = MessageCreateForm()
        context = {
            'form': form,
            'discussion_id': discussion_id,
        }
        return render(request, RESPONSE_CREATE_TEMPLATE, context)
    elif request.method == 'POST':
        form = MessageCreateForm(data=request.POST)
        if form.is_valid():
            response = Response()
            response.topic = get_object_or_404(Discussion, id=discussion_id)
            response.user = request.user
            response.text = form.cleaned_data['text']
            response.save()
            return HttpResponseRedirect(INDEX_ROUTE + str(discussion_id))
    else:
        raise PermissionDenied()


def discussion_detail(request, discussion_id):
    """
    Show discussion and responses
    """
    if request.method == 'GET':
        discussion = get_object_or_404(Discussion, id=discussion_id)
        response_list = Response.objects.filter(
            topic=discussion).order_by('date_publication')
        vote_count_dict = retrieve_discussion_votes(discussion, response_list)
        context = {
            'discussion': discussion,
            'response_list': response_list,
            'vote_count_dict': vote_count_dict,
        }
        # if user is logged in retrieve list of votes for that user and discussion
        if request.user.id:
            messages_voted_by_user_list = retrieve_user_discussion_votes(
                request.user, discussion)
            context['messages_voted_by_user_list'] = messages_voted_by_user_list
        return render(request, DISCUSSION_DETAIL_TEMPLATE, context)
    else:
        raise PermissionDenied()


def retrieve_discussion_votes(discussion, response_list):
    """
    Return a dictionary of votes for given discussion and responses
    """
    vote_count_dict = {}
    vote_count_dict[discussion.id] = Vote.objects.filter(
        message=discussion).count()
    for response in response_list:
        vote_count_dict[response.id] = Vote.objects.filter(
            message=response).count()
    return vote_count_dict


def retrieve_user_discussion_votes(user, discussion):
    """
    Return list of messages voted given user and discussion
    """
    discussion_and_responses = [discussion]
    discussion_and_responses += Response.objects.filter(topic=discussion)
    user_discussion_votes = Vote.objects.filter(
        message__in=discussion_and_responses).filter(user=user)
    messages_voted_by_user_list = []
    for vote in user_discussion_votes:
        messages_voted_by_user_list.append(vote.message)
    return messages_voted_by_user_list


@register.filter
def get_item_from_dict(dictionary, key):
    """
    Return value from key in a dictionary
    """
    return dictionary[key]


def message_vote(request, message_id):
    """
    Add or remove vote
    """
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        vote_user_message = Vote.objects.filter(
            user=request.user).filter(message=message)
        if(vote_user_message.count() == 0):
            new_vote = Vote(user=request.user, message=message)
            new_vote.save()
            return HttpResponse('vote')
        elif(vote_user_message.count() == 1):
            vote_user_message.delete()
            return HttpResponse('unvote')
    else:
        raise PermissionDenied()


def response_reply_create(request, discussion_id, message_id):
    """
    Show form to create a reply to a message when GET and create a reply for given message when POST
    """
    if not request.user.id:
        raise PermissionDenied()
    message_to_reply = Message.objects.get(id=message_id)
    if request.method == 'GET':
        form = MessageCreateForm()
        context = {
            'form': form,
            'discussion_id': discussion_id,
            'message_to_reply': message_to_reply
        }
        return render(request, RESPONSE_CREATE_TEMPLATE, context)
    elif request.method == 'POST':
        form = MessageCreateForm(data=request.POST)
        if form.is_valid():
            response = Response()
            response.topic = get_object_or_404(
                Discussion, id=discussion_id)
            response.reply_to = message_to_reply
            response.user = request.user
            response.text = form.cleaned_data['text']
            response.save()
            return HttpResponseRedirect(INDEX_ROUTE + str(discussion_id))
    else:
        raise PermissionDenied()
