############################################################
# NOTE: this file interacts directly with the gpt api, be  #
# careful about calling it because we are on a hard limit  #
# token count, don't call more than you need to            #
############################################################

import os
from openai import OpenAI
from pathlib import Path
import re
import json

with open('secret/gpt.json', 'r') as config_file:
    config = json.load(config_file)

client = OpenAI(api_key=config.get("gpt_api_key"))

# Example list of movies
# Uncomment for testing
# test_list_of_movies = "1. Inception\n2. The Shawshank Redemption\n3. The Dark Knight\n4. Pulp Fiction\n5. The Godfather"

# Returns the recommended movies
# Expects string input liked_movies and string input disliked_movies
# Year is no longer used but I don't wanna remove it because then it wouldn't make sense to give the result in a dictionary and then I gotta change how that's handled in app.py and it's gonna break things
def next_movies(liked_movies, disliked_movies):
    
    user_message = "A person likes these movies: " + liked_movies + "; but dislikes these movies: " + disliked_movies + "; Can you recommend 10 movies that are not already listed that the person may enjoy watching? Only output a list with title of the movie and year in parenthesis behind the title."

    messages = [
        {"role": "system", "content": 'You recommend movies as a numbered list to a person based on the other movies they like.'},
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
    # Theoretically could fetch with something like movies_list[0]["title"]
    movies_list = [{"title": match[0], "year": int(match[1])} for match in movie_matches]

    # Print to terminal for verification
    print("fetched")

    # Return the list of next movies
    return movies_list

# Uncomment for testing
# print(next_movies(test_list_of_movies))