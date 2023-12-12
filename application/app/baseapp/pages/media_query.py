## https://community.plotly.com/t/switch-between-these-two-layouts-based-on-screen-size/66230/3

from dash import Dash
import dash_bootstrap_components as dbc

import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/media_query', title="Media Query")

top = dbc.Col('top', style={'height': '10em', 'background-color': '#636EFA'})
middle = dbc.Col('middle', style={'height': '20em', 'background-color': '#EF553B'})
bottom = dbc.Col('bottom', style={'height': '8em', 'background-color': '#00CC96'})

layout_inner = [
    dbc.Col(
        top,
        xs=dict(order=1, size=12),
        sm=dict(order=1, size=6)
    ),
    dbc.Col(
        middle,
        xs=dict(order=2, size=12),
        sm=dict(order=3, size=6)
    ),
    dbc.Col(
        bottom,
        xs=dict(order=3, size=12),
        sm=dict(order=2, size=6)
    )
]

layout = dbc.Container(layout_inner, className='root-container')
