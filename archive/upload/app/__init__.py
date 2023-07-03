from flask import Flask, flash, request, redirect, url_for
## both following dead ends
##from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
## from flask_uploads import UploadSet, configure_uploads

from flask_sqlalchemy import SQLAlchemy
import mariadb

from app.database import db_session

import os

from werkzeug.utils import secure_filename

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

## while testing without https
##>> os.environ["OAUTHLIB_INSECURE_TRANSPORT"]="1"

UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')

#UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy()

from app.database import init_db

def create_app():
    app = Flask(__name__,  instance_relative_config=True)
    #mail_server = environ.get('MAIL_SERVER')

    init_db()
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    from app.hello.routes import hello_page_bp
    from app.upload.routes import upload_page_bp
    app.register_blueprint(hello_page_bp)
    app.register_blueprint(upload_page_bp)
    
    from app.dash_private.routes import dash_private_page_bp
    from app.dash_public.routes import dash_public_page_bp
    app.register_blueprint(dash_private_page_bp)
    app.register_blueprint(dash_public_page_bp)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    return app
