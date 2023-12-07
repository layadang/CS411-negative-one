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
from model_training.gpt import *

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

# Default initial list:
top_10_movies = [
                "Everything Everywhere All at Once",   # Action/Sci-fi
                "La La Land",                          # Romance/Musical
                "Inception",                           # Sci-fi
                "Spider-Man: No Way Home",             # Marvel
                "Legally Blonde",                      # Comedy
                "The Shining",                         # Horror
                "Fast & Furious",                      # Action/Crime
                "Toy Story",                           # Animation
                "Love Actually",                       # Romance                   
                "Get Out"                              # Horror/Comedy
                 ]

# MAIN PAGE:
@app.route("/")
def home():
    global email
    global image_file
    global first_name
    email = ""
    user_data = session.get("user")

    email = ""
    # user is signed in:
    if user_data:
        json_str = json.dumps(user_data)
        resp = json.loads(json_str)
        # Check if 'userinfo' key exists before trying to access 'given_name'
        userinfo = resp.get('userinfo')
        if userinfo:           
            first_name = userinfo['given_name'] 
            name = userinfo['name']
            email = userinfo['email']
           
            post = {
                "_id": email,
                "name": name
                # Add like later
            }
            num = registered_users.find_one({"_id": email})
            if num == None:
                 registered_users.insert_one(post)
                #  print('User registration successful', 200)  # successful response
                
            # registered_users.update_one(post, {"name": name}, upsert = True)
            
        # resets the titles list they already gone through
        session.pop('titles', None) 
        titles = session.get('titles', top_10_movies)
        session['titles'] = titles 
        
        current_movie_index = session.get('current_movie_index', 0)

        title = titles[current_movie_index]
        # call find_movie() function from info_get.py
        info = find_movie(title)

        # need to implement skip on these if any of them are empty string
        image_file = info[1]
        description = info[2]
        genres = info[3]

        return render_template("index.html", 
                               first_name=first_name,
                               title=title,
                               image_file=image_file,
                               description=description,
                               genres=genres
                               )
    
    else:
        # user is not signed in:
        user_data = None
        return render_template("not-signed-in.html")

# HEART BUTTON CLICKED:
liked_movies = []
@app.route("/like")
def like():
    global top_10_movies
    global liked_movies
    global disliked_movies
    global current_movie_title
    
    current_movie_index = session.get('current_movie_index', 0)
    total_movies = 11  # to reset list

    next_movie_index = (current_movie_index + 1) % (total_movies-1)

    if (next_movie_index == 0):
        unfilter_movies = next_movies(", ".join(liked_movies), ", ".join(disliked_movies))
        # Ensure that next_movies returns a list of dictionaries with 'title' as one of the keys
        top_10_movies = [movie['title'] for movie in unfilter_movies]
        titles = top_10_movies
    else:
        # Retrieve titles from the session
        titles = session.get('titles', [])

    session['current_movie_index'] = next_movie_index
    
    # Get the current movie title
    current_movie_title = titles[current_movie_index]
    liked_movies.append(current_movie_title)
    print(current_movie_title)
    registered_users.update_one({ "_id": email},{ "$push": {"liked": current_movie_title}})
    return redirect(url_for('home', current_movie_title=current_movie_title))

# X BUTTON CLICKED
disliked_movies = []
@app.route("/dislike")
def dislike():
    global top_10_movies
    global liked_movies
    global disliked_movies
    global current_movie_title

    current_movie_index = session.get('current_movie_index', 0)
    total_movies = 11  # to reset list

    next_movie_index = (current_movie_index + 1) % (total_movies-1)

    if (next_movie_index == 0):
        unfilter_movies = next_movies(", ".join(liked_movies), ", ".join(disliked_movies))
        # Ensure that next_movies returns a list of dictionaries with 'title' as one of the keys
        top_10_movies = [movie['title'] for movie in unfilter_movies]
        titles = top_10_movies
    else:
        # Retrieve titles from the session
        titles = session.get('titles', [])

    session['current_movie_index'] = next_movie_index
    
    # Get the current movie title
    current_movie_title = titles[current_movie_index]
    disliked_movies.append(current_movie_title)
    print(current_movie_title)
    registered_users.update_one({ "_id": email},{ "$push": {"disliked": current_movie_title}})
    return redirect(url_for('home', current_movie_title=current_movie_title))

