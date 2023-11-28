import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/') ## path='/' makes it the home page for the pages app

layout1 = html.Div(children=[
    html.H1(children='This is our Analytics page'),
	html.Div([
        "Select a city: ",
        dcc.RadioItems(['New York City', 'Montreal','San Francisco'],
        'Montreal',
        id='analytics-input')
    ]),
	html.Br(),
    html.Div(id='analytics-output'),
])


row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
		dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
            ]
        ),
    ]
)

layout = row

'''
@callback(
    Output(component_id='analytics-output', component_property='children'),
    Input(component_id='analytics-input', component_property='value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'
'''
