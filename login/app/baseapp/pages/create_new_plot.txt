import dash
from dash import html, dcc, callback, Output, Input, State
#from flask import session
from flask import request

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/create_new_plot')
page_name = 'create_new_plot'
baseapp_prefix = '/login/baseapp'

## id='plot_name_form_field_id',

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url_create_new_plot", refresh=True), ## important to allow redirects
    html.Div("Create New Plot"),
    fl.plot_name_input_row,
    html.Button('Print', id=page_name + '_print_' + 'button_id', n_clicks=0),
    html.Button('Create', id=page_name + '_create_' + 'button_id', n_clicks=0),
    html.Button('Cancel',  id=page_name + '_cancel_' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id="whatbutton")
    ])


@callback(
    Output('url_create_new_plot', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    Input(page_name + '_print_' + 'button_id', "n_clicks"),
    Input(page_name + '_create_' + 'button_id', "n_clicks"),
    Input(page_name + '_cancel_' + 'button_id', "n_clicks"),
    State("plot_name_form_field_id", "value"),
        prevent_initial_call=True
)
def button_click_create_new_plot(button0,button1,button2,plot_name_input):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print("create new plot >> prop id >>  " ,prop_id)
    #msg = prop_id
    if page_name + '_print_' + 'button_id' == prop_id :
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        session_key = request.cookies.get('session')
        print('cnp : session key >>',session_key)
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        href_return = '/app/baseapp/create_new_plot'
        return href_return
    elif page_name + '_create_' + 'button_id' == prop_id :
        href_return = baseapp_prefix+ '/select_limits_to_plot'
        return href_return
    elif page_name + '_cancel_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = baseapp_prefix+ '/plot_menu'
        return href_return
    else:
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return
        
