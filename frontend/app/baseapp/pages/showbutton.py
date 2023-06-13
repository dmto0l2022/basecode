import flask
import dash
from dash import Dash, dcc, html, Input, Output, State, callback

dash.register_page(__name__, path='/showbutton')

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Button('Submit', id='submit_button', n_clicks=0),
    dcc.Link(html.Button('LOGIN'),
                           href='/app/applogin')])


'''
@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )
'''

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    #Output("hidden_div_for_redirect_callback", "children"),
    Input('submit_button', 'n_clicks'),
    prevent_initial_call=True)
def button_click(n_clicks):
    print('trigger')
    href_login=dash.page_registry['pages.app_login']['path']
    # When you click the button, change the end of the url to 'ABC'
    #return dcc.Location(pathname="/app/applogin", id="someid_doesnt_matter")
    return href_login
'''
@app.callback(Output('location', 'href'),
              Input('example-graph', 'clickData'),
              prevent_initial_call=True)
def redirect_to_url(clickData):
    # do something with clickData
    url = 'https:www.example.com'
    return url
'''
