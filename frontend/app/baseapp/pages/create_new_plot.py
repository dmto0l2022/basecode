import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

#import formlibrary as fl

dash.register_page(__name__, path='/create_new_plot')

###############

#### create new plot form

create_new_plot_form_title = html.Div(html.P(children='Create New Plot', className = "NOPADDING_CONTENT FORM_TITLE"))


create_new_plot_form_content_old  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Create New Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

create_new_plot_form_content = plot_name_input_row

next_button =  html.Div(dbc.Button("Next",  id="create_new_plot_next_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="create_new_plot_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

create_new_plot_form = html.Div(
    [dcc.Location(id="url", refresh=True),
     create_new_plot_form_title,
     create_new_plot_form_content,
     next_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

new_plot_row = create_new_plot_form

layout = new_plot_row

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("next_buttonid", "n_clicks"),
    Input("cancel_buttonid", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "next_buttonid" == prop_id :
        #msg = "Button 1 was most recently clicked"
        #href_return = dash.page_registry['pages.select_limits_to_plot']['path']
        href_return = '/app/baseapp/select_limits_to_plot'
        return href_return
    elif "cancel_buttonid" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/app/baseapp/homepage'
        return href_return
    else:
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/app/baseapp/homepage'
        return href_return
        
