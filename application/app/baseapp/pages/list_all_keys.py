import dash

from dash import Dash
from dash import dcc, html
from dash import Input, Output, callback
from dash import dash_table, no_update  # Dash version >= 2.0.0
import pandas as pd
import plotly.express as px
import json
import requests
import pickle
import dash_bootstrap_components as dbc

from flask import request, session

from app.baseapp.libraries import formlibrary as fl
from app.baseapp.libraries import main_table as mt
## from app.baseapp.libraries import get_dmtool_user as gdu

import requests
import json
import redis


###########################################################

dash.register_page(__name__, path='/list_all_keys')
page_name = "list_all_keys"
page_title = 'List All Keys'
baseapp_prefix = '/application/baseapp'

button_styling_1 = {'font-size': '12px',
                  'width': '70px',
                  'display': 'inline-block', 
                  'margin-bottom': '1px',
                  'margin-right': '0px',
                  'margin-top': '1px',
                  'height':'19px',
                  'verticalAlign': 'center'}

### table data
#table_column_names=['id','user_id','api_key','public_key', 'created_at','modified_at','ceased_at']

main_table_id = 'user_api_keys_table_main'
table_meta_data_data = [
                        ['id', '2%'],
                        ['user_id', '2%'],
                        ['api_key', '18%'],
                        ['public_key', '18%'],
                        ['created_at', '5%'],
                        ['modified_at', '5%'],
                        ['ceased_at', '5%']
                       ]

row_height = '13px'
table_font_size = '12px'

fastapi_url_all = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/user_api_keys" ## multiple limit operations
fastapi_url_one = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/user_api_key/" ## single limit operations
'''
dmtool_user_id = gdu.dmtool_userid

internal_header={'dmtool-userid':'999'}

main_table_1 = mt.get_main_table(page_title,
                main_table_id,
                table_meta_data_data,
                row_height,
                table_font_size,
                fastapi_url_all,
                fastapi_url_one,
                dmtool_user_id)
'''

main_table_1 = dash_table.DataTable()
######################################################

