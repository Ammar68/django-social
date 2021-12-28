from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


class FriendList(Model):
    user_id = models.ForeignKey('posts.Person', on_delete=models.CASCADE)
    friend_id = models.CharField(max_length=32)
    start_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user_id.username


class MessageManager(models.Manager):
    def create_message(self, message_content, from_user, to_user_id):
        message = self.create(message_content, from_user, to_user_id)

class Message(Model):
    message_content = models.CharField(max_length=256)
    from_user = models.ForeignKey('posts.Person', on_delete=models.CASCADE)
    to_user_id =  models.CharField(max_length=32)
    sent_at = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)
    
    objects = MessageManager()

    def __str__(self) -> str:
        return self.from_user.username


class Group(Model):
    name = models.CharField(max_length=64)
    created_by = models.CharField(max_length=16)
    group_id = models.CharField(max_length=32, unique=True, null=False)
    users = models.ManyToManyField('posts.Person', through='Membership')
    messages = models.ManyToManyField('GroupMessage', through='GroupMessageRelation')

    def __str__(self) -> str:
        return self.name
    
    def get_users(self, group_id):
        users = Membership.objects.filter(group=self)
        return users


class Membership(models.Model): 
    person = models.ForeignKey('posts.Person', on_delete=models.CASCADE) 
    group = models.ForeignKey(Group, on_delete=models.CASCADE) 
    date_joined = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64, default=None, null=True)


class GroupMessage(Model):
    message_content = models.CharField(max_length=256)
    from_user = models.ForeignKey('posts.Person', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.from_user.username

class GroupMessageRelation(Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE) 
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE)
