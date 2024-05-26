from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    favorites = models.ManyToManyField('Movie', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class UserActivity(models.Model):
    date = models.DateField()
    movie = models.CharField(max_length=50)
    show = models.CharField(max_length=50) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Actor(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    biography = models.CharField(blank=True)
    profile_img_url = models.URLField(blank=True)

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
    
class RandomPick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

