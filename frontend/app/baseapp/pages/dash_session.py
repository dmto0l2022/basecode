import dash
from dash import html, dcc, callback, Output, Input
from flask import session

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/dash_session')

data_here = html.Div(id='div2',children=['data here'])
submit_button = html.Button('Submit', id='submit-val', n_clicks=0)

import dash_bootstrap_components as dbc
from dash import html

row1 = html.Div(
    [
        dbc.Row(dbc.Col(data_here))
    ]
)

row2 = html.Div(
    [
        dbc.Row(dbc.Col(submit_button))
    ]
)

row = html.Div(
    [
        dbc.Row(dbc.Col(data_here)),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(submit_button),
            ]
        ),
    ]
)

layout = row

@callback(
	Output('div2', 'children'),
	Input('submit-val', 'n_clicks'))
def getvalue(clicks_in):
	return_value = {}
	if not session:
		return_value = {'nodata':'nodata'}
	else:
		for key, value in session.items():
	              return_value[key] = value
	return return_value
