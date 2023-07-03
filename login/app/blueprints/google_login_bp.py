
from flask import Blueprint, render_template

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password

from flask_security.models import fsqla_v3 as fsqla

from flask_login import current_user

import random

from flask_dance.contrib.google import make_google_blueprint, google

from app import db

google_login_bp = make_google_blueprint(
    client_id='YOUR-CLIENT-ID-HERE',
    client_secret='YOUR-CLIENT-SECRET-HERE',
    scope=['https://www.googleapis.com/auth/userinfo.email',
           'https://www.googleapis.com/auth/userinfo.profile'],
    offline=True,
    reprompt_consent=True,
    backend=SQLAlchemyBackend(OAuth, db.session, user=current_user)
)

#app.register_blueprint(google_blueprint)


@app.route('/google_login/')
def index():
    google_data = None
    user_info_endpoint = 'oauth2/v2/userinfo'
    if current_user.is_authenticated and google.authorized:
        google_data = google.get(user_info_endpoint).json()
    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)


@app.route('/google_login/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    resp = blueprint.session.get('/oauth2/v2/userinfo')
    user_info = resp.json()
    user_id = str(user_info['id'])
    oauth = OAuth.query.filter_by(provider=blueprint.name,
                                  provider_user_id=user_id).first()
    if not oauth:
        oauth = OAuth(provider=blueprint.name,
                      provider_user_id=user_id,
                      token=token)
    else:
        oauth.token = token
        db.session.add(oauth)
        db.session.commit()
        login_user(oauth.user)
    if not oauth.user:
        user = GoogleUser(email=user_info["email"],
                    name=user_info["name"])
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)

    return False
