from django.urls import path


from accounts import urls

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('discussion_create', views.discussion_create, name='discussion_create'),
    path('response_create/<int:discussion_id>',
         views.response_create, name='response_create'),
    path('response_reply_create/<int:discussion_id>/<int:message_id>',
         views.response_reply_create, name='response_reply_create'),
    path('<int:discussion_id>', views.discussion_detail, name='discussion_detail'),
    path('message_vote/<int:message_id>',
         views.message_vote, name='message_vote'),
    path('delete_discussion/<int:discussion_id>',
         views.delete_discussion, name='delete-discussion'),
    path('delete_response/<int:response_id>',
         views.delete_response, name='delete-response'),
    path('contact', views.contact, name='contact'),
]
