from dash import Dash, html, Input, Output, ctx, callback

import dash

dash.register_page(__name__, path='/which_button')

layout = html.Div([
    html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
    html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
    html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
    html.Div(id='container-button-timestamp')
])

@callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')
)
def displayClick(btn1, btn2, btn3):
    msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if "btn-nclicks-1" == prop_id:
        msg = "Button 1 was most recently clicked"
    elif "btn-nclicks-2" == prop_id:
        msg = "Button 2 was most recently clicked"
    elif "btn-nclicks-3" == prop_id:
        msg = "Button 3 was most recently clicked"
    return html.Div(msg)
