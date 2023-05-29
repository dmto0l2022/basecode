import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import libraries.formlibrary as fl

dash.register_page(__name__, path='/app/list_all_limits')


#### list all limits

list_all_limits_form_title = html.Div(html.P(children='List All Limits', className = "NOPADDING_CONTENT FORM_TITLE"))

list_all_limits_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='List All Limits', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

edit_button =  html.Div(dbc.Button("Edit", id="list_all_limits_edit_button_id", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="list_all_limits_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

list_all_limits_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_all_limits_form_title,
     list_all_limits_form_content,
     edit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

layout = list_all_limits_form


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("list_all_limits_edit_button_id", "n_clicks"),
    Input("list_all_limits_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "list_all_limits_edit_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.show_limit']['path']
        return href_return
    elif "list_all_limits_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
