import time

from os import environ, path

from fastapi import Depends, FastAPI

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from starlette.config import Config
## from starlette.config import environ
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.datastructures import MutableHeaders
from authlib.integrations.starlette_client import OAuth, OAuthError

from starlette.concurrency import iterate_in_threadpool

import json

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session, init_db

from routers import routers
from routers import songs
from routers import users

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

api_base_url = '/dmtool/fastapi_about/'

app = FastAPI(title="DMTOOL API Server - About",
              ##servers=[
        ##{"url": "http://dev1.dmtool.info", "description": "Dev environment"}
              ##],
              ##root_path="/apiorm/",
              openapi_url= api_base_url + "openapi.json",
              docs_url= api_base_url + "docs",
              ##redoc_url=None,
              ##root_path_in_servers=False,
             )


app.include_router(routers.router)
app.include_router(songs.router)
app.include_router(users.router)

