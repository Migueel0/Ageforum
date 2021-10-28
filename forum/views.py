from django.http import HttpResponse
from django.http.request import validate_host
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError

from forum.forms import UserSignUpForm

from .models import Discussion

ROOT_ROUTE = '/'

def index(request):
    """
    Show all discussions
    """
    discussion_list = Discussion.objects.order_by('-date_publication')[:50]
    context = {
        'discussion_list': discussion_list,
    }
    return render(request, 'forum/index.html', context)


def author_sign_up(request):
    """
    Show author sign up form when accessing through GET and try to sign up author when accessing through POST
    """
    if request.method == 'GET':
        form = UserSignUpForm()
        context = {
            'form':form
        }
        return render(request, 'forum/author_sign_up.html', context)
    elif request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(ROOT_ROUTE)
        else:
            return render(request, 'forum/author_sign_up.html')
    
