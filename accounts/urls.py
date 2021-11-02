from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('profile/<int:user_id>', views.user_detail, name='user_detail'),
    path('profile/', views.logged_user_detail, name='logged_user_detail'),
]