import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/data_menu')
page_name = 'data_menu'
baseapp_prefix = '/application/baseapp'

navbar_brand = html.A(className='navbar-brand', href='#')
image_path = 'assets/DMToolsLogo.png'
nav_image = html.Img(src=image_path)

button_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("New"), xs=12, sm=12, md=6, lg=2, xl=2, xxl=2),
                dbc.Col(html.Div("Edit"),xs=12, sm=12, md=6, lg=2, xl=2, xxl=2),
                dbc.Col(html.Div("List"),xs=12, sm=12, md=6, lg=2, xl=2, xxl=2),
            ]
        ),
    ]
)


layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Div("Data Menu"),
    button_row,
    html.Button('Create New', id=page_name + '_create_new_' + 'button_id', n_clicks=0),
    html.Button('Edit Existing', id=page_name + '_edit_existing_' + 'button_id', n_clicks=0),
    html.Button('List', id=page_name + '_list__' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id="whatbutton")
    ])


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input(page_name + '_create_new_' + 'button_id', "n_clicks"),
    Input(page_name + '_edit_existing_' + 'button_id', "n_clicks"),
    Input(page_name + '_list__' + 'button_id', "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(button1,button2,button3):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name + '_create_new_' + 'button_id' == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = baseapp_prefix + '/create_new_limit'
        return href_return
    elif page_name + '_edit_existing_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = baseapp_prefix + '/edit_existing_limit'
        return href_return
    elif page_name + '_list__' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = baseapp_prefix +'/list_all_limits'
        return href_return
    else:
        href_return = baseapp_prefix + '/limit_menu'
        return href_return
