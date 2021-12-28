from django.contrib import admin
from .models import Message, FriendList, Group, GroupMessage, Membership

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user_id', 'sent_at')
    list_filter = ('from_user', 'to_user_id')


@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'friend_id', 'start_date')
    list_filter = ('user_id', 'friend_id')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by',]
    list_filter = ('created_by',)

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'sent_at')
    list_filter = ('from_user', )

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['group', 'person']
    list_filter = ['group', 'person']