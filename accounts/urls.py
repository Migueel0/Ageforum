from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('profile/', views.user_info, name='user_info'),
]