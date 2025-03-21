
from django import template
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render
from accounts.forms import EditForm, SignUpForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login,logout
from django.template.defaulttags import register

from forum.models import Discussion, Response, User, Vote


ROOT_URL = '/'

PROFILE_INFO_TEMPLATE = "registration/user_detail.html"
SIGN_UP_TEMPLATE = 'registration/sign_up.html'
CHANGE_INFO_TEMPLATE = 'registration/change_user_detail.html'
CHANGE_PASSWORD_TEMPLATE = 'registration/change_password.html'
PASSWORD_SUCCESS_TEMPLATE = 'registration/password_success.html'


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_success")


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = SIGN_UP_TEMPLATE

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(ROOT_URL)
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(ROOT_URL)

def password_success(request):
    return render(request, PASSWORD_SUCCESS_TEMPLATE)


def user_detail(request, user_id):
    """
    Show user profile info
    """
    if request.method == 'GET':
        discussion_list = Discussion.objects.filter(
            user=user_id).order_by('-date_publication')
        response_list = Response.objects.filter(
            user=user_id).order_by('-date_publication')

        # elements needed for showing user likes
        vote_list = Vote.objects.filter(
            user=get_object_or_404(User, id=user_id))
        vote_list = list(vote_list)
        discussion_in_vote_list = retrieve_discussion_in_vote_list(vote_list)
        range_vote_list = range(len(vote_list))

        context = {
            'user': get_object_or_404(User, id=user_id),
            'discussion_list': discussion_list,
            'response_list': response_list,
            'discussion_in_vote_list': discussion_in_vote_list,
            'vote_list': vote_list,
            'range_vote_list': range_vote_list,
        }
        return render(request, PROFILE_INFO_TEMPLATE, context)
    else:
        raise PermissionDenied()


def logged_user_detail(request):
    """
    Show user logged in profile info
    """
    if request.method == 'GET':
        if request.user.id:
            discussion_list = Discussion.objects.filter(
                user=request.user).order_by('-date_publication')
            response_list = Response.objects.filter(
                user=request.user).order_by('-date_publication')

            # elements needed for showing user likes
            vote_list = Vote.objects.filter(user=request.user)
            vote_list = list(vote_list)
            discussion_in_vote_list = retrieve_discussion_in_vote_list(
                vote_list)
            range_vote_list = range(len(vote_list))

            context = {
                'discussion_list': discussion_list,
                'response_list': response_list,
                'discussion_in_vote_list': discussion_in_vote_list,
                'vote_list': vote_list,
                'range_vote_list': range_vote_list,
            }
            return render(request, PROFILE_INFO_TEMPLATE, context)
        else:
            return HttpResponseRedirect(ROOT_URL)
    else:
        raise PermissionDenied()


def change_user_detail(request):
    """
    change user profile info
    """
    if not request.user.id:
        return HttpResponseRedirect(ROOT_URL)
    if request.method == 'GET':
        return render(request, CHANGE_INFO_TEMPLATE)
    elif request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user_email = form.cleaned_data['email']
            user_email = user_email.replace(" ", "")
            if (user_email == '' or not User.objects.filter(email=user_email).count() == 0) and user.email != user_email:
                # username empty or already exists
                form.add_error(
                    'email', 'La direccion de correo electrónico ya existe')
                context = {
                    'form': form
                }
                return render(request, CHANGE_INFO_TEMPLATE, context)
            user.email = user_email
            username_form = form.cleaned_data['username']
            username_form = username_form.replace(" ", "")
            if (username_form == '' or not User.objects.filter(username=username_form).count() == 0) and user.username != username_form:
                # username empty or already exists
                form.add_error(
                    'username', 'El nombre de usuario ya existe')
                context = {
                    'form': form
                }
                return render(request, CHANGE_INFO_TEMPLATE, context)
            user.username = username_form

            avatar_form = form.cleaned_data['avatar']
            if avatar_form:
                user.avatar = avatar_form
            biography_form = form.cleaned_data['biography']
            user.biography = biography_form
            user.save()
            return HttpResponseRedirect('/accounts/profile/')
        else:
            context = {
                'form': form
            }
            return render(request, CHANGE_INFO_TEMPLATE, context)
    else:
        raise PermissionDenied()


@register.filter
def get_message_from_vote_list(vote_list, index):
    return vote_list[index].message.text


@register.filter
def get_id_from_discussion_list(discussion_list, index):
    return discussion_list[index].id


def retrieve_discussion_in_vote_list(vote_list):
    """
    Returns a list of discussions given the list of votes
    """
    discussion_in_vote_list = []
    for vote in vote_list:
        discussion = Discussion.objects.filter(id=vote.message.id).first()
        if not discussion:
            response = Response.objects.get(id=vote.message.id)
            discussion = response.topic
        discussion_in_vote_list.append(discussion)
    return discussion_in_vote_list
