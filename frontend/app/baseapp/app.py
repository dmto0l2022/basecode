import dash
from dash import dcc
from dash import html
from dash import Dash, html
from dash import Input, Output, State
from dash import dash_table

from dash import callback_context

import plotly.graph_objects as go
from plotly.subplots import make_subplots

#from dash import Dash, Input, Output, callback

from jupyter_dash import JupyterDash

import dash_bootstrap_components as dbc

import dash_daq as daq

from datetime import date
import pandas as pd

PAGES_STYLE = "/assets/pagesstyles.css"
CONTENT_STYLES = "/assets/content.css"
#external_stylesheets=[dbc.themes.BOOTSTRAP, PAGES_STYLE, CONTENT_STYLES]


COMPONENT_STYLE = "/assets/forms.css"
external_stylesheets=[dbc.themes.BOOTSTRAP, COMPONENT_STYLE, PAGES_STYLE, CONTENT_STYLES]

import libraries.formlibrary as fl

#app = JupyterDash(__name__,
#                  ##requests_pathname_prefix= "/",
#                  external_stylesheets=external_stylesheets,
#                  meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
#                 suppress_callback_exceptions=True)


#app = Dash(__name__, use_pages=True,requests_pathname_prefix='/app/multipage/')
app = Dash(__name__,
            use_pages=True,
            requests_pathname_prefix='/',
            external_stylesheets=external_stylesheets,
            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
            suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
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
])

## locally
if __name__ == '__main__':
    app.run_server(debug=True)
