from app import init_app

application = init_app()

#from app import current_user

from app import session

from urllib.parse import urlparse, urlunparse

from secure_cookie.session import SessionMiddleware

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from werkzeug.wrappers import Request, Response, ResponseStream

from werkzeug.debug import DebuggedApplication

from werkzeug.utils import redirect

######################

## authlib_google2_bp

## https://requests-oauthlib.readthedocs.io/en/v1.3.1/examples/real_world_example_with_refresh.html

from pprint import pformat
from time import time

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

import flask
import redis
import requests
import chardet

from flask import Blueprint


from authlib.integrations.flask_client import OAuth

import requests
from requests_oauthlib import OAuth2Session

import os
import sys

from flask import current_app

from os import environ, path
from dotenv import load_dotenv

import requests
import json
from http.cookies import SimpleCookie

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

fastapi_url = environ.get("FASTAPI_URL")

print('BASE_DIR')
print(BASE_DIR)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

oauth = OAuth(current_app)

authlib_google2_bp = Blueprint('authlib_google2_bp', __name__,url_prefix='/app/login/google2')


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

@authlib_google2_bp.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Google)
    using an URL with a few key OAuth parameters.
    """
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline", prompt="select_account")

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    #try:
    cookie = flask.request.cookies.get('session')
    #print("google2 cookie text >>>> ", cookie)
    #session_cookie = "session:" + cookie
        
    #r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
    #all_keys = r.keys('*')
    #print(all_keys)
    #print(type(all_keys))
    #for k in all_keys:
    #    val = r.get(k)
    #    print(k)
    #    print('---------------------------------------')
    #    print(val)
    #    print('=======================================')
            
    #first = all_keys[0]
    #val = r.get('session:3d6eaeb7-c227-4444-ac90-208da7732203')
    #current_session_data = r.get(session_cookie)
    #print('current session google2 cookie >>>>>>>', current_session_data)

    #detected = chardet.detect(current_session_data)
    #print(detected["encoding"])
    #decoded_current_session_data = current_session_data.decode(detected["encoding"])
    
    #print('decoded_current_session_data string')
    #print('-------------here----------------')
    #print(decoded_current_session_data)
    #print('------------to here--------------')

    
    #Simple_Cookie = SimpleCookie()
    #Simple_Cookie.load(decoded_current_session_data)
    
    # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
    # which is incompatible with requests. Manually construct a dictionary instead.
    #Simple_Cookies = {k: v.value for k, v in Simple_Cookie.items()}
    #print("Simple Cookie >>>>>" , Simple_Cookie)
    
    #all_values = []
    #email = []
    
    #splt = decoded_current_session_data.split('”Œ')
    
    #next_value = 0
    
    #for s in splt:
    #    s1 = s.split('Œ')
    #    for l1 in s1:
    #        if next_value == 1:
    #            email.append(l1)
    #            next_value = 0
    #        if 'email' in l1:
    #            next_value = 1
    #        all_values.append(l1)
    #try:
    #    current_email_from_cookie = email[0].lstrip()
    #except:
    #    current_email_from_cookie = 'No email'
    
    
    #print('________all____________')
    #print(all_values)
    #print('________current_email_from_cookie____________')
    #print(current_email_from_cookie)
    #except:
    #a = 1
    
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@authlib_google2_bp.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    google = OAuth2Session(client_id, redirect_uri=redirect_uri,
                           state=session['oauth_state'])
    token = google.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session['oauth_token'] = token

    google = OAuth2Session(client_id, token=token)
    profile_data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    google_id = profile_data['id']
    url_get = fastapi_url + "/apiorm/authlibuser/google/" + google_id
    print("url_get >>>" , url_get)
    google_req = requests.get(url_get)
    print("google user status code >>>> " , google_req.status_code)
    if google_req.status_code == 404:
        url = fastapi_url + "/apiorm/authlibuser/google/"
        #json={"key": "value"}
        json = {
          "authlib_id": google_id,
          "authlib_provider": "google"
        }
        post_request = requests.post(url, json=json)
        print('post request status code >>> ' ,post_request.status_code)
   
    google_req = requests.get(url_get)
    #dmtool_userid = google_req.json()['id']
    #print('dmtool_userid >>>>>>', dmtool_userid)
    print(google_req.json())
    
    return redirect(url_for('.menu'))


@authlib_google2_bp.route("/menu", methods=["GET"])
def menu():
    """"""
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/app/login/google2/profile"> Get account profile</a></li>
        <li><a href="/app/login/google2/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/app/login/google2/manual_refresh"> Explicitly refresh the token</a></li>
        <li><a href="/app/login/google2/validate"> Validate the token</a></li>
    </ul>

    <pre>
    %s
    </pre>
    """ % pformat(session['oauth_token'], indent=4)


