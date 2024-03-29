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

#from jupyter_dash import JupyterDash

import dash_bootstrap_components as dbc

import dash_daq as daq

from datetime import date
import pandas as pd

PAGES_STYLE = "/assets/pagesstyles.css"
CONTENT_STYLES = "/assets/content.css"
ALL_STYLES = "/assets/allstyles.css"
#external_stylesheets=[dbc.themes.BOOTSTRAP, PAGES_STYLE, CONTENT_STYLES]


COMPONENT_STYLE = "/assets/forms.css"
external_stylesheets=[dbc.themes.BOOTSTRAP, ALL_STYLES, COMPONENT_STYLE]

# import libraries.formlibrary as fl

from app.baseapp.libraries import formlibrary as fl

from app.baseapp.libraries import pagecomponents as pc

from app.baseapp.libraries import create_test_data

#app = JupyterDash(__name__,
#                  ##requests_pathname_prefix= "/",
#                  external_stylesheets=external_stylesheets,
#                  meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
#                 suppress_callback_exceptions=True)


#app = Dash(__name__, use_pages=True,requests_pathname_prefix='/app/multipage/')
app = Dash(__name__,
            use_pages=True,
            requests_pathname_prefix='/app/baseapp/',
            external_stylesheets=external_stylesheets,
            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
            ##suppress_callback_exceptions=True,
	  )

server = app.server

headertext = 'Dark Matter Tool'
footertext = 'ACG'



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
		    pc.side_bar_left,
		    pc.side_bar_right,
		    pages_container_box,
		    pc.page_footer_1],
                   className="container-fluid PAGE_PARENT_CONTAINER",
                  )

app.layout = layout4

	
## locally
#if __name__ == '__main__':
#    app.run_server(debug=True)
