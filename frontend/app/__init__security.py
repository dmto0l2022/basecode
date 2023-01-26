import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore

from . import database as dbf ##import db_session, init_db
from . import models as modf ## import User, Role

import mariadb

from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

import os

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

def create_app():
     # Create app
     app = Flask(__name__)
     app.config['DEBUG'] = True

     # Generate a nice key using secrets.token_urlsafe()
     app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
     # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
     # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
     app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

     with app.app_context():
        #app.config["APPLICATION_ROOT"] = "/app"
        #SCRIPT_NAME
        #app.config["SCRIPT_NAME"] = "/app"
        ##>> from . import routes, models, oauth  # Import routes, models and oauth helper
        from . import routes, mail, security ## models
     
        # Setup Flask-Security
        user_datastore = SQLAlchemySessionUserDatastore(dbf.db_session, modf.User, modf.Role)
        app.security = Security(app, user_datastore)
        # Create a user to test with
        d = dbf.init_db()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))
        dbf.db_session.commit()
        
        mail = Mail(app)
     
        return app
