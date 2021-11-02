from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render
from accounts.forms import SignUpForm
from django.core.exceptions import PermissionDenied

from forum.models import User



PROFILE_INFO_TEMPLATE = "registration/user_detail.html"
SIGN_UP_TEMPLATE = 'registration/sign_up.html'


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = SIGN_UP_TEMPLATE


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