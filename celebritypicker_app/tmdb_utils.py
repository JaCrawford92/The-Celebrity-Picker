import requests
from django.conf import settings

def get_popular_celebrities(region=None):
    url = 'https://api.themoviedb.org/3/person/popular'
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

def get_celebrities_by_date(date):
    popular_people_url = 'https://api.themoviedb.org/3/person/popular'
    person_details_url = 'https://api.themoviedb.org/3/person/{}?language=en-US'
    params = {
        'api_key': settings.TMDB_API_KEY
    }
    try:
        response = requests.get(popular_people_url, params=params)
        response.raise_for_status()
        celebrities = response.json().get('results', [])
        print(f"TMDB celebrities: {celebrities}")
        filtered_celebrities = []
        for celeb in celebrities:
            person_response = requests.get(person_details_url.format(celeb['id']), params=params)
            person_response.raise_for_status()
            celeb_details = get_celebrity_details(celeb['id'])
            print(f"Checking celebrity: {celeb_details['name']} with birthday {celeb_details.get('birthday')}")
            if celeb_details.get('birthday') == date.strftime('%Y-%m-%d'):
                celeb_details['works'] = celeb_details.get('known_for', [])
                filtered_celebrities.append(celeb_details)
        print(f"Filtered celebrities: {filtered_celebrities}")
        return filtered_celebrities
    except requests.RequestException as e:
        print(f"Error fetching celebrities by date: {e}")
        return []