import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/plot_menu')
page_name = 'plot_menu'


layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Div("Create New Plot"),
    html.Button('Create', id=page_name + '_create_new_' + 'button_id', n_clicks=0),
    html.Button('Cancel', id=page_name + '_edit_existing_' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id="whatbutton")
    ])


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input(page_name + '_create_' + 'button_id', "n_clicks"),
    Input(page_name + '_cancel_' + 'button_id', "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name + '_create_' + 'button_id' == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = '/app/baseapp/select_limits_to_plot'
        return href_return
    elif page_name + '_cancel_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = '/app/baseapp/plot_menu'
        return href_return
    else:
        href_return = '/baseapp/create_new_plot'
        return href_return
        
