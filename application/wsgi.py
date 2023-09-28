from app import init_app
import pickle
application = init_app()

from urllib.parse import urlparse, urlunparse, quote

from secure_cookie.session import SessionMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Request, Response, ResponseStream
from werkzeug.debug import DebuggedApplication
from werkzeug.utils import redirect

from jinja2 import Environment, FileSystemLoader

from pprint import pformat
from time import time

import redis
import requests
import chardet

import json
import ast
import chardet
from datetime import datetime

import requests

import io

import os
import sys
from os import environ, path
from dotenv import load_dotenv

import json

fastapi_url = environ.get("FASTAPI_URL")

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, "/app/.env"))

print('BASE_DIR')
print(BASE_DIR)

#from app.dashapps.crud_table import app as app0
#from app.dashapps.interactive_table import app as app1
#from app.dashapps.basic_table import app as app2
from app.dashapps.session_app import app as app3
from app.baseapp.app import app as app4

app = init_app()

class Middleware:

    def __init__(self, wsgi):
        self.wsgi = wsgi
        self.redisserver = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        self.SESSION_COOKIE_NAME = "session"
        self.template_path = path.join(BASE_DIR, "/workdir/frontend/werkzeug/templates")
        #print('template path')
        #print(template_path)
        self.jinja_env = Environment(loader=FileSystemLoader(self.template_path),
                             autoescape=True)
    
    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')
    
    def __call__(self, environ, start_response):
        
        #print('environ data')
        #print('---------------------')
        #print(environ_data)
        
        request = Request(environ)
        try:
            session_key = request.cookies.get(self.SESSION_COOKIE_NAME)
            print('session key >>',session_key)
            redis_key = 'session:'+session_key
            print('redis_key >>',redis_key)
        except:
            a = 1
        
        dmtool_authorised = False
        try:
            val = self.redisserver.get(redis_key)
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
        
        #if ('wsgi' not in request.path and 'session_app' not in request.path and 'baseapp' not in request.path ) :
        #    print('wsgi and session_app and baseapp not in path')
        #    return self.wsgi(environ,start_response)       
        #elif ('wsgi' in request.path or 'session_app' in request.path or 'baseapp' in request.path) and (dmtool_authorised==True) :
        #    return self.wsgi(environ,start_response)
        
        #else:
        #    unauthorised_response = self.render_template('unauthorised.html')
        #return unauthorised_response(environ, start_response)
        return self.wsgi(environ,start_response)
        

application = DispatcherMiddleware(app, {
    #'/app/wsgi_app0': app0.server,  
    #'/app/wsgi_app1': app1.server,
    #'/app/wsgi_app2': app2.server,
    '/login/session_app': app3.server,
    '/login/baseapp': app4.server,
})  

application = Middleware(application)

application = DebuggedApplication(application, True)
