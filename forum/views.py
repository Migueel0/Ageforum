from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import password_changed
from django.http import HttpResponse
from django.http.request import validate_host
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

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


def sign_up(request):
    """
    Show sign up form when accessing through GET and try to sign up when accessing through POST
    """
    if request.method == 'GET':
        form = SignUpForm()
        context = {
            'form': form
        }
        return render(request, SIGN_UP_TEMPLATE, context)
    elif request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(INDEX_ROUTE)
        else:
            context = {
                'form': form
            }
            return render(request, SIGN_UP_TEMPLATE, context)


def login(request):
    """
    Show login form when executing through GET and try to login when executing through POST
    """
    if request.method == 'GET':
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, LOGIN_TEMPLATE, context)
    elif request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request,
                                username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])
            # A backend authenticated the credentials
            return HttpResponseRedirect(INDEX_ROUTE)
        else:
            context = {
                'login_form': login_form
            }
            return render(request, LOGIN_TEMPLATE, context)
