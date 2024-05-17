import requests
from django.conf import settings

def get_popular_movies(region=None):
    url = 'https://api.themoviedb.org/3/movie/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'region': region  # Optionally filter popular movies by region
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        # Log error here (if logging is configured)
        print(f"Error fetching popular movies: {e}")
        return {}  # Return an empty dictionary or use a more sophisticated error handling strategy

def get_celebrity_details(celeb_id):
    url = f'https://api.themoviedb.org/3/person/{celeb_id}'
    params = {'api_key': settings.TMDB_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Consider logging the error or handling it appropriately
        print(f"Error fetching details for celebrity ID {celeb_id}: {e}")
        return {}

        