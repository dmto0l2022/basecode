import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/edit_existing_limit')

#### edit existing limit form

edit_existing_limit_form_title = html.Div(html.P(children='Edit Existing Limit', className = "NOPADDING_CONTENT FORM_TITLE"))


edit_existing_limit_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Edit Existing Limit', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

save_button =  html.Div(dbc.Button("Save",id="edit_existing_limit_save_button_id", color="primary"), className = "FORM_SAVE_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="edit_existing_limit_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

edit_existing_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_existing_limit_form_title,
     edit_existing_limit_form_content,
     save_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


layout = edit_existing_limit_form


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("edit_existing_limit_save_button_id", "n_clicks"),
    Input("edit_existing_limit_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "edit_existing_limit_save_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.list_all_limits']['path']
        return href_return
    elif "edit_existing_limit_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
