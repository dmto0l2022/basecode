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

dash.register_page(__name__, path='/logout')

page_name = 'logout'

##logout_frame = html.Iframe(src="/app/logout",style={"height": "80vh", "width": "80vw"})

layout = html.Div(children="Now logged out",style={"height": "80vh", "width": "80vw"})
