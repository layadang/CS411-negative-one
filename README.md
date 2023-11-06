# CS411 Team Negative One: Movie Recommendation Project

## Overview

This is a Movie Recommendation project that provides personalized movie recommendations to users. It utilizes a Flask-based front-end, a custom-trained Language Model (LLM) recommendation system, the IMDb public sample API, Google OAuth for authentication, and MongoDB to store user information. The project combines these technologies to deliver a seamless movie recommendation experience. The user interface is similar to Tinder. 

## Features

- **User Authentication**: Users can log in using their Google accounts via OAuth, ensuring secure and authenticated access to the system.

- **Movie Recommendations**: The core of the project is a custom-trained Language Model (LLM) recommendation system through Google Vertex AI. It provides movie recommendations based on a user's preferences and viewing history.

- **IMDb Public Sample API**: The project uses the IMDb public sample API to fetch movie data, including titles, ratings, and descriptions.

- **User Profile**: User information, including their watchlist and ratings, is stored in a MongoDB database, enabling the system to personalize recommendations.

## Prerequisites

Before you start, ensure you have Python installed and preferably using Python interpreter 3.11.2.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/layadang/CS411-negative-one.git
   ```

2. Install dependencies:

   ```bash
   pip install request
   pip install flask
   pip install oauthlib
   ```

3. Obtain Google OAuth API credentials:

   - Ask Laya to configure the OAuth client ID and client secret for now

5. Start the application:

   ```bash
   python app.py
   ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Log in using your Google account.
2. Explore movie recommendations based on your watchlist and ratings.
3. Add movies to your watchlist and rate them to receive more personalized recommendations.

## License

This project is not currently licensed RIP.

## Contribution

This project is built by Team Negative One:

- Laya: front end via flask, oauth config
- Xinny: google vertex llm training with imdb api
- Harris, Cindy, Xavier: user info database through mongodb

Happy movie watching! 🍿🎬
