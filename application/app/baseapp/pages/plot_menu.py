import dash
from dash import html, dcc, callback, Output, Input

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/plot_menu')
page_name = 'plot_menu'
baseapp_prefix = '/application/baseapp'

'''
<!-- Example split danger button -->
<div class="btn-group">
  <button type="button" class="btn btn-danger">Action</button>
  <button type="button" class="btn btn-danger dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    <span class="sr-only">Toggle Dropdown</span>
  </button>
  <div class="dropdown-menu">
    <a class="dropdown-item" href="#">Action</a>
    <a class="dropdown-item" href="#">Another action</a>
    <a class="dropdown-item" href="#">Something else here</a>
    <div class="dropdown-divider"></div>
    <a class="dropdown-item" href="#">Separated link</a>
  </div>
</div>

html.Button(
[
html.Span(className=‘navbar-toggler-icon’)
],
className=“navbar-toggler”,
type=‘button’,
**{
‘data-toggle’: ‘collapse’,
‘data-target’: “#navbarNav”,
‘aria-controls’: “navbarNav”,
‘aria-expanded’: “false”,
‘aria-label’: “Toggle navigation”
}
),

'''
danger_button = html.Button("Danger", className="btn btn-danger",type="button")

new_plot_button = html.Button("New Plot", id=page_name+"new_plot_button", className="btn btn-primary",type="button")

dropdown_button = html.Button(id=page_name + "dropdown_button", type="button",
                           className = "btn btn-danger dropdown-toggle dropdown-toggle-split",
                           **{
                            'data-toggle' : 'dropdown',
                            'aria-haspopup' : 'true',
                            'aria-expanded' : 'false',
                            },
                            children=html.Span(className="sr-only", children=['Plot Menu'])
                          )

drop_down_new =  html.A(id=page_name + "dropdown_action", children=['New'], href=baseapp_prefix + '/create_new_plot', className="dropdown-item")
drop_down_edit =  html.A(id=page_name + "dropdown_action", children=['Edit'], href=baseapp_prefix + '/edit_existing_plot', className="dropdown-item")
drop_down_list =  html.A(id=page_name + "dropdown_action", children=['List'], href=baseapp_prefix + '/list_all_plots', className="dropdown-item")

dropdown_menu = html.Div(id=page_name + "dropdown_menu", children = [drop_down_new,drop_down_edit,drop_down_list], className = "dropdown-menu")

split_button = html.Div(children=[new_plot_button,dropdown_button,dropdown_menu], className="btn-group")

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url", refresh=True), ## important to allow redirects
    #html.Div("Plot Menu"),
    split_button,
    #html.Button('Create New', id=page_name + '_create_new_' + 'button_id', n_clicks=0),
    #html.Button('Edit Existing', id=page_name + '_edit_existing_' + 'button_id', n_clicks=0),
    #html.Button('List', id=page_name + '_list__' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id=page_name+"whatbutton")
    ])


@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input(page_name+"new_plot_button", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name+"new_plot_button" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return
    else:
        href_return = baseapp_prefix + '/plot_menu'
        return href_return
        



