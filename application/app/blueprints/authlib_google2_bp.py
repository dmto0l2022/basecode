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

fastapi_about_url = environ.get("FASTAPI_ABOUT_URL")

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("FLASK_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("FLASK_GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_CALLBACK = environ.get("FLASK_GOOGLE_CLIENT_CALLBACK")

oauth = OAuth(current_app)

authlib_google2_bp = Blueprint('authlib_google2_bp', __name__,url_prefix='/application/login/google')


# This information is obtained upon registration of a new Google OAuth
# application at https://code.google.com/apis/console
client_id = GOOGLE_CLIENT_ID
client_secret = GOOGLE_CLIENT_SECRET
redirect_uri = GOOGLE_CLIENT_CALLBACK
#redirect_uri = 'https://dev1.dmtool.info/application/login/google/callback'

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
    email = profile_data['email']
    internal_header = {'dmtool-userid': '999'}
    fastapi_about_url = "http://container_fastapi_about_1:8016/"
    get_user_api = "dmtool/fastapi_about/internal/about/user/"
    get_or_create_user_url = fastapi_about_url + get_user_api + email
    google_req = requests.get(get_or_create_user_url,headers=internal_header)
    
    print("get_or_create_user_url >>>" , get_or_create_user_url)
    #google_req = requests.get(url_get)
    print("google user status code >>>> " , google_req.status_code)
    
    if google_req.status_code == 404:
        url = fastapi_url + "/dmtool/fastapi_about/internal/about/user"
        #json={"key": "value"}
        json = {
          "email" : email,
          "authlib_id": 999,
          "authlib_provider": "google"
        }
        post_request = requests.post(url, json=json, headers=internal_header)
        print('new google user request status code >>> ' ,post_request.status_code)


    print("new google user request json >>>>>>>>>>>>>>" , google_req.json())
    dmtool_userid = google_req.json()['id']
    print('dmtool_userid >>>>>>', dmtool_userid)
    #print(google_req.json())
    session['dmtool_userid'] = dmtool_userid
    #google_req = requests.get(url_get)
    #dmtool_userid = google_req.json()['id']
    #print('dmtool_userid >>>>>>', dmtool_userid)
    #print(google_req.json())

    #session['dmtool_userid'] = dmtool_userid

    permissions_url = fastapi_about_url + "/dmtool/fastapi_about/internal/about/user_permission/"
    
    request_permissions = permissions_url + str(dmtool_userid)
    print('request_permissions >>>>', request_permissions)
    
    authorisation_check = requests.get(request_permissions,headers=internal_header)

    ## leaving this code in case we need to block an email address
    
    if authorisation_check.status_code == 404:
        authorisation_create = requests.post(request_permissions,headers=internal_header)
        #session['dmtool_authorised'] = 0
        session['dmtool_authorised'] = 1
    else:
        session['dmtool_authorised'] = 1
    
    print('authorisation_check.json() >>>>>>', authorisation_check.json())
    #session['dmtool_authorised'] = authorisation_check.json()['authorised']
    
    #return redirect(url_for('.menu'))
    return redirect('/application/baseapp/')


@authlib_google2_bp.route("/menu", methods=["GET"])
def menu():
    """"""
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/application/login/google/profile"> Get account profile</a></li>
        <li><a href="/application/login/google/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/application/login/google/manual_refresh"> Explicitly refresh the token</a></li>
        <li><a href="/application/login/google/validate"> Validate the token</a></li>
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

@authlib_google2_bp.route('/logout')
def logout():
    session['dmtool_userid'] = '0'
    session['dmtool_authorised'] = 0
    session.clear()
    return redirect('https://dev1.dmtool.info/')
