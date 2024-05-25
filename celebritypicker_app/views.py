from django.shortcuts import render, redirect
from .forms import DateForm, UserProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .tmdb_utils import get_popular_celebrities, get_celebrity_details, get_celebrities_by_date
from django.http import JsonResponse
from datetime import datetime
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile, RandomPick, Movie, Show, Actor, UserActivity


def home(request):
    page = request.GET.get('page', 1)  # Get the current page from the query parameter
    celebrities, total_pages = get_popular_celebrities(page=page)  # Get celebrities and total pages

    paginator = Paginator(celebrities, 10)  # Show 10 celebrities per page
    try:
        celebrities = paginator.page(page)
    except PageNotAnInteger:
        celebrities = paginator.page(1)
    except EmptyPage:
        celebrities = paginator.page(paginator.num_pages)

    return render(request, 'celebritypicker/home.html', {
        'popular_celebrities': celebrities,
        'total_pages': total_pages,
        'current_page': int(page)
    })

def about(request):
    return render(request, 'celebritypicker/about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def celebrity_birthdays(request):
    form = DateForm(request.POST or None)
    page = request.GET.get('page', 1)

    if request.method == 'POST' and form.is_valid():
        selected_date = form.cleaned_data['selected_date']
        celebrities = get_celebrities_by_date(selected_date, page=page)

        paginator = Paginator(celebrities, 10)  # Show 10 celebrities per page
        try:
            celebrities = paginator.page(page)
        except PageNotAnInteger:
            celebrities = paginator.page(1)
        except EmptyPage:
            celebrities = paginator.page(paginator.num_pages)

        context = {
            'celebrities': celebrities,
            'selected_date': selected_date,
            'form': form,
        }
        return render(request, 'celebritypicker/celebrity_birthdays.html', context)
    else:
        return render(request, 'celebritypicker/celebrity_birthdays.html', {'form': form})


def celebrity_details(request, celeb_id):
    celeb_details = get_celebrity_details(celeb_id)
    known_for = celeb_details.get('known_for', [])
    print(f"Known for: {known_for}")
    print(f"Details: {celeb_details}")

    if celeb_details.get('profile_path'):
        base_img_url = 'https://image.tmdb.org/t/p/w500'
        profile_image_url = f"{base_img_url}{celeb_details.get('profile_path')}"
    else:
        profile_image_url = None

    return render(request, 'celebritypicker/celebrity_details.html', {
       'celeb_details': celeb_details,
       'known_for': known_for,
       'profile_image_url': profile_image_url
    })


def random_movie_or_show(request):
    celeb_id = request.GET.get('celeb_id')
    celeb_details = get_celebrity_details(celeb_id)
    works = celeb_details.get('known_for', [])
    if works:
       chosen_work = random.choice(works)
       return JsonResponse({'title': chosen_work['title'], 'overview': chosen_work['overview']})
    return JsonResponse({'error': 'No known works found for this celebrity!'})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    random_picks = RandomPick.objects.filter(user=request.user)
    return render(request, 'celebritypicker/profile.html', {'profile': user_profile, 'random_picks': random_picks})

@login_required
def delete_pick(request, pick_id):
    RandomPick.objects.filter(id=pick_id, user=request.user).delete()
    return redirect('profile')

@login_required
def update_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'celebritypicker/update_profile.html', {'form': form})

   