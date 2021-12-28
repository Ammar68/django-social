from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *


class IndexView(TemplateView):
    template_name = 'chat.html'
    
    def get(self, request, *args, **kwargs):
        user_id = request.user
        friend_list = FriendList.objects.filter(user_id_id=user_id)
        return render(template_name=self.template_name, request=request, context={'list' : friend_list,})

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')


def friend_list(request):
    list = FriendList.objects.all()#filter(user_id=request.user.id)
    return render(template_name='friends.html', request=request, context={'list' : list})


class MessageListView(TemplateView):
    sender = None
    receiver = None
    
    def get(self, request, receiver_id, *args, **kwargs):
        self.get_sender(request.user)
        self.get_receiver(User.objects.get(pk=receiver_id))
        try:
            list = self.get_query()
        except Message.DoesNotExist:
            return render(template_name='messages.html', request=request, context={'list' : "No messages found !", 'reciver_id': self.receiver.id})
        else :
            return render(template_name='messages.html', request=request, context={'list' : list})

    def post(self, request, receiver_id, *args, **kwargs):
        Message.objects.create(message_content=request.POST.get('message'), from_user=request.user, to_user_id=receiver_id)
        return render(template_name='messages.html', request=request, context={'list' : self.get_query()})
    
    def get_query(self):
        list = Message.objects.filter(
            Q(from_user=self.sender, to_user_id=self.receiver.id) | Q(to_user_id=self.sender.id, from_user=self.receiver)
            ).order_by('sent_at')
        return list
    
    def get_sender(self, user):
        self.sender = user
    
    def get_receiver(self, user):
        self.receiver = user
    

class GroupsView(TemplateView):
    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(template_name='groups.html', request=request, context={"groups" : groups})

    def post(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(template_name='groups.html', request=request, context={"groups" : groups})


class GroupChatView(TemplateView):
    group = None

    def get(self, request, group_id, *args, **kwargs):
        self.set_group(group_id)
        return render(template_name='group_chat.html', request=request, context={'list' : self.get_messages(), 'reciver_id': group_id})

    def post(self, request, group_id, *args, **kwargs):
        self.set_group(group_id)
        message = request.POST.get('message')
        self.send_message(message,request.user)
        return render(template_name='group_chat.html', request=request, context={'list' : self.get_messages(), 'reciver_id': group_id})

    def get_messages(self):
        group = self.get_group()
        return Group.messages.all()
        
    def set_group(self, group):
        group = Group.objects.get(group_id=group)
        self.group = group

    def get_group(self):
        return self.group

    def send_message(self, message, user):
        msg = GroupMessage.objects.add(message_content=message, from_user=user)
        Group.messages.add(msg)
        