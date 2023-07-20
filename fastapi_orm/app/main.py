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

from starlette.config import Config

import json

from starlette.requests import Request

from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

## from starlette.middleware.sessions import SessionMiddleware
#################

from redis import Redis
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.config import environ

from starlette_session import SessionMiddleware
from starlette_session.backends import BackendType




################
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

#config = Config('.env_fastapi_google')  # read config from .env file
#oauth = OAuth(config)
#oauth.register(
#    name='google',
#    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#    client_kwargs={
#        'scope': 'openid email profile'
#    }
#)

'''
scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
'''


oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=environ['FASTAPI_CLIENT_ID'],
    client_secret=environ['FASTAPI_CLIENT_SECRET'],
    client_kwargs={
        'scope': "https://www.googleapis.com/auth/userinfo.email",
    }
)


app = FastAPI(title="DMTOOL API Server",
              ##servers=[
        ##{"url": "http://dev1.dmtool.info", "description": "Dev environment"}
              ##],
              ##root_path="/apiorm/",
              openapi_url="/apiorm/openapi.json",
              docs_url="/apiorm/docs",
              ##redoc_url=None,
              ##root_path_in_servers=False,
             )

redis_client = Redis(host="container_redis_1", port=6379)
#app = Starlette(debug=True, routes=routes)

app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    cookie_name="session",
    backend_type=BackendType.redis,
    backend_client=redis_client,
)

#app.add_middleware(SessionMiddleware, secret_key="secret-string")

'''
app = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path="/api/v1",
    root_path_in_servers=False,
)
'''

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

@app.get('/apiorm/setup_session')
async def setup_session(request: Request) -> JSONResponse:
    #request.session.update({"data": "session_data"})
    request.session['data'] = "session_data"
    request.session['user_name'] = "session_user"
    return JSONResponse({"session": request.session})

@app.get('/apiorm/clear_session')
async def clear_session(request: Request):
    request.session.clear()
    return JSONResponse({"session": request.session})

@app.get('/apiorm/view_session')
def view_session(request: Request) -> JSONResponse:
    request = Request(environ)
    try:
        session_key = request.cookies.get('session')
        print('session key >>',session_key)
        redis_key = 'session:'+session_key
        print('redis_key >>',redis_key)
    except:
        a = 1
    
    try:
        val = self.redisserver.get(redis_key)
        print(redis_key)
        print('---------val------------------------------')
        print(val)
        print('--------- decoded val------------------------------')
        decoded_val = pickle.loads(val)
        print(decoded_val)
    return JSONResponse({"session": request.session})


@app.get('/apiorm/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/apiorm/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/apiorm/login">login</a>')

@app.route('/apiorm/login')
async def login_via_google(request):
    google = oauth.create_client('google')
    #redirect_uri = request.url_for('authorize_google')
    redirect_uri = 'http://dev1.dmtool.info/apiorm/auth'
    return await google.authorize_redirect(request, redirect_uri)


@app.get('/apiorm/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    request.session['user_login'] = 'user_login'
    return RedirectResponse(url='/apiorm/')


@app.get('/apiorm/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/apiorm/')

register_tortoise(
    app,
    db_url=MARIADB_URI,
    modules={"models": ["models.dmtool","models.users","models.metadata"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
