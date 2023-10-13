import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
from dash import html, dcc

import json
import requests

import base64

import pandas as pd

from app.baseapp.libraries import formlibrary as fl

import xml.etree.ElementTree as ET

baseapp_prefix = '/application/baseapp'

dash.register_page(__name__, path='/login')

page_name = 'login'

## login_frame = html.Iframe(src="/application/login/google",style={"height": "80vh", "width": "80vw"})

login_link = html.Div([
    dcc.Link(href='/application/login/google', title='google login',  target='_blank')
])

layout = html.Div(children=[login_link],style={"height": "80vh", "width": "80vw"})

