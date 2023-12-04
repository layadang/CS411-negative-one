import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(Path(".env"))

client = OpenAI(api_key=os.getenv("gpt_api_key"))

# Example list of movies
list_of_movies = "1. Inception\n2. The Shawshank Redemption\n3. The Dark Knight\n4. Pulp Fiction\n5. The Godfather"
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
print(recommendations_content)