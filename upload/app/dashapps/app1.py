import dash
from dash import html

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/app1/'
)

app.layout = html.Div("Dash app 1")  
