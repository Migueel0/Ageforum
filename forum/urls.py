from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('discussion_create', views.discussion_create, name='discussion_create'),
]

