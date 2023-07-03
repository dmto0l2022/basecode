from app import init_app

from app import current_user

from app import session

from urllib.parse import urlparse, urlunparse

from secure_cookie.session import SessionMiddleware

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from werkzeug.wrappers import Request, Response, ResponseStream

from werkzeug.debug import DebuggedApplication

from werkzeug.utils import redirect


application = Middleware(application)

application = DebuggedApplication(application, True)
