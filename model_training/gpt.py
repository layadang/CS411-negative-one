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
# Expects string input list_of_movies for movies that user has liked
def next_movies(list_of_movies):
    
    user_message = "A person likes these movies: " + list_of_movies + "; Can you recommend 10 different movies the person may also like? Only output a list with title of the movie and year in parenthesis behind the title."

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