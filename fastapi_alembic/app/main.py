import time

from os import environ, path

from fastapi import Depends, FastAPI

from starlette.requests import Request
from starlette.responses import JSONResponse

from starlette.config import Config
## from starlette.config import environ
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from starlette.concurrency import iterate_in_threadpool

import json
import redis
from redis import Redis

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session, init_db

from routers import routers
from routers import songs
from routers import users
from routers import dmtools
from routers import metadata

## https://github.com/authlib/demo-oauth-client/blob/master/fastapi-google-login/app.py

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

api_base_url = '/dmtool/fastapi/'

app = FastAPI(title="DMTOOL API Server - Alembic",
              ##servers=[
        ##{"url": "http://dev1.dmtool.info", "description": "Dev environment"}
              ##],
              ##root_path="/apiorm/",
              openapi_url= api_base_url + "openapi.json",
              docs_url= api_base_url + "docs",
              ##redoc_url=None,
              ##root_path_in_servers=False,
             )

app.add_middleware(SessionMiddleware, secret_key="!secret")


redisserver = redis.StrictRedis(host='container_redis_1', port=6379, db=0)

oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=environ['FASTAPI_CLIENT_ID'],
    client_secret=environ['FASTAPI_CLIENT_SECRET'],
    client_kwargs={
        'scope': "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    }
)

app.include_router(routers.router)
app.include_router(songs.router)
app.include_router(users.router)
app.include_router(dmtools.router)
app.include_router(metadata.router)

redirect_uri = 'https://dev1.dmtool.info/dmtool/fastapi/auth'

@app.get(api_base_url)
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.get(api_base_url + 'login')
async def login(request: Request):
    redirect_uri = 'https://dev1.dmtool.info/dmtool/fastapi/auth'
    #redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get(api_base_url + 'auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url=api_base_url)


@app.get(api_base_url + 'logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url=api_base_url)

'''

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    print(f"response_body={response_body[0].decode()}")
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("#################### alembic request headers ##############")
    print(request.headers)
    print("#######################################################")
    try:  
        print("#################### alembic request 'x-forwarded-for' ##############")
        print(request.headers['x-forwarded-for'])
    except:
        print("no request.headers['x-forwarded-for']")
    
    print("#################### alembic request url path ##############")
    print(request.url.path)
    print("#######################################################")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    #print("#################### alembic response headers ##############")
    #print(response.headers)
    #print("#################### alembic response json() ##############")
    #print(response.json())
    #print("#################### alembic response content ##############")
    #print(response.content)
    #print("######################################################")
    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    print(f"response_body={response_body[0].decode()}")
  
    return response

'''
