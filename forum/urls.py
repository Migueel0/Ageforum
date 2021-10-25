from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>', views.post_detail, name='post_detail'),
    path('author_create', views.author_create, name='author_create'),
    path('author_login', views.author_login, name='author_login'),
    path('author_logout', views.author_logout, name='author_logout'),
    path('post_create', views.post_create, name='post_create'),
    path('response_create', views.response_create, name='response_create'),
    path('author_details/<int:author_id>', views.author_details, name='author_details'),
    path('tinymce/', include('tinymce.urls')),
]
