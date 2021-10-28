from django.urls import path

from .views import SignUpView


urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
]