## https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py

from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

#GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
#GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
