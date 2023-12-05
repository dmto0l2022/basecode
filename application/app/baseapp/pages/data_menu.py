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


collapse_button = html.Button([html.Span(className='navbar-toggler-icon')],
				className='navbar-toggler',
				type='button',
				**{
				'data-toggle': 'collapse',
    				'data-target':'#data_menu_navbarNav',
				'aria-controls': 'data_menu_navbarNav',
				'aria-expanded': 'false',
				'aria-label': 'Toggle navigation'
				}
				)

just_nav_options = html.Div(className="collapse navbar-collapse", id="data_menu_navbarNav",
	children=[
		html.Ul(children=[
		            html.Li([
		                    html.A('New', href='/application/baseapp/new_data', className='nav-link')],className='nav-item' ),
		            html.Li([
		                    html.A('Edit', href='/application/baseapp/edit_data', className='nav-link')], className='nav-item' ),
			    html.Li([
		                    html.A('List', href='/application/baseapp/list_data', className='nav-link')], className='nav-item' ),
			    html.Li([
		                    html.A('Help', href='/application/baseapp/help', className='nav-link')], className='nav-item' ),
            			], className='navbar-nav')
			  ])

nav_bar = html.Nav(className = 'navbar navbar-expand-lg navbar-expand-sm fixed-top navbar-light bg-light',
		   children=[html.Div(className='container-fluid',
			   children=[
				navbar_brand,
				nav_image,
				collapse_button,
				just_nav_options
					])
			    ])



layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    html.Div("Data Menu"),
    nav_bar,
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
