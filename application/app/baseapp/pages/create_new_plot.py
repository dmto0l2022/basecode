import dash
from dash import html, dcc, callback, Output, Input, State
#from flask import session
from flask import request

import dash_bootstrap_components as dbc

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

import requests
import json
import redis
import pickle

from app.baseapp.libraries import page_menu as page_menu


dash.register_page(__name__, path='/create_new_plot')
page_name = 'create_new_plot'
baseapp_prefix = '/application/baseapp'

show_example = 1 ## default is to show examples
label_column_width = 3
input_column_width = 7
example_column_width = 2

## This function is included in case examples need to be suppressed

FORM_COLUMN_LABEL_STYLE = {
    'color': 'black',
    'font-size': '12px',
    'font-weight': 'bold',
    'text-align':'right',
    'padding':'0 !important',
    'margin': '0 !important',
    'border-style': 'none',
    'width': '100%'}


FORM_LABEL_COLUMN_STYLE =  {
    'padding': '0 !important',
    'margin': '0 !important',
    'border-style': 'none',
    'width': '1'
}

FORM_ROW_STYLE =  {
  'font':'bold',
  'font-size': '12px',
  'width':'100%',
  'height':'25px'
}

## /*width:140px;*/

FORM_COLUMN_DATA_STYLE = {
  'font':'bold',
  'font-size': '12px',
  'width':'100%',
  'height':'24px',
  'line-height': '80%',
  'padding':'0 !important',
  'margin': '0 !important',
  'border': '1px solid black'
}

FORM_COLUMN_TEXTINPUT_STYLE = {
    'font':'bold',
    'font-size': '12px',
    'height': '100%',
    'width':'100%'
}

FORM_TEXTINPUT_COLUMN_STYLE = {
    'padding':'0 !important',
    'margin': '0 !important',
    'border-style': 'none'
}


FORM_EXAMPLE_COLUMN_STYLE = {
    'padding':'0 !important',
    'margin': '0 !important',
    'border-style': 'none'
}




def get_example_column(show_example_in):
    return_val =  dbc.Col()
    if show_example_in == 1:
        return_val = dbc.Col(dcc.Input(id='plot_name_example_field_id',
                                          type='text',
                                          value='example',
                                          readOnly=True,
                                          className='FORM_COLUMN_EXAMPLE'),
                            style=FORM_EXAMPLE_COLUMN_STYLE,
                            width=example_column_width)
    else:
        return_val = dbc.Col(style=FORM_EXAMPLE_COLUMN_STYLE,width=example_column_width)
    return return_val

example_column = get_example_column(show_example)

plot_name_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Plot Name :',className='FORM_COLUMN_LABEL'),
                    style=FORM_LABEL_COLUMN_STYLE,
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(id=page_name + 'plot_name',
                              type='text',maxLength=40,
                              style=FORM_COLUMN_TEXTINPUT_STYLE),
                    style=FORM_TEXTINPUT_COLUMN_STYLE,
                    width = input_column_width
                ),
                example_column,        
                dbc.Popover(
                    dbc.PopoverBody('enter plot unique name'),
                    target="plot_name_example_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Unique Name for Plot M'),
                    target="plot_name_example_field_id",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

## from app.baseapp.libraries import page_menu as page_menu

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

drop_down_create =  html.A(id=page_name + "dropdown_action", children=['Create New Plot'], href=baseapp_prefix + '/create_new_plot', className="dropdown-item")
drop_down_edit =  html.A(id=page_name + "dropdown_action", children=['Edit Existing Plot'], href=baseapp_prefix + '/edit_existing_plot', className="dropdown-item")
drop_down_list =  html.A(id=page_name + "dropdown_action", children=['List Your Plots'], href=baseapp_prefix + '/list_all_plots', className="dropdown-item")
drop_down_exit =  html.A(id=page_name + "dropdown_action", children=['Exit'], href=baseapp_prefix + '/home', className="dropdown-item")

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

action_feedback_div_style =  {'position':'absolute','top': '633px','padding':'0','margins':'0','left':'0','border':'5px solid green',
                            'background-color':'pink','height':'30px', 'width':'600px', 'overflow-y': 'scroll'}

ActionFeedBackDiv = html.Div(id=page_name + "action_feedback", children=['Action Feedback'],style=action_feedback_div_style)


layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
    app_page_menu,
    plot_name_input_row,
    ActionFeedBackDiv
    ])


@callback(
    [Output(page_name + 'url', 'href',allow_duplicate=True),
    Output(page_name + "action_feedback", 'children')],
    Input(page_name+"create_plot_button", "n_clicks"),
    State(page_name + 'plot_name', "value"),
        prevent_initial_call=True
)
def button_click_create_new_plot(button0,plot_name_input):
    msg = "No actions taken"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print("create new plot >> prop id >>  " ,prop_id)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX create new plot XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    
    if page_name+"create_plot_button" == prop_id :
        ## generic metadata
        request_header = {'dmtool-userid': str(dmtool_userid)}
        fastapi_about_url = "http://container_fastapi_data_1:8014/"
        
        ## create new plot metadata 
        create_plot_api = "dmtool/fastapi_data/internal/data/plot/"
        create_new_plot_api = fastapi_about_url + create_plot_api
        
        ## create new plot data
        data = {"name": plot_name_input}

        ## make request
        create_new_plot_response = requests.post(create_new_plot_api, json=data, headers=request_header)
        json_data = json.loads(create_new_plot_response.text)
        
        ## manage non 200 responses
        response_status_code = create_new_plot_response.status_code
        print("status code >>>> " , page_name + ">>>>>" + str(response_status_code))
        
        if response_status_code != 200:
            print("json_data cnp >>>>>>>>>", json_data)
            msg = json.dumps(json_data, separators=(',', ':'))
        else:      
            ## parse response data
            json_data = json.loads(create_new_plot_response.text)
            print("json_data cnp >>>>>>>>>", json_data)
                        
            new_plot_id = json_data['id']
            new_plot_name = json_data['name']
            print("create_new_plot_req plot id >>>> " , new_plot_id)
    
            msg = baseapp_prefix+ '/select_limits_to_plot/?plot_id='+str(new_plot_id)
            href_return = baseapp_prefix + '/create_new_plot'
        return href_return, msg
    else:
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return, msg
        
