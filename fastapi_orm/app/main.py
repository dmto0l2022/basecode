# pylint: disable=E0611,E0401
## starting point was https://tortoise.github.io/examples/fastapi.html
## https://fastapi.tiangolo.com/tutorial/bigger-applications/

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

from typing import List

from fastapi import FastAPI, HTTPException
'''
from models import Experiment_Pydantic, ExperimentIn_Pydantic, Experiments
from models import Limit_Display_Pydantic, Limit_DisplayIn_Pydantic, Limit_Display
from models import Limit_Ownership_Pydantic, Limit_OwnershipIn_Pydantic, Limit_Ownership   
from models import Limit_Pydantic, LimitIn_Pydantic, Limits
from models import Plot_Ownership_Pydantic, Plot_OwnershipIn_Pydantic, Plot_Ownership
from models import Plot_Pydantic, PlotIn_Pydantic, Plots
'''

from routers import users
from routers import dmtool
from routers import metadata

from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI(title="DMTOOL API Server", openapi_url="/apiorm/openapi.json", docs_url="/apiorm/docs", redoc_url=None)

class Status(BaseModel):
    message: str


MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")

MARIADB_URI = "mysql://" + MARIADB_USERNAME + ":" + \
                MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                + MARIADB_DATABASE

print(MARIADB_URI)

app.include_router(dmtool.router)
app.include_router(users.router)
app.include_router(metadata.router)

register_tortoise(
    app,
    db_url=MARIADB_URI,
    modules={"models": ["models.dmtool","models.users","models.metadata"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
