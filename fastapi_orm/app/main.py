# pylint: disable=E0611,E0401
## starting point was https://tortoise.github.io/examples/fastapi.html
## https://fastapi.tiangolo.com/tutorial/bigger-applications/

import os
from os import environ, path
import pickle
from functools import wraps
from typing import Awaitable
import time

from dotenv import load_dotenv

import secrets
import string
import random

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR')
print(BASE_DIR)

from typing import List

from fastapi import HTTPException,Header,Depends,FastAPI

from starlette.config import Config

import json

from starlette.requests import Request

from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

## from starlette.middleware.sessions import SessionMiddleware
#################

import redis
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
import hashlib
import os
from passlib.context import CryptContext

#set your salt as an env variable
private_salt = os.getenv("API_SALT")

pwd_hash = CryptContext(schemes=['bcrypt'], deprecated='auto')



def hash_api_key(api_key):
    return pwd_hash.hash(api_key)


def verify_hashed_key(api_key, hashed_api_key):
    return pwd_hash.verify(api_key,hashed_api_key)

def generate_api_key(user_id: str) -> str:
    try:
        salt = private_salt
        key = user_id + salt
        generated_key = hashlib.sha256(key.encode()).hexdigest()
        #format the key to your needs
        formated_key = f"MV_SECRET_{generated_key}"
        return formated_key
    except Exception as e:
        raise e
'''

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

## this breaks the app
#app.add_middleware(
#    SessionMiddleware,
#    secret_key="secret",
#    cookie_name="session",
#    backend_type=BackendType.redis,
#    backend_client=redis_client,
#)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    try:
        if (request.session['authenticated'] != 'yes' and "session" in request.url._url):
            response = HTMLResponse(f'<p>Unauthorised Request!</p>')
        else:
            response = response
    except:
        if ("session" in request.url._url):
            response = HTMLResponse(f'<p>Unauthorised Request!</p>')
        else:
            response = response
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

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
    try:
        session_key = request.cookies.get('session')
        print('session key >>',session_key)
        redis_key = 'session:'+session_key
        print('redis_key >>',redis_key)
    except:
        a = 1
    
    try:
        all_keys = redis_server.keys('*')
        print('---------- all keys -----------')
        print(all_keys)
    except:
        a = 1
        
    try:
        val = redisserver.get(redis_key)
        print(redis_key)
        print('---------val------------------------------')
        print(val)
        print('--------- decoded val------------------------------')
        decoded_val = pickle.loads(val)
        print(decoded_val)
    except:
        a = 1

    try:
        return JSONResponse({"session": request.session})
    except:
        return JSONResponse({"session": "no current session"})


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
    print("lvg:request >>>>>", request)
    #redirect_uri = request.url_for('authorize_google')
    redirect_uri = 'https://dev1.dmtool.info/apiorm/auth/'
    return await google.authorize_redirect(request, redirect_uri)


@app.get('/apiorm/auth')
async def auth(request: Request):
    request.session['authenticated'] = 'no'
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    
    ## profile_data = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    ##profile_data = profile_data['id']
    #user = await oauth.google.parse_id_token(request, access_token)
    #user = access_token.get('userinfo')
    #user = access_token['userinfo']
    #user = oauth.google.parse_id_token(access_token, None) ## needed the await
    #user = await oauth.google.parse_id_token(access_token, nonce=access_token['userinfo']['nonce'])
    user_data = await oauth.google.parse_id_token(access_token, None) ## undocumented solution
    #userinfo = access_token['userinfo']
    print('user >>>>>', user_data)
    print('email >>>>>', user_data['email'])
    print('access_token >>>>>>' , access_token)
    #print('user >>>>>>' , user)
    ##if profile_data:
    ##    request.session['profile_data'] = profile_data
    request.session['user_login'] = 'user_login'
    request.session['email'] = user_data['email']
    request.session['authenticated'] = 'yes'
    return RedirectResponse(url='/apiorm/')


@app.get('/apiorm/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/apiorm/')

@app.get('/apiorm/protected')
async def protected(request: Request) -> JSONResponse:
    #user = request.session.get('user')
    #token = await oauth.google.authorize_access_token(request)
    #userinfo = token['userinfo']
    #if userinfo:
    #    print(userinfo)
    #    return JSONResponse({"userinfo": userinfo})
    #else:
    #    return JSONResponse({"userinfo": "none"})
    print("request.client >>>>" , request.client)
    print("request.cookies >>>>" , request.cookies)
    print("request.headers >>>>" , request.headers)
    ## access_token = request.headers.get('Authorization')
    ##print("access_token >>>>" , access_token)
    cookie = request.headers.get('cookie')
    print("cookie >>>>" , cookie)
    #user = request.session.get('user')
    #print("user >>>>" , user)
    name = 'unknown'
    try:
        if request.session['authenticated'] == "yes":
            email = request.session['email']
            return HTMLResponse(f'<p>Hello {email}!</p><a href=/logout>Logout</a>')
    except:
        return HTMLResponse(f'<p>Hello!</p><a href=/login>Login</a>')
    #return JSONResponse({"name": name})

#def check_authenticated(func):
#    @wraps(func)
#    def wrapper(request, *args, **kwargs):
#        if request.session['authenticated'] != 'yes':
#            raise HTTPException(status_code=401, detail="User not authenticated")
#        return wrapper

async def is_authenticated(request: Request) -> Awaitable[str]:
    authenticated = request.session.get('authenticated')
    return authenticated

#def login_required(f):
#    @wraps(f)
#    def wrapper(request, *args, **kwargs):
#        a = is_authenticated(request)
#        if a == "no":
#            return HTMLResponse('<a href="/apiorm/login">login</a>')
#        return f(request, *args, **kwargs)
#    return wrapper

@app.get('/apiorm/authenticationcheck')
async def authentication_check(request: Request) -> JSONResponse:
    #request.session.update({"data": "session_data"})
    if await is_authenticated(request) == 'yes':
        email = request.session['email']
        return JSONResponse({"authenticated email": email})
    else:
        return JSONResponse({"authenticated email": "not authenticated"})
    
register_tortoise(
    app,
    db_url=MARIADB_URI,
    modules={"models": ["models.dmtool","models.users","models.metadata"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
