from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
#              for i in range(N))

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

MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")


print("useename, container, password, database")
print(MARIADB_USERNAME)
print(MARIADB_CONTAINER)
print(MARIADB_PASSWORD)
print(MARIADB_DATABASE)


#FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY") ## from file
FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY") ## generated

MARIADB_URI = 'mariadb+mariadbconnector://' + MARIADB_USERNAME + ':' + MARIADB_PASSWORD + '@' + MARIADB_CONTAINER + ':3306/' + MARIADB_DATABASE

print(MARIADB_URI)

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(MARIADB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
