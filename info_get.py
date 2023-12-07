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

# hardcoding in incorrect movie info that the api gets
# realistically - api should have a sort by most popular option...
# not implementing search movie+year (we don't trust GPT to return correct year most of the time)

def find_movie(title):
    if (title == "500 Days of Summer"):
        title = "(500) Days of Summer" # (good movie <3)
    
    movie_name = title.replace(" ", "%20")
    api_url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/" + movie_name

    params = {
        'info': 'base_info',
        'exact': 'true',
        'titleType': 'movie',
    }

    # found these errors while manually testing
    if (title == "Tangled"):
        params['year'] = '2010'
    if (title == "Beauty and the Beast"):
        params['year'] = '1991'
    if (title == "Clueless"):
        params['year'] = '1995'
    if (title == "Her"):
        params['year'] = '2013'
    if (title == "Coco"):
        params['year'] = '2017'
    if (title == "Inside Out"):
        params['year'] = '2015'
    if (title == "Whiplash"):
        params['year'] = '2014'
    if (title == "The Holiday"):
        params['year'] = '2006'
    if (title == "Aladdin"):
        params['year'] = '2019'
    if (title == "About Time"):
        params['year'] = '2013'

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

# print(find_movie("Beauty and the Beast"))
