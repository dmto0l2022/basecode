import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/homepage')

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Button('Create New Plot', id='create_new_plot_button_id', n_clicks=0),
    html.Button('Edit Existing Plot', id='edit_existing_plot_button_id', n_clicks=0),
    html.Button('Create New Limit', id='create_new_limit_button', n_clicks=0),
    html.Button('Edit Existing Limit', id='edit_existing_limit_button', n_clicks=0),
    html.Div('No Button Pressed', id="whatbutton"),
    dcc.Link(html.Button('LOGIN'),
                           href='/app/applogin')])


'''
@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )
'''

'''
app.layout = html.Div(
    [
        dbc.Button("Show Example 1", id="open1", n_clicks=0),
        dbc.Button("Show Example 2", id="open2", n_clicks=0),
        html.Div('No Button Pressed', id="whatbutton"),
        example_modal
    ]
)
'''

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("create_new_plot_button_id", "n_clicks"),
    Input("edit_existing_plot_button_id", "n_clicks"),
    Input("create_new_limit_button", "n_clicks"),
    Input("edit_existing_limit_button", "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(button1,button2,button3,button4):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "create_new_plot_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = '/app/baseapp/create_new_plot'
        return href_return
    elif "edit_existing_plot_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = '/app/baseapp/edit_existing_plot'
        return href_return
    elif "create_new_limit_button" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = '/app/baseapp/create_new_limit'
        return href_return
    elif "edit_existing_limit_button" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_limit']['path']
        href_return = '/app/baseapp/edit_existing_limit'
        return href_return
    else:
        href_return = '/baseapp/homepage'
        return href_return
        

'''
@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    #Output("hidden_div_for_redirect_callback", "children"),
    Input('create_new_plot_button_id', 'n_clicks'),
    prevent_initial_call=True)
def button_click(n_clicks):
    print('trigger')
    href_login=dash.page_registry['pages.app_login']['path']
    # When you click the button, change the end of the url to 'ABC'
    #return dcc.Location(pathname="/app/applogin", id="someid_doesnt_matter")
    return href_login

@app.callback(Output('location', 'href'),
              Input('example-graph', 'clickData'),
              prevent_initial_call=True)
def redirect_to_url(clickData):
    # do something with clickData
    url = 'https:www.example.com'
    return url
'''
