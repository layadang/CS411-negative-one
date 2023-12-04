# standard and flask library imports:
# oauth set up reference: https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023
import os
import json
import requests

from flask import Flask, abort, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from pymongo.mongo_client import MongoClient

# our other function:
from info_get import *

app = Flask(__name__)

# Configuration
with open('secret/config.json', 'r') as config_file:
    config = json.load(config_file)

app.secret_key = config.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register(
    "myApp",
    client_id=config.get("GOOGLE_CLIENT_ID"),
    client_secret=config.get("GOOGLE_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email https://www.googleapis.com/auth/userinfo.profile",
    },
    server_metadata_url=f'{config.get("OAUTH2_META_URL")}',
)

# MongoDB Atlas connection
client = MongoClient(config.get("mongo_uri"))
db = client["TestCluster1"]
registered_users = db["RegisteredUsers"]

@app.route('/register', methods=['POST'])
def register_user():
    """
    Endpoint for registering new users.
    The request body should contain 'first_name' and 'email'.
    """
    # Check if the Content-Type is 'application/json'
    if request.content_type != 'application/json':
        return 'Request must be in JSON format', 400

    user_info = request.json()
    user_data = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        # More fields can be added as needed
    }
    # registered_users.insert_one(user_data)
    return 'User registration successful', 200  # successful response

@app.route("/")
def home():
    user_data = session.get("user")

    # user is signed in:
    if user_data:
        json_str = json.dumps(user_data)
        resp = json.loads(json_str)
        
        # Check if 'userinfo' key exists before trying to access 'given_name'
        userinfo = resp.get('userinfo')
        if userinfo:            
            name = userinfo['name']
            email = userinfo['email']
           
            post = {
                
                "_id": email,
                "name": name
                
                # Add like later
            }
            
            registered_users.insert_one(post)
            print('User registration successful', 200)  # successful response

        titles = ["Iron Man", 
                  "Good Will Hunting", 
                  "Nefarious", 
                  "Elf", 
                  "Endgame", 
                  "Inception", 
                  "10 Things I Hate About You", 
                  "Love Actually"]
        
        current_movie_index = session.get('current_movie_index', 0)

        title = titles[current_movie_index]

        # call find_movie() function from info_get.py
        info = find_movie(title)

        # need to implement skip on these if any of them are empty
        image_file = info[1]
        description = info[2]
        genres = info[3]

        return render_template("index.html", 
                               session=user_data,
                               title=title,
                               image_file=image_file,
                               description=description,
                               genres=genres)
    
    else:
        # user is not signed in:
        return render_template("not-signed-in.html", 
                               session=user_data)

# when checkmark button is clicked
@app.route("/like")
def like():
    current_movie_index = session.get('current_movie_index', 0)
    # CHANGE THIS, theoretically many movies we dont need:
    total_movies = 8

    # Reset 0 if all movies reached
    next_movie_index = (current_movie_index + 1) % total_movies

    session['current_movie_index'] = next_movie_index
    
    return redirect(url_for('home'))

@app.route("/dislike")
def dislike():
    current_movie_index = session.get('current_movie_index', 0)
    # CHANGE THIS, theoretically many movies we dont need:
    total_movies = 8

    # Reset 0 if all movies reached
    next_movie_index = (current_movie_index + 1) % total_movies

    session['current_movie_index'] = next_movie_index
    
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signin-google")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.myApp.authorize_access_token()

    # fetch user data with access token
    personDataUrl = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses"
    personData = requests.get(personDataUrl, headers={
        "Authorization": f"Bearer {token['access_token']}"
    }).json()
    token["personData"] = personData
    # set complete user information in the session
    session["user"] = token
    
    return redirect(url_for("home"))

@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.get(
        "FLASK_PORT"), debug=True)