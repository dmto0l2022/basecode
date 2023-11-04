import dash
from dash import html, dcc, callback, Output, Input, State
#from flask import session
from flask import request

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

import requests
import json
import redis
import pickle

r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)


dash.register_page(__name__, path='/create_new_plot')
page_name = 'create_new_plot'
baseapp_prefix = '/application/baseapp'

## id='plot_name_form_field_id',

layout = html.Div([
    #html.Div(id="hidden_div_for_redirect_callback"),
    dcc.Location(id="url_create_new_plot", refresh=True), ## important to allow redirects
    html.Div("Create New Plot"),
    fl.plot_name_input_row,
    html.Button('Print', id=page_name + '_print_' + 'button_id', n_clicks=0),
    html.Button('Create', id=page_name + '_create_' + 'button_id', n_clicks=0),
    html.Button('Cancel',  id=page_name + '_cancel_' + 'button_id', n_clicks=0),
    html.Div('No Button Pressed', id="whatbutton")
    ])


@callback(
    Output('url_create_new_plot', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    Input(page_name + '_print_' + 'button_id', "n_clicks"),
    Input(page_name + '_create_' + 'button_id', "n_clicks"),
    Input(page_name + '_cancel_' + 'button_id', "n_clicks"),
    State("plot_name_form_field_id", "value"),
        prevent_initial_call=True
)
def button_click_create_new_plot(button0,button1,button2,plot_name_input):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print("create new plot >> prop id >>  " ,prop_id)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX create new plot XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    session_key = request.cookies.get('session')
    print('create new plot : session key >>',session_key)
    redis_session_key = "session:"+session_key

    val = r.get(redis_session_key)
    print(redis_session_key)
    print('---------val------------------------------')
    print(val)
    print('--------- decoded val------------------------------')
    decoded_val = pickle.loads(val)
    print(decoded_val)
    dmtool_userid = decoded_val['dmtool_userid']
    dmtool_authorised = decoded_val['dmtool_authorised']
    print('dmtool_userid in cnp >>>' ,decoded_val['dmtool_userid'])
    print('=======================================')
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    #msg = prop_id
    if page_name + '_print_' + 'button_id' == prop_id :
        #href_return = '/application/baseapp/create_new_plot'
        #return href_return
        
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return
    elif page_name + '_create_' + 'button_id' == prop_id :
        request_header = {'dmtool-userid': str(dmtool_userid)}
        fastapi_about_url = "http://container_fastapi_data_1:8014/"
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
        #print("get_or_create_user_url >>>" , get_or_create_user_url)
        #google_req = requests.get(url_get)
        #print("google user status code >>>> " , google_req.status_code)

        href_return = baseapp_prefix+ '/select_limits_to_plot/?plot_id='+new_plot_id+'&plot_name='+new_plot_name
        #href_return = baseapp_prefix + '/create_new_plot'
        return href_return
    elif page_name + '_cancel_' + 'button_id' == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.edit_existing_plot']['path']
        href_return = baseapp_prefix+ '/plot_menu'
        return href_return
    else:
        href_return = baseapp_prefix + '/create_new_plot'
        return href_return
        
