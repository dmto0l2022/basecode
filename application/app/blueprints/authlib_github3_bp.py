## https://requests-oauthlib.readthedocs.io/en/v1.3.1/examples/real_world_example.html
## may need
## https://requests-oauthlib.readthedocs.io/en/v1.3.1/examples/real_world_example_with_refresh.html

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

from flask import Blueprint


import requests
from authlib.integrations.flask_client import OAuth
# from authlib.integrations.requests_client import OAuth2Session

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

authlib_github3_bp = Blueprint('authlib_github3_bp', __name__,url_prefix='/app/login/github3')

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

@authlib_github3_bp.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(GITHUB_CLIENT_ID)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@authlib_github3_bp.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(GITHUB_CLIENT_ID, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=GITHUB_CLIENT_SECRET,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('authlib_github3_bp.profile'))


@authlib_github3_bp.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(GITHUB_CLIENT_ID, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())
