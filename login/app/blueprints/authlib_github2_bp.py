## thank you to https://github.com/SchBenedikt/Text-Editor/blob/main/auth.py

from flask import Flask, redirect, request, session, url_for
from flask import Blueprint


import requests
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session

scope = 'user:email'  # we want to fetch user's email


import os
import sys

from flask import current_app

from os import environ, path
from dotenv import load_dotenv

import requests
import json

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GITHUB_CLIENT_ID = environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = environ.get("GITHUB_CLIENT_SECRET")

#CONF_URL = 'https://accounts.github.com/.well-known/openid-configuration'

oauth = OAuth(current_app)

authlib_github2_bp = Blueprint('authlib_github2_bp', __name__,url_prefix='/app/login/github2')
'''
github = oauth.register(
    name="github",
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    #authorize_url="http://dev1.dmtool.info/app/login/github2/callback",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
'''

@authlib_github2_bp.route("/home")
def home():
    username = session.get("username")
    if username:
        # Display the username and project names
        return f"Hello {username}! You're now logged in"
    else:
        return f"Hello! You're not logged in"

#@authlib_github2_bp.route("/")
#def index():
#    # Check if the username is saved in the session
#    username = session.get("username")
#    if username:
#        # Display the username and project names
#        return f"Hello {username}! You're now logged in. Projects: {', '.join(projects)}"
#    else:
#        # Username is not saved, redirect to the login page
#        return redirect(url_for("authlib_github2_bp.login"))


@authlib_github2_bp.route("/login")
def login():
    # Check if the user is already authenticated
    if "access_token" in session:
        # User is already authenticated, redirect to the index page
        return redirect(url_for("authlib_github2_bp.home"))
    #redirect_url = "http//dev1.dmtool.info/app/login/github2/callback"
    client = OAuth2Session(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, scope=scope)
    authorization_endpoint = 'https://github.com/login/oauth/authorize'
    uri, state = client.create_authorization_url(authorization_endpoint)
    print(uri)
    #authorization_response = 'https://example.com/github?code=42..e9&state=d..t'
    authorization_response = uri
    token_endpoint = 'https://github.com/login/oauth/access_token'
    token = client.fetch_token(token_endpoint, authorization_response=authorization_response)
    print(token)
    state = restore_previous_state()
    # using requests
    client = OAuth2Session(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, state=state)
    # User is not authenticated, start the OAuth process
    #return github.authorize_redirect(url_for("authlib_github2_bp.callback", _external=True))
    #return github.authorize_redirect(redirect_url, _external=True)
    return url_for("authlib_github2_bp.home")


@authlib_github2_bp.route("/callback")
def callback():
    # Check if the user is already authenticated
    if "access_token" in session:
        # User is already authenticated, redirect to the index page
        return redirect(url_for("authlib_github2_bp.home"))

    # Get the OAuth code from the request
    code = request.args.get("code")

    # Exchange the OAuth code for an access token
    access_token = get_access_token(code)

    # Save the access token in the session
    session["access_token"] = access_token

    # Get the username from the GitHub API
    username = get_username()

    # Save the username in the session
    session["username"] = username

    # Save user information to the about.txt file
    #save_user_info(username)

    # Redirect the user to the index page
    return redirect(url_for("authlib_github2_bp.home"))



def get_access_token(code):
    # Configure the access token request
    payload = {
        "client_id": '"' + GITHUB_CLIENT_ID + '"',
        "client_secret": '"' + GITHUB_CLIENT_SECRET + '"',
        "code": code,
    }

    headers = {
        "Accept": "application/json",
    }

    # Send the access token request
    response = requests.post(
        "https://github.com/login/oauth/access_token", json=payload, headers=headers
    )

    # Extract the access token from the response
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token

    # Return None in case of an error
    return None


def get_username():
    access_token = session.get("access_token")

    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get("https://api.github.com/user", headers=headers)

        if response.status_code == 200:
            username = response.json()["login"]
            return username
    return None

'''
def get_projects():
    access_token = session.get("access_token")

    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get("https://api.github.com/user/repos", headers=headers)

        if response.status_code == 200:
            projects = [project["name"] for project in response.json()]
            return projects
    return []


def save_projects(projects):
    with open("projects.txt", "w") as file:
        file.write("\n".join(projects))

'''

'''
def save_user_info(username):
    access_token = session.get("access_token")

    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.get("https://api.github.com/user", headers=headers)

        if response.status_code == 200:
            user_info = response.json()
            with open("about.txt", "w") as file:
                file.write(f"Username: {username}\n")
                file.write(f"Name: {user_info['name']}\n")
                file.write(f"Email: {user_info['email']}\n")
                # Write other contact information as desired

'''