@authlib_google2_bp.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    google = OAuth2Session(client_id, token=session['oauth_token'])
    profile_json = jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    #data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    #name = data['name']
    #print('name >>>>',name)
    #session['name'] = name
    #email = data['email']
    #print('email >>>>',email)
    #session['email'] = email
    return jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())


@authlib_google2_bp.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Googles API.
    token['expires_at'] = time() - 10

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    def token_updater(token):
        session['oauth_token'] = token

    google = OAuth2Session(client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_updater)

    # Trigger the automatic refresh
    jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    return jsonify(session['oauth_token'])


@authlib_google2_bp.route("/manual_refresh", methods=["GET"])
def manual_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    google = OAuth2Session(client_id, token=token)
    session['oauth_token'] = google.refresh_token(refresh_url, **extra)
    return jsonify(session['oauth_token'])

@authlib_google2_bp.route("/validate", methods=["GET"])
def validate():
    """Validate a token with the OAuth provider Google.
    """
    token = session['oauth_token']

    # Defined at https://developers.google.com/accounts/docs/OAuth2LoginV1#validatingtoken
    validate_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
                    'access_token=%s' % token['access_token'])

    # No OAuth2Session is needed, just a plain GET request
    return jsonify(requests.get(validate_url).json())
##############
from app import init_app
#from app import session


from jinja2 import Environment, FileSystemLoader

import json
import ast
import chardet
from datetime import datetime

import mariadb

import io

import os

from os import environ, path
from dotenv import load_dotenv
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, "/app/.env"))

#print('BASE_DIR + APP')
#print(path.join(BASE_DIR, "/app/"))


## MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_USERNAME = environ.get("MARIADB_USERNAME")
MARIADB_PASSWORD = environ.get("MARIADB_PASSWORD")
MARIADB_DATABASE = environ.get("MARIADB_DATABASE")
MARIADB_CONTAINER = environ.get("MARIADB_CONTAINER")

MARIADB_URI = "mariadb+mariadbconnector://" + MARIADB_USERNAME + ":" + \
                MARIADB_PASSWORD + "@" + MARIADB_CONTAINER + ":3306/"\
                + MARIADB_DATABASE

##from app import current_user

##from app import session

from urllib.parse import urlparse, urlunparse, quote

##from secure_cookie.session import SessionMiddleware

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from werkzeug.wrappers import Request, Response, ResponseStream

from werkzeug.debug import DebuggedApplication

from werkzeug.utils import redirect

#from app.dashapps.crud_table import app as app0
from app.dashapps.interactive_table import app as app1
#from app.dashapps.basic_table import app as app2
from app.dashapps.session_app import app as app3

from app.baseapp.app import app as app4

import redis
'''
r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
all_keys = r.keys('*')
#print(all_keys)
print(type(all_keys))
#first = all_keys[0]
#val = r.get('session:3d6eaeb7-c227-4444-ac90-208da7732203')
for k in all_keys:
    val = r.get(k)
    print(k)
    print('---------------------------------------')
    print(val)
    print('=======================================')
'''

app = init_app()

