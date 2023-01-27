from app import init_app

import json
import ast

##from app import current_user

##from app import session

from urllib.parse import urlparse, urlunparse

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
        ##self.redisserver = redis.StrictRedis(host='container_redis_1', port=6379, decode_responses=True)

        
    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        ##r_middle = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        environ_data = repr(environ).encode('utf-8')
        #print(type(environ_data))
        #print(environ_data)
        http_cookie = environ['HTTP_COOKIE']
        
        import os

        handler = {}

        #cookies = os.environ['HTTP_COOKIE']
        cookies = http_cookie.split('; ')

        for cookie in cookies:
            cookie = cookie.split('=')
            handler[cookie[0]] = cookie[1]

        for k in handler:
            print(k + " = " + handler[k])
            print('--------------')
        
        
        #print(http_cookie)
        print('---------------------------')
        #val = r_middle.get(http_cookie.encode('UTF-8'))
        ##current_session = 'session=3d6eaeb7-c227-4444-ac90-208da7732203'
        current_session = b'session:3d6eaeb7-c227-4444-ac90-208da7732203'
        val = self.redisserver.hget(current_session)
        
        #print(ast.literal_eval(val.decode("utf-8","ignore")))
        
        ##session_data = self.redisserver.get(current_session)
        ##session_dict = json.loads(session_data.decode('utf-8','ignore'))
        
        #dict = json.loads(self.redisserver.get(current_session))
        ##print(session_dict)
        ##print('TTTTTTTTTTTTTTTTTTTTTTTT')
        ##dict = self.redisserver.hgetall(current_session)
        print(val.decode("utf-8","ignore"))
        #print('--------------------------')
        print(val)
        print('=============================')
        
        ##print(val['email'])
        
        all_keys = self.redisserver.keys('*')
        print(all_keys)
        
        request = Request(environ)
        url_return_parts = urlparse(request.url)
        welcome_url_parts = url_return_parts._replace(path='/app/welcome')
        url_return = urlunparse(welcome_url_parts)
        #all_keys = r.keys('*')
        #print(all_keys)
        #print(session['Username'])
        print(url_return)
        print('path: %s, url: %s' % (request.path, request.url))
        # just do here everything what you need
        if 'wsgi' not in request.path:
            return self.wsgi(environ, start_response)
        else:
            print('it contains wsgi')
            print(url_return)
            
            print('-----------')
            #url_return = urlparse(request.url)
            #url_return._replace(path='/app/welcome')
            start_response('301 Redirect', [('Location', url_return),])
            return []
           
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
