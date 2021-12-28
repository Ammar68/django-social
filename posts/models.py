from django.db import models
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    friends = models.ManyToManyField('self')
    


class Post(models.Model):
    user = models.ForeignKey(Person, related_name='+', on_delete=models.CASCADE)
    content = models.TextField()
    media = models.ImageField(upload_to='files/', default=None)
    likers = models.ManyToManyField(Person, through='Like')
    comments = models.ManyToManyField('Comment', through='CommentPostRelation')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.content


class Comment(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentPostRelation(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)