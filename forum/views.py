from datetime import datetime, timedelta

import pytz
from Ageforum.settings import ROOT_URLCONF
from django.contrib.auth.password_validation import password_changed
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Max
from django.db.models.aggregates import Min
from django.db.models.functions import Coalesce
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from forum.forms import ContactForm, DiscussionCreateForm, MessageCreateForm


from .models import Discussion, Message, Response, Vote

# routes
INDEX_ROUTE = '/'

# templates urls
INDEX_TEMPLATE = 'forum/index.html'
DISCUSSION_CREATE_TEMPLATE = 'forum/discussion_create.html'
RESPONSE_CREATE_TEMPLATE = 'forum/response_create.html'
DISCUSSION_DETAIL_TEMPLATE = 'forum/discussion_detail.html'
CONTACT_TEMPLATE = 'forum/contact.html'

EDIT_DISCUSSION_TEMPLATE = 'forum/edit_text.html'
EDIT_RESPONSE_TEMPLATE = 'forum/edit_response_text.html'

RESPONSE_DELETE_TEMPLATE = 'forum/response_delete/<int:response.id>.html'
FORUM_EMAIL_ADDRESS = 'foro.age.of.empires.iv@outlook.com'

# Delete a discussion:


def delete_discussion(request, discussion_id):

    discussion = Discussion.objects.get(pk=discussion_id)
    if request.user.id != discussion.user.id:
        raise PermissionDenied()
    else:
        discussion.delete()

    return redirect(INDEX_ROUTE)


def delete_response(request, response_id):

    response = Response.objects.get(pk=response_id)

    if request.user.id != response.user.id:
        raise PermissionDenied()
    else:
        response.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def edit_text(request, discussion_id,):

    edit_text = Discussion.objects.get(pk=discussion_id)
    form = DiscussionCreateForm(data=request.POST or None, instance=edit_text)
    context = {
        'edit_text': edit_text,
        'form': form
    }
    if request.user.id != edit_text.user.id:
        raise PermissionDenied()
    else:
        if form.is_valid():
            form.save()
            return redirect('/' + str(discussion_id))
    return render(request, EDIT_DISCUSSION_TEMPLATE, context)


def edit_response_text(request, message_id,discussion_id):
    if not request.user.id:
        raise PermissionDenied()
    edit_response_text = Message.objects.get(pk=message_id)
    form = MessageCreateForm(data=request.POST or None,
                             instance=edit_response_text)
    context = {
        'edit_response_text': edit_response_text,
        'form': form
    }
    if form.is_valid():
        form.save()
        return redirect("/"+ str(discussion_id))
    return render(request, EDIT_RESPONSE_TEMPLATE, context)



def index(request):
    """
    Show all discussions ordered by last Response date
    """
    discussion_list = Discussion.objects.alias(
        latest_reply=Coalesce(
            Max('response__date_publication'), 'date_publication')
    ).order_by('-latest_reply')

    discussion_number_response_dict = __retrieve_discussion_number_response_dict(
        discussion_list)
    discussion_last_message_date_dict = __retrieve_discussion_last_message_date_dict(
        discussion_list)

    context = {
        'discussion_list': discussion_list,
        'discussion_number_response_dict': discussion_number_response_dict,
        'discussion_last_message_date_dict': discussion_last_message_date_dict
    }
    return render(request, INDEX_TEMPLATE, context)


def __retrieve_discussion_last_message_date_dict(discussion_list):
    """
    Return dictionary with date of last response for each discussion
    """
    discussion_last_message_date_dict = {}
    for discussion in discussion_list:
        last_discussion_reponse = Response.objects.filter(
            topic=discussion).order_by('date_publication').last()
        if last_discussion_reponse:
            discussion_last_message_date_dict[discussion.id] = __format_timedelta(
                datetime.now(pytz.utc) - last_discussion_reponse.date_publication)
        else:  # no responses in discussion yet -> show date of publication of discussion
            discussion_last_message_date_dict[discussion.id] = __format_timedelta(
                datetime.now(pytz.utc) - discussion.date_publication)
    return discussion_last_message_date_dict


