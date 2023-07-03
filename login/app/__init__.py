import os

from flask import Flask, render_template, render_template_string, redirect, url_for, session
from flask import flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin,
                         current_user, login_user, logout_user)
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import (OAuthConsumerMixin,
                                               SQLAlchemyBackend)
import redis
from . import database_bind as dbind

from flask_security import Security, current_user, auth_required, SQLAlchemySessionUserDatastore


#from flask_mailman import Mail

from werkzeug.middleware.proxy_fix import ProxyFix

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

path = os.path.dirname(os.path.realpath(__file__))





@app.route('/')
def index():
    google_data = None
    user_info_endpoint = 'oauth2/v2/userinfo'
    if current_user.is_authenticated and google.authorized:
        google_data = google.get(user_info_endpoint).json()
    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)


@app.route('/logout')
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



########################################################


from flask_login import LoginManager
login_manager = LoginManager()

# outside of app factory
db = dbind.SQLAlchemy_bind()

import os
from os import environ, path

from dotenv import load_dotenv

import secrets
import string
import random
# initializing size of string
N = 32
# using secrets.choice()
# generating random strings
#res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
#              for i in range(N))

#res = ''.join(random.choices(string.ascii_letters, k=N))

# print result
#print("The generated random string : " + str(res))

#os.environ["SECRET_KEY"] = os.urandom(32)
#os.environ["SECRET_KEY"] = res

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

'''
# must be defined after db = SQLAlchemy_bind() if in same module
from sqlalchemy import Column, Integer, String

class User(db.Base):
    __tablename__ = 'users_new'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    password = Column(String(25), unique=True)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
'''

# app factory
def init_app():
    MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
    MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
    MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
    MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")
    
    #FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY") ## from file
    FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY") ## generated
   
    MARIADB_URI = "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" + \
                    MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                    + MARIADB_DATABASE
    print(MARIADB_URI)
    app = Flask(__name__)
    filename = os.path.join(app.instance_path, 'my_folder', 'my_file.txt')
    print('filename')
    print(filename)
    #SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT",'146585145368132386173505678016728509634')
    app.config['SQLALCHEMY_DATABASE_URI'] = MARIADB_URI
    ###
    ## session
    # Configure Redis for storing the session data on the server-side
   
    with app.app_context():  
    
         # import your database tables if defined in a different module
         from . import models as md
         #from . import mail, security
         from . import security
         # for example if the User model above was in a different module:
         # Setup Flask-Security
      
         login_manager.init_app(app)
         login_manager.login_view = 'google.login'
         
         @login_manager.user_loader
         def load_user(user_id):
             return User.get(user_id)

         #@login_manager.user_loader
         #def load_user(user_id):
         #    return User.query.get(int(user_id))

         db.init_app(app)

         user_datastore = SQLAlchemySessionUserDatastore(db.session, md.User, md.Role)
         app.security = Security(app, user_datastore)

         # This processor is added to all templates
         #@app.security.context_processor
         #def security_context_processor():
         #    return dict(hello="world")
         
         # This processor is added to only the confirmation view
         #@app.security.send_confirmation_context_processor
         #def send_confirmation_context_processor():
         #    return dict(confirmation_link="https://dmtools.het.brown.edu/app/confirm")
         
         #mail = Mail(app)

         ## setup session data
         app.config['SESSION_TYPE'] = 'redis'
         app.config['SESSION_REDIS'] = redis.from_url('redis://container_redis_1:6379')
         
         server_session = Session()
         
         server_session.init_app(app)

         #server_session.app.session_interface.db.create_all()
         
         from app.blueprints.google_login_bp import google_login_bp
         app.register_blueprint(google_login_bp)
      
         ##users_bp
         #from app.blueprints.users_bp import users_bp
         #app.register_blueprint(users_bp)

         return app
