import os
from os import environ, path

from dotenv import load_dotenv

import secrets
import string
import random

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
#MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_DATABASE = "dev"
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")
#MARIADB_CONTAINER = "0.0.0.0"

MARIADB_URI = "mysql://" + MARIADB_USERNAME + ":" + \
                MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                + MARIADB_DATABASE

print("aerich db >>>" , MARIADB_URI)

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

TORTOISE_ORM_DICT = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': 'container_mariadb',
                'port': '3306',
                'user': 'pythonuser',
                'password': 'pythonuser',
                'database': 'dev',
            }
        },
        # Using a DB_URL string
        ##'default': 'postgres://postgres:qwerty123@localhost:5432/events'
    },
    'apps': {
        'models': {
            'models': ["models", "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}

TORTOISE_ORM = {
    'connections': {
        # Using a DB_URL string
        'default': 'mysql://pythonuser:pythonuser@container_mariadb:3306/dev'
    },
    'apps': {
        'models': {
            'models': ["models", "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}


## mysql+aiomysql://pythonuser:pythonuser@container_mariadb:3306/dev

TORTOISE_MODELS_LIST = ["models", "aerich.models"]

def init_db(app: FastAPI) -> None:
    ##Tortoise.init_models(["models"], "models")
    register_tortoise(
        app,
        db_url=MARIADB_URI,
        modules={"models": TORTOISE_MODELS_LIST},
        generate_schemas=False,
        add_exception_handlers=True,
    )

async def init_tortoise():
    await Tortoise.init(TORTOISE_ORM)
