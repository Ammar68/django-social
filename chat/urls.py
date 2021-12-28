from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='chat'),
    path('<int:receiver_id>/', MessageListView.as_view()),
    path('friends', friend_list, name='friends'),
    path('groups', GroupsView.as_view(), name='groups'),
    path('groups/<str:group_id>/', GroupChatView.as_view(), name='group_chat'),
]
