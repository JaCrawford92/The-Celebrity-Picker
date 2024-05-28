from django.shortcuts import render, redirect
from .forms import DateForm, UserProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from .tmdb_utils import get_popular_celebrities, get_celebrity_details, get_celebrities_by_date
from django.http import JsonResponse
import random
import json
from .models import UserProfile, RandomPick, Movie, Show

def home(request):
    page = request.GET.get('page', 1)  # Get the current page from the query parameter
    try:
        page = int(page)
    except ValueError:
        page = 1

    celebrities, total_pages = get_popular_celebrities(page=page)  # Get celebrities and total pages

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

def clear_filter(request):
    if 'selected_date' in request.session:
        del request.session['selected_date']
    return redirect('celebrity_birthdays')

def celebrity_birthdays(request):
    form = DateForm(request.POST or None)
    page = request.GET.get('page', 1)
    selected_date = None
    celebrities = []
    total_pages = 1

    if request.method == 'POST' and form.is_valid():
        selected_date = form.cleaned_data['selected_date']
        request.session['selected_date'] = selected_date
        page = 1  # Store the selected date (MM-DD) in session

    if 'selected_date' in request.session:
        selected_date = request.session['selected_date']

    if selected_date:
        if isinstance(selected_date, str):
            date_str = selected_date
        else:
            date_str = selected_date.strftime('%m-%d')
        celebrities, total_pages = get_celebrities_by_date(date_str, page=page)
    else:
        celebrities, total_pages = get_popular_celebrities(page=page)

    return render(request, 'celebritypicker/celebrity_birthdays.html', {
        'form': form,
        'celebrities': celebrities,
        'selected_date': selected_date,
        'total_pages': total_pages,
        'current_page': int(page)
    })

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
        # Log the structure of chosen_work
        print(json.dumps(chosen_work, indent=4))
        # Safely access the keys
        title = chosen_work.get('title') or chosen_work.get('name')
        if title:
            overview = chosen_work.get('overview', 'No overview available')
            poster_path = chosen_work.get('poster_path')
            return JsonResponse({'title': title, 'overview': overview, 'poster_path': poster_path})
        else:
            return JsonResponse({'error': 'No title or name found for the selected work!'})
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

@csrf_exempt
@login_required
def save_random_pick(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        overview = data.get('overview')
        poster_path = data.get('poster_path')
        
        if title and overview:
            RandomPick.objects.create(user=request.user, title=title, overview=overview, poster_path=poster_path)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def mark_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pick_id = data.get('pick_id')
        try:
            random_pick = RandomPick.objects.get(id=pick_id, user=request.user)
            random_pick.is_favorite = True
            random_pick.save()
            return JsonResponse({'status': 'success'})
        except RandomPick.DoesNotExist:
            return JsonResponse({'error': 'Random pick not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def unmark_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pick_id = data.get('pick_id')
        try:
            random_pick = RandomPick.objects.get(id=pick_id, user=request.user)
            random_pick.is_favorite = False
            random_pick.save()
            return JsonResponse({'status': 'success'})
        except RandomPick.DoesNotExist:
            return JsonResponse({'error': 'Random pick not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_pick(request, pick_id):
    try:
        random_pick = RandomPick.objects.get(id=pick_id, user=request.user)
        if not random_pick.is_favorite:
            random_pick.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Cannot delete favorite pick'}, status=400)
    except RandomPick.DoesNotExist:
        return JsonResponse({'error': 'Random pick not found'}, status=404)

    
# @csrf_exempt
# @login_required
# def add_favorite_movie(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         movie_id = data.get('movie_id')
#         try:
#             movie = Movie.objects.get(id=movie_id)
#             profile = UserProfile.objects.get(user=request.user)
#             profile.favorites_movies.add(movie)
#             return JsonResponse({'status': 'success'})
#         except Movie.DoesNotExist:
#             return JsonResponse({'error': 'Movie not found'}, status=404)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# @csrf_exempt
# @login_required
# def add_favorite(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         media_type = data.get('media_type')
#         media_id = data.get('media_id')
#         if media_type and media_id:
#             response = tmdb_favorite_action(media_type, media_id, favorite=True)
#             return JsonResponse(response)
#         return JsonResponse({'error': 'Invalid data'}, status=400)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# @csrf_exempt
# @login_required
# def remove_favorite(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         media_type = data.get('media_type')
#         media_id = data.get('media_id')
#         if media_type and media_id:
#             response = tmdb_favorite_action(media_type, media_id, favorite=False)
#             return JsonResponse(response)
#         return JsonResponse({'error': 'Invalid data'}, status=400)
#     return JsonResponse({'error': 'Invalid request'}, status=400)


   