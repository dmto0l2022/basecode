from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

MARIADB_USERNAME = environ.get('MARIADB_USERNAME')
MARIADB_PASSWORD = environ.get('MARIADB_PASSWORD')
MARIADB_CONTAINER = environ.get('MARIADB_CONTAINER')
MARIADB_DATABASE = environ.get('MARIADB_DATABASE')

SQLALCHEMY_DATABASE_URI =  "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" \
                            + MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/" \
                            + MARIADB_DATABASE


engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.models
    Base.metadata.create_all(bind=engine)
