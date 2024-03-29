import time

from os import environ, path
import sys

from fastapi import Depends, FastAPI, Request


from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder

from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

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
import redis
from redis import Redis

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy import exc
## may need to add further Database Handling Errors - see link for types of exception
## https://github.com/zzzeek/sqlalchemy/blob/main/lib/sqlalchemy/exc.py

from db import get_session, init_db

from routers import routers
from routers import songs
from routers import heroes
from routers import dmtools_public
from routers import dmtools_internal
from routers import metadata

## https://github.com/authlib/demo-oauth-client/blob/master/fastapi-google-login/app.py

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

api_base_url = '/dmtool/fastapi_data/'

app = FastAPI(title="DMTOOL API Server - Data",
              ##servers=[
        ##{"url": "http://dev1.dmtool.info", "description": "Dev environment"}
              ##],
              ##root_path="/apiorm/",
              openapi_url= api_base_url + "openapi.json",
              docs_url= api_base_url + "docs",
              ##redoc_url=None,
              ##root_path_in_servers=False,
             )


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
app.include_router(heroes.router)
app.include_router(dmtools_public.router)
app.include_router(dmtools_internal.router)
app.include_router(metadata.router)

## https://console.cloud.google.com/apis/

##@app.request_validation_exception_handler(RequestValidationError)

## The below are very important to help an API user to know why their API call has failed
## Other errors and quality assessments may create other types of error and we may need to create
## manageement routines for these.

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.exception_handler(exc.IntegrityError)
async def integrity_error_handler(request: Request, exc: Exception):
    print("exception details >>>>>>>>>>>" , sys.exc_info())
    exception_type, exception_value, exception_traceback = sys.exc_info()
    #message = str(exception_type) + " | " + str(exception_value) + " | " + str(exception_traceback)
    message = "Integrity Error"
    exception_value_str = str(exception_value)
    exception_value_list = exception_value_str.split(') (')
    error_message_working = exception_value_list[1]
    error_message_raw = error_message_working.split("\n[SQL")[0]
    #error_message_1 = error_message_raw.replace("(", "")
    #error_message_2 = error_message_1.replace('"', '')
    #error_message = error_message_2.replace("\\", "")
    replace_these = ["(", ")", '"', "\\"]
    error_message = error_message_raw
    for replace_char in replace_these:
        error_message = error_message.replace(replace_char, "")
    
    exception_traceback_str = str(exception_traceback)
    return JSONResponse(status_code=500,
                        content=jsonable_encoder({"code": 500, "msg": message,
                                                  "exception_type_str": str(exception_type),
                                                  "exception_value_str": str(exception_value),
                                                  "error_msg": error_message,
                                                  "exception_value": exception_value,
                                                  "exception_traceback":exception_traceback_str }))

#@app.exception_handler(500)
#async def internal_exception_handler(request: Request, exc: Exception):
#    return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Tool Server Error"}))


'''
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
'''
'''

request_validation_exception_handler
http_validation_exception_handler
unhandled_exception_handler

async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    )
    return PlainTextResponse(str(exc), status_code=500)

async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.debug("Our custom http_exception_handler was called")
    return await _http_exception_handler(request, exc)

async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom request_validation_exception_handler was called")
    body = await request.body()
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {"errors": exc.errors(), "body": body.decode(), "query_params": query_params}
    logger.info(detail)
    return await _request_validation_exception_handler(request, exc)
'''


redirect_uri = 'https://dev1.dmtool.info/dmtool/fastapi_data/auth'

@app.get(api_base_url)
async def homepage(request: Request):
    email = request.session.get('email')
    if email:
        data = json.dumps(email)
        html = (
            f'<pre>{data}</pre>'
            '<a href="https://dev1.dmtool.info/dmtool/fastapi_data/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="https://dev1.dmtool.info/dmtool/fastapi_data/login">login</a>')


@app.get(api_base_url + 'login')
async def login(request: Request):
    redirect_uri = 'https://dev1.dmtool.info/dmtool/fastapi_data/auth'
    #redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)
'''
@app.get("/a")
def func_a(request: Request):
    request.session["my_var"] = "1234"
    print(request.cookies.get('session'))
    return 'OK'

@app.get("/b")
def func_b(request: Request):
    my_var = request.session.get("my_var", None)
    print(request.cookies.get('session'))
    return my_var
'''

