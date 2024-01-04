import dash
from dash import html, dcc, callback, Output, Input, State
#from flask import session
from flask import request

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

import requests
import json
import redis
import pickle



dash.register_page(__name__, path='/create_new_plot')
page_name = 'create_new_plot'
baseapp_prefix = '/application/baseapp'

from app.baseapp.libraries import page_menu as page_menu

plot_name_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Plot Name :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = 3
                ),
                dbc.Col(
                    dcc.Input(id=page_name + 'plot_name',
                              type='text',maxLength=40,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = 8
                ),
                example_column,        
                dbc.Popover(
                    dbc.PopoverBody('enter plot unique name'),
                    target="plot_name_example_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Plot of Experiment M'),
                    target="plot_name_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW '),
    ]
)

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

action_button = html.Button("Create New Plot",
                                       id=page_name+"create_plot_button",
                                       className="btn btn-primary",type="button",
                                       style=button_padding)

app_page_menu = page_menu.page_top_menu(page_name,action_button,relevant_dropdowns)


layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
    plot_name_input_row,
    app_page_menu,
    html.Div(id=page_name + "action_feedback", children=['Action Feedback'])
    ])


@callback(
    [Output(page_name + 'url', 'href',allow_duplicate=True),
    Output(page_name + "action_feedback", 'children')],
    Input(page_name+"create_plot_button", "n_clicks"),
    State("plot_name_form_field_id", "value"),
        prevent_initial_call=True
)
def button_click_create_new_plot(button0,plot_name_input):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print("create new plot >> prop id >>  " ,prop_id)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX create new plot XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    #msg = prop_id
    if page_name+"create_plot_button" == prop_id :
        request_header = {'dmtool-userid': str(dmtool_userid)}
        fastapi_about_url = "http://container_fastapi_data_1:8014/"
        
        ## create new plot record
        create_plot_api = "dmtool/fastapi_data/internal/data/plot/"
        data = {"name": plot_name_input}
        create_new_plot_api = fastapi_about_url + create_plot_api
        create_new_plot_response = requests.post(create_new_plot_api, json=data, headers=request_header)
        json_data = json.loads(create_new_plot_response.text)
        print("json_data cnp >>>>>>>>>", json_data)
        print("create_new_plot_req status code >>>> " , create_new_plot_response.status_code)
        new_plot_id = json_data['id']
        new_plot_name = json_data['name']
        print("create_new_plot_req plot id >>>> " , new_plot_id)

        href_return = baseapp_prefix+ '/select_limits_to_plot/?plot_id='+str(new_plot_id)
        #href_return = baseapp_prefix + '/create_new_plot'
        return href_return
    else:
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return
        
