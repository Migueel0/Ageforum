from datetime import datetime
from django.db import connection, models
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

    def save(self, *args, **kwargs):
        # Insertar manualmente en forum_message
        super().save(*args, **kwargs)
        message_id = self.id + 100
        date = datetime.now()
        cursor = connection.cursor()
        text = self.text
        if self.text == '':
            text = "''"
        message_query = "INSERT INTO forum_message (id, user_id, text, date_publication) VALUES (%s, %s, %s, %s)" % (message_id, self.user.id,text, f"'{date}'")
        print(message_query)
        cursor.executescript(message_query)
        cursor.close()
        
        cursor = connection.cursor()
        query = "INSERT INTO forum_discussion (message_ptr_id, views,title) VALUES ('%s', '%s', '%s')" % (message_id, self.views, self.title)
        print(query)
        cursor.executescript(query)  
        

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