def get_layout():    
  
    #submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

    new_button =  html.Button("New", id= page_name + "new_button_id", style=button_styling_1)

    save_button =  html.Button("Save", id= page_name + "save_button_id", style=button_styling_1)

    cancel_button =  html.Button("Cancel",  id=page_name + "cancel_button_id", style=button_styling_1)

    home_button =  html.Button("Home",  id=page_name + "home_button_id", style=button_styling_1)

    debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                      html.Div(id=page_name+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                      html.Div(id=page_name+"button-output-div", children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                      className="PAGE_DEBUG_CONTENT")

    ##dmtool_user_id = gdu.dmtool_userid
    dmtool_user_id = '999'
    internal_header={'dmtool-userid':'999'}


    main_table_1 = mt.get_main_table(page_title,
                                     main_table_id,
                                     table_meta_data_data,
                                     row_height,
                                     table_font_size,
                                     fastapi_url_all,
                                     fastapi_url_one,
                                     dmtool_user_id)
    
    table_layout = html.Div(
        [
            dcc.Location(id= page_name + "url", refresh=True), ## important to allow redirects
            html.Div(children= page_title, className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(
                [
                    main_table_1.dash_table_main
                ],
                className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT"
            ),
            debug_output,
            html.Div(id= page_name + "page_buttons", children=[new_button,save_button,cancel_button,home_button], className="PAGE_FOOTER_BUTTONS"),
        ],
        className="row NOPADDING_CONTENT"
    )

    return table_layout
    

layout = get_layout


#layout = table_layout
#layout = list_all_limits_form

#layout = no_output


@callback(
    [Output(page_name+"cell-output-div", "children"),
     Output(page_name+"button-output-div", "children"),
     Output(main_table_id,'data'),
     Output(main_table_id, "active_cell")],
    [Input(main_table_id, "active_cell"),Input(page_name + "new_button_id", "n_clicks"),
    Input(page_name + "save_button_id", "n_clicks"),
    Input(page_name + "cancel_button_id", "n_clicks"),
    Input(page_name + "home_button_id", "n_clicks")],
    ##prevent_initial_call=True
)
def action_taken(active_cell_in,newbutton,savebutton,cancelbutton,homebutton):
    active_cell_reset = None
    return_cell_msg = "No cells clicked yet"
    button_press_msg = "None of the buttons have been clicked yet"
    return_data_dict = main_table_1.main_table_data_dict
    print('------------------------------- call back triggered -------------------------')
    print("list all keys : active_cell >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" ,active_cell_in)
    print("list all keys : active_cell reset  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" ,active_cell_reset)

    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    session_key = request.cookies.get('session')
    print('list all keys : session key >>',session_key)
    redis_session_key = "session:"+session_key
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXlist all keys current session object XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    #current_session = requests.Session()
    #print("current session ID >>>>> ",current_session.cookies['sessionid'])
    #dmtool_userid = current_session['dmtool_userid']
    #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    #print('list all keys : current user >>', dmtool_userid)
    #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    #print('Flask session object >>>>>>>>>>>>>>>>>>>>', session)
    #print('Flask session dmtool id >>>>>>>>>>>>>>>', session['dmtool_userid'])
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXREDIS INSIDE PAGES DASH HERE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    
    r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
    all_keys = r.keys('*')
    print("redis all keys >>>>>", all_keys)
    print("redis all keys >>>>>", type(all_keys))
    print("redis get session data")
    for k in all_keys:
        val = r.get(k)
        print("k>>>>" , k)
        print('---------------------------------------')
        print("val>>>>", val)
        print('=======================================')

    session_data = r.get(redis_session_key)
    print('--------- list all keys -- decoded val------------------------------')
    decoded_val = pickle.loads(session_data)
    print(decoded_val)
    print('--------- list all keys -- decoded val------------------------------')

    dmtool_userid = decoded_val['dmtool_userid']
    print('lal : dmtool_userid >>>>>>>>>>>>' , dmtool_userid)
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXREDIS INSIDE PAGES DASH TO HERE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    
    #first = all_keys[0]
    #val = r.get('session:3d6eaeb7-c227-4444-ac90-208da7732203')
    #current_session_data = r.get(session_cookie)
    #print('current session google2 cookie >>>>>>>', current_session_data)

    main_table_1 = mt.get_main_table(page_title,
                                     main_table_id,
                                     table_meta_data_data,
                                     row_height,
                                     table_font_size,
                                     fastapi_url_all,
                                     fastapi_url_one,
                                     dmtool_user_id)
    main_table_1.RefreshTableData()
    
    if active_cell_in:

        #row = active_cell["row_id"]
        row_id = active_cell_in["row_id"]
        #print(f"row_id: {row_id}")
        
        #row = active_cell["row_id"]
        column_id = active_cell_in["column_id"]
        #print(f"column_id: {column_id}")
        
        row = active_cell_in["row"]
        #print(f"row: {row}")
    
        #country = df.at[row, "country"]
        #print(country)
        id = main_table_1.main_table_data_frame.at[row, "id"]
        #print("id >> ", id)
    
        column = active_cell_in["column"]
        #print(f"column: {column}")
        #print("---------------------")
        
        cell_value = main_table_1.main_table_data_frame.iat[active_cell_in['row'], active_cell_in['column']]
    
        #print("cell_value > ", cell_value)
    
        #print("---------------------")
    
        #print("table data frame")
        #print("---------------------")
    
        #print(updated_data_frame)
    
        #print("---------------------")
    
        
        if cell_value == 'delete':
            main_table_1.DeleteRow(id)
            main_table_1.RefreshTableData()
    
        if cell_value == 'ceased':
            main_table_1.CeaseRow(id)
            main_table_1.RefreshTableData()
                
        return_cell_msg = row, " ", column, " ",cell_value, " ", id
        
        return  return_cell_msg, button_press_msg, main_table_1.main_table_data_dict, active_cell_reset
    
    else:

        print("Button has been pressed")
        button_press_msg = "None of the buttons have been clicked yet"
        prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
        print("prop_id >>>>>>>>>>>" , prop_id)
        #msg = prop_id
        if page_name + "new_button_id" == prop_id :
            button_press_msg = "New Button was most recently clicked"
            main_table_1.NewRow('1')
            main_table_1.RefreshTableData()
            #href_return = dash.page_registry['pages.show_limit']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict, active_cell_reset
        elif page_name + "save_button_id" == prop_id :
            button_press_msg = "Save Button was most recently clicked"
            #href_return = dash.page_registry['pages.show_limit']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict, active_cell_reset
        elif page_name + "cancel_button_id" == prop_id:
            button_press_msg = "Cancel Button was most recently clicked"
            #href_return = dash.page_registry['pages.home']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict, active_cell_reset
        elif page_name + "home_button_id" == prop_id:
            button_press_msg = "Home Button was most recently clicked"
            #href_return = dash.page_registry['pages.home']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict, active_cell_reset
        else:
            href_return = dash.page_registry['pages.home']['path']
            button_press_msg = "No Button Clicked"
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict, active_cell_reset




'''
@callback(
    [Output(page_name+"cell-output-div", "children"),
     Output(main_table_id,'data')],
    Input(main_table_id, "active_cell"),
)
def cell_clicked(active_cell):
    
    main_table_1.RefreshTableData()
    
    if active_cell is None:
        return no_update

    #row = active_cell["row_id"]
    row_id = active_cell["row_id"]
    #print(f"row_id: {row_id}")
    
    #row = active_cell["row_id"]
    column_id = active_cell["column_id"]
    #print(f"column_id: {column_id}")
    
    row = active_cell["row"]
    #print(f"row: {row}")

    #country = df.at[row, "country"]
    #print(country)
    id = main_table_1.main_table_data_frame.at[row, "id"]
    #print("id >> ", id)

    column = active_cell["column"]
    #print(f"column: {column}")
    #print("---------------------")
    
    cell_value = main_table_1.main_table_data_frame.iat[active_cell['row'], active_cell['column']]

    #print("cell_value > ", cell_value)

    #print("---------------------")

    #print("table data frame")
    #print("---------------------")

    #print(updated_data_frame)

    #print("---------------------")

    
    if cell_value == 'delete':
        main_table_1.DeleteRow(id)
        main_table_1.RefreshTableData()

    if cell_value == 'cease':
        main_table_1.CeaseRow(id)
        main_table_1.RefreshTableData()
            
    return_data = row, " ", column, " ",cell_value, " ", id
    return return_data, main_table_1.main_table_data_dict




@callback(
    #Output(page_name + "url", 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [Output(page_name+"button-output-div", "children"), Output(main_table_id,'data')],
    [
    Input(page_name + "new_button_id", "n_clicks"),
    Input(page_name + "save_button_id", "n_clicks"),
    Input(page_name + "cancel_button_id", "n_clicks"),
    Input(page_name + "home_button_id", "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(newbutton,savebutton,cancelbutton,homebutton):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name + "new_button_id" == prop_id :
        msg = "New Button was most recently clicked"
        main_table_1.NewRow('1')
        main_table_1.RefreshTableData()
        #href_return = dash.page_registry['pages.show_limit']['path']
        #return href_return
        return [msg, main_table_1.main_table_data_dict]
    elif page_name + "save_button_id" == prop_id :
        msg = "Save Button was most recently clicked"
        #href_return = dash.page_registry['pages.show_limit']['path']
        #return href_return
        return [msg, main_table_1.main_table_data_dict]
    elif page_name + "cancel_button_id" == prop_id:
        msg = "Cancel Button was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        #return href_return
        return [msg, main_table_1.main_table_data_dict]
    elif page_name + "home_button_id" == prop_id:
        msg = "Home Button was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        #return href_return
        return [msg, main_table_1.main_table_data_dict]
    else:
        href_return = dash.page_registry['pages.home']['path']
        msg = "No Button Clicked"
        return [msg, main_table_1.main_table_data_dict]

'''
