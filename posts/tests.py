from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import response
from django.test import TestCase
from .models import Post

class PostModelTest(TestCase):
    def test_creating_posts(self):
        User.objects.create(username='amar', password='1234')
        user = User.objects.get(username='amar')
        post = Post(content="New post created", user=user)
        self.assertEqual(str(post), post.content)
        #self.fail("Test Failed. Not yet emplemented")
    def test_plural_name(self):
        self.assertEqual(str(Post._meta.verbose_name_plural), "posts")


class ProjectViewTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
    
    def test_home_for_auth_user(self):
        User.objects.create(username='amar', password='1234')
        self.client.post('/login/', context={'username' : 'amar', 'password' : '1234'})
        #user = authenticate(username='amar', password='1234')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
