import requests
from django.conf import settings
from datetime import datetime

def get_popular_celebrities(page=1):
    url = 'https://api.themoviedb.org/3/person/popular'
    person_details_url = 'https://api.themoviedb.org/3/person/{}?language=en-US'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'page': page
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        celebrities = response.json().get('results', [])
        
        detailed_celebrities = []
        for celeb in celebrities:
            person_response = requests.get(person_details_url.format(celeb['id']), params=params)
            person_response.raise_for_status()
            celeb_details = person_response.json()
            detailed_celebrities.append(celeb_details)
        
        total_pages = response.json().get('total_pages', 1)
        return detailed_celebrities, total_pages
    except requests.RequestException as e:
        print(f"Error fetching popular celebrities: {e}")
        return [], 1

def get_celebrity_details(celeb_id):
    url = f'https://api.themoviedb.org/3/person/{celeb_id}'
    combined_credits_url = f'https://api.themoviedb.org/3/person/{celeb_id}/combined_credits'
    params = {'api_key': settings.TMDB_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        celeb_data = response.json()
        print(f"Celebrity data {celeb_data}")

        # Fetch combined credits
        combined_credits_response = requests.get(combined_credits_url, params=params)
        combined_credits_response.raise_for_status()
        combined_credits_data = combined_credits_response.json()
        celeb_data['known_for'] = combined_credits_data.get('cast', [])
        print(f"Combined credits data {combined_credits_data}")

        return celeb_data
    except requests.RequestException as e:
        print(f"Error fetching details for celebrity ID {celeb_id}: {e}")
        return {}


def get_celebrities_by_date(date, page=1):
    url = 'https://api.themoviedb.org/3/person/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'page': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        celebrities = data.get('results', [])

        filtered_celebrities = []
        for celeb in celebrities:
            person_response = requests.get(f'https://api.themoviedb.org/3/person/{celeb["id"]}', params={'api_key': settings.TMDB_API_KEY})
            person_response.raise_for_status()
            person_details = person_response.json()
            if 'birthday' in person_details and person_details['birthday']:
                celeb_month_day = '-'.join(person_details['birthday'].split('-')[1:])  # Get the MM-DD part of the birthday
                if celeb_month_day == date:
                    filtered_celebrities.append(person_details)

        # total_pages = data.get('total_pages', 1)
        return filtered_celebrities
    except requests.RequestException as e:
        print(f"Error fetching celebrities by date: {e}")
        return [], 1


