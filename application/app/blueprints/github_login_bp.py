from flask import Flask, jsonify, url_for
from authlib.integrations.flask_client import OAuth

from flask import current_app as app

from flask import Blueprint, render_template

github_login_bp = Blueprint('github_login_bp', __name__)

oauth = OAuth(app)
github = oauth.register('github')

@app.route('/app/github/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/app/github/authorize')
def authorize():
    token = github.authorize_access_token()
    # you can save the token into database
    profile = github.get('/user', token=token)
    return jsonify(profile)
