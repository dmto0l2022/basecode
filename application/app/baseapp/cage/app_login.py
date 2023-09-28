import dash
from dash import html, dcc, callback, Output, Input

from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/app_login')

login_row = fl.login_form

layout = login_row

@callback(
    Output('url', 'href',allow_duplicate=True),
    #Output("hidden_div_for_redirect_callback", "children"),
    Input('submit_button1', 'n_clicks'),
    prevent_initial_call=True)
def button_click(n_clicks):
    print('trigger')
    href_home=dash.page_registry['pages.home']['path']
    # When you click the button, change the end of the url to 'ABC'
    #return dcc.Location(pathname="/app/applogin", id="someid_doesnt_matter")
    return href_home
