from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    AbstractUser._meta.get_field('email')._unique = True
    avatar = models.ImageField(upload_to='avatars', blank=True)
    biography = models.TextField(max_length=100, blank =True)
  


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100000,blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return super().__hash__()


class Discussion(Message):
    title = models.CharField(max_length=500)
    views = models.PositiveBigIntegerField(default=0)


class Response(Message):
    topic = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='message_replied', null=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'message'], name='unique_user_vote')
        ]
