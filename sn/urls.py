from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('chat/', include('chat.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
]
