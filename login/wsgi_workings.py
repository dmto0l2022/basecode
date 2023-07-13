from app import init_app
import pickle

application = init_app()

#from app import current_user

#from app import session

from urllib.parse import urlparse, urlunparse

from secure_cookie.session import SessionMiddleware

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from werkzeug.wrappers import Request, Response, ResponseStream

from werkzeug.debug import DebuggedApplication

from werkzeug.utils import redirect


from pprint import pformat
from time import time

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

import flask
import redis
import requests
import chardet
from authlib.integrations.flask_client import OAuth
import requests
from requests_oauthlib import OAuth2Session

import os
import sys


from os import environ, path
from dotenv import load_dotenv

import requests
import json


BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

fastapi_url = environ.get("FASTAPI_URL")

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

# This information is obtained upon registration of a new Google OAuth
# application at https://code.google.com/apis/console
client_id = GOOGLE_CLIENT_ID
client_secret = GOOGLE_CLIENT_SECRET

redirect_uri = 'http://dev1.dmtool.info/app/login/google2/callback'

# Uncomment for detailed oauthlib logs
#import logging
#import sys
#log = logging.getLogger('oauthlib')
#log.addHandler(logging.StreamHandler(sys.stdout))
#log.setLevel(logging.DEBUG)

# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"

refresh_url = token_url # True for Google but not all providers.

scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]



##############
from app import init_app
#from app import session

from jinja2 import Environment, FileSystemLoader

import json
import ast
import chardet
from datetime import datetime

import requests

import io

import os

from os import environ, path
from dotenv import load_dotenv
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, "/app/.env"))

from urllib.parse import urlparse, urlunparse, quote

##from secure_cookie.session import SessionMiddleware

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from werkzeug.wrappers import Request, Response, ResponseStream

from werkzeug.debug import DebuggedApplication

from werkzeug.utils import redirect

#from app.dashapps.crud_table import app as app0
#from app.dashapps.interactive_table import app as app1
#from app.dashapps.basic_table import app as app2
from app.dashapps.session_app import app as app3
#from app.baseapp.app import app as app4

SESSION_COOKIE_NAME = "session"
import redis
app = init_app()

