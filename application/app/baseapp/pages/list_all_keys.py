import dash

from dash import Dash
from dash import dcc, html
from dash import Input, Output, callback
from dash import dash_table, no_update  # Dash version >= 2.0.0
import pandas as pd
import plotly.express as px
import json
import requests
import dash_bootstrap_components as dbc

from app.baseapp.libraries import formlibrary as fl

import requests
import json

'''
class MakeApiCall():

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
            
    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
'''


fastapi_url_all = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/user_api_keys" ## multiple limit operations
fastapi_url_one = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/user_api_key/" ## single limit operations
internal_header={'dmtool-userid':'999'}

dash.register_page(__name__, path='/list_all_keys')
page_name = "list_all_keys"
page_title = 'List All Keys'
baseapp_prefix = '/application/baseapp'

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
font_size = '12px'
'''
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(self):
    print("Hello my name is " + self.name)
'''

class get_main_table:
    def __init__(self, page_title_in, main_table_id_in,table_meta_data_data_in,row_height_in, table_font_size_in, fastapi_url_all_in, fastapi_url_one_in):
        self.page_title = page_title_in
        self.main_table_id = main_table_id_in
        self.table_meta_data_data = table_meta_data_data_in
        self.row_height = row_height_in
        self.table_font_size = table_font_size_in
        self.fastapi_url_all = fastapi_url_all_in
        self.fastapi_url_one = fastapi_url_one_in
        self.table_meta_data_columns = ['name', 'width']
        self.button_meta_data_data =[
                            ['edit', '2%'],
                            ['ceased', '2%'],
                            ['delete', '2%']
                            ]
        self.all_table_meta_data_data = self.table_meta_data_data + self.button_meta_data_data
        self.table_meta_data_all_df = pd.DataFrame(data=self.all_table_meta_data_data, columns=self.table_meta_data_columns)
        self.table_meta_data_data_df = pd.DataFrame(data=self.table_meta_data_data, columns=self.table_meta_data_columns)
        self.conditional_column_widths = []
        self.table_column_names_data = []
        self.get_conditional_column_widths()
        self.get_all_column_names():

    def get_conditional_column_widths(self):
            
        for index, row in table_meta_data_all_df.iterrows():
            #print(row['name'], row['age'])
            add_dict = {'if': {'column_id': row['name'] },'width':row['width']}
            self.conditional_column_widths.append(add_dict)
        print("conditional_column_widths>>>>>>>>>>>>", self.conditional_column_widths)

    def get_all_column_names():
        for index, row in table_meta_data_data_df.iterrows():  
            self.table_column_names_data = self.table_column_names_data + [row['name']]
        print("table_column_names>>>>>>>>>>>>", self.table_column_names_data)
        
   
    def get_dash_table():
        table_cell_styles = {'textAlign': 'left','padding': '0px','font_size': self.table_font_size,
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'border': '1px solid black',
                            'height': row_height_in,
                        }

        css_row_heights = [
                            {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                            {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                            {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + row_height_in + "; height: " + row_height_in + ";line-height: " + row_height_in + ";max-height: " + row_height_in + ";"},  # set height of header
                            {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + row_height_in + "; height: " + row_height_in + ";line-height: " + row_height_in + ";max-height: " + row_height_in + ";"},
                            {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + row_height_in + "; height: " + row_height_in + ";line-height: " + row_height_in + ";max-height: " + row_height_in + ";"},  # set height of body rows
                            {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + row_height_in + "; height: " + row_height_in + ";line-height: " + row_height_in + ";max-height: " + row_height_in + ";"},  # set height of header
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + row_height_in + "; height: " + row_height_in + ";line-height: " + row_height_in + ";max-height: " + row_height_in + ";"},
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + row_height_in + "; height: " + row_height_in + ";line-height: " + row_height_in + ";max-height: " + row_height_in + ";"}
                            ]
    
        button_styling = {'font-size': '12px', 'width': '70px', 'display': 'inline-block', 
                          'margin-bottom': '1px', 'margin-right': '0px','margin-top': '1px', 'height':'19px',
                          'verticalAlign': 'center'}


    ###
    
    def DeleteRow(key_in):
        delete_url = fastapi_url_one_in + str(key_in)
        requests.delete(delete_url, headers=internal_header)
    
    def CeaseRow(key_in):
        cease_url = fastapi_url_one_in + str(key_in)
        print('cease >>' + str(key_in))
        requests.put(cease_url, headers=internal_header)
    
    
    def RefreshTableData():
        url = fastapi_url_all_in
        response_data_frame = pd.DataFrame()
        try:
            r = requests.get(url, headers=internal_header)
            response_data = r.json()
            print('response data')
            print('===================')
            print(response_data)
            print('===================')
            response_data_frame = pd.DataFrame(response_data)
        except:
            a = 1
    
        all_table_column_names = table_column_names_data+['edit','ceased','delete']
      
        if response_data_frame.empty:
            empty_data = [table_column_names_data+['edit','ceased','delete']]
            updated_data_frame_ret = pd.DataFrame(data=empty_data, columns=all_table_column_names)
            updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
        else:
            lst = table_column_names_data
            updated_data_frame_ret = response_data_frame[response_data_frame.columns.intersection(lst)]
            updated_data_frame_ret = updated_data_frame_ret[lst]
            #updated_data_frame_ret['create'] = "create"
            updated_data_frame_ret['edit'] = "edit"
            updated_data_frame_ret['ceased'] = "ceased"
            #updated_data_frame_ret['update'] = "update"
            updated_data_frame_ret['delete'] = "delete"
            updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
        return updated_data_dict_ret, updated_data_frame_ret, all_table_column_names
    
    
    #table_data_dict_initial, table_data_frame_initial, column_names = RefreshTableData()
    initial_active_cell = {"row": 0, "column": 0, "column_id": "id", "row_id": 0}

