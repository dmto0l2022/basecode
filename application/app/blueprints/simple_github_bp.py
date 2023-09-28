# https://docs.authlib.org/en/v0.15.4/client/index.html

from flask import Flask, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)
github = oauth.register('github', {...})

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    # you can save the token into database
    profile = github.get('/user', token=token)
    return jsonify(profile)
