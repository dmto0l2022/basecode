import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/admin_menu')
page_name = 'admin_menu'
baseapp_prefix = '/application/baseapp'

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
    html.Div("Admin Menu"),
    html.Button('Create New Key', id=page_name + '_create_new_key_' + 'button_id', n_clicks=0),
    html.Button('List all Keys', id=page_name + '_list_all_keys_' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id=page_name + "whatbutton")
    ])


@callback(
    Output(page_name +'url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input(page_name + '_create_new_key_' + 'button_id', "n_clicks"),
    Input(page_name + '_list_all_keys_' + 'button_id', "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(button1,button2,button3):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name + '_create_new_key_' + 'button_id' == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = baseapp_prefix + '/create_new_key'
        return href_return
    elif page_name + '_list_all_keys_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = baseapp_prefix + '/list_all_keys'
        return href_return
    else:
        href_return = baseapp_prefix + '/admin_menu'
        return href_return