class Middleware:

    def __init__(self, wsgi):
        self.wsgi = wsgi
        self.redisserver = redis.Redis(host='container_redis_1', port=6379, db=0)
        
        #template_path = os.path.join(os.path.dirname(__file__), '/werkzeug/templates')
        #BASE_DIR = path.abspath(path.dirname(__file__))
        template_path = path.join(BASE_DIR, "/workdir/frontend/werkzeug/templates")
        #print('template path')
        #print(template_path)
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                             autoescape=True)
    
    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')
    
    def getcurrentuser(self):
        x = requests.get('http://dev1.dmtool.info/app/session/getgoogleid')
        print(x.status_code)
        print(x.json)
        if x.status_code == 200:
            dmtool_userid = x.json()['google_id']
        else:
            dmtool_userid = '999999'
        print('dmtool_userid >>>>>>', dmtool_userid)
        #print(google_req.json())
        
        
        print('============================================================')
        current_date = datetime.now()
        print(current_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        
        return dmtool_userid
    
    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        ##r_middle = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        environ_data = repr(environ).encode('utf-8')
        #print('environ type')
        #print(type(environ))
        print('environ data')
        print('---------------------')
        print(environ_data)
        ################
        #redis_server = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        
        ################
        
        #try:
        #current_user = self.getcurrentuser()
        #print('current session data')
        #print('-------------------')
        #print(session_data)
        #print('current user')
        #print('-------------------')
        #print(current_user)
        #print('current user email')
        #print('-------------------')
        #print(current_user_email)
        #print('current email domain')
        #print('-------------------')
        #print(email_domain)
        #except:
        #print('no current session')
        #session_data = {}
        #current_user = 'unknown'
        #current_user_email = 'unknown'
        #email_domain = 'unknown'
            
        request = Request(environ)
        try:
            session_key = request.cookies.get(SESSION_COOKIE_NAME)
            print('session key >>',session_key)
            redis_key = 'session:'+session_key
            print('redis_key >>',redis_key)
        except:
            a = 1
        
        #redis_server = redis.Redis(host='container_redis_1', port=6379, decode_responses=True)
        redis_server = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        #redis_server = redis.StrictRedis(host='container_redis_1', port=6379, charset="utf-8", decode_responses=True)
        dmtool_authorised = False
        try:
            val = redis_server.get(redis_key)
            print(redis_key)
            print('---------val------------------------------')
            print(val)
            print('--------- decoded val------------------------------')
            decoded_val = pickle.loads(val)
            print(decoded_val)
            dmtool_userid = decoded_val['dmtool_userid']
            dmtool_authorised = decoded_val['dmtool_authorised']
            print('dmtool_userid >>>' ,decoded_val['dmtool_userid'])
            print('=======================================')
            
        except:
            print('no session')
        '''
        try:
            all_keys = redis_server.keys('*')
            print(all_keys)
            print(type(all_keys))
            #session_key = request.cookies.get(SESSION_COOKIE_NAME)
            first = all_keys[0]
            #val = r.get('session:3d6eaeb7-c227-4444-ac90-208da7732203')
            for k in all_keys:
                val = r.get(k)
                print(k)
                print('---------------------------------------')
                print(val)
                print('=======================================')
        except:
            print('no keys')
        '''
        ##url_return_parts = urlparse(request.url)
        ##welcome_url_parts = url_return_parts._replace(path='/app/welcome')
        ##url_return = urlunparse(welcome_url_parts)
        #all_keys = r.keys('*')
        #print(all_keys)
        #print(session['Username'])
        ##print(url_return)
        #print('path: %s, url: %s' % (request.path, request.url))
        # just do here everything what you need
        #if 'wsgi' not in request.path:
        #    print('wsgi not in path')
        #    return self.wsgi(environ, start_response)
        #elif 'wsgi' in request.path and email_domain == 'gaitskell.com':
        #    print('authorised email domain')
        #    return self.wsgi(environ, start_response)
        #else:
        #    print('url contains wsgi - from unknown or unauthorised email domain')
        #    ##print(url_return)
        #    print('-----------')
        #    #url_return = urlparse(request.url)
        #    #url_return._replace(path='/app/welcome')
        #    start_response('301 Redirect', [('Location', '/app/welcome'),])
        #    return []
        
        if ('wsgi' not in request.path and 'session_app' not in request.path) :
            print('wsgi and session_app not in path')
            #response = Response('Hello World!')
            #response = request.get_response(self.wsgi)
            #print('------------ response ---------------')
            #print(response)
            return self.wsgi(environ,start_response)       
        #else:
        #    print('wsgi in path')
        #    #environ['PATH_INFO']='/app/welcome'
        #    response = Response('Hello World!')
        #    print(response)
        #    return response(environ,start_response)
        elif ('wsgi' in request.path or 'session_app' in request.path) and (dmtool_authorised==True) :
            return self.wsgi(environ,start_response)
        
        else:
            #body = environ['wsgi.input']
            #print('request.path >>>>' , request.path)
            #print('email_domain >>>>', email_domain)
            #print('wsgi or baseapp in path not gaitskell.com or brown.edu')
            #print('body')
            #print(body)
            #modified_body = body
            #new_stream = io.BytesIO(modified_body)
            #environ['wsgi.input'] = new_stream
            ##start_response('302 Found', [('Location','/app/welcome')])
            #hello_response = Response('Hello World!')
            ##return response(environ, start_response)
            ##redirect_response = redirect('/app/welcome',code=302)
            
            ##headers = [('Location', '/app/welcome')]
            ##r = Response("redirected", status=302, headers=headers)
            ##return r(environ, start_response)
            #body = b'Hello world!\n'
            #status = '200 OK'
            #headers = [('Content-type', 'text/plain')]
            #start_response(status, headers)
            
            #hello_response = Response('Hello World!')
            unauthorised_response = self.render_template('unauthorised.html')
            #return hello_response(environ, start_response)
        return unauthorised_response(environ, start_response)
##return [body]
##return self.wsgi(environ,redirect_response)
    '''
useremail
https://gist.github.com/devries/4a747a284e75a5d63f93

from urllib import quote

class SSLRedirect(object):
    def __init__(self,app):
        self.app=app

    def __call__(self,environ,start_response):
        proto = environ.get('HTTP_X_FORWARDED_PROTO') or environ.get('wsgi.url_scheme', 'http')

        if proto=='https':
            return self.app(environ,start_response)

        else:
            url = 'https://'

            if environ.get('HTTP_HOST'):
                url += environ['HTTP_HOST']
            else:
                url += environ['SERVER_NAME']

            url += quote(environ.get('SCRIPT_NAME', ''))
            url += quote(environ.get('PATH_INFO', ''))
            if environ.get('QUERY_STRING'):
                url += '?' + environ['QUERY_STRING']

            status = "301 Moved Permanently"
            headers = [('Location',url),('Content-Length','0')]

            start_response(status,headers)

            return ['']

'''

application = DispatcherMiddleware(app, {
    #'/app/wsgi_app0': app0.server,  
    #'/app/wsgi_app1': app1.server,
    #'/app/wsgi_app2': app2.server,
    '/app/session_app': app3.server,
    #'/app/baseapp': app4.server,
})  

application = Middleware(application)

application = DebuggedApplication(application, True)
