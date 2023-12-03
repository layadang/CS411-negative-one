# standard and flask library imports:
# oauth set up reference: https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023
import os
import json
import requests

from flask import Flask, abort, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth
from pymongo import MongoClient

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
mongo_uri = "mongodb+srv://CS411ProjectDatabase:negativeone@testcluster1.gfaawrr.mongodb.net/?retryWrites=true&w=majority"  # Replace with your actual MongoDB URI
client = MongoClient(mongo_uri)
db = client.TestCluster1
registered_users = db.RegisteredUsers

@app.route('/register', methods=['POST'])
def register_user():
    """
    Endpoint to register a new user.
    Expects 'first_name' and 'email' in the request body.
    """
    user_data = request.json

    # Validate that both first_name and email are present in the request
    if not user_data or 'first_name' not in user_data or 'email' not in user_data:
        abort(400)  # Bad request

    # Extract first_name and email from the request data
    first_name = user_data['first_name']
    email = user_data['email']

    # Insert the new user data into the MongoDB collection
    try:
        registered_users.insert_one({"email": email, "first_name": first_name})
    except:
        abort(500)  # Internal server error

    return '', 204  # No content response


@app.route("/")
def home():
    user_data = session.get("user")

    if user_data:
        json_str = json.dumps(user_data)
        resp = json.loads(json_str)
        print("hello")
        
        # Check if 'userinfo' key exists before trying to access 'given_name'
        userinfo = resp.get('userinfo')
        if userinfo:
            given_name = userinfo['given_name']
        
        titles = ["The Hunger Games", "Spriggan", "Nefarious", "Kill Switch"]
        current_movie_index = session.get('current_movie_index', 0)
        title = titles[current_movie_index]

        info = find_movie(title)
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
        return render_template("not_signed_in.html", 
                               session=user_data)

@app.route("/like")
def like():
    current_movie_index = session.get('current_movie_index', 0)
    # CHANGE THIS:
    total_movies = 4 

    # Reset 0 if all movies reached?
    next_movie_index = (current_movie_index + 1) % total_movies

    session['current_movie_index'] = next_movie_index

    return redirect(url_for('home'))

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
