from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import User

admin.site.register(User, ModelAdmin)
