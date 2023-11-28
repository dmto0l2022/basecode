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

no_padding = {'padding': '0 !important',    'padding-left': '0',    'padding-right':'0',   'margin-left':'0',    'margin-right': '0';
color_style = {'backgroundColor': 'blue', 'border' : '1px black solid'}
size_style = {'height' : '100%', 'width' : '100%'}

full_style = no_padding | color_style | size_style

sized_square = html.Div(style=full_style)

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sized_square, md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
		dbc.Col(html.Div("One of three columns"), md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of three columns"), md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
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
