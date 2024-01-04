import dash
from dash import html, dcc, callback
from dash import Input, Output, State
from dash import clientside_callback
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/') ## path='/' makes it the home page for the pages app

page_name = 'home'
baseapp_prefix = '/application/baseapp'

from app.baseapp.dashboard_libraries import get_dmtool_user as gdu
from app.baseapp.libraries import page_menu as page_menu

create_plot_button = html.Button("Create Plot", id=page_name+"create_plot_button", className="btn btn-primary",type="button")

dropdown_button = html.Button(id=page_name + "dropdown_button", type="button",
                           className = "btn btn-danger dropdown-toggle dropdown-toggle-split",
                           **{
                            'data-toggle' : 'dropdown',
                            'aria-haspopup' : 'true',
                            'aria-expanded' : 'false',
                            },
                            children=html.Span(className="sr-only", children=['Create Plot Menu'])
                          )

drop_down_create =  html.A(id=page_name + "dropdown_action", children=['New'], href=baseapp_prefix + '/create_new_plot', className="dropdown-item")
drop_down_edit =  html.A(id=page_name + "dropdown_action", children=['Edit'], href=baseapp_prefix + '/edit_existing_plot', className="dropdown-item")
drop_down_list =  html.A(id=page_name + "dropdown_action", children=['List'], href=baseapp_prefix + '/list_all_plots', className="dropdown-item")
drop_down_exit =  html.A(id=page_name + "dropdown_action", children=['Exit'], href=baseapp_prefix + '/plot_menu', className="dropdown-item")

dropdown_menu = html.Div(id=page_name + "dropdown_menu", children = [drop_down_create,drop_down_edit,drop_down_list, drop_down_exit], className = "dropdown-menu")

relevant_dropdowns = [drop_down_create,drop_down_edit,drop_down_list,drop_down_exit] 

button_padding = {'height':'33px','padding-left':'12px','padding-right':'12px' ,
                          'padding-top':'0px',
                          'padding-bottom':'0px',
                          'margin':'0', 'border': '0', 'vertical-align':'middle'}

action_button = html.Button("Home",
                                       id=page_name+"home_button",
                                       className="btn btn-primary",type="button",
                                       style=button_padding)

app_page_menu = page_menu.page_top_menu(page_name,action_button,relevant_dropdowns)

layout = html.Div([
    dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
    dcc.Store(id= page_name + 'screen_size_store', storage_type='local'),
    app_page_menu,
    html.Div(id=page_name + "action_feedback", children=['Action Feedback'])
    ])


clientside_callback(
        """
        function(href) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            var jsn = {width: w, height: h};
            const myJSON = JSON.stringify(jsn); 
            return jsn;
        }
        """,
        Output(page_name + 'screen_size_store', 'data'),
        Input(page_name + 'url', 'href')
    )

@callback(Input(page_name +'url', 'href'), State(page_name + 'screen_size_store', 'data'))
def get_owned_data(href: str, page_size_in):
    page_size_as_string = json.dumps(page_size_in)
    print('home : get_user_owned_data callback triggered ---- page size >>>>>>>' + page_size_as_string)
    screen_height = page_size_in['height']
    print('screen_height >>>>>>>>>>', screen_height)
    plots_table_height = str(screen_height * 0.5) + 'px'
    ## get user id from cookie
    dmtooluser_cls = gdu.GetUserID()
    self.dmtool_userid = dmtooluser_cls.dmtool_userid

@callback(
    [Output(page_name + 'url', 'href',allow_duplicate=True),
    Output(page_name + "action_feedback", 'children')],
    Input(page_name+"create_plot_button",'btn_clicks'),
        prevent_initial_call=True
)
def button_click_do_something(button0):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    #msg = prop_id
    if page_name+"create_plot_button" == prop_id :
        request_header = {'dmtool-userid': str(dmtool_userid)}
        fastapi_about_url = "http://container_fastapi_data_1:8014/"
        href_return = baseapp_prefix + '/'
        return href_return, ''
    else:
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return, ''
