from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=500)
    email = models.CharField(max_length=64)



class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.IntegerField()
    author_id = models.IntegerField()
    author_username = models.CharField(max_length=64)
    body = models.CharField(max_length=256)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

 

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    author_id = models.IntegerField()
    author_username = models.CharField(max_length=64)
    # comments = models.ManyToManyField(Comment, related_name="comments", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

