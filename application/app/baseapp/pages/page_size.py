from dash import clientside_callback

import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(__name__, path='/page_size')

page_prefix_url = '/application/baseapp/'
page_name = 'page_size'


layout = html.Div([
    dcc.Location(id=page_name + 'url'),
    html.Div(id=page_name + 'viewport-container', children=[html.P(children=['Size Here'],id='sizehere')])
])

'''
@callback(
    Output("graph", "figure"),
    Input("store", "data"),
)
def update(store):
    dff = pd.DataFrame(store)
    return px.scatter(
        dff,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
    )
'''

clientside_callback(
    """
    function(href) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        var jsn = {width: w, height: h};
        const myJSON = JSON.stringify(jsn); 
        return [myJSON, jsn];
    }
    """,
    Output('sizehere', 'children'),
    Output('screen_size_store', 'data'),
    Input(page_name + 'url', 'href')
)
