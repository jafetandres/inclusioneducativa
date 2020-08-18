import uuid
from django.db import models
from core.models import Usuario


class UserProfile(models.Model):
    user = models.OneToOneField(Usuario,
                                on_delete=models.CASCADE, related_name='profile')
    last_visit = models.DateTimeField()


# This model is used to give date and time when a message was created/modified.
class DateTimeModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Room(DateTimeModel):
    name = models.CharField(max_length=50, blank=True, null=True)
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    members = models.ManyToManyField(Usuario)

    def __str__(self):
        memberset = self.members.all()
        members_list = []
        for member in memberset:
            members_list.append(member.username)

        return ", ".join(members_list)


class Message(DateTimeModel):
    sender = models.ForeignKey(Usuario,
                               on_delete=models.CASCADE, related_name='sender')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    recipients = models.ManyToManyField(Usuario,
                                        related_name='recipients')

    def __str__(self):
        return f'{self.text} sent by "{self.sender.nombres}" in Room "{self.room}"'

    class Meta:
        ordering = ['-id']
