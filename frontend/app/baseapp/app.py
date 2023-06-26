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
#external_stylesheets=[dbc.themes.BOOTSTRAP, PAGES_STYLE, CONTENT_STYLES]


COMPONENT_STYLE = "/assets/forms.css"
external_stylesheets=[dbc.themes.BOOTSTRAP, COMPONENT_STYLE, PAGES_STYLE, CONTENT_STYLES]

# import libraries.formlibrary as fl

from app.baseapp.libraries import formlibrary as fl

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

def GetHeaderAndFooter(headertext, footertext):


    hdivs = html.P(headertext)
    header1 = html.Div([hdivs], style={**FULL_DIV,**NOPADDING},)

    fdivs = [html.P(footertext)]
    
    footer1 = html.Div(fdivs, style={**FULL_DIV,**NOPADDING},)

    headerrow_out =  html.Div(className="row",children=[header1],
                           style={**HEADER_ROW,**NOPADDING})

    footerrow_out =  html.Div(className="row",children=[footer1],
                           style={**FOOTER_ROW,**NOPADDING})
    
    return headerrow_out, footerrow_out

headerrow, footerrow = GetHeaderAndFooter(headertext, footertext)

l_sidebar_in = 'L sidebar'
r_sidebar_in = 'R sidebar'

def GetSideBars(l_sidebar_in, r_sidebar_in):

    l_sidebar_col_out =  html.Div(children='L sidebar',
                                  className="col col-lg-1",
                                  style={**NOPADDING, **SIDEBAR_DIV})
    
    r_sidebar_col_out =  html.Div(children='R sidebar',
                                  className="col col-lg-1",
                                  style={**NOPADDING, **SIDEBAR_DIV})
    
    
    return l_sidebar_col_out, r_sidebar_col_out


l_sidebar_col, r_sidebar_col = GetSideBars(l_sidebar_in, r_sidebar_in) 

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
	])


layout4 = html.Div([headerrow,pages_container,footerrow],
                   className="container-fluid",
                   style=MASTER_CONTAINER_STYLE,
                  )

app.layout = layout4

	
## locally
#if __name__ == '__main__':
#    app.run_server(debug=True)
