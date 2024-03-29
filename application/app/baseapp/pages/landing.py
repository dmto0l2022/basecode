import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/landing') ## path='/' makes it the home page for the pages app

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


page_content_style = {'position':'absolute', 'top': '0px','height':  '100%',
		'width' : '100%','left': '0','background-color': 'green',
		'overflow-y': 'scroll'}

no_padding = {'padding': '0 !important',    'padding-left': '0',    'padding-right':'0',   'margin-left':'0',    'margin-right': '0'}
background_color_style = {'backgroundColor': 'lightgrey', 'border' : '1px black solid'}
font_style={'color': 'black', 'fontSize': 14}
size_style = {'height' : '100%', 'width' : '100%'}

full_style = no_padding | background_color_style | font_style | size_style

sized_square = html.Div(children=['Content'],style=full_style)

## xs=12, sm=12, md=12, lg=6, xl=6, xxl=6

two_columns = dbc.Row(
            [
                dbc.Col(sized_square, xs=12, sm=12, md=12, lg=12, xl=12, xxl=12, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
		dbc.Col(sized_square, xs=12, sm=12, md=12, lg=12, xl=12, xxl=12, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
            ],
		className='g-0', style={'height':'100%'},
        ),


row_two_columns = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sized_square, xs=12, sm=12, md=12, lg=6, xl=6, xxl=6, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
		dbc.Col(two_columns, xs=12, sm=12, md=12, lg=6, xl=6, xxl=6, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
            ],
		className='g-0', style={'height':'100%'},
        ), ] , style = page_content_style)
	    
row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sized_square, md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
		dbc.Col(sized_square, md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(sized_square, md=4, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
            ],
		className='g-0', style={'height':'100%'},
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3, style={'color': 'blue', 'fontSize': 14, 'border' : '1px black solid'}),
            ],
		className='g-0',
        ),
    ],
    className="PAGE_CONTENT")

layout = row_two_columns

'''
@callback(
    Output(component_id='analytics-output', component_property='children'),
    Input(component_id='analytics-input', component_property='value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'
'''
