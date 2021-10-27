from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, response, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import make_password, check_password

from .models import Author, Post, Response
from .forms import AuthorCreateForm, AuthorLoginForm, PostCreateForm, ResponseForm

import datetime
import ast

ROOT_URL = '/'
AUTHOR_CREATE_URL = 'forum/author_create.html'

author_logged_in: Author
post_current: Post


def index(request):
    post_list = Post.objects.order_by('-pub_date')[:50]
    context = {
        'post_list': post_list,
        'author_logged_in': author_logged_in
    }
    return render(request, 'forum/index.html', context)


def post_detail(request, post_id):
    global post_current
    global author_logged_in
    post = get_object_or_404(Post, pk=post_id)
    post_current = post
    context = {'post': post,
               'author_logged_in': author_logged_in,
               }
    if author_logged_in:
        author = get_object_or_404(Author, pk=author_logged_in.id)
        author_logged_in = author
        author_post_votes = set(ast.literal_eval(author_logged_in.post_votes))
        author_response_votes = set(
            ast.literal_eval(author_logged_in.response_votes))
        context['author_post_votes'] = author_post_votes
        context['author_response_votes'] = author_response_votes
    return render(request, 'forum/post_detail.html', context)


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
            # check is username exists
            number_authors_with_same_username = Author.objects.filter(
                username=author.username).count()
            if number_authors_with_same_username != 0:
                # author_exists
                return render(request, AUTHOR_CREATE_URL, {'form': form, 'author_exist': True})
            author.email = form.cleaned_data['email']
            number_authors_with_same_email = Author.objects.filter(
                email=author.email).count()
            if number_authors_with_same_email != 0:
                # email exists
                return render(request, AUTHOR_CREATE_URL, {'form': form, 'email_exist': True})
            author.password = form.cleaned_data['password']
            password_repeat = form.cleaned_data['password_repeat']
            if(author.password != password_repeat):
                # password mismatch
                return render(request, AUTHOR_CREATE_URL, {'form': form, 'password_mismatch': True})
            # encode password
            author.password = make_password(author.password)
            author.avatar = form.cleaned_data['avatar']
            author.join_date = datetime.datetime.now(
                tz=datetime.timezone.utc)
            author.save()
            # set author logged in
            global author_logged_in
            author_logged_in = author
            # redirect to index:
            return HttpResponseRedirect(ROOT_URL)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthorCreateForm()
    return render(request, AUTHOR_CREATE_URL, {'form': form})


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
                # check if password encoded is equals to the password store in the DB
                if check_password(password, author.password):
                    last_login_date = datetime.datetime.now(
                        tz=datetime.timezone.utc)
                    author.last_login_date = last_login_date
                    author.save()
                    # set author logged in
                    global author_logged_in
                    author_logged_in = author
                    # redirect to index:
                    return HttpResponseRedirect(ROOT_URL)
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
    return HttpResponseRedirect(ROOT_URL)


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
            return HttpResponseRedirect(ROOT_URL)
    else:
        if author_logged_in == None:
            return HttpResponseRedirect(ROOT_URL)
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
            return HttpResponseRedirect(ROOT_URL + str(post.id))
    else:
        if author_logged_in == None:
            return HttpResponseRedirect(ROOT_URL)
        form = ResponseForm()

    return render(request, 'forum/response_create.html', {'form': form, 'author_logged_in': author_logged_in, 'post_current': post_current})


def author_details(request, author_id):
    """
    Show author details from author ID
    """
    author_details = Author.objects.get(pk=author_id)
    return render(request, 'forum/author_details.html', {'author_logged_in': author_logged_in, 'author_details': author_details})


def post_vote(request, author_id, post_id):
    """
    Vote or unvote question
    :returns 'Vote' if upvote is made. 'Unvote' is unvote is made
    """
    if request.method == 'POST':
        # search and set author by id
        global author_logged_in
        author_logged_in = get_object_or_404(Author, id=author_id)
        # Add vote to author post_vote string list
        author_post_votes = set(
            ast.literal_eval(author_logged_in.post_votes))
        if(post_id not in author_post_votes):  # vote
            author_post_votes.add(post_id)
            author_logged_in.post_votes = str(author_post_votes)
            # Sum vote to post
            post_current.votes += 1
            # save into DB
            author_logged_in.save()
            post_current.save()
            return HttpResponse("Vote")
        else:  # unvote
            author_post_votes.remove(post_id)
            author_logged_in.post_votes = str(author_post_votes)
            # Subtract vote to post
            post_current.votes -= 1
            # save into DB
            author_logged_in.save()
            post_current.save()
            return HttpResponse("Unvote")


def response_vote(request, author_id, response_id):
    """
    Vote or unvote response. 
    :returns 'Vote' if upvote is made. 'Unvote' is unvote is made
    """
    if request.method == 'POST':
        # search and set author by id
        global author_logged_in
        author_logged_in = Author.objects.get(id=author_id)
        # Add vote to author response_vote string list
        author_response_votes = set(
            ast.literal_eval(author_logged_in.response_votes))
        if(response_id not in author_response_votes):  # vote
            author_response_votes.add(response_id)
            author_logged_in.response_votes = str(author_response_votes)
            # Sum vote to response
            response = Response.objects.get(id=response_id)
            response.votes += 1
            # save into DB
            author_logged_in.save()
            response.save()
            return HttpResponse("Vote")
        else:  # unvote
            author_response_votes.remove(response_id)
            author_logged_in.response_votes = str(author_response_votes)
            # Subtract vote to response
            response = Response.objects.get(id=response_id)
            response.votes -= 1
            # save into DB
            author_logged_in.save()
            response.save()
            return HttpResponse("Unvote")