# STAR BUTTON CLICKED
@app.route("/add")
def add():
    global top_10_movies
    global liked_movies
    global disliked_movies
    global current_movie_title

    current_movie_index = session.get('current_movie_index', 0)
    total_movies = 11  # to reset list

    next_movie_index = (current_movie_index + 1) % (total_movies-1)

    if (next_movie_index == 0):
        unfilter_movies = next_movies(", ".join(liked_movies), ", ".join(disliked_movies))
        # Ensure that next_movies returns a list of dictionaries with 'title' as one of the keys
        top_10_movies = [movie['title'] for movie in unfilter_movies]
        titles = top_10_movies
    else:
        # Retrieve titles from the session
        titles = session.get('titles', [])

    session['current_movie_index'] = next_movie_index
    
    # Get the current movie title
    current_movie_title = titles[current_movie_index]

    registered_users.update_one({ "_id": email},{ "$push": {"toWatchLater": current_movie_title, "imageURL": image_file, "liked": current_movie_title}})

    return redirect(url_for('home', current_movie_title=current_movie_title))

# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html", first_name=first_name)

# TO WATCH LIST PAGE
@app.route("/to-watch-list")
def to_watch_list():
    document = registered_users.find_one({"_id": email})

    # return format is array of strings
    to_watch_later = document.get('toWatchLater', [])
    image_url = document.get('imageURL', [])

    return render_template('to-watch-list.html', 
                           first_name=first_name,
                           to_watch_later=to_watch_later,
                           image_url=image_url)

# DATABASE FEATURES:
# adding a feature for clear the to watch later list
@app.route('/clear-to-watch-later')
def clear_to_watch_later():
    # Update the document to clear the 'toWatchLater' field
    result = registered_users.update_one(
        {"_id": email},
        {"$set": {"toWatchLater": [], "imageURL": []}}
    )

    if result.modified_count:
        print("cleared to watch success")
    else:
        print("cleared likes/dislikes failed")

    return to_watch_list()
    
@app.route('/clear-likes-dislikes')
def clear_likes_dislikes():
    # Update the document to clear the 'liked' and 'disliked' fields
    result = registered_users.update_one(
        {"_id": email},
        {"$set": {"liked": [], "disliked": []}}
    )

    if result.modified_count:
        print("cleared likes/dislikes success")
    else:
        print("cleared likes/dislikes failed")

    return home()

@app.route('/clear-user-data')
def clear_user_data():
    # Update the document to clear the 'liked', 'disliked', 'toWatchLater', and 'imageURL' fields
    result = registered_users.update_one(
        {"_id": email},
        {"$set": {"liked": [], "disliked": [], "toWatchLater": [], "imageURL": []}}
    )

    if result.modified_count:
        print("cleared all data success")
    else:
        print("cleared all data failed")

# Need to be renamed. This is actually REDO for AddedtoWatch
@app.route('/undo-add')
def undo_add():
    # Assume the most recently added item is sent in the request
    # For example, {"last_liked": "Some Item"}
    
    # Use $pull to remove the item from the 'liked' array
    result = registered_users.update_one(
        {"_id": email},
        {"$pull": {"toWatchLater": current_movie_title}}
    )

    if result.modified_count:
        print("undo add success")
    else:
        print("undo add failed")

    return home()
    
@app.route('/swap')
def switch_like_dislike():
    # Assume the current movie title is sent in the request
    # For example, {"current_movie_title": "Some Movie"}
    
    query = {"_id": email, "liked": {"$in": [current_movie_title]}}
    document = registered_users.find_one(query)
    print(document)
    print(bool(document))
    if bool(document):
        # Remove the movie from the 'liked' array
        registered_users.update_one(
            {"_id": email},
            {"$pull": {"liked": current_movie_title}}
        )

        # Add the movie to the 'disliked' array
        result = registered_users.update_one(
            {"_id": email},
            {"$push": {"disliked": current_movie_title}}
        )

        if result.modified_count:
            print("swap successful")
        else:
            print("swap not successful")
    else:
        registered_users.update_one(
            {"_id": email},
            {"$pull": {"disliked": current_movie_title}}
        )

        # Add the movie to the 'disliked' array
        result = registered_users.update_one(
            {"_id": email},
            {"$push": {"liked": current_movie_title}}
        )
        if result.modified_count:
            print("switch success")
        else:
            print("switch failed")

    return home()

# OAUTH SETUP:
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

# Function to run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.get(
        "FLASK_PORT"), debug=True)
