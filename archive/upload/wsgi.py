from app import create_app

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from app.dashapps.app1 import app as app1

app = create_app()

application = DispatcherMiddleware(app, {
    '/app1': app1.server,
})  
