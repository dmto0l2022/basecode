import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__)
page_name = 'plot_menu'

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Button('Create New Plot', id='create_new_plot_button_id', n_clicks=0),
    html.Button('Edit Existing Plot', id='edit_existing_plot_button_id', n_clicks=0),
    html.Button('List Existing Plots', id='list_existing_plot_button_id', n_clicks=0),
    html.Div('No Button Pressed', id="whatbutton"),])


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("create_new_plot_button_id", "n_clicks"),
    Input("edit_existing_plot_button_id", "n_clicks"),
    Input("list_existing_plot_button_id", "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(button1,button2,button3):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print("plot_menu - button id >>>>>>>>>>> ", prop_id)
    #msg = prop_id
    if "create_new_plot_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = '/app/baseapp/create_new_plot'
        return href_return
    elif "edit_existing_plot_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = '/app/baseapp/list_user_plots'
        return href_return
    elif "list_existing_plot_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = '/app/baseapp/list_user_plots'
        return href_return
    else:
        href_return = '/baseapp/plot_menu'
        return href_return
        

