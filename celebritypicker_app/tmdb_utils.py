import requests
from django.conf import settings
from datetime import datetime

def get_popular_celebrities(page=1):
    url = 'https://api.themoviedb.org/3/person/popular'
    person_details_url = 'https://api.themoviedb.org/3/person/{}?language=en-US'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'page': page  # Add pagination parameter
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        celebrities = response.json().get('results', [])
        total_pages = response.json().get('total_pages', 1)  # Get the total number of pages
        
        detailed_celebrities = []
        for celeb in celebrities:
            person_response = requests.get(person_details_url.format(celeb['id']), params=params)
            person_response.raise_for_status()
            celeb_details = person_response.json()
            detailed_celebrities.append(celeb_details)
        
        return detailed_celebrities, total_pages
    except requests.RequestException as e:
        print(f"Error fetching popular celebrities: {e}")
        return [], 1 

def get_celebrity_details(celeb_id):
    url = f'https://api.themoviedb.org/3/person/{celeb_id}'
    params = {'api_key': settings.TMDB_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        celeb_data = response.json()
        base_img_url = 'https://image.tmdb.org/t/p/w100'  # You can adjust the size
        # Add profile image URL to celeb_data if it exists
        if celeb_data.get('profile_path'):
            celeb_data['profile_img_url'] = f"{base_img_url}{celeb_data['profile_path']}"
        else:
            celeb_data['profile_img_url'] = None  # Or a default placeholder image URL
        return celeb_data
    except requests.RequestException as e:
        print(f"Error fetching details for celebrity ID {celeb_id}: {e}")
        return {}

def get_celebrities_by_date(date, page=1, limit=10):
    popular_people_url = 'https://api.themoviedb.org/3/person/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'page': page
    }
    try:
        response = requests.get(popular_people_url, params=params)
        response.raise_for_status()
        celebrities = response.json().get('results', [])
        filtered_celebrities = []
        print(celebrities)
        for celeb in celebrities:
            if 'birthday' in celeb:
                # Convert the birthday to a datetime object
                birthday = datetime.strptime(celeb['birthday'], '%Y-%m-%d')
                # Extract month and day from the birthday and selected date
                birthday_month_day = birthday.strftime('%m-%d')
                selected_month_day = date.strftime('%m-%d')
                # Check if the month and day match
                if birthday_month_day == selected_month_day:
                    celeb_details = get_celebrity_details(celeb['id'])
                    celeb_details['works'] = celeb_details.get('known_for', [])
                    filtered_celebrities.append(celeb_details)
                    if len(filtered_celebrities) >= limit:
                        break
        return filtered_celebrities
    except requests.RequestException as e:
        print(f"Error fetching celebrities by date: {e}")
        return []