def __format_timedelta(timedelta: timedelta):
    """
    Return timedelta in days, hours o minutes
    """
    days = timedelta.days
    hours = timedelta.seconds//3600
    minutes = timedelta.seconds//60
    if days > 0:
        return str(days) + 'd'
    elif hours > 0:
        return str(hours) + 'h'
    else:
        return str(minutes) + 'm'


def __retrieve_discussion_number_response_dict(discussion_list):
    """
    Return dictionary with number of responses for each discussion
    """
    discussion_number_response_dict = {}
    for discussion in discussion_list:
        response_count = Response.objects.filter(topic=discussion).count()
        discussion_number_response_dict[discussion.id] = response_count
    return discussion_number_response_dict


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
            if response.text:
                response.save()
                send_mail(
                    'Foro Age of Empires IV: Han respondido en tu discusión',
                    'Han respondido en tu discusión: https://www.foroageofempiresiv.com/' +
                    str(response.topic.id),
                    FORUM_EMAIL_ADDRESS,
                    [response.topic.user.email],
                    fail_silently=False,
                )
            return HttpResponseRedirect(INDEX_ROUTE + str(discussion_id))
    else:
        raise PermissionDenied()


def discussion_detail(request, discussion_id):
    """
    Show discussion and responses
    """
    if request.method == 'GET':
        discussion = get_object_or_404(Discussion, id=discussion_id)
        discussion.views += 1
        discussion.save()
        response_list = Response.objects.filter(
            topic=discussion).order_by('date_publication')
        vote_count_dict = __retrieve_discussion_votes(
            discussion, response_list)
        context = {
            'discussion': discussion,
            'response_list': response_list,
            'vote_count_dict': vote_count_dict,
        }
        # if user is logged in retrieve list of votes for that user and discussion
        if request.user.id:
            messages_voted_by_user_list = __retrieve_user_discussion_votes(
                request.user, discussion)
            context['messages_voted_by_user_list'] = messages_voted_by_user_list
        return render(request, DISCUSSION_DETAIL_TEMPLATE, context)
    else:
        raise PermissionDenied()


def __retrieve_discussion_votes(discussion, response_list):
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


def __retrieve_user_discussion_votes(user, discussion):
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
    message_to_reply: Message = Message.objects.get(id=message_id)
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
            # send email to user of message replied (reply_to)
            email_user = message_to_reply.user.email
            send_mail(
                'Foro Age of Empires IV: Han respondido a tu mensaje',
                'Han respondido a tu mensaje: https://www.foroageofempiresiv.com/' +
                str(response.topic.id),
                FORUM_EMAIL_ADDRESS,
                [email_user],
                fail_silently=False,
            )
            # send mail to author of discussion if it is different. Otherwise he/she will receive 2 emails
            email_discussion_author = response.topic.user.email
            if email_discussion_author != email_user:
                send_mail(
                    'Foro Age of Empires IV: Han respondido en tu discusión',
                    'Han respondido en tu discusión: https://www.foroageofempiresiv.com/' +
                    str(response.topic.id),
                    FORUM_EMAIL_ADDRESS,
                    [email_discussion_author],
                    fail_silently=False,
                )
            return HttpResponseRedirect(INDEX_ROUTE + str(discussion_id))
    else:
        raise PermissionDenied()


def contact(request):
    """
    Show form to contact us when GET and send the message to us when POST
    """
    if request.method == 'GET':
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, CONTACT_TEMPLATE, context)
    elif request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                'Desde: '+form.cleaned_data['email'] +
                '. Mensaje: ' + form.cleaned_data['message'],
                FORUM_EMAIL_ADDRESS,
                [FORUM_EMAIL_ADDRESS],
                fail_silently=False,
            )
            return HttpResponseRedirect(INDEX_ROUTE)
    else:
        raise PermissionDenied()

def error_404(request,exception):
        return render(request,'forum/404_error.html', status=404)

#def error_500(request):
#        data = {}
#       return render(request,'myapp/error_500.html', data)
