from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render

from .models import Discussion

INDEX_ROUTE = '/'
INDEX_TEMPLATE = 'forum/index.html'
SIGN_UP_TEMPLATE = 'forum/sign_up.html'
LOGIN_TEMPLATE = 'forum/login.html'


def index(request):
    """
    Show all discussions
    """
    discussion_list = Discussion.objects.order_by('-date_publication')[:50]
    context = {
        'discussion_list': discussion_list,
    }
    return render(request, INDEX_TEMPLATE, context)