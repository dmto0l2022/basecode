import os
from os import environ, path
#from flask_session import Session
from flask import request, session
import redis

import dash
from dash import dcc
from dash import html
from dash import Dash, html
from dash import Input, Output, State, callback
from dash import dash_table, no_update  # Dash version >= 2.0.0

from dash import callback_context

import plotly.graph_objects as go
from plotly.subplots import make_subplots

####

import plotly.express as px
import json
import requests
import pickle
import dash_bootstrap_components as dbc

from flask import request, session

#from app.baseapp.libraries import formlibrary as fl
#from app.baseapp.libraries import main_table as mt
## from app.baseapp.libraries import get_dmtool_user as gdu

import redis

####



#from dash import Dash, Input, Output, callback

#from jupyter_dash import JupyterDash

import dash_bootstrap_components as dbc

import dash_daq as daq

from datetime import date
import pandas as pd

from dotenv import load_dotenv
BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))
## requests_pathname_prefix
REQUESTS_PATHNAME_PREFIX = environ.get("REQUESTS_PATHNAME_PREFIX")
FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY")


#PAGES_STYLE = "/assets/pagesstyles.css"
#CONTENT_STYLES = "/assets/content.css"
ALL_STYLES = "/application/baseapp/allstyles.css"
#external_stylesheets=[dbc.themes.BOOTSTRAP, PAGES_STYLE, CONTENT_STYLES]


#COMPONENT_STYLE = "/login/baseapp/forms.css"
external_stylesheets=[dbc.themes.BOOTSTRAP, ALL_STYLES]

# import libraries.formlibrary as fl

#from app.baseapp.libraries import formlibrary as fl

from app.baseapp.libraries import pagecomponents as pc

#from app.baseapp.libraries import create_test_data

#app = JupyterDash(__name__,
#                  ##requests_pathname_prefix= "/",
#                  external_stylesheets=external_stylesheets,
#                  meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
#                 suppress_callback_exceptions=True)


#app = Dash(__name__, use_pages=True,requests_pathname_prefix='/app/multipage/')
app = Dash(__name__,
            use_pages=True,
            requests_pathname_prefix=REQUESTS_PATHNAME_PREFIX,#  '/login/baseapp/',
            external_stylesheets=external_stylesheets,
            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
            ##suppress_callback_exceptions=True,
	  )


server = app.server
server.config['SECRET_KEY'] = FLASK_SECRET_KEY
server.config['FLASK_DEBUG'] = 0

#server.config['SESSION_COOKIE_PATH'] =  '/'

## setup session data ## this created a new session
#server.config['SESSION_TYPE'] = 'redis'
#server.config['SESSION_REDIS'] = redis.from_url('redis://container_redis_1:6379')
#server_session = Session()
#server_session.init_app(server)

headertext = 'Dark Matter Tool'
footertext = 'ACG'

### no drop down
nav_menu = html.Div([
    html.Ul([
            html.Li([
                    dcc.Link('Page A', href='/page-a')
                    ], className=''),
            html.Li([
                    dcc.Link('Page B', href='/page-b')
                    ], className=''),
            ], className='nav navbar-nav')
], className='navbar navbar-default navbar-static-top')

'''
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
    Dropdown button
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item" href="#">Action</a></li>
    <li><a class="dropdown-item" href="#">Another action</a></li>
    <li><a class="dropdown-item" href="#">Something else here</a></li>
  </ul>
</div>
'''

navbar_dropdown = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.I(className="bi bi-check-circle-fill me-2")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)

pages_container = html.Div([
	html.H1('Multi-page app with Dash Pages'),
	    html.Div(
	        [
	            html.Div(
	                dcc.Link(
	                    f"{page['name']} - {page['path']}", href=page["relative_path"]
	                )
	            )
	            for page in dash.page_registry.values()
	        ]
	    ),
		dash.page_container
	], className='PAGE_CONTENT')


pages_container_box = html.Div(children=[dash.page_container],className='PAGE_CONTENT')

layout4 = html.Div([pc.page_header_0,
		    pc.page_header_1,
		    pc.page_header_2,
		    navbar_dropdown,
		    ##pc.side_bar_left,
		    ##pc.side_bar_right,
		    pages_container_box,
		    pc.page_footer_1],
                   #className="container-fluid PAGE_PARENT_CONTAINER",
		   className="container-fluid PAGE_PARENT_CONTAINER",
                  )

app.layout = layout4

	
## locally
#if __name__ == '__main__':
#    app.run_server(debug=True)
