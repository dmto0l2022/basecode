from dash import Dash
from dash import html
##from werkzeug.wsgi import DispatcherMiddleware
##from werkzeug.middleware.dispatcher import DispatcherMiddleware
#from flask import Blueprint
import flask
from flask import current_app, Blueprint, render_template
dash_public_page_bp = Blueprint('dash_public_page_bp', __name__)

server = flask.Flask(__name__)
#dash_app1 = Dash(__name__, server = server, url_base_pathname='/dash1/')
#dash_app1.layout = html.Div([html.H1('Hi there, I am Dash1')])

@dash_public_page_bp.route('/dmpublic/')
def publiclanding():
     #return "This will be a public dash app"
     return flask.redirect('/app1')

#current_app.wsgi_app = DispatcherMiddleware(server, {'/dash1': dash_app1.server})

#current_app = DispatcherMiddleware(server, {
#    '/dash1': dash_app1.server
#})

'''
from dash import Dash
from werkzeug.wsgi import DispatcherMiddleware
import flask
from werkzeug.serving import run_simple
import dash_html_components as html

server = flask.Flask(__name__)
dash_app1 = Dash(__name__, server = server, url_base_pathname='/dashboard/')
dash_app2 = Dash(__name__, server = server, url_base_pathname='/reports/')
dash_app1.layout = html.Div([html.H1('Hi there, I am Dash1')])
dash_app2.layout = html.Div([html.H1('Hi there, I am Dash2')])
@server.route('/')
@server.route('/hello')
def hello():
    return 'hello world!'

@server.route('/dashboard/')
def render_dashboard():
    return flask.redirect('/dash1')


@server.route('/reports/')
def render_reports():
    return flask.redirect('/dash2')

app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server
})
'''
