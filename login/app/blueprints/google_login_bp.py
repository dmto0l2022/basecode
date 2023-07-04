## https://github.com/ASHIK11ab/Flask-Series/blob/OAuth-implementation/app.py
from flask import Blueprint
from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
####

from flask_dance.consumer import OAuth2ConsumerBlueprint

from flask_dance.contrib.google import make_google_blueprint, google



'''
@app.route("/")
def index():
    if not batman_example.session.authorized:
        return redirect(url_for("batman-example.login"))
    resp = batman_example.session.get("me")
    assert resp.ok
    return resp.text
'''

###


#app = Flask(__name__)

#oauth = OAuth(app)

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

#app.config['GOOGLE_CLIENT_ID'] = GOOGLE_CLIENT_ID
#app.config['GOOGLE_CLIENT_SECRET'] = GOOGLE_CLIENT_SECRET

google_login_bp = Blueprint('google_login_bp', __name__)

'''
google_login_bp = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)
'''

'''
batman_example = OAuth2ConsumerBlueprint(
    "batman-example", __name__,
    client_id="<CLIENT_ID>",
    client_secret="<SECRET>",
    base_url="https://graph.facebook.com",
    authorization_url="https://www.facebook.com/dialog/oauth",
    token_url="https://graph.facebook.com/oauth/access_token",
)
'''
'''
google_login_cbp = OAuth2ConsumerBlueprint(
    import_name = 'google',
    name = 'google',
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)
'''

google_login_cbp = OAuth2ConsumerBlueprint(
    "oauth-google", __name__,
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    base_url="https://www.googleapis.com/oauth2/v1/",
    token_url="https://accounts.google.com/o/oauth2/token",
    authorization_url="https://accounts.google.com/o/oauth2/auth",
)

@google_login_bp.route("/app/login/google")
def index():
    if not google_login_cbp.session.authorized:
        return redirect(url_for("google.login"))
    resp = google_login_cbp.session.get("me")
    assert resp.ok
    return resp.text

'''
# Google login route
@google_login_bp.route('/app/login/google')
def google_login():
    google = google_login_cbp.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route / call back
@google_login_bp.route('/app/login/google/authorize')
def google_authorize():
    google = google_login_cbp.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return "You are successfully signed in using google"
'''

