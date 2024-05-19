from django.shortcuts import render, redirect
from django.contrib.auth import login
from django. contrib.auth.forms import UserCreationForm
from .tmdb_utils import get_popular_movies, get_celebrity_details
from django.http import JsonResponse
# Create your views here.
def home(request):
    popular_movies = get_popular_movies()
    return render(request, 'celebritypicker/home.html', {'popular_movies': popular_movies})

def about(request):
    return render(request, 'celebritypicker/about.html')

def signup(request):
  error_message = ''
  # if method is a POST request
  if request.method == 'POST':
    # user data from the signup form
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # our new user is saved!
      user = form.save()
      # login our newly signed up user
      login(request, user)
      # redirect them to the homepage
      return redirect('index')
    # else form is not valid, give the user an error message
    else: 
      error_message = 'Invalid sign up - try again'
  # GET request or a bad POST request, render out an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  # render out the signup page, with an error message or not!
  return render(request, 'registration/signup.html', context)

def celebrity_details(request, celeb_id):
    celeb_details = get_celebrity_details(celeb_id)
    base_img_url = 'https://image.tmdb.org/t/p/w500'
    profile_img_url = f"{base_img_url}{celeb_details.get('profile_path')}" if celeb_details.get('profile_path') else None
    return render(request, 'celebritypicker/celebrity_details.html', {
       'celeb_details': celeb_details, 
       'profile_img_url': profile_img_url
       })
