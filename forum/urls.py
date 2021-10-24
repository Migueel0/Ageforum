from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>', views.post_detail, name='post_detail'),
    path('author_create_form', views.author_create_form, name='author_create_form'),
    path('author_login_form', views.author_login_form, name='author_login_form'),
    path('author_logout', views.author_logout, name='author_logout'),
    path('post_create', views.post_create, name='post_create'),
    path('response_create', views.response_create, name='response_create'),
    path('author_details', views.author_details, name='author_details'),
]
