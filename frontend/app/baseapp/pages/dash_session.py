import dash
from dash import html, dcc, callback, Output, Input
from app import session

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/dash_session')

layout = html.Div([html.Div(id='div2'),html.Div(id='div3')])

@callback(
	Output('div2', 'children'),
	Input('div3', 'children'))
def update_user(children):
	return 'User: {}'.format(session.get('email', None))


