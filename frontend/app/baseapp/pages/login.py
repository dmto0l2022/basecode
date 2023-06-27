import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
from dash import html, dcc

dash.register_page(__name__)
page_name = 'login'

import dash_bootstrap_components as dbc
from dash import Input, Output

login_frame = html.Iframe(src="/app/login",style={"height": "80vh", "width": "80vw"})

layout = html.Div(children=[login_frame],style={"height": "80vh", "width": "80vw"})

