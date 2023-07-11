import dash
from dash import html, dcc, callback, Output, Input
from flask import session

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/dash_session')

data_here = html.Div(id='div2',children=['data here'])
submit_button = html.Button('Submit', id='submit-val', n_clicks=0)
layout = html.Div(children=[data_here,submit_button],id='content1')

@callback(
	Output('div2', 'children'),
	Input('submit-val', 'n_clicks'))
def getvalue(clicks_in):
	return_value = {}
	for key, value in session.items():
              return_value[key] = value
	return return_value
