## https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py
## commit as at 4 July - login works

## next look into interpretation of the token and profile
## >>>>  https://docs.authlib.org/en/latest/client/flask.html

from flask import Flask, url_for, Blueprint
from flask import session

from flask import render_template, redirect
from flask import current_app
from authlib.integrations.flask_client import OAuth

from os import environ, path
from dotenv import load_dotenv

import requests
import json

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GITHUB_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GITHUB_CLIENT_SECRET")

#CONF_URL = 'https://accounts.github.com/.well-known/openid-configuration'

oauth = OAuth(current_app)

authlib_github_bp = Blueprint('authlib_github_bp', __name__,url_prefix='/app/login/github')

oauth.register(
    name='github',
    access_token_url='https://github.com/login/oauth/access_token',
    #authorize_url='https://github.com/login/oauth/authorize',
    authorize_url='http://dev1.dmtool.info/login/github/auth',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'read:user'},
  )


#oauth.register(
#    name='github',
#    server_metadata_url=CONF_URL,
#    client_kwargs={
#        'scope': 'read:user'
#    }
#)

@authlib_github_bp.route('/home')
def homepage():
    user = session.get('dmtool_user_id')
    return render_template('home.html', user=user)


@authlib_github_bp.route('/login')
def login():
    #redirect_uri = url_for('auth', _external=True)
    redirect_uri = url_for('authlib_github_bp.auth', _external=True)
    print(redirect_uri) 
    return oauth.github.authorize_redirect(redirect_uri)
    #redirect_uri = 'http://dev1.dmtool.info/app/login/github/auth'
    #return oauth.github.authorize_redirect(redirect_uri)


@authlib_github_bp.route('/auth')
def auth():
    token = oauth.github.authorize_access_token()
    #user = token['userinfo']
    #print('token data type >>>',type(token))
    print(token)
    '''
    print(token['userinfo'])
    email = user.get("email")
    email_verified = user.get("email_verified")
    name = user.get("name")
    given_name = user.get("given_name")
    family_name = user.get("family_name")
    
    iss = user.get("iss") ##: 'https://accounts.google.com'

    # The API endpoint
    # url = "https://jsonplaceholder.typicode.com/posts/1"
    url = "http://container_fastapi_orm_1:8008/apiorm/authlibuser/" + email
    # A GET request to the API
    response = requests.get(url)
    #url = "http://localhost:8080"
    #data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #r = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 404:
        new_user = {}
        new_user['email'] = email
        new_user['email_verified'] = email_verified
        new_user['name'] = name
        new_user['given_name'] = given_name
        new_user['family_name'] = family_name

        new_user_json = {
              "email": "string",
              "email_verified": True,
              "name": "string",
              "given_name": "string",
              "family_name": "string"
            }
        
        #json_data = json.dumps(newuser)
        url = "http://container_fastapi_orm_1:8008/apiorm/authlibusers"
        # response = requests.post(url, data=json.dumps(newuser), headers=headers)
        # response = requests.post(url, data=json.dumps(new_user_json))
        # json={"key": "value"}
        response = requests.post(url, json=new_user, headers=headers)
        # Print the response
        response_json = response.json()
        #print(response_json)
    
    url = "http://container_fastapi_orm_1:8008/apiorm/authlibuser/" + email
    # A GET request to the API
    response = requests.get(url)
    response_json = response.json()
    user_id = response_json['id']
    print("user_id >>" , user_id)
    session['dmtool_user_id'] = user_id
    '''
    
    return redirect(url_for('authlib_github_bp.homepage'))


@authlib_github_bp.route('/logout')
def logout():
    session.pop('dmtool_user_id', None)
    return redirect(url_for('authlib_github_bp.homepage'))
