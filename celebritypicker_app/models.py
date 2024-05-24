from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class UserActivity(models.Model):
    date = models.DateField()
    movie = models.CharField(max_length=50)
    show = models.CharField(max_length=50) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Actor(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    actors = models.ManyToManyField(Actor, related_name='movies')

    def __str__(self):
        return self.title
    
class Show(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    actors = models.ManyToManyField(Actor, related_name='shows')

    def __str__(self):
        return self.title
