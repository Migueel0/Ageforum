from django.http import HttpResponse, response
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import Author,Post,Response


def index(request):
    post_list = Post.objects.order_by('-pub_date')[:50]
    context = {
        'post_list': post_list,
    }
    return render(request, 'forum/index.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'forum/post_detail.html', {'post': post})

def author_form(request):
    author = Author()
    return render(request, 'forum/author_form.html', {'author': author})