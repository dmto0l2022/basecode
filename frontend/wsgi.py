from app import init_app

from app import current_user

from app import session

from urllib.parse import urlparse, urlunparse

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from werkzeug.wrappers import Request, Response, ResponseStream

from werkzeug.debug import DebuggedApplication

from werkzeug.utils import redirect

from app.dashapps.interactive_table import app as app1
from app.dashapps.basic_table import app as app2
from app.dashapps.session_app import app as app3

from app.dashpages.app import app as app4

app = init_app()

class Middleware:

    def __init__(self, wsgi):
        self.wsgi = wsgi
        
    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)
        url_return_parts = urlparse(request.url)
        welcome_url_parts = url_return_parts._replace(path='/app/welcome')
        url_return = urlunparse(welcome_url_parts)
        print(session['Username'])
        print(url_return)
        print('path: %s, url: %s' % (request.path, request.url))
        # just do here everything what you need
        if 'wsgi' in request.path:
            print('it contains wsgi')
            print(url_return)
            print('-----------')
            #url_return = urlparse(request.url)
            #url_return._replace(path='/app/welcome')
            start_response('301 Redirect', [('Location', url_return),])
            return []
        else:
            return self.wsgi(environ, start_response)
'''

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
