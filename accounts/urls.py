from django.urls import path
from .views import PasswordsChangeView
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('accounts/logout/',view=views.logout_view,name='logout_view'),
    path('profile/<int:user_id>', views.user_detail, name='user_detail'),
    path('profile/', views.logged_user_detail, name='logged_user_detail'),
    path('change-profile', views.change_user_detail, name='change_user_detail'),
    #path('password', auth_views.PasswordChangeView.as_view(template_name = 'registration/change_password.html')),
    path('password', views.PasswordsChangeView.as_view(template_name = 'registration/change_password.html')),
    path("password_success", views.password_success, name ="password_success")
]
