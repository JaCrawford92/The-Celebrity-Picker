from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('celebrity/picker/', views.celebritypicker_index, name='index'),
    path('celebrity/<int:celeb_id>/', views.celebrity_details, name='celebrity_details'),
]