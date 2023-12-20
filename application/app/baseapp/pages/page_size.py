from dash import clientside_callback


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
