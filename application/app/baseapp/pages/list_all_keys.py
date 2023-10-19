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


'''
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(self):
    print("Hello my name is " + self.name)
'''

class get_main_table:
    def __init__(self, page_title_in,
                 main_table_id_in,
                 table_meta_data_data_in,
                 row_height_in,
                 table_font_size_in,
                 fastapi_url_all_in,
                 fastapi_url_one_in):

        self.page_title = page_title_in
        self.main_table_id = main_table_id_in
        self.table_meta_data_data = table_meta_data_data_in
        self.row_height = row_height_in
        self.table_font_size = table_font_size_in
        self.fastapi_url_all = fastapi_url_all_in
        self.fastapi_url_one = fastapi_url_one_in
        self.internal_header = {'dmtool-userid':'999'}
        self.table_meta_data_columns = ['name', 'width']
        self.button_meta_data_data =[
                            ['edit', '2%'],
                            ['ceased', '2%'],
                            ['delete', '2%']
                            ]
        self.all_table_meta_data_data = self.table_meta_data_data + self.button_meta_data_data
        self.table_meta_data_all_df = pd.DataFrame(data=self.all_table_meta_data_data, columns=self.table_meta_data_columns)
        self.table_meta_data_data_df = pd.DataFrame(data=self.table_meta_data_data, columns=self.table_meta_data_columns)

        self.table_cell_styles = {'textAlign': 'left','padding': '0px','font_size': self.table_font_size,
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'border': '1px solid black',
                            'height': row_height_in,
                        }

        self.css_row_heights = [
                            {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                            {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                            {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                            {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                            ]
    
        self.button_styling = {'font-size': '12px', 'width': '70px', 'display': 'inline-block', 
                              'margin-bottom': '1px', 'margin-right': '0px','margin-top': '1px', 'height':'19px',
                              'verticalAlign': 'center'}
        
        self.initial_active_cell = {"row": 0, "column": 0, "column_id": "id", "row_id": 0}

        
        self.conditional_column_widths = []
        self.table_column_names_data = []
        self.get_conditional_column_widths()
        self.get_data_column_names()
        self.all_table_column_names = self.table_column_names_data+['edit','ceased','delete']
        self.main_table_data_dict = {}
        self.main_table_data_frame = pd.DataFrame()
        self.RefreshTableData()
        self.dash_table_main = dash_table.DataTable()
        self.get_dash_table()
        
        

    def get_conditional_column_widths(self):
            
        for index, row in self.table_meta_data_all_df.iterrows():
            #print(row['name'], row['age'])
            add_dict = {'if': {'column_id': row['name'] },'width':row['width']}
            self.conditional_column_widths.append(add_dict)
        print("conditional_column_widths>>>>>>>>>>>>", self.conditional_column_widths)

    def get_data_column_names(self):
        for index, row in self.table_meta_data_data_df.iterrows():  
            self.table_column_names_data = self.table_column_names_data + [row['name']]
        print("table_column_names_data>>>>>>>>>>>>", self.table_column_names_data)
        
   
    
    ###
    
    def DeleteRow(self,key_in):
        delete_url = self.fastapi_url_one + str(key_in)
        requests.delete(delete_url, headers=self.internal_header)
    
    def CeaseRow(self,key_in):
        cease_url = self.fastapi_url_one + str(key_in)
        print('cease >>' + str(key_in))
        requests.put(cease_url, headers=self.internal_header)

    def NewRow(self,dmtool_user_in):
        new_url = self.fastapi_url_one + str(dmtool_user_in)
        print('new api key >>' + str(dmtool_user_in))
        dmtooluser_header = {'dmtool-userid':'1'}
        requests.post(new_url, headers=dmtooluser_header)
    
    
    def RefreshTableData(self):
        #url = fastapi_url_all_in
        response_data_frame = pd.DataFrame()
        try:
            r = requests.get(self.fastapi_url_all, headers = self.internal_header)
            response_data = r.json()
            print('response data')
            print('===================')
            print(response_data)
            print('===================')
            self.response_data_frame = pd.DataFrame(response_data)
        except:
            a = 1
    
        #all_table_column_names = table_column_names_data+['edit','ceased','delete']
      
        if self.response_data_frame.empty:
            empty_data = self.table_column_names_data+['edit','ceased','delete']
            print("RefreshTableData >> empty_data >>>>>>", empty_data)
            print("RefreshTableData >> all_table_column_names>>>>>>>>>>", self.all_table_column_names)
            self.main_table_data_frame = pd.DataFrame(data = [empty_data], columns = self.all_table_column_names)
            self.main_table_data_dict = self.main_table_data_frame.to_dict('records')
        else:
            lst = self.table_column_names_data
            self.main_table_data_frame = self.response_data_frame[self.response_data_frame.columns.intersection(lst)]
            self.main_table_data_frame = self.main_table_data_frame[lst]
            #updated_data_frame_ret['create'] = "create"
            self.main_table_data_frame['edit'] = "edit"
            self.main_table_data_frame['ceased'] = "ceased"
            #updated_data_frame_ret['update'] = "update"
            self.main_table_data_frame['delete'] = "delete"
            self.main_table_data_dict = self.main_table_data_frame.to_dict('records')
        
        
    
    def get_dash_table(self):
    
        self.dash_table_main = dash_table.DataTable(
            id = self.main_table_id,
            data = self.main_table_data_dict,
            columns=[{"name": c, "id": c} for c in self.all_table_column_names],
            fixed_rows={'headers': True},
            filter_action='none',
            style_cell=self.table_cell_styles,
            css=self.css_row_heights,
            style_cell_conditional=self.conditional_column_widths,
            tooltip_duration=None,
            )
    
    
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


internal_header={'dmtool-userid':'999'}

main_table_1 = get_main_table(page_title,
                 main_table_id,
                 table_meta_data_data,
                 row_height,
                 table_font_size,
                 fastapi_url_all,
                 fastapi_url_one)

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


    main_table_1 = get_main_table(page_title,
                 main_table_id,
                 table_meta_data_data,
                 row_height,
                 table_font_size,
                 fastapi_url_all,
                 fastapi_url_one)
    
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
     Output(main_table_id,'data')],
    [Input(main_table_id, "active_cell"),Input(page_name + "new_button_id", "n_clicks"),
    Input(page_name + "save_button_id", "n_clicks"),
    Input(page_name + "cancel_button_id", "n_clicks"),
    Input(page_name + "home_button_id", "n_clicks")],
    prevent_initial_call=True
)
def action_taken(active_cell,newbutton,savebutton,cancelbutton,homebutton):
    
    main_table_1.RefreshTableData()
    return_cell_msg = ""
    button_press_msg = ""
    return_data_dict = main_table_1.main_table_data_dict
    
    if active_cell is not None:

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
                
        return_cell_msg = row, " ", column, " ",cell_value, " ", id
        
        return  return_cell_msg, button_press_msg, main_table_1.main_table_data_dict
    
    else:
            
        #msg = "None of the buttons have been clicked yet"
        prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
        #msg = prop_id
        if page_name + "new_button_id" == prop_id :
            msg = "New Button was most recently clicked"
            main_table_1.NewRow('1')
            main_table_1.RefreshTableData()
            #href_return = dash.page_registry['pages.show_limit']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict
        elif page_name + "save_button_id" == prop_id :
            msg = "Save Button was most recently clicked"
            #href_return = dash.page_registry['pages.show_limit']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict
        elif page_name + "cancel_button_id" == prop_id:
            msg = "Cancel Button was most recently clicked"
            #href_return = dash.page_registry['pages.home']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict
        elif page_name + "home_button_id" == prop_id:
            msg = "Home Button was most recently clicked"
            #href_return = dash.page_registry['pages.home']['path']
            #return href_return
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict
        else:
            href_return = dash.page_registry['pages.home']['path']
            msg = "No Button Clicked"
            return return_cell_msg, button_press_msg, main_table_1.main_table_data_dict




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
