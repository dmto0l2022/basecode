import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

#import formlibrary as fl

dash.register_page(__name__, path='/app/select_limits_to_plot')

#### select limits to plot

select_limits_to_plot_form_title = html.Div(html.P(children='Select Limits to Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

select_limits_to_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Select Limits to Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

next_button =  html.Div(dbc.Button("Next",  id="next_button_select_limits_to_plot", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button_select_limits_to_plot", color="secondary"), className = "FORM_CANCEL_BUTN")


select_limits_to_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     select_limits_to_plot_form_title,
     select_limits_to_plot_form_content,
     next_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


layout = select_limits_to_plot_form

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("next_button_select_limits_to_plot", "n_clicks"),
    Input("cancel_button_select_limits_to_plot", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "next_button_select_limits_to_plot" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.style_plot_and_traces']['path']
        return href_return
    elif "cancel_button_select_limits_to_plot" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
