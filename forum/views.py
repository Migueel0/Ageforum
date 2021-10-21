from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, response, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import Author,Post,Response
from .forms import AuthorCreateForm, AuthorLoginForm

import datetime


author_logged_in = None

def index(request):
    post_list = Post.objects.order_by('-pub_date')[:50]
    context = {
        'post_list': post_list,
        'author_logged_in': author_logged_in
    }
    return render(request, 'forum/index.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'forum/post_detail.html', {'post': post})

def author_create_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthorCreateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = Author()
            author.username = form.cleaned_data['username']
            author.password = form.cleaned_data['password']
            passwordRepeat = form.cleaned_data['passwordRepeat']
            if(author.password != passwordRepeat):
                #TODO raise error in form
                raise forms.ValidationError("Passwords do not match")
            author.email = form.cleaned_data['email']
            author.avatar = form.cleaned_data['avatar']
            author.join_date = datetime.datetime.now()
            author.save()
            #set author logged in
            global author_logged_in
            author_logged_in = author
            # redirect to index:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthorCreateForm()

    return render(request, 'forum/author_create_form.html', {'form': form})

def author_login_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthorLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = Author.objects.filter(username=form.cleaned_data['username']).first()
            password = form.cleaned_data['password']
            if author.password == password:
                #set author logged in
                global author_logged_in
                author_logged_in = author
                # redirect to index:
                return HttpResponseRedirect('/')
    else:
        form = AuthorLoginForm()

    return render(request, 'forum/author_login_form.html', {'form': form})

def author_logout(request):
    global author_logged_in
    author_logged_in = None
    return HttpResponseRedirect('/')