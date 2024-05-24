from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('celebrity/<int:celeb_id>/', views.celebrity_details, name='celebrity_details'),
    path('celebrity/birthdays/', views.celebrity_birthdays, name='celebrity_birthdays'),
    path('celebrity/random/', views.random_movie_or_show, name='random_movie_or_show'),
]