from django.db import models

# Create your models here.

class profile(models.Model):
    date = models.DateField()
    movie = models.CharField(max_length=50)
    show = models.CharField(max_length=50) 

class actor(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return self.name
    
class movie(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateField()
    actors = models.ManyToManyField(actor)

    def __str__(self):
        return self.title
    
class show(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateField()
    actors = models.ManyToManyField(actor)

    def __str__(self):
        return self.title
