import dash
from dash import html, dcc, callback, Output, Input
from flask import session

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/dash_session')

def create_layout():
    layout02 = html.Div([
    html.Div(children=[session['dmtool_email_address']],id='display-value')
    ])
    return layout02
    
layout = create_layout()
