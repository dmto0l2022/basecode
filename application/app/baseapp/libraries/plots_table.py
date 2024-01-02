#import dash
#from dash import Dash
#from dash import dcc, html
#from dash import Input, Output, callback
from dash import dash_table, no_update  # Dash version >= 2.0.0
import pandas as pd
import json
import requests
import pickle

#from app.baseapp.libraries import formlibrary as fl
#from app.baseapp.dashboard_libraries import get_limit_data as gld
#from app.baseapp.dashboard_libraries import get_limit_data_cls as gldc

class get_table:
    def __init__(self, page_title_in,
                 main_table_id_in,
                 table_meta_data_data_in,
                 table_height_in,
                 row_height_in,
                 table_font_size_in,
                 dmtool_userid_in
                ):

        self.page_title = page_title_in
        self.main_table_id = main_table_id_in
        self.table_meta_data_data = table_meta_data_data_in
        self.table_height = table_height_in
        self.page_size = 1000
        self.row_height = row_height_in
        self.table_font_size = table_font_size_in
        self.dmtool_userid = dmtool_userid_in
        self.dmtool_user_header = {'dmtool-userid':str(self.dmtool_userid)}
        self.internal_header = {'dmtool-userid':'0'}
        self.table_meta_data_columns = ['name', 'width']
        self.button_meta_data_data =[
                            ['add', '4%'],
                            ['edit', '4%'],
                            ['archive', '4%'],
                            ['delete', '4%']
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
                                  'height': self.row_height,
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
                            {"selector": ".dash-spreadsheet.dash-freeze-top, .dash-spreadsheet.dash-virtualized",  "rule": "max-height: inherit !important;" },
                            {"selector": ".dash-table-container" ,  "rule":  "max-height: calc(" + self.table_height + " - 100px);"}
            ]
    
        self.button_styling = {'font-size': '12px', 'width': '70px', 'display': 'inline-block', 
                              'margin-bottom': '1px', 'margin-right': '0px','margin-top': '1px', 'height':'19px',
                              'verticalAlign': 'center'}

        self.table_style = {'overflowY': 'auto', 'overflowX': 'auto', 'height': self.table_height, 'maxHeight': self.table_height}
                    
        self.initial_active_cell = {"row": 0, "column": 0, "column_id": "id", "row_id": 0}
        
        
        self.conditional_column_widths = []
        self.table_column_names_data = []
        self.get_conditional_column_widths()
        self.get_data_column_names()
        self.all_table_column_names = self.table_column_names_data+['+','~','-','X']
        self.table_data_dict = {}
        self.table_data_frame = pd.DataFrame()
        self.response_data_frame = pd.DataFrame()
        #self.RefreshTableData()
        self.dash_table = dash_table.DataTable()
        self.get_dash_table()

    def set_table_height(self,table_height_in):
        self.table_height = table_height_in
    
    def set_dmtool_userid(self,dmtool_userid_in):
        self.dmtool_userid = dmtool_userid_in
        

    def get_conditional_column_widths(self):
            
        for index, row in self.table_meta_data_all_df.iterrows():
            #print(row['name'], row['age'])
            add_dict = {'if': {'column_id': row['name'] },'width':row['width']}
            self.conditional_column_widths.append(add_dict)
        #print("conditional_column_widths>>>>>>>>>>>>", self.conditional_column_widths)

    def get_data_column_names(self):
        for index, row in self.table_meta_data_data_df.iterrows():  
            self.table_column_names_data = self.table_column_names_data + [row['name']]
        #print("table_column_names_data>>>>>>>>>>>>", self.table_column_names_data)
        
    
    def RefreshTableData(self):
        plots_api = '/dmtool/fastapi_data/internal/data/plots'
        api_server = "http://container_fastapi_data_1:8014"
        all_plots_api = api_server + plots_api
        print("mt : all_plots_api >>>>>>>>>>>>", all_plots_api)
        
        try:
            r = requests.get(all_plots_api, headers = self.dmtool_user_header)
            response_data = r.json()
            #print('all plots response data')
            #print('===================')
            print(response_data)
            print('===================')
            self.response_data_frame = pd.DataFrame(response_data)
        except:
            self.response_data_frame = pd.DataFrame()
  
        add_symbol = "+"
        edit_symbol = "~"
        delete_symbol = "X"
        archive_symbol = "-"
        
        if self.response_data_frame.empty:
            empty_data = self.table_column_names_data+['~','+','-','X']
            self.table_data_frame = pd.DataFrame(data = [empty_data], columns = self.all_table_column_names)
            self.table_data_dict = self.table_data_frame.to_dict('records')
        else:
            lst = self.table_column_names_data
            self.table_data_frame = self.response_data_frame[self.response_data_frame.columns.intersection(lst)]
            self.table_data_frame = self.table_data_frame[lst]
            #updated_data_frame_ret['create'] = "create"
            self.table_data_frame['~'] = edit_symbol
            self.table_data_frame['+'] = add_symbol
            self.table_data_frame['-'] = archive_symbol
            self.table_data_frame['X'] = delete_symbol
            self.table_data_dict = self.table_data_frame.to_dict('records')
    
        
    
    def get_dash_table(self):
        #print("column names : " , self.table_column_names_data)
        #print("column widths : " , self.conditional_column_widths)
        self.RefreshTableData()
        
        #print("plot table : style_table_dict >>>>>>", self.table_style)
        self.dash_table = dash_table.DataTable(
            virtualization=True,
            id = self.table_id,
            data = self.table_data_dict,
            columns=[{"name": c, "id": c} for c in self.all_table_column_names],
            fixed_rows={'headers': True},
            style_data={'whiteSpace': 'nowrap', 'height': self.row_height},
            style_cell=self.table_cell_styles,
            css=self.css_row_heights,
            style_cell_conditional=self.conditional_column_widths,
            tooltip_duration=None,
            page_size=1000,
            style_table=self.table_style
            )

