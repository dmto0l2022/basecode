import dash

import dash_bootstrap_components as dbc
import flask
from flask import session, jsonify

from dash import Dash, dcc, html, Input, Output, dash_table, no_update

import json

server = flask.Flask(__name__)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],server=server, requests_pathname_prefix='/app/session_app/')

import os
from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

print('BASE_DIR_DASHAPP')
print(BASE_DIR)

FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY")

app.layout = html.Div([
            html.H1(children="Hello world!",className="hello",id="div3",
    style={'color':'#00361c','text-align':'center'
          }),
            html.H1(children=FLASK_SECRET_KEY ,id="div2",
    style={'color':'#00361c','text-align':'center'
          })
      ])

'''@app.callback(
	Output('div2', 'children'),
	[Input('div3', 'children')])
def update_id(children):
	return 'id: {}'.format(session.get('sessionid', None))
'''

#app.layout = dbc.Container(
#    dbc.Alert("Hello Bootstrap!", color="success"),
#    session_div,
#    className="p-5",
#)
