from django.contrib.auth import get_user_model
from django.db import models
from django_chatter.models import DateTimeModel
from core.models import Usuario

User = Usuario


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username


class Room(DateTimeModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    participants = models.ManyToManyField(
        User, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)
