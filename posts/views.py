from django.core.exceptions import ValidationError
from django.http import response
from posts.forms import UserForm
from django.db import models
from django.forms.forms import Form
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, LoginView, redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.views.generic.base import View
from .models import Comment, Person, Post
from chat.models import Message, Group, GroupMessage


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'index.html'
    login_url = '/login/' 
    redirect_field_name = 'redirect_to'
    
    posts = Post.objects.all().order_by('created_at').reverse()
    context = {
        "posts" : posts,
        "page_name" : 'Social',
        }

    def get(self, request, *args, **kwargs):
        self.set_user(request.user)
        if request.user.is_anonymous:
            return redirect('/login')
        return render(template_name='index.html', request=request, context=self.context)

    def post(self, request, *args, **kwargs):
        content = request.POST.get('post_content')
        postMedia = request.POST.get('postMedia')
        print("\n\n\n {} \n\n\n".format(postMedia))
        if request.user.is_anonymous:
            return redirect('/login')
        if content:
            if content is None:
                raise ValueError("Content Can't be empty.")
            elif len(content) > 0:
                newPost = Post.objects.create(content=content, user=request.user, media=postMedia)
        if request.POST.get('like'):
            post = Post.objects.get(pk=request.POST.get('post'))
            if request.user not in post.likers.all():
                post.likers.add(request.user)
            elif request.user in post.likers.all():
                pass
        if request.POST.get('search_query'):
            posts = Post.objects.filter(content__contains=request.POST.get('search_query'))
            self.context['posts'] = posts
        if request.POST.get('comment'):
            post = Post.objects.get(pk=request.POST.get('post'))
            post.comments.add(Comment.objects.create(content=request.POST.get('comment'), user=request.user))
        return self.get(request)
    
    def set_user(self, user):
        self.user = user
    
    def get_user(self):
        return self.user


class Login(TemplateView):
    
    def get(self, request, *args, **kwargs):
        context = {}
        return render(template_name='registration/login.html', request=request, context=context)

    def post(self, request, *args, **kwargs):
        context = {}
        login = LoginView.as_view()(request)
        if login:
            return HttpResponseRedirect('/')
        else:
            return render(template_name='registration/login.html', request=request, context=context)

class Signup(View):
    form = UserCreationForm
    context = {
        'form' : form,
        'page_name' : "Signup new User",
    }
    def get(self, request):
        if request.user.is_authenticated:
            redirect('/')
        return render(template_name='registration/signup.html', request=request, context=self.context)
    def post(self, request):
        try :
            if request.POST.get('password1') == request.POST.get('password2'):
                user = Person.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password1'), first_name=request.POST.get('fname'), last_name=request.POST.get('lname'))
            else :
                self.context['message'] = "Password Error : Please enter your password again."
                return self.get(request)
            login = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
            if login:
                self.context = {}
                return redirect('/')
        except Exception as e:
            self.context.update({'message' : e})
            return render(template_name='registration/signup.html', request=request, context=self.context)
        print(user.username)


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        userForm = UserForm(instance=request.user)
        return render(template_name='profile.html', request=request, context={'form' : userForm})

    def post(self, request, *args, **kwargs):
        userForm = UserForm(request.POST)
        try :
            if userForm.is_valid():
                userForm.save()
        except Exception as e:
            print(e)
            raise ValidationError('Error', 'Error with the profile data')
        return render(template_name='profile.html', request=request, context={'form' : userForm})

def post_info(request, post_id):
    return response.HttpResponse("error{}".format(post_id))

@login_required(login_url='/login/')
def logout(request):
    return LogoutView.as_view(next_page='/login/')(request)

