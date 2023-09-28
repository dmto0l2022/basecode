## authlib_google2_bp

## https://requests-oauthlib.readthedocs.io/en/v1.3.1/examples/real_world_example_with_refresh.html

from pprint import pformat
from time import time

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

import flask
import redis
import requests
import chardet

from flask import Blueprint


from authlib.integrations.flask_client import OAuth

import requests
from requests_oauthlib import OAuth2Session

import os
import sys

from flask import current_app

from os import environ, path
from dotenv import load_dotenv

import requests
import json
from http.cookies import SimpleCookie

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

fastapi_url = environ.get("FASTAPI_URL")

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

oauth = OAuth(current_app)

authlib_google2_bp = Blueprint('authlib_google2_bp', __name__,url_prefix='/login/google2')


# This information is obtained upon registration of a new Google OAuth
# application at https://code.google.com/apis/console
client_id = GOOGLE_CLIENT_ID
client_secret = GOOGLE_CLIENT_SECRET

redirect_uri = 'https://dev1.dmtool.info/login/google2/callback'

# Uncomment for detailed oauthlib logs
#import logging
#import sys
#log = logging.getLogger('oauthlib')
#log.addHandler(logging.StreamHandler(sys.stdout))
#log.setLevel(logging.DEBUG)

# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"

refresh_url = token_url # True for Google but not all providers.

scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@authlib_google2_bp.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Google)
    using an URL with a few key OAuth parameters.
    """
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline", prompt="select_account")

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    #try:
    cookie = flask.request.cookies.get('session')
    #print("google2 cookie text >>>> ", cookie)
    #session_cookie = "session:" + cookie
        
    #r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
    #all_keys = r.keys('*')
    #print(all_keys)
    #print(type(all_keys))
    #for k in all_keys:
    #    val = r.get(k)
    #    print(k)
    #    print('---------------------------------------')
    #    print(val)
    #    print('=======================================')
            
    #first = all_keys[0]
    #val = r.get('session:3d6eaeb7-c227-4444-ac90-208da7732203')
    #current_session_data = r.get(session_cookie)
    #print('current session google2 cookie >>>>>>>', current_session_data)

    #detected = chardet.detect(current_session_data)
    #print(detected["encoding"])
    #decoded_current_session_data = current_session_data.decode(detected["encoding"])
    
    #print('decoded_current_session_data string')
    #print('-------------here----------------')
    #print(decoded_current_session_data)
    #print('------------to here--------------')

    
    #Simple_Cookie = SimpleCookie()
    #Simple_Cookie.load(decoded_current_session_data)
    
    # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
    # which is incompatible with requests. Manually construct a dictionary instead.
    #Simple_Cookies = {k: v.value for k, v in Simple_Cookie.items()}
    #print("Simple Cookie >>>>>" , Simple_Cookie)
    
    #all_values = []
    #email = []
    
    #splt = decoded_current_session_data.split('”Œ')
    
    #next_value = 0
    
    #for s in splt:
    #    s1 = s.split('Œ')
    #    for l1 in s1:
    #        if next_value == 1:
    #            email.append(l1)
    #            next_value = 0
    #        if 'email' in l1:
    #            next_value = 1
    #        all_values.append(l1)
    #try:
    #    current_email_from_cookie = email[0].lstrip()
    #except:
    #    current_email_from_cookie = 'No email'
    
    
    #print('________all____________')
    #print(all_values)
    #print('________current_email_from_cookie____________')
    #print(current_email_from_cookie)
    #except:
    #a = 1
    
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@authlib_google2_bp.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    google = OAuth2Session(client_id, redirect_uri=redirect_uri,
                           state=session['oauth_state'])
    token = google.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session['oauth_token'] = token

    google = OAuth2Session(client_id, token=token)
    profile_data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    google_id = profile_data['id']
    #url_get = fastapi_url + "/apiorm/authlibuser/google/" + google_id
    #print("url_get >>>" , url_get)
    #google_req = requests.get(url_get)
    #print("google user status code >>>> " , google_req.status_code)
    #if google_req.status_code == 404:
    #    url = fastapi_url + "/apiorm/authlibuser/google/"
    #    #json={"key": "value"}
    #    json = {
    #      "authlib_id": google_id,
    #      "authlib_provider": "google"
    #    }
    #    post_request = requests.post(url, json=json)
    #    print('post request status code >>> ' ,post_request.status_code)
   
    #google_req = requests.get(url_get)
    #dmtool_userid = google_req.json()['id']
    #print('dmtool_userid >>>>>>', dmtool_userid)
    #print(google_req.json())

    #session['dmtool_userid'] = dmtool_userid

    #url = fastapi_url + "/apiorm/authlibuser/permissions/"
    #request_permissions = url + str(dmtool_userid)
    #print('request_permissions >>>>', request_permissions)
    
    #authorisation_check = requests.get(request_permissions)
    #if authorisation_check.status_code == 404:
    #    session['dmtool_authorised'] = False
    #else:
    #    session['dmtool_authorised'] = True
    
    #print('authorisation_check.json() >>>>>>', authorisation_check.json())
    #session['dmtool_authorised'] = authorisation_check.json()['authorised']
    
    return redirect(url_for('.menu'))


@authlib_google2_bp.route("/menu", methods=["GET"])
def menu():
    """"""
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/app/login/google2/profile"> Get account profile</a></li>
        <li><a href="/app/login/google2/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/app/login/google2/manual_refresh"> Explicitly refresh the token</a></li>
        <li><a href="/app/login/google2/validate"> Validate the token</a></li>
    </ul>

    <pre>
    %s
    </pre>
    """ % pformat(session['oauth_token'], indent=4)


@authlib_google2_bp.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    google = OAuth2Session(client_id, token=session['oauth_token'])
    profile_json = jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    #data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    #name = data['name']
    #print('name >>>>',name)
    #session['name'] = name
    #email = data['email']
    #print('email >>>>',email)
    #session['email'] = email
    return jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())


@authlib_google2_bp.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Googles API.
    token['expires_at'] = time() - 10

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    def token_updater(token):
        session['oauth_token'] = token

    google = OAuth2Session(client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_updater)

    # Trigger the automatic refresh
    jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    return jsonify(session['oauth_token'])


@authlib_google2_bp.route("/manual_refresh", methods=["GET"])
def manual_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    google = OAuth2Session(client_id, token=token)
    session['oauth_token'] = google.refresh_token(refresh_url, **extra)
    return jsonify(session['oauth_token'])

@authlib_google2_bp.route("/validate", methods=["GET"])
def validate():
    """Validate a token with the OAuth provider Google.
    """
    token = session['oauth_token']

    # Defined at https://developers.google.com/accounts/docs/OAuth2LoginV1#validatingtoken
    validate_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
                    'access_token=%s' % token['access_token'])

    # No OAuth2Session is needed, just a plain GET request
    return jsonify(requests.get(validate_url).json())

