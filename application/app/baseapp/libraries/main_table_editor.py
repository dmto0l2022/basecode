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
#from app.baseapp.dashboard_libraries import get_limit_data as gld
from app.baseapp.dashboard_libraries import get_limit_data_cls as gldc

import requests
import json
import redis

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
                 fastapi_url_one_in,
                 dmtool_userid_in
                ):

        self.page_title = page_title_in
        self.main_table_id = main_table_id_in
        self.table_meta_data_data = table_meta_data_data_in
        self.row_height = row_height_in
        self.table_font_size = table_font_size_in
        self.fastapi_url_all = fastapi_url_all_in
        self.fastapi_url_one = fastapi_url_one_in
        self.dmtool_userid = dmtool_userid_in
        self.dmtool_user_header = {'dmtool-userid':str(self.dmtool_userid)}
        self.internal_header = {'dmtool-userid':'999'}
        self.table_meta_data_columns = ['name', 'width']
        self.button_meta_data_data =[
                            ['edit', '3%'],
                            ['ceased', '3%'],
                            ['delete', '3%']
                            ]
        self.all_table_meta_data_data = self.table_meta_data_data + self.button_meta_data_data
        self.table_meta_data_all_df = pd.DataFrame(data=self.all_table_meta_data_data, columns=self.table_meta_data_columns)
        self.table_meta_data_data_df = pd.DataFrame(data=self.table_meta_data_data, columns=self.table_meta_data_columns)

        self.table_cell_styles = {'textAlign': 'left',
                                  'padding': '0px',
                                  'font_size': self.table_font_size,
                                  'overflow': 'hidden',
                                  'textOverflow': 'ellipsis',
                                  'border': '1px solid black',
                                  'height': row_height_in,
                                  'overflow': 'hidden',
                                  'maxWidth': 0 ## made things work!!
                                 }

        self.css_row_heights = [
                            {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                            {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                            {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                            {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            ##{"selector": ".dash-table-container" , "rule": "max-height: calc(100vh - 84px);"}                
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
        self.response_data_frame = pd.DataFrame()
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
        print('cease url >>' + str(cease_url))
        #dmtooluser_header = {'dmtool-userid':'1'}
        requests.post(cease_url, headers=self.dmtool_user_header)

    def NewRow(self,dmtool_user_in):
        new_url = self.fastapi_url_one
        print('new api key >>' + str(dmtool_user_in))
        data = {"user_id": 1}
        #dmtooluser_header = {'dmtool-userid':'1'}
        requests.post(new_url,json=data, headers=self.dmtool_user_header)
    
    
    def RefreshTableData(self):
        #url = fastapi_url_all_in
        
        if "limit" in self.fastapi_url_all:
            #limit_list_df, trace_list_df, limit_data_df, limit_list_dict = gld.GetLimits(self.dmtool_userid)
            self.limit_data = gldc.LimitData(self.dmtool_userid, 0, [])
            self.response_data_frame = self.limit_data.limit_list_df.copy()
        elif "api_key" in self.fastapi_url_all:
            try:
                print("mt : fastapi_url_all for api key >>>>>>>>>>>>", self.fastapi_url_all)
                r = requests.get(self.fastapi_url_all, headers = self.dmtool_user_header)
                response_data = r.json()
                print('response data')
                print('===================')
                print(response_data)
                print('===================')
                self.response_data_frame = pd.DataFrame(response_data)
            except:
                a = 1
        else:
            self.response_data_frame = pd.DataFrame()
        
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
        print("column names : " , self.table_column_names_data)
        print("column widths : " , self.conditional_column_widths)
        
        self.dash_table_main = dash_table.DataTable(
            #virtualization=True,
            id = self.main_table_id,
            data = self.main_table_data_dict,
            columns=[{"name": c, "id": c} for c in self.all_table_column_names],
            fixed_rows={'headers': True},
            #filter_action='none',
            style_data={'whiteSpace': 'nowrap', 'height': self.row_height},
            style_cell=self.table_cell_styles,
            css=self.css_row_heights,
            style_cell_conditional=self.conditional_column_widths,
            tooltip_duration=None,
            #style_table={'minHeight': '700px', 'height': '700px', 'maxHeight': '700px'},
            #style_table={'minHeight': '100%', 'height': '100%', 'maxHeight': '100%'},
            style_table={'height': 'calc(90vh-84px)', 'maxHeight': 'calc(90vh-84px)'},
            page_size=45
            )
    
 
