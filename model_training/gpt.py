import os
from openai import OpenAI
from pathlib import Path
import re
import json

with open('secret/gpt.json', 'r') as config_file:
    config = json.load(config_file)

client = config.get("gpt_api_key")

def next_movies(list_of_movies):
    # Example list of movies
    # list_of_movies = "1. Inception\n2. The Shawshank Redemption\n3. The Dark Knight\n4. Pulp Fiction\n5. The Godfather"
    
    user_message = "A person likes these movies: " + list_of_movies + "; Can you recommend 10 different movies the person may also like? Only output a list with title of the movie and year in parenthesis behind the title."

    messages = [
        {"role": "system", "content": 'You recommend movies to a person based on the other movies they like.'},
        {"role": "user", "content": user_message},
    ]

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )

    recommendations_content = chat_completion.choices[0].message.content

    # Use regular expression to match movie names and years
    movie_matches = re.findall(r'\d+\.\s+(.+)\s+\((\d{4})\)', recommendations_content)

    # Create a list of movie json objects with names and years
    movies_list = [{"title": match[0], "year": int(match[1])} for match in movie_matches]

    # Return the list of next movies
    return movies_list