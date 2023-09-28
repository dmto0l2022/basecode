import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

#import formlibrary as fl

dash.register_page(__name__, path='/edit_existing_plot')


#### edit existing plot form

edit_existing_plot_form_title = html.Div(html.P(children='Edit Existing Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

edit_existing_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Edit Existing Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)


next_button =  html.Div(dbc.Button("Next",  id="edit_existing_plot_next_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="edit_existing_plot_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")


edit_existing_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_existing_plot_form_title,
     edit_existing_plot_form_content,
     next_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

layout = edit_existing_plot_form


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("edit_existing_plot_next_button_id", "n_clicks"),
    Input("edit_existing_plot_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "edit_existing_plot_next_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.list_user_plots']['path']
        return href_return
    elif "edit_existing_plot_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
