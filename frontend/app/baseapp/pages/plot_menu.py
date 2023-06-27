import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/plot_menu')
page_name = 'plot_menu'

layout = html.Div([
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Div("Plots Main Menu")])



