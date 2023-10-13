import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/login_menu')
page_name = 'login_menu'
baseapp_prefix = '/application/baseapp'

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
    html.Div("Login Menu"),
    html.Button('Login', id=page_name + '_login_' + 'button_id', n_clicks=0),
    html.Button('Logout', id=page_name + '_logout_' + 'button_id', n_clicks=0),
    html.Button('Admin', id=page_name + '_admin_' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id=page_name + "whatbutton")
    ])


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input(page_name + '_login_' + 'button_id', "n_clicks"),
    Input(page_name + '_logout_' + 'button_id', "n_clicks"),
    Input(page_name + '_admin_' + 'button_id', "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(button1,button2,button3):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name + '_login_' + 'button_id' == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = baseapp_prefix + '/login'
        return href_return
    elif page_name + '_logout_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = baseapp_prefix + '/logout'
        return href_return
    elif page_name + '_admin_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = baseapp_prefix +'/login_menu'
        return href_return
    else:
        href_return = baseapp_prefix + '/login_menu'
        return href_return
