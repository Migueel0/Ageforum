from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    avatar = models.ImageField(upload_to='avatars', blank=True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100000)
    date_publication = models.DateTimeField()

    def __str__(self):
        return self.id

class Discussion(Message):
    title = models.CharField(max_length=1000)

class Response(Message):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)