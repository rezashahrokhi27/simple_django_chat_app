from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Chat(models.Model):
    roomname = models.CharField(blank=True, max_length=50)
    members = models.ManyToManyField(user, null=True, blank=True)

    def __str__(self):
        return self.roomname



class Message(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    related_chat = models.ForeignKey(Chat, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_message(self, roomname):
        return Message.objects.filter(related_chat__roomname=roomname).order_by('-timestamp')
    def __str__(self):
        return f'{self.author.username}'