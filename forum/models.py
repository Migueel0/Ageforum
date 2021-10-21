from typing_extensions import Required
from django.db import models

class Author(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(required=True)
    join_date = models.DateTimeField('join date')
    last_login_date = models.DateTimeField()
    avatar = models.ImageField(upload_to='avatar')

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    post_title = models.CharField(max_length=200)
    post_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title  

class Response(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    votes = models.IntegerField(default=0)

    def __str__(self):
        return 'Response of: ' + self.post.post_title  