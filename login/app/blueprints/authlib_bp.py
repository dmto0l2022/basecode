## https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py

from flask import Flask, url_for, session, Blueprint
from flask import render_template, redirect
from flask import current_app
from authlib.integrations.flask_client import OAuth

from os import environ, path
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(current_app)

authlib_bp = Blueprint('authlib_bp', __name__,url_prefix='/app/login/authlib')


oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)



@authlib_bp.route('/home')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@authlib_bp.route('/login')
def login():
    #redirect_uri = url_for('auth', _external=True)
    redirect_uri = 'http://dev1.dmtool.info/app/login/authlib/auth'
    return oauth.google.authorize_redirect(redirect_uri)


@authlib_bp.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect(url_for('authlib_bp.homepage'))


@authlib_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('authlib_bp.homepage'))
