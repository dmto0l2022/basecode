from flask import Flask
from flask import flash
from . import database_bind as dbind

# outside of app factory
db = dbind.SQLAlchemy_bind()

import os
from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

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

    MARIADB_URI = "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" + \
                    MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                    + MARIADB_DATABASE
    print(MARIADB_URI)
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = MARIADB_URI
    # import your database tables if defined in a different module
    from . import models
    # for example if the User model above was in a different module:
    db.init_app(app)
    from app.blueprints.home_bp import home_bp
    app.register_blueprint(home_bp)
    from app.blueprints.plotids_bp import plotids_bp
    app.register_blueprint(plotids_bp)
    ##
    ##todo_bp
    from app.blueprints.todo_bp import todo_bp
    app.register_blueprint(todo_bp)
    
    return app
