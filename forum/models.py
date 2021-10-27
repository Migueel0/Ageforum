from django.db import models
from tinymce.models import HTMLField


class Author(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=30, unique=True)
    join_date = models.DateTimeField()
    last_login_date = models.DateTimeField(null=True)
    avatar = models.ImageField(upload_to='avatars', null=True)
    # post vote is a list with the ids of voted posts
    post_votes = models.CharField(max_length=1000, null=True,default='{}')
    response_votes = models.CharField(max_length=1000, null=True,default='{}')

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    post_title = models.CharField(max_length=200)
    post_text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title


class Response(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return 'Response of: ' + self.post.post_title
