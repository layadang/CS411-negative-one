# CS411 Team Negative One: Movie Recommendation Project

## Overview

This is a Movie Recommendation project that provides personalized movie recommendations to users. It utilizes a Flask-based front-end, LLM recommendation system through OpenAI, the IMDb public sample API, Google OAuth for authentication, and MongoDB to store user information. The project combines these technologies to deliver a seamless movie recommendation experience. The user interface is similar to Tinder. 

## Features

- **User Authentication**: Users can log in using their Google accounts via OAuth, ensuring secure and authenticated access to the system.

- **Movie Recommendations**: ChatGPT API is prompted with info about the user, and it provides movie recommendations based on a user's preferences and viewing history.

- **RapidAPI MovieDatabase**: The project uses the MovieDatabase API from RapidAPI to fetch movie data, including titles, years, images, genres, and plots.

- **User Profile**: User information, including their likes, dislikes, and starred movies, is stored in a MongoDB database.

## Prerequisites

Before you start, ensure you have Python installed and preferably using Python version 3.9.6. Please sync your Python path on your local machine and your Python interpreter to 3.9.6 if you are experiencing any issues.

## Getting Started

1. Clone the repository:

   ```bash
   git clone git@github.com:layadang/CS411-negative-one.git
   ```

2. Install dependencies:

   ```bash
   pip install request
   pip install flask
   pip install oauthlib
   pip install pymongo==4.6.1
   pip install pandas
   pip install openai
   pip install google.cloud (if you run dead code)
   ```
   refer to requirements.txt for more version info

3. Obtain Google OAuth API credentials:

   - must obtain MovieDatabase API key from Laya and Xinny (depending on which file you are trying to run)
   - must obtain Google Oauth credentials from Laya
   - must obtain ChatGPT API key from Xinny
   - must obtain Google Vertex AI API key from Xinny (if you run dead code)

5. Start the application:

   ```bash
   python app.py
   ```

6. Access the application in your web browser at `http://localhost:5001`.

## Usage

1. Log in using your Google account.
2. Explore movie recommendations based on your likes, dislikes, and watchlist.
3. Add movies to your watchlist and rate them to receive more personalized recommendations.

## License

This project is not currently licensed RIP.

## Contribution

This project is built by Team Negative One:
- Laya: front end via flask, oauth config
- Xinny: ~google vertex llm training with moviedatabase data~ integrating chatgpt api
- Harris, Cindy, Xavier: user info database through mongodb

Happy movie watching! 🍿🎬
