from django.contrib import admin

from .models import Author,Post,Response

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Response)