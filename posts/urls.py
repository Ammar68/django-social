from django.urls import path
from .views import *

urlpatterns = [
    path(r'', IndexView.as_view(), name='home'),
    path(r'profile/', ProfileView.as_view(), name='profile'),
    path(r'login/', Login.as_view(), name='login'),
    path(r'signup/', Signup.as_view(), name='signup'),
    path(r'logout/', logout, name='logout'),
    path(r'<str: psot_id>', post_info, name='full_post')
    
]
