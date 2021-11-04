from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render
from accounts.forms import SignUpForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login

from forum.models import User


ROOT_URL = '/'

PROFILE_INFO_TEMPLATE = "registration/user_detail.html"
SIGN_UP_TEMPLATE = 'registration/sign_up.html'
CHANGE_INFO_TEMPLATE = 'registration/change_user_detail.html'

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


def user_detail(request, user_id):
    """
    Show user profile info
    """
    if request.method == 'GET':
        context = {
            'user': get_object_or_404(User, id=user_id),
        }
        return render(request, PROFILE_INFO_TEMPLATE, context)
    else:
        raise PermissionDenied()


def logged_user_detail(request):
    """
    Show user logged in profile info
    """
    if request.method == 'GET':
        context = {
            'user': get_object_or_404(User, id=request.user.id),
        }
        return render(request, PROFILE_INFO_TEMPLATE, context)
    else:
        raise PermissionDenied()


def change_user_detail(request):
    """
    change user profile info
    """
    if request.method == 'GET':
        context = {
            'user': get_object_or_404(User, id=request.user.id),
        }
        return render(request, CHANGE_INFO_TEMPLATE, context)
    else:
        raise PermissionDenied()
