from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, response, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import Author, Post, Response
from .forms import AuthorCreateForm, AuthorLoginForm, PostCreateForm, ResponseForm

import datetime


author_logged_in = None
post_current = None


# Django
def index(request):
    post_list = Post.objects.order_by('-pub_date')[:50]
    context = {
        'post_list': post_list,
        'author_logged_in': author_logged_in
    }
    return render(request, 'forum/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    global post_current
    post_current = post
    return render(request, 'forum/post_detail.html', {'post': post, 'author_logged_in': author_logged_in})


def author_create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthorCreateForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = Author()
            author.username = form.cleaned_data['username']
            #check is username exists
            authorWithSameUsername = Author.objects.filter(
                username=author.username)
            if len(authorWithSameUsername) == 0:
                author.password = form.cleaned_data['password']
                password_repeat = form.cleaned_data['password_repeat']
                if(author.password != password_repeat):
                    # TODO raise error in form
                    raise forms.ValidationError("Passwords do not match")
                author.email = form.cleaned_data['email']
                author.avatar = form.cleaned_data['avatar']
                author.join_date = datetime.datetime.now(tz=datetime.timezone.utc)
                author.save()
                # set author logged in
                global author_logged_in
                author_logged_in = author
                # redirect to index:
                return HttpResponseRedirect('/')
            else:
                return render(request, 'forum/author_create.html', {'form': form, 'author_exist':True})            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthorCreateForm()
    return render(request, 'forum/author_create.html', {'form': form})


def author_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthorLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = Author.objects.filter(
                username=form.cleaned_data['username']).first()
            if author:  # author exists
                password = form.cleaned_data['password']
                if author.password == password:
                    # set author logged in
                    global author_logged_in
                    author_logged_in = author
                    # redirect to index:
                    return HttpResponseRedirect('/')
                else:
                    login_error = True
            else:
                login_error = True
        else:
            login_error = True
            
        form = AuthorLoginForm()
        return render(request, 'forum/author_login.html',
                              {'form': form, 'author_logged_in': author_logged_in, 'login_error': login_error})
    else:
        form = AuthorLoginForm()
    return render(request, 'forum/author_login.html', {'form': form, 'author_logged_in': author_logged_in})


def author_logout(request):
    global author_logged_in
    author_logged_in = None
    return HttpResponseRedirect('/')


def post_create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostCreateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            author = author_logged_in
            post_title = form.cleaned_data['post_title']
            post_text = form.cleaned_data['post_text']
            pub_date = datetime.datetime.now(tz=datetime.timezone.utc)
            post = Post(author=author, post_title=post_title,
                        post_text=post_text, pub_date=pub_date)
            post.save()
            return HttpResponseRedirect('/')
    else:
        form = PostCreateForm()
    return render(request, 'forum/post_create.html', {'form': form, 'author_logged_in': author_logged_in})


def response_create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ResponseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        # process the data in form.cleaned_data as required
            author = author_logged_in
            post = post_current
            response_text = form.cleaned_data['response_text']
            pub_date = datetime.datetime.now(tz=datetime.timezone.utc)
            response = Response(author=author, post=post,
                            response_text=response_text, pub_date=pub_date)
            response.save()
            return HttpResponseRedirect('/' + str(post.id))
    else:
        form = ResponseForm()

    return render(request, 'forum/response_create.html', {'form': form, 'author_logged_in': author_logged_in, 'post_current': post_current})

def author_details(request):
    return render(request, 'forum/author_details.html', {'author_logged_in': author_logged_in})
    