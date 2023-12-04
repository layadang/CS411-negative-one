# standard and flask library imports:
# oauth set up reference: https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023
import os
import json
import requests

from flask import Flask, abort, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from pymongo import MongoClient

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
db = client["TestCluster1"]
registered_users = db["RegisteredUsers"]

@app.route('/register', methods=['POST'])
def register_user():
    """
    注册新用户的端点。
    请求体中应包含 'first_name' 和 'email'。
    """
    # Check if the Content-Type is 'application/json'
    if request.content_type != 'application/json':
        return '请求必须是 JSON 格式', 400

    user_info = request.json()
    user_data = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        # 可以根据需要添加更多字段
    }
    registered_users.insert_one(user_data)
    return '用户注册成功', 200  # 成功响应

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
            register_user()


    return render_template("index.html", session=user_data)


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