class Middleware:

    def __init__(self, wsgi):
        self.wsgi = wsgi
        self.redisserver = redis.Redis(host='container_redis_1', port=6379, db=0)
        self.connection = mariadb.connect(
                    user=MARIADB_USERNAME,
                    password=MARIADB_PASSWORD,
                    host=MARIADB_CONTAINER,
                    port=3306,
                    database=MARIADB_DATABASE
                    )   
    
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
    
    def getcurrentemail(self,current_user_in):
        
        current_user_email = 'unknown@unknown.com'
        email_domain = 'unknown.com'
        
        print('============================================================')
        current_date = datetime.now()
        print(current_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        print('==================request data==============================')
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, email, username, active, confirmed_at FROM data.`user` where fs_uniquifier = %s" \
                       , (current_user_in,)) ## , is important
        
        try:
            user_details = cursor.fetchall()
            for row in user_details:
                current_user_email = row["email"]
            cursor.close()
            #session['dmtool_email_address'] = current_user_email
            #print('current user email > ' , current_user_email)
            email_domain = current_user_email.split('@')[1]
            #print('email domain > ', email_domain)
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        except:
            current_user_email = 'unknown'
            email_domain = 'unknown'
        
        
        return current_user_email, email_domain
    
    def getcurrentuser(self,current_session_data_in):
        
        ##data = b"\x95\xc3\x8a\xb0\x8ds\x86\x89\x94\x82\x8a\xba"
        detected = chardet.detect(current_session_data_in)
        #print(detected["encoding"])
        decoded_current_session_data = current_session_data_in.decode(detected["encoding"])
        #print('decoded_current_session_data string')
        #print('-------------here----------------')
        #print(decoded_current_session_data)
        #print('------------to here--------------')
        
        all_values = []
        user_id = []
        
        splt = decoded_current_session_data.split('”Œ')
        
        next_value = 0
        
        for s in splt:
            s1 = s.split('Œ')
            for l1 in s1:
                if next_value == 1:
                    user_id.append(l1)
                    next_value = 0
                if 'user' in l1:
                    next_value = 1
                all_values.append(l1)
        try:
            current_user_from_cookie = user_id[0].lstrip()
        except:
            current_user_from_cookie = 'No user'
        
        
        #print('________all____________')
        #print(all_values)
        #print('________current_user_from_cookie____________')
        #print(current_user_from_cookie)
        
        return current_user_from_cookie
        '''
        
        ##decoded_utf8 = val.decode('Windows-1252').encode('utf-8','ignore')
        ##print(decoded_utf8)
        
        #print(ast.literal_eval(val.decode("utf-8","ignore")))
        
        ##session_data = self.redisserver.get(current_session)
        ##session_dict = json.loads(session_data.decode('utf-8','ignore'))
        
        #dict = json.loads(self.redisserver.get(current_session))
        ##print(session_dict)
        ##print('TTTTTTTTTTTTTTTTTTTTTTTT')
        ##dict = self.redisserver.hgetall(current_session)
        #print(val.decode("utf-8","ignore"))
        #print('--------------------------')
        #print(val)
        print('+++++++++++++++++++++++++++')
        #print(type(val))
        print('=============================')
        
        ##print(val['email'])
        
        ##all_keys = self.redisserver.keys('*')
        ##print(all_keys)
        
        '''
        return current_user_from_cookie
    
    def getcookiedata(self, environ_in):
        
        http_cookie = environ_in['HTTP_COOKIE']
        
        import os

        handler = {}

        #cookies = os.environ['HTTP_COOKIE']
        cookies = http_cookie.split('; ')
        current_cookie = cookies[0]
        colon_cookie = current_cookie.replace("=",":")
        #print('colon cookie')
        #print(colon_cookie)
        
        for cookie in cookies:
            cookie = cookie.split('=')
            handler[cookie[0]] = cookie[1]

        #for k in handler:
        #    print(k + " = " + handler[k])
        #    print('--------------')
        
        
        #print(http_cookie)container_frontend_1
        #print('---------------------------')
        encoded_cookie = bytes(colon_cookie, 'Windows-1252')
        #str_1_encoded = bytes(str_1,'UTF-8')
        
        #print('encoded cookie')
        #print(encoded_cookie)
        
        current_session_data = self.redisserver.get(encoded_cookie)
        #print('current session data')
        ##current_session = 'session=3d6eaeb7-c227-4444-ac90-208da7732203'
        #current_session = b'session:3d6eaeb7-c227-4444-ac90-208da7732203'
        #print(current_session_data)
        #val = self.redisserver.get(current_session)
        
        #print('===================================')
        
        import chardet
        
        try:
            current_user = self.getcurrentuser(current_session_data)
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        except:
            current_user = 'no user'
        
        try:
            current_user_email, email_domain = self.getcurrentemail(current_user)
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        except:
            current_user_email = 'anon@unknowndomain.com'
            email_domain = 'unknowndomain.com'
            
        
        return current_session_data, current_user, current_user_email, email_domain

    
        
    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        ##r_middle = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        environ_data = repr(environ).encode('utf-8')
        #print('environ type')
        #print(type(environ))
        #print('environ data')
        #print('---------------------')
        #print(environ_data)
        try:
            session_data,current_user, current_user_email, email_domain = self.getcookiedata(environ)
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
        except:
            print('no current session')
            session_data = {}
            current_user = 'unknown'
            current_user_email = 'unknown'
            email_domain = 'unknown'
            
        request = Request(environ)
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

        if ('wsgi' not in request.path and 'baseapp' not in request.path) :
            print('wsgi and baseapp not in path')
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
        elif ('wsgi' in request.path or 'baseapp' in request.path) and (email_domain == 'gaitskell.com' or email_domain == 'brown.edu') :
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
            
            hello_response = Response('Hello World!')
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
    '/app/wsgi_app1': app1.server,
    #'/app/wsgi_app2': app2.server,
    '/app/session_app': app3.server,
    '/app/baseapp': app4.server,
})  

application = Middleware(application)

application = DebuggedApplication(application, True)
