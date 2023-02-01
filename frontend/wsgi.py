from app import init_app

import json
import ast
import chardet
from datetime import datetime

import mariadb

import os
from os import environ, path
from dotenv import load_dotenv
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, "/app/.env"))

print('BASE_DIR + APP')
print(path.join(BASE_DIR, "/app/"))

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

from app.dashapps.interactive_table import app as app1
from app.dashapps.basic_table import app as app2
from app.dashapps.session_app import app as app3

from app.dashpages.app import app as app4

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
    
    def getcurrentemail(self,current_user_in):
        
        current_user_email = 'unknown@unknown.com'
        email_domain = 'unknown.com'
        
        print('============================================================')
        current_date = datetime.now()
        print(current_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        print('==================request data==============================')
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, email, username, active, confirmed_at FROM world.`user` where fs_uniquifier = %s" \
                       , (current_user_in,)) ## , is important
        
        try:
            user_details = cursor.fetchall()
            for row in user_details:
                current_user_email = row["email"]
            cursor.close()
            print('current user email > ' , current_user_email)
            email_domain = current_user_email.split('@')[1]
            print('email domain > ', email_domain)
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
        print('decoded_current_session_data string')
        print('-------------here----------------')
        print(decoded_current_session_data)
        print('------------to here--------------')
        
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
        
        
        print('________all____________')
        print(all_values)
        print('________current_user_from_cookie____________')
        print(current_user_from_cookie)
        
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
        print('colon cookie')
        print(colon_cookie)
        
        for cookie in cookies:
            cookie = cookie.split('=')
            handler[cookie[0]] = cookie[1]

        for k in handler:
            print(k + " = " + handler[k])
            print('--------------')
        
        
        #print(http_cookie)
        print('---------------------------')
        encoded_cookie = bytes(colon_cookie, 'Windows-1252')
        #str_1_encoded = bytes(str_1,'UTF-8')
        
        print('encoded cookie')
        print(encoded_cookie)
        
        current_session_data = self.redisserver.get(encoded_cookie)
        print('current session data')
        ##current_session = 'session=3d6eaeb7-c227-4444-ac90-208da7732203'
        #current_session = b'session:3d6eaeb7-c227-4444-ac90-208da7732203'
        print(current_session_data)
        #val = self.redisserver.get(current_session)
        
        print('===================================')
        
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
        print('environ type')
        print(type(environ))
        print('environ data')
        print('---------------------')
        print(environ_data)
        try:
            session_data,current_user, current_user_email, email_domain = self.getcookiedata(environ)
            print('current session data')
            print('-------------------')
            print(session_data)
            print('current user')
            print('-------------------')
            print(current_user)
            print('current user email')
            print('-------------------')
            print(current_user_email)
            print('current email domain')
            print('-------------------')
            print(email_domain)
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
        print('path: %s, url: %s' % (request.path, request.url))
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

        if 'wsgi' not in request.path:
            print('wsgi not in path')
            return self.wsgi(environ,start_response)

        else:
            print('wsgi in path')
            #environ['PATH_INFO']='/app/welcome'
            return self.wsgi(environ,start_response)
        
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
    '/app/wsgi_app1': app1.server,
    '/app/wsgi_app2': app2.server,
    '/app/session_app': app3.server,
    '/app/multipage': app4.server,
})  

application = Middleware(application)

application = DebuggedApplication(application, True)
