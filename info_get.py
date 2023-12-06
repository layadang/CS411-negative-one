import os
import requests
import json

with open('secret/api-key.json', 'r') as api_file:
    api = json.load(api_file)

def make_api_request(url, params, headers):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        res = response.json() 

        return(res)
    
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None


def find_movie(title):
    movie_name = title.replace(" ", "%20")
    api_url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/" + movie_name
    params = {
        'info': 'base_info',
        'exact': 'true',
        'titleType': 'movie',
    }

    headers = {
        "X-RapidAPI-Key": api.get("laya-Key"),
        "X-RapidAPI-Host": api.get("laya-Host")
    }

    res = make_api_request(api_url, params, headers)
    try: 
        image_url = res['results'][0]['primaryImage']['url']
    except TypeError as e:
        image_url = ""
    except IndexError as e:
        image_url = ""
    try:
        description = res['results'][0]['plot']['plotText']['plainText']
    except TypeError as e:
        description = ""
    except IndexError as e:
        description = ""
    try:
        genres = res['results'][0]['genres']['genres']
        genres_str = ', '.join([genre['text'] for genre in genres])
    except TypeError as e:
        genres_str = ""
    except IndexError as e:
        genres_str = ""

    return title, image_url, description, genres_str

#print(find_movie("Nefarious"))
# print(find_movie("The Avengers"))

# find_movie("The Hunger Games")