import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
from dash import html, dcc

dash.register_page(__name__)
page_name = 'help'

import dash_bootstrap_components as dbc
from dash import Input, Output

input_group = dbc.InputGroup(
    [
        dbc.Button("Random name", id= page_name + "-button", n_clicks=0),
        dbc.Input(id=page_name + "-button-input", placeholder="name"),
    ]
)

help_text = html.Div(children=["Help will appear here!"])

layout = html.Div(children=[input_group,help_text])

@callback(
    Output(page_name + "-button-input", "value"),
    [Input(page_name + "-button", "n_clicks")],
)
def on_button_click(n_clicks):
    if n_clicks:
        names = ["Arthur Dent", "Ford Prefect", "Trillian Astra"]
        which = n_clicks % len(names)
        return names[which]
    else:
        return ""
