import dash
from dash import html, dcc, callback, Output, Input
from flask import session

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/dash_session')

def create_layout():
    layout02 = html.Div([
    html.H3(‘App 1’),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
        {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
        'NYC', 'MTL', 'LA'
        ]
        ],
        value=]
        ),
    html.Div(children=[session['dmtool_email_address'],id=‘app-1-display-value’)
    ])
    return layout02
    
layout = create_layout()