@app.get(api_base_url + 'auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

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
  
    return RedirectResponse(url=api_base_url)


'''
@app.get(api_base_url + 'logout')
async def logout(request: Request):
    session = request.cookies.get('session')
    ##request.session.pop('email', None)
    if session:
        request.delete_cookie("session")
    return RedirectResponse(url="https://dev1.dmtool.info/dmtool/fastapi/login")
'''

@app.get(api_base_url + 'logout')
async def logout(request: Request):
    request.session.clear()
    return {"session":"cleared"}


'''
@app.get(api_base_url + 'logout')
async def logout(request: Request,call_next):
    #response.delete_cookie("session")
    #response.delete_cookie("session_vars")
    request.session['email'] = 'no email'
    request.session['authenticated'] = 'no'
    response = await call_next(request)
    response.set_cookie('session', expires=0, max_age=0, secure=True, samesite='none')
    response.set_cookie('session_vars', expires=0, max_age=0, secure=True, samesite='none')
    return response
'''

'''
@app.get(api_base_url + 'logout')
async def logout(response: Response,):
    #response.delete_cookie("session")
    #response.delete_cookie("session_vars")
    response.session['email'] = 'no email'
    response.session['authenticated'] = 'no'
    response.set_cookie('session', expires=0, max_age=0, secure=True, samesite='none')
    response.set_cookie('session_vars', expires=0, max_age=0, secure=True, samesite='none')
    return {"ok": True}
'''

'''
@app.get(api_base_url + 'logout')
async def logout(response: HTMLResponse,):
    #response = RedirectResponse(url="https://dev1.dmtool.info/dmtool/fastapi/login", status_code= 302)
    try:
        response.delete_cookie(key='access_token', httponly=True)
        print('session cookie deleted')
    except:
        a = 0

    try:  
        response.delete_cookie(key='session', httponly=True)
        print('access token cookie deleted')
    except:
        a = 0
    
    response = HTMLResponse('<a href="https://dev1.dmtool.info/dmtool/fastapi/login">login</a>')

    return response
'''




#@app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
#@app.add_exception_handler(HTTPException, http_exception_handler)
##@app.add_exception_handler(Exception, unhandled_exception_handler)

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    print("#################### session email address ##############")
    email = ""
    try:
        get_email = request.session.get("email", None)
        #print(request.cookies.get('session'))
        email = get_email
    except:
        email = "no email"
    #if session:
    #    response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True)

    print('session email >>>>>', email)
    #new_header = MutableHeaders(request._headers)
    #new_header["email"]= email
    #request._headers = new_header
    #request.scope.update(headers=request._headers.raw)

    #response.headers['email'] = email
  
    print("#################### alembic updated request headers ##############")
    print(request.headers)
    print("#################### alembic request url path ##############")
    print(request.url.path)
    print("#################### alembic request client host ##############")
    print(request.client.host)
    print("#######################################################")
    #print("#################### alembic response content ##############")
    #print(response.content)
    #print("######################################################")
    #try:  
    #    response_body = [chunk async for chunk in response.body_iterator]
    #    response.body_iterator = iterate_in_threadpool(iter(response_body))
    #    print(f"response_body={response_body[0].decode()}")
    #except:
    #    print("no async content")
    
    login_response = HTMLResponse('<a href="https://dev1.dmtool.info/dmtool/fastapi_data/login">login</a>')

    if 'internal' in request.url.path and request.client.host == '127.0.0.1':
        return response
    elif 'docs' in request.url.path or 'openapi.json' in request.url.path:
        return response
    #elif 'internal' in request.url.path and request.client.host != '127.0.0.1':
    #    return login_response
    elif 'internal' in request.url.path and request.client.host != '127.0.0.1':
         return response
    elif 'login' in request.url.path  and (email == 'no email' or email==None):
        return response
    elif 'auth' in request.url.path  and (email == 'no email' or email==None):
        return response
    elif 'public' in request.url.path  and (email == 'no email' or email==None):
        return response
    elif 'public' in request.url.path  and (email != 'no email' and email !=None):
        return response
    elif 'test' in request.url.path  and (email == 'no email' or email==None):
        return response
    else:
        return login_response
    
    

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
    session = request.cookies.get('session')
    print("##########  print session #############################################")
    print(request.session)
    try:  
        print("#################### alembic request host ##############")
        host = request.headers['host']
        print(host)
        if host == "container_fastapi_alembic_1:8014":
            print("internal request")
        else:
            print("request from internet")
            try:
                email = session.get('email')
                print("from user " , email)
            except:
              print("unknown requester")
          
    except:
        print("no request.headers['host']")
  
    try:  
        print("#################### alembic request 'x-forwarded-for' ##############")
        print(request.headers['x-forwarded-for'])
    except:
        print("no request.headers['x-forwarded-for']")

    print("#################### alembic request email address ##############")
    try:
        email = session.get('email')
        #email = request.session['email']
        print(email)
    except:
        print("no email")
  
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
    print("#################### alembic response content ##############")
    #print(response.content)
    print("######################################################")
    #try:  
    #    response_body = [chunk async for chunk in response.body_iterator]
    #    #response.body_iterator = iterate_in_threadpool(iter(response_body))
    #    #print(f"response_body={response_body[0].decode()}")
    #except:
    #    print("no async content")
  
    return response
'''

app.add_middleware(SessionMiddleware, secret_key = "123456", session_cookie="session")
