import os
import requests
import json

def make_api_request(url, params, headers):
    try:

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        res = response.json()

        return(res['results'][0]['primaryImage']['url'])
    
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None


def find_movie(title):

    api_url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/" + title
    params = {
        'info': 'base_info',
        'titleType': 'movie',
    }

    headers = {
        "X-RapidAPI-Key": "deba0d8e00msh8e8b85337b08fc9p10c542jsn1c6116b93fb4",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    return make_api_request(api_url, params, headers)

print(find_movie("Nefarious"))