from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app
import mariadb
import os

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

#current_app.config['SQLALCHEMY_DATABASE_URI'] = MARIADB_URI

#engine = create_engine(MARIADB_URI)

#Session = sessionmaker(engine)

#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()

# service_app_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class AppDb:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        
        MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
        MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
        MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
        MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")

        MARIADB_URI = "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" + \
                        MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                        + MARIADB_DATABASE
  
        self.sqlalchemy_db_uri = MARIADB_URI
        #sqlalchemy_engine_options = app.config.get('SQLALCHEMY_ENGINE_OPTIONS')

        self.engine = create_engine(
            self.sqlalchemy_db_uri
        )
        
        engine = create_engine(
            self.sqlalchemy_db_uri
        )
        
        sqlalchemy_scoped_session = scoped_session(
            sessionmaker(
                bind=self.engine,
                expire_on_commit=False
            )
        )

        setattr(self, 'session', sqlalchemy_scoped_session)
            
        self.session = sqlalchemy_scoped_session
        
 
