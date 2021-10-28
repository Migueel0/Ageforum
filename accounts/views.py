from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from accounts.forms import SignUpForm


PROFILE_INFO_TEMPLATE = "registration/user_info.html"


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'


def user_info(request):
    """
    Show user profile info
    """
    context = {
        'user': request.user,
    }
    return render(request, PROFILE_INFO_TEMPLATE, context)
