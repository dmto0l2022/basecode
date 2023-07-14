import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

# import formlibrary as fl

dash.register_page(__name__, path='/show_user_plot')

#### show plot

show_user_plot_form_title = html.Div(html.P(children='Show User Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

show_user_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Show User Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

edit_button =  html.Div(dbc.Button("Edit",  id="show_user_plot_edit_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

save_button =  html.Div(dbc.Button("Save",  id="show_user_plot_save_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="show_user_plot_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")


show_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     show_user_plot_form_title,
     show_user_plot_form_content,
     edit_button, save_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


layout = show_plot_form

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("show_user_plot_edit_button_id", "n_clicks"),
    Input("show_user_plot_save_button_id", "n_clicks"),
    Input("show_user_plot_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2,button3):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "show_user_plot_edit_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.edit_user_plot']['path']
        return href_return
    elif "show_user_plot_save_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.select_limits_to_plot']['path']
        return href_return
    elif "show_user_plot_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