###########################################################

def get_layout():

    table_data_dict, table_data_frame, table_column_names = RefreshTableData()
    
    main_table = dash_table.DataTable(
        id = main_table_id,
        data = table_data_dict,
        columns=[{"name": c, "id": c} for c in table_column_names],
        fixed_rows={'headers': True},
        filter_action='none',
        style_cell=table_cell_styles,
        css=css_row_heights,
        style_cell_conditional=conditional_column_widths,
        tooltip_duration=None,
        )
    
    
  
    #submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

    save_button =  html.Button("Save", id= page_name + "save_button_id", style=button_styling)

    cancel_button =  html.Button("Cancel",  id=page_name + "cancel_button_id", style=button_styling)

    home_button =  html.Button("Home",  id=page_name + "home_button_id", style=button_styling)

    debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                      html.Div(id=page_name+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                      html.Div(id=page_name+"button-output-div", children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                      className="PAGE_DEBUG_CONTENT")

  
    table_layout = html.Div(
        [
            dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
            html.Div(children=page_title, className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(
                [
                    main_table
                ],
                className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT"
            ),
            debug_output,
            html.Div(id=page_name+"page_buttons", children=[save_button,cancel_button,home_button], className="PAGE_FOOTER_BUTTONS"),
        ],
        className="row NOPADDING_CONTENT"
    )

    return table_layout
    

layout = get_layout


#layout = table_layout
#layout = list_all_limits_form

#layout = no_output


@callback(
    [Output(page_name+"cell-output-div", "children"), Output(main_table_id,'data')], Input(main_table_id, "active_cell"),
)
def cell_clicked(active_cell):
    
    updated_data_dict, updated_data_frame, column_names = RefreshTableData()
    
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
    id = updated_data_frame.at[row, "id"]
    #print("id >> ", id)

    column = active_cell["column"]
    #print(f"column: {column}")
    #print("---------------------")
    
    cell_value = updated_data_frame.iat[active_cell['row'], active_cell['column']]

    #print("cell_value > ", cell_value)

    #print("---------------------")

    #print("table data frame")
    #print("---------------------")

    #print(updated_data_frame)

    #print("---------------------")

    
    if cell_value == 'delete':
        DeleteRow(id)
        updated_data_dict, updated_data_frame, column_names = RefreshTableData()

    if cell_value == 'cease':
        CeaseRow(id)
        updated_data_dict, updated_data_frame, column_names = RefreshTableData()
            
    return_data = row, " ", column, " ",cell_value, " ", id
    return return_data, updated_data_dict




@callback(
    #Output(page_name + "url", 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    Output(page_name+"button-output-div", "children"),
    [
    Input(page_name + "save_button_id", "n_clicks"),
    Input(page_name + "cancel_button_id", "n_clicks"),
    Input(page_name + "home_button_id", "n_clicks"),
        ],
        prevent_initial_call=True
)
def button_click(savebutton,cancelbutton,homebutton):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if page_name + "save_button_id" == prop_id :
        msg = "Save Button was most recently clicked"
        #href_return = dash.page_registry['pages.show_limit']['path']
        #return href_return
        return msg
    elif page_name + "cancel_button_id" == prop_id:
        msg = "Cancel Button was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        #return href_return
        return msg
    elif page_name + "home_button_id" == prop_id:
        msg = "Home Button was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        #return href_return
        return msg
    else:
        href_return = dash.page_registry['pages.home']['path']
        msg = "No Button Clicked"
        return msg

