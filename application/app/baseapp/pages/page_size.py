from dash import clientside_callback

import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(__name__, path='/page_size')

page_prefix_url = '/application/baseapp/'
page_name = 'page_size'


layout = html.Div([
    dcc.Location(id=page_name + 'url'),
    html.Div(id=page_name + 'viewport-container', children=['Size Here'])
])

clientside_callback(
    """
    function(href) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        return h;
    }
    """,
    Output(page_name + 'viewport-container', 'value'),
    Input(page_name + 'url', 'href')
)
