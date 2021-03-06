from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Message, User, Discussion, Response, Vote

admin.site.register(User, ModelAdmin)
admin.site.register(Discussion)
admin.site.register(Response)
admin.site.register(Message)
admin.site.register(Vote)
