import os
import requests
import json

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
        'exact' :'true',
        'titleType': 'movie',
    }

    headers = {
        "X-RapidAPI-Key": "deba0d8e00msh8e8b85337b08fc9p10c542jsn1c6116b93fb4",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    res = make_api_request(api_url, params, headers)
    image_url = res['results'][0]['primaryImage']['url']
    description = res['results'][0]['plot']['plotText']['plainText']
    genres = res['results'][0]['genres']['genres']
    genres_str = ', '.join([genre['text'] for genre in genres])

    return title, image_url, description, genres_str

#print(find_movie("Nefarious"))
# print(find_movie("The Avengers"))

# find_movie("The Hunger Games")