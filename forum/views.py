from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Author,Post,Response


def index(request):
    post_list = Post.objects.order_by('-pub_date')[:50]
    context = {
        'post_list': post_list,
    }
    return render(request, 'forum/index.html', context)