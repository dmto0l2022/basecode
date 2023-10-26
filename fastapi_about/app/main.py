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
from routers import users_internal

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


#MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
#redirect_uri = 'https://dev1.dmtool.info/dmtool/fastapi_about/auth'
#api_base_url = '/dmtool/fastapi_about/'

redirect_url = environ.get("FASTAPI_ABOUT_REDIRECT_URL")
fastapi_url= environ.get("FASTAPI_ABOUT_URL")
data_server_internal_url= environ.get("FASTAPI_DATA_INTERNAL_SERVER")
api_base_url =  '/dmtool/fastapi_about/'
print("about url >>>>>>>>>>", fastapi_url)
print(fastapi_url + "openapi.json")
##app = FastAPI(title="DMTOOL API Server - About")

app = FastAPI(title="DMTOOL API Server - About",
              openapi_url = api_base_url + "openapi.json",
              docs_url = api_base_url + "docs"
             )


app.include_router(routers.router)
app.include_router(songs.router)
app.include_router(users.router)
app.include_router(users_internal.router)

########

oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=environ['FASTAPI_ABOUT_CLIENT_ID'],
    client_secret=environ['FASTAPI_ABOUT_CLIENT_SECRET'],
    client_kwargs={
        'scope': "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    }
)


@app.get(api_base_url)
async def homepage(request: Request):
    email = request.session.get('email')
    if email:
        data = json.dumps(email)
        html = (
            f'<pre>{data}</pre>'
            '<a href="' + fastapi_url + '"logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="' + fastapi_url + 'login">login</a>')


@app.get(api_base_url + 'login')
async def login(request: Request):
    #redirect_uri = 'https://dev1.dmtool.info/dmtool/fastapi_about/auth'
    #redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_url)


''' rem
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
rem '''


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


''' rem
@app.get(api_base_url + 'logout')
async def logout(request: Request):
    session = request.cookies.get('session')
    ##request.session.pop('email', None)
    if session:
        request.delete_cookie("session")
    return RedirectResponse(url="https://dev1.dmtool.info/dmtool/fastapi/login")
rem '''


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

    request.referer: 'https://dev1.dmtool.info/dmtool/fastapi_about/docs'
    
    login_response = HTMLResponse('<a href="https://dev1.dmtool.info/dmtool/fastapi_data/login">login</a>')

    if 'internal' in request.url.path and request.client.host == '127.0.0.1':
        return response
    elif 'docs' in request.url.path or 'openapi.json' in request.url.path:
        return response
    elif request.referer == 'https://dev1.dmtool.info/dmtool/fastapi_about/docs': ## for testing
        return response
    #elif 'internal' in request.url.path and request.client.host != '127.0.0.1':
    #    return login_response
    elif 'internal' in request.url.path and request.client.host != '127.0.0.1': ## for testing only
        return response
    elif 'login' in request.url.path  and (email == 'no email' or email==None):
        return response
    elif 'auth' in request.url.path  and (email == 'no email' or email==None):
        return response
    elif 'public' in request.url.path  and (email == 'no email' or email==None):
        return response
    elif 'public' in request.url.path  and (email != 'no email' and email !=None):
        return response
    else:
        print("request.url.path >>>>>>>>>>>" , request.url.path)
        return response

''' rem

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
rem '''

app.add_middleware(SessionMiddleware, secret_key = "123456", session_cookie="session")
