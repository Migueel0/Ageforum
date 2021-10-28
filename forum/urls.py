from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('author_sign_up', views.author_sign_up, name='author_sign_up'),
]
