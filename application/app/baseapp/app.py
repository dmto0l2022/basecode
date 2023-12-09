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
external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, ALL_STYLES]

#external_scripts = [
#    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},

'''
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
'''

## these are required to enable the dropdown menus to work
external_scripts = [
{ 'src':"https://code.jquery.com/jquery-3.3.1.slim.min.js", 'integrity':"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo", 'crossorigin':"anonymous"},
{ 'src':"https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js", 'integrity':"sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1", 'crossorigin':"anonymous"},
{ 'src':"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js", 'integrity':"sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM", 'crossorigin':"anonymous"}
]

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
	    external_scripts=external_scripts,
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
nav_menu = html.Div(id='id 111', children=[
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


  <div class="dropdown">
      <!-- Link or button to toggle dropdown -->
        <a id="drop1" href="#" role="button" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>
      <ul class="dropdown-menu" role="menu" aria-labelledby="dLabel">
        <li><a tabindex="-1" href="#">Action</a></li>
        <li><a tabindex="-1" href="#">Another action</a></li>
        <li><a tabindex="-1" href="#">Something else here</a></li>
        <li class="divider"></li>
        <li><a tabindex="-1" href="#">Separated link</a></li>
      </ul>
    </div>


<nav class="navbar navbar-expand-lg navbar-expand-sm fixed-top navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#"></a>
    <img src="./DMToolsLogo.png" alt="Logo" class="d-inline-block align-text-top">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/application/baseapp/">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/application/login/google">Login</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/application/testapp/landing">Public</a>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
'''

nav_bar_height = '35px'

navbar_brand = html.A(className='navbar-brand', href='#',style={'height':nav_bar_height})
image_path = 'assets/DMToolsLogo.png'
nav_image = html.Img(src=image_path,style={'height':nav_bar_height})


collapse_button = html.Button([html.Span(className='navbar-toggler-icon')],
				className='navbar-toggler',
				type='button',
				**{
				'data-toggle': 'collapse',
    				'data-target':'#navbarNav',
				'aria-controls': 'navbarNav',
				'aria-expanded': 'false',
				'aria-label': 'Toggle navigation'
				})


no_padding_or_margins = {'padding':'0px', 'margin':'0px', 'line-height': '20px'}

just_nav_options = html.Div(className="collapse navbar-collapse", id="navbarNav",
	children=[
		html.Ul(children=[
		            html.Li([
		                    html.A('Plot', href='/application/baseapp/plot_menu', className='nav-link',style=no_padding_or_margins)],className='nav-item' ,style=no_padding_or_margins),
		            html.Li([
		                    html.A('Data', href='/application/baseapp/data_menu', className='nav-link',style=no_padding_or_margins)], className='nav-item' ,style=no_padding_or_margins),
			    html.Li([
		                    html.A('Admin', href='/application/baseapp/admin_menu', className='nav-link',style=no_padding_or_margins)], className='nav-item' ,style=no_padding_or_margins),
			    html.Li([
		                    html.A('Help', href='/application/baseapp/help', className='nav-link',style=no_padding_or_margins)], className='nav-item' ,style=no_padding_or_margins),
            			], className='navbar-nav',style=no_padding_or_margins)
			  ])

nav_bar = html.Nav(className = 'navbar navbar-expand-lg navbar-expand-sm fixed-top navbar-light bg-light',
		   children=[html.Div(className='container',
			   children=[
				navbar_brand,
				nav_image,
				collapse_button,
				just_nav_options
					])
			    ],style={'height':nav_bar_height} | no_padding_or_margins)

'''

just_nav_options = html.Div( className="collapse navbar-collapse", id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/application/baseapp/">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/application/login/google">Login</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/application/testapp/landing">Public</a>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
        </li>
      </ul>
    </div>


## aria help : https://community.plotly.com/t/can-data-attributes-be-created-in-dash/7222/13

html.Div(**{‘data-label’: ‘’})


html.Button(
[
html.Span(className=‘navbar-toggler-icon’)
],
className=“navbar-toggler”,
type=‘button’,
**{
‘data-toggle’: ‘collapse’,
‘data-target’: “#navbarNav”,
‘aria-controls’: “navbarNav”,
‘aria-expanded’: “false”,
‘aria-label’: “Toggle navigation”
}
),
'''

menu_icon = html.I(className="bi bi-menu-button")

dropdown_button = html.Div(children=[menu_icon, ##'Drop Down Button',
			html.Span(className='navbar-toggler-icon')
			],
			className='btn btn-secondary dropdown-toggle',
			id='dropdownMenuButton1',**{
			'data-toggle': 'dropdown',
			'aria-expanded': 'false'
			}
			) 

nav_menu_button = html.Div(id='nav_menu_button',
    children=[dropdown_button,
	html.Ul([
            html.Li([
                    html.A('Plot', href='#', className='dropdown-item')]),
            html.Li([
                    html.A('Data', href='#', className='dropdown-item')]),
	    html.Li([
                    html.A('Admin', href='#', className='dropdown-item')]),
	    html.Li([
                    html.A('Help', href='#', className='dropdown-item')]),
            ], className='dropdown-menu', **{'aria-labelledby':'dropdownMenuButton1'}
                ) ], className='dropdown')




####


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
	], className='PAGE_CONTENT') ##, style={'overflow': 'auto'})


pages_container_box = html.Div(children=[dash.page_container],
			       style={'position': 'absolute',
					    'top': 'var(--header_height)',
					    'height' :  'calc(100% - 80px)',
					    'width' : 'var(--content_width)',
					    'left': 'var(--sidebar_width)',
					    'background-color': 'lightgray',
					    'overflow-y': 'scroll'})

layout4 = html.Div([##pc.page_header_0,
		    ##pc.page_header_1,
		    ##pc.page_header_2,
		    #nav_menu_button,
		    nav_bar,
		    ##pc.side_bar_left,
		    ##pc.side_bar_right,
		    pages_container_box,
		    pc.page_footer_1],
		   className="container",
                  )

app.layout = layout4

	
## locally
#if __name__ == '__main__':
#    app.run_server(debug=True)
