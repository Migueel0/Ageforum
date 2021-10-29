from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render

from forum.forms import DiscussionCreateForm

from .models import Discussion

INDEX_ROUTE = '/'
INDEX_TEMPLATE = 'forum/index.html'
DISCUSSION_CREATE_TEMPLATE = 'forum/discussion_create.html'
DISCUSSION_DETAIL_TEMPLATE = 'forum/discussion_detail.html'


def index(request):
    """
    Show all discussions
    """
    discussion_list = Discussion.objects.order_by('-date_publication')[:50]
    context = {
        'discussion_list': discussion_list,
    }
    return render(request, INDEX_TEMPLATE, context)


def discussion_create(request):
    """
    Show form to create a discussion when GET and create a discussion when
    """
    if request.method == 'GET':
        form = DiscussionCreateForm()
        context = {
            'form': form
        }
        return render(request, DISCUSSION_CREATE_TEMPLATE, context)
    elif request.method == 'POST':
        form = DiscussionCreateForm(request.POST)
        if form.is_valid:
            discussion = form.save()
            #TODO NOT NULL constraint failed: forum_message.date_publication
            context = {
                'discussion': discussion
            }
            return render(request, DISCUSSION_DETAIL_TEMPLATE, context)