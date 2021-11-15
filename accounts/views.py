from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render
from accounts.forms import EditForm, SignUpForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login

from forum.models import Discussion, Response, User


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
        discussion_list = Discussion.objects.filter(user=user_id).order_by('date_publication').reverse()
        response_list = Response.objects.filter(user=user_id).order_by('date_publication').reverse() 
        context = {
            'user': get_object_or_404(User, id=user_id),
            'discussion_list':discussion_list, 
            'response_list':response_list
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
            discussion_list = Discussion.objects.filter(user=request.user).order_by('date_publication').reverse()
            response_list = Response.objects.filter(user=request.user).order_by('date_publication').reverse()
            context = {
                'discussion_list':discussion_list, 
                'response_list':response_list

            }
            return render(request, PROFILE_INFO_TEMPLATE,context)
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
            username_form = form.cleaned_data['username']
            username_form.replace(" ", "")
            if username_form == '' or not User.objects.filter(username=username_form).count() == 0:
                # username empty or already exists
                form.add_error('username','El nombre de usuario ya existe')
                context = {
                    'form': form
                }
                return render(request, CHANGE_INFO_TEMPLATE, context)        
            user.username = username_form
            avatar_form = form.cleaned_data['avatar']
            if avatar_form:
                user.avatar = avatar_form
            user.save()
            return HttpResponseRedirect('/accounts/profile/')
        else:
            context = {
                'form': form
            }
            return render(request, CHANGE_INFO_TEMPLATE, context)
    else:
        raise PermissionDenied()
