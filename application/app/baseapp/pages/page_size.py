from dash import clientside_callback

import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(__name__, path='/page_size')

page_prefix_url = '/application/baseapp/'


layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='viewport-container')
])

clientside_callback(
    """
    function(href) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        return {'height': h, 'width': w};
    }
    """,
    Output('viewport-container', 'children'),
    Input('url', 'href')
)
