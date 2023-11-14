import dash
from dash import Dash
import dash_bootstrap_components as dbc
from flask import session
from furl import furl
from flask import request

#import formlibrary as fl
import requests
import json
import redis
import pickle

#r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)


dash.register_page(__name__, path='/select_limits_to_plot')
dmtool_userid = 16384 ## testing
page_name = 'select_limits_to_plot'
listoflimits = []

#### select limits to plot

from dash import dcc
from dash import html
from dash import callback
from dash import Output, Input, State
from dash import callback_context
from dash import dash_table

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_bootstrap_components as dbc

import pandas as pd

import plotly.express as px
from itertools import cycle

# colors
# palette = cycle(px.colors.qualitative.Bold)

from app.baseapp.dashboard_libraries import all_data_tables as adt

from app.baseapp.dashboard_libraries import get_limit_data as gld

#from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

from app.baseapp.libraries import main_table_editor as mte

dash.register_page(__name__, path='/select_limits_to_plot')

#guid = gdu.GetUserID()

#print("guid.dmtool_userid >>>>>>>>>>>>>>>>", guid.dmtool_userid)

dashdataandtables = adt.DashDataAndTables(dmtool_userid)

#####

class SelectLimitsToPlotDashBoardLayout():
    def __init__(self,pagename_in, dmtool_userid_in,  listoflimits_in):
        self.page_name = pagename_in
        self.page_title = pagename_in
        self.dmtool_userid = dmtool_userid_in
        self.main_table_id =  self.page_name + "data_table_id"
        self.table_meta_data_main_table = [
                                        ['id', '3%'],
                                        ['experiment', '3%'],
                                        ['data_comment', '44%'],
                                        ['data_label', '44%'],
                                    ]
        
        self.row_height = '12px'
        self.table_font_size = '11px'
        self.filter_table_heights = '60px'
        
        self.filter_table_cell_styles = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': self.table_font_size,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': self.row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
        
        self.filter_table_css_row_heights = [ {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                                    ]

        self.data_table_cell_styles = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': self.table_font_size,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': self.row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
        
        self.data_table_css_row_heights = [ {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                                    ]

        self.limits_to_plot_table_cell_styles = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': self.table_font_size,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': self.row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
        
        self.limits_to_plot_table_css_row_heights = [ {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                                    ]

        self.button_styling_1 = {'font-size': '12px',
                          'width': '70px',
                          'display': 'inline-block', 
                          'margin-bottom': '1px',
                          'margin-right': '0px',
                          'margin-top': '1px',
                          'height':'19px',
                          'verticalAlign': 'center'}

        self.internal_header={'dmtool-userid':'0'}

        

        self.experiments_df = pd.DataFrame()
        self.result_types_df = pd.DataFrame()
        self.spin_dependency_df = pd.DataFrame()
        self.greatest_hit_df = pd.DataFrame()
        self.limits_df = pd.DataFrame()
        self.limits_table_df = pd.DataFrame()
        self.limits_metadata_df = pd.DataFrame()
        self.limits_traces_df = pd.DataFrame()
        self.limits_data_df = pd.DataFrame()
        self.official_df = pd.DataFrame()
        self.years_df = pd.DataFrame()
        
        self.years_table = dash_table.DataTable()
        self.official_table = dash_table.DataTable()
        self.experiments_table = dash_table.DataTable()
        self.result_types_table = dash_table.DataTable()
        self.spin_dependency_table = dash_table.DataTable()
        self.greatest_hit_table = dash_table.DataTable()
        self.limits_table = dash_table.DataTable()
        self.plots_table = dash_table.DataTable()
        self.multiple_api = 'limits'
        self.single_api = 'limit'
        self.fastapi_data_url = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/"
        self.fastapi_metadata_url = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/metadata/"
        self.fastapi_url_all_limits = self.fastapi_data_url + self.multiple_api ## multiple limit operations
        self.fastapi_url_one_limit = self.fastapi_data_url + self.single_api + "/" ## single limit operations

        self.dropdown_route = 'dropdown_valuepair'
        self.fastapi_get_dropdown = self.fastapi_metadata_url + self.dropdown_route + "?variable_in="
        
        self.style_header_var={ 'backgroundColor': 'black','color': 'white'}

        self.limits_to_plot_df = pd.DataFrame()
        self.RowLimitsToPlot = dbc.Row()
        
        self.PopulateMainDataTable()
       
        self.PopulateFilterDataFrames()
        self.CreateFilterTables()
        self.CreateFilterRow()
        self.CreateLimitsToPlot()


    def PopulateFilterDataFrames(self):
        #do some parsing
        dropdown_route = 'metadata/dropdown_valuepair'
        fastapi_url = "http://container_fastapi_about_1:8014/dmtool/fastapi_data/internal/"
        fastapi_get_dropdown = fastapi_url + dropdown_route + "?variable_in="
        
        ## external api route
        ##  'https://dev1.dmtool.info/dmtool/fastapi_data/internal/dropdown_valuepair?variable_in=year' \

        ## each table uses the following
        #r = requests.get(url, headers=headers)
        #response_data = r.json()
        #print('response data')
        #print('===================')
        #print(response_data)
        #print('===== response data frame ==============')
        #response_data_frame = pd.DataFrame(response_data)
        #response_data_frame = pd.DataFrame.from_dict(response_data['limits'])
        #print(response_data_frame)
        #print('===== response data frame ==============')
        
        
        #self.all_dropdown_pairs = \
        #    pd.read_sql('SELECT variable,label, value, data_type FROM dropdown_valuepairs', con=self.engine)
        
        ## experiment drop down table ##
        experiments_req_url = self.fastapi_get_dropdown + 'experiment'
        print("experiments_req_url >>>>>>>>>>>>",experiments_req_url)
        r = requests.get(experiments_req_url)
        experiments_response_data = r.json()
        print("experiments_response_data >>>>>>>>>>>>" ,experiments_response_data)
        
        self.experiments_df = pd.DataFrame.from_dict(experiments_response_data)
        self.experiments_df.reset_index(drop=True, inplace=True)
        
        ## result type drop down table ##
        
        result_types_req_url = self.fastapi_get_dropdown + 'result_type'
        r = requests.get(result_types_req_url)
        result_types_response_data = r.json()
        
        self.result_types_df  = pd.DataFrame.from_dict(result_types_response_data)
        
        self.result_types_df.reset_index(drop=True, inplace=True)

        ## spin dependency drop down table ##
        
        spin_dependency_req_url = self.fastapi_get_dropdown + 'spin_dependency'
        r = requests.get(spin_dependency_req_url)
        spin_dependency_response_data = r.json()
        
        self.spin_dependency_df  =  pd.DataFrame.from_dict(spin_dependency_response_data)
        
        self.spin_dependency_df.reset_index(drop=True, inplace=True)
        
        ## result type drop down table ##
        
        greatest_hit_req_url = self.fastapi_get_dropdown + 'greatest_hit'
        r = requests.get(greatest_hit_req_url)
        greatest_hit_response_data = r.json()
        
        self.greatest_hit_df = pd.DataFrame.from_dict(greatest_hit_response_data)
        
        #self.greatest_hit_df.reset_index(drop=True, inplace=True)

        official_req_url = self.fastapi_get_dropdown + 'official'
        r = requests.get(official_req_url)
        official_response_data = r.json()
        
        self.official_df = pd.DataFrame.from_dict(official_response_data)
        
        #self.official_df.reset_index(drop=True, inplace=True)

        year_req_url = self.fastapi_get_dropdown + 'year'
        r = requests.get(year_req_url)
        year_response_data = r.json()
        
        self.years_df = pd.DataFrame.from_dict(year_response_data)

        ####
    def CreateFilterTables(self):
        
        self.years_table = dash_table.DataTable(
            id=self.page_name+'years_table',
            columns=[
                {'name': 'year', 'id': 'label', 'type': 'text'},
            ],
            data=self.years_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            fixed_rows={'headers': True},
            #page_size=3,
            style_cell_conditional=[
                {'if': {'column_id': 'year'},
                 'width': '90%'},
            ],
            style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            selected_rows=[],
            style_table={
                'height': self.filter_table_heights,
            },
            style_header=self.style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.official_table = dash_table.DataTable(
            id=self.page_name+'official_table',
            columns=[
                {'name': 'official', 'id': 'label', 'type': 'boolean'},
            ],
            data=self.official_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            fixed_rows={'headers': True},
            style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            selected_rows=[],
            style_table={
                'height': self.filter_table_heights,
            },
            style_header=self.style_header_var,
            #style_data={
             #   'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
             #   ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.experiments_table = dash_table.DataTable(
            id=self.page_name+'experiments_table',
            columns=[
                {'name': 'experiment', 'id': 'label', 'type': 'text'},
            ],
            data=self.experiments_df.to_dict('records'),
           filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            fixed_rows={'headers': True},
            style_table={
                'height': self.filter_table_heights,
            },
            style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            selected_rows=[],
            style_header=self.style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.result_types_table = dash_table.DataTable(
            id=self.page_name+'result_types_table',
            columns=[
                {'name': 'result_type', 'id': 'label', 'type': 'text'},
            ],
            data=self.result_types_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            fixed_rows={'headers': True},
            selected_rows=[],
            style_table={
                'height': self.filter_table_heights,
            },
            style_header=self.style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.spin_dependency_table = dash_table.DataTable(
            id=self.page_name+'spin_dependency_table',
            columns=[
                {'name': 'spin_dependency', 'id': 'label', 'type': 'text'},
            ],
            data=self.spin_dependency_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            fixed_rows={'headers': True},
            selected_rows=[],
            style_table={
                'height': self.filter_table_heights,
            },
            style_header=self.style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.greatest_hit_table = dash_table.DataTable(
            id=self.page_name+'greatest_hit_table',
            columns=[
                {'name': 'greatest_hit', 'id': 'label', 'type': 'text'},
            ],
            data=self.greatest_hit_df.to_dict('records'),
            #page_size=5,
            fixed_rows={'headers': True},
            filter_action='none',
            row_selectable='multi',
            selected_rows=[],
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
             style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            style_table={
                'height': self.filter_table_heights,
            },
            style_header=self.style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
                ##'overflow': 'hidden',
                ##'textOverflow': 'ellipsis',
            #}
        )


        self.filter_table_df = pd.DataFrame(data=[],columns=['variable','label','value'])
        
        self.debug_dropdown_table = dash_table.DataTable(
            id='debug_dropdown_table',
            data=self.filter_table_df.to_dict('records'),
            columns=[{'name': 'variable', 'id': 'variable'},
                     {'name': 'label', 'id': 'label'},
                     {'name': 'value', 'id': 'value'},
                     ],
            #fixed_rows={'headers': True},
            page_size=5,
            filter_action='none',
            #row_selectable='multi',
            #selected_rows=[],
            style_cell=self.filter_table_cell_styles,
            css=self.filter_table_css_row_heights,
            style_table={'height': '25vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'variable'},
                 'width': '25%'},
                {'if': {'column_id': 'label'},
                 'width': '25%'},
                {'if': {'column_id': 'value'},
                 'width': '25%'},
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header=self.style_header_var,
            #tooltip_data=[
            #    {
            #        column: {'value': str(value), 'type': 'markdown'}
            #        for column, value in row.items()
            #    } for row in data
            #],
            tooltip_duration=None,
        )

    def CreateFilterRow(self):

        self.RowFilters =  dbc.Row([
                dbc.Col(
                    [
                        self.official_table
                    ],
                    width=2,
                    ),
                dbc.Col(
                    [
                        self.experiments_table
                    ],
                    width=2,
                    ),
                dbc.Col(
                    [
                        self.result_types_table
                    ],
                    width=2,
                    ),
                dbc.Col(
                    [
                        self.spin_dependency_table
                    ],
                    width=2,
                    ),
               dbc.Col(
                    [
                        self.years_table
                    ],
                    width=2,
                    ),
               dbc.Col(
                    [
                        self.greatest_hit_table
                    ],
                    width=2,
                    ),
        ])

    def PopulateMainDataTable(self):
        ClsMainDataTable = mte.get_main_table(self.page_title,
                                             self.main_table_id,
                                             self.table_meta_data_main_table,
                                             self.row_height,
                                             self.table_font_size,
                                             self.fastapi_url_all_limits,
                                             self.fastapi_url_one_limit,
                                             self.dmtool_userid)
        
        self.main_data_table = ClsMainDataTable.dash_table_main

    
    def CreateLimitsToPlot(self):

        ## creates empty limits to plot table and sets the unique id
        
        self.limits_to_plot_df = pd.DataFrame(data=None, columns=['id','plot_id','limit_id','data_reference','data_label'])
        
        style_header_var={ 'backgroundColor': 'black','color': 'white'}
        
        self.limits_to_plot_table = dash_table.DataTable(
            id=self.page_name+'limits_to_plot_table',
            data=self.limits_to_plot_df.to_dict('records'),
            columns=[{'name': 'id', 'id': 'id'},
                     {'name': 'limit_id', 'id': 'limit_id'},
                     {'name': 'data_reference', 'id': 'data_reference'},
                     {'name': 'data_label', 'id': 'data_label'}
                     ],
            #fixed_rows={'headers': True},
            page_size=7,
            style_cell=self.limits_to_plot_table_cell_styles,
            css=self.limits_to_plot_table_css_row_heights,
            #sort_action='native',
            #sort_mode='multi',
            #sort_as_null=['', 'No'],
            #sort_by=[{'column_id': 'expid', 'direction': 'desc'}],
            filter_action='none',
            row_deletable=True,
            #row_selectable='multi',
            #selected_rows=[],
            style_table={'height': '25vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'id'},
                 'width': '5%'},
                {'if': {'column_id': 'limit_id'},
                 'width': '10%'},
                {'if': {'column_id': 'data_reference'},
                 'width': '25%'},
                {'if': {'column_id': 'data_label'},
                 'width': '55%'},
            ],
            style_data={
                'whiteSpace': 'nowrap'
            },
            style_header=style_header_var,
        ) 

        self.RowLimitsToPlot = dbc.Row([dbc.Col(
                [
                     self.limits_to_plot_table
                ],
                width=12,)],
                    className ="TABLE_ROW NOPADDING")

    
   
    
    def GetDebugTable():
        row2_debug_ret = dbc.Row([dbc.Col(
                    [
                        dashdataandtables.debug_dropdown_table
                    ],
                    width=12,),
                       ])
    
        row3_1_debug_ret = dbc.Row([dbc.Col(
                    [
                        dashdataandtables.debug_dropdown_table
                    ],
                    width=12,),
                       ], className ="TABLE_ROW NOPADDING")
        
        #row3 = dbc.Row([dbc.Col(html.Div('List Here',id='tbl_out'),width=12,),])
        return row2_debug_ret, row3_1_debug_ret

    
    def CreateLayout(self):

        self.DivPlotName = html.Div(children='Plot Name Here',id=page_name +'_plot_name_id')
        
        
        
        new_button =  html.Button("New", id= page_name + "new_button_id", style=self.button_styling_1)
        save_button =  html.Button("Save", id= page_name + "save_button_id", style=self.button_styling_1)
        cancel_button =  html.Button("Cancel",  id=page_name + "cancel_button_id", style=self.button_styling_1)
        home_button =  html.Button("Home",  id=page_name + "home_button_id", style=self.button_styling_1)
        list_button =  html.Button("List",  id=page_name + "list_button_id", style=self.button_styling_1)
        self.RowOfButtons = dbc.Row(id= page_name + "page_buttons", children=[new_button,save_button,cancel_button,home_button,list_button], className="PAGE_FOOTER_BUTTONS"),
        
        
        self.RowLimits = dbc.Row([dbc.Col(
                            [ self.main_data_table],
                            width=12,)],
                            className ="NOPADDING_CONTENT")

        self.RowListOfLimits = dbc.Row(html.P(children='List of limits appear here',id=page_name+'limit_list'))
        
        maincolumn = dbc.Col(
                    [
                        dcc.Location(id=page_name+'url',refresh=True),
                        self.DivPlotName,
                        self.RowFilters,
                        self.RowLimits,
                        self.RowLimitsToPlot,
                        #self.RowOfButtons,
                        self.RowListOfLimits
                    ],
                    width=12,)
        
        self.layout = html.Div(id=page_name+'content',children=maincolumn,className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
    '''
    def callback1(self):
        @callback(
        Output(self.page_name + 'main_limits_table', 'data'),
        #Output('debug_dropdown_table', 'data'),
        #Output(component_id='tbl_out', component_property='children'),
        #
        Input(self.page_name + 'years_table', 'active_cell'),
        Input(self.page_name + 'years_table', 'derived_virtual_selected_rows'),
        #
        Input(self.page_name + 'official_table', 'active_cell'),
        Input(self.page_name + 'official_table', 'derived_virtual_selected_rows'),
        #
        Input(self.page_name + 'experiments_table', 'active_cell'),
        Input(self.page_name + 'experiments_table', 'derived_virtual_selected_rows'),
        #
        Input(self.page_name + 'result_types_table', 'active_cell'),
        Input(self.page_name + 'result_types_table', 'derived_virtual_selected_rows'),
        #
        Input(self.page_name + 'spin_dependency_table', 'active_cell'),
        Input(self.page_name + 'spin_dependency_table', 'derived_virtual_selected_rows'),
        #
        Input(self.page_name + 'greatest_hit_table', 'active_cell'),
        Input(self.page_name + 'greatest_hit_table', 'derived_virtual_selected_rows'),
        )
        def update_graphs(
            active_cell_years,
            derived_virtual_selected_rows_years,
            #
            active_cell_official,
            derived_virtual_selected_rows_official,
            #
            active_cell_experiments,
            derived_virtual_selected_rows_experiments,
            #
            active_cell_resulttypes,
            derived_virtual_selected_rows_result_types,
            #
            active_cell_spin_dependency,
            derived_virtual_selected_rows_spin_dependency,
            #
            active_cell_greatest_hit,
            derived_virtual_selected_rows_greatest_hit,
            
        ):
            
            try:
                dfs = [
                    sltpdb.years_df.loc[derived_virtual_selected_rows_years],
                    sltpdb.experiments_df.loc[derived_virtual_selected_rows_experiments],
                    sltpdb.result_types_df.loc[derived_virtual_selected_rows_result_types],
                    sltpdb.spin_dependency_df.loc[derived_virtual_selected_rows_spin_dependency],
                    sltpdb.official_df.loc[derived_virtual_selected_rows_official],
                    sltpdb.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit],
                ]
                non_empty_dfs = [df for df in dfs if not df.empty]
                all_filters_df = pd.concat(non_empty_dfs)
            except:
                all_filters_df = pd.DataFrame()
        
            # print('sltp : all filters >>>>> ', all_filters_df)
            ## boolean filters
            #   dashdataandtables.official_df.loc[derived_virtual_selected_rows_official]
            #   dashdataandtables.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit]
                    
            # https://stackoverflow.com/questions/60964165/ignore-empty-dataframe-when-merging
        
            all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits(dmtool_userid) 
            
            unfiltered_df = all_limit_list_df.copy()
            print('sltp : unfiltered_df >>>', unfiltered_df) 
            #df.drop(df.index , inplace=True)
            
            filtered_df = unfiltered_df.drop(unfiltered_df.index)
            #filtered_df
            
            if all_filters_df.empty:
                filtered_df = unfiltered_df
            else:
                for index, row in all_filters_df.iterrows():
                    #print(row['variable'], row['value'])
                    matching_records = unfiltered_df[unfiltered_df['experiment'] == 'empty']
                    if row['data_type'] == 'number':
                        matching_records = unfiltered_df[unfiltered_df[row['variable']] == int(row['value'])]
                    elif row['data_type'] == 'text':
                        matching_records = unfiltered_df[unfiltered_df[row['variable']] == row['value']]
                    elif row['data_type'] == 'boolean':
                        if row['value'] == 1:
                            matching_records = unfiltered_df[unfiltered_df[row['variable']] == True]
                    else:
                            a = 1
                    filtered_df = pd.concat([filtered_df, matching_records])
                    #filtered_df = matching_records
                    #filtered_df = filtered_df[filtered_df[row['variable']] == row['value']] 
            
            filtered_df = filtered_df.drop_duplicates()
            #filtered_df
           
            data1 = all_filters_df.to_dict("records")
            data2 = filtered_df.to_dict("records")
            #print(data1)
            #data1=dff2.to_dict("records")
            #list_output = str(selectedcontinent_list) if selectedcontinent_list else "Click the table"
            return data2 #, list_output
        '''

#def get_layout():
#    layout_out = html.Div(id=page_name+'content',children=[maincolumn],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
#    #layout_out = html.Div(id=page_name+'content',children=[main_table_1.dash_table_main],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
#    
#    return layout_out

sltpdb = SelectLimitsToPlotDashBoardLayout(page_name, dmtool_userid,  listoflimits)
sltpdb.CreateLayout()
layout = sltpdb.layout
#sltpdb.callback1

### add callbacks to layout object

@callback(
    Output(page_name + 'main_limits_table', 'data'),
    #Output('debug_dropdown_table', 'data'),
    #Output(component_id='tbl_out', component_property='children'),
    #
    Input(page_name + 'years_table', 'active_cell'),
    Input(page_name + 'years_table', 'derived_virtual_selected_rows'),
    #
    Input(page_name + 'official_table', 'active_cell'),
    Input(page_name + 'official_table', 'derived_virtual_selected_rows'),
    #
    Input(page_name + 'experiments_table', 'active_cell'),
    Input(page_name + 'experiments_table', 'derived_virtual_selected_rows'),
    #
    Input(page_name + 'result_types_table', 'active_cell'),
    Input(page_name + 'result_types_table', 'derived_virtual_selected_rows'),
    #
    Input(page_name + 'spin_dependency_table', 'active_cell'),
    Input('spin_dependency_table', 'derived_virtual_selected_rows'),
    #
    Input(page_name + 'greatest_hit_table', 'active_cell'),
    Input(page_name + 'greatest_hit_table', 'derived_virtual_selected_rows'),
    )
def update_graphs(
    active_cell_years,
    derived_virtual_selected_rows_years,
    #
    active_cell_official,
    derived_virtual_selected_rows_official,
    #
    active_cell_experiments,
    derived_virtual_selected_rows_experiments,
    #
    active_cell_resulttypes,
    derived_virtual_selected_rows_result_types,
    #
    active_cell_spin_dependency,
    derived_virtual_selected_rows_spin_dependency,
    #
    active_cell_greatest_hit,
    derived_virtual_selected_rows_greatest_hit,
    
):
    
    try:
        dfs = [
            sltpdb.years_df.loc[derived_virtual_selected_rows_years],
            sltpdb.experiments_df.loc[derived_virtual_selected_rows_experiments],
            sltpdb.result_types_df.loc[derived_virtual_selected_rows_result_types],
            sltpdb.spin_dependency_df.loc[derived_virtual_selected_rows_spin_dependency],
            sltpdb.official_df.loc[derived_virtual_selected_rows_official],
            sltpdb.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit],
        ]
        non_empty_dfs = [df for df in dfs if not df.empty]
        all_filters_df = pd.concat(non_empty_dfs)
    except:
        all_filters_df = pd.DataFrame()

    # print('sltp : all filters >>>>> ', all_filters_df)
    ## boolean filters
    #   dashdataandtables.official_df.loc[derived_virtual_selected_rows_official]
    #   dashdataandtables.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit]
            
    # https://stackoverflow.com/questions/60964165/ignore-empty-dataframe-when-merging

    all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits(dmtool_userid) 
    
    unfiltered_df = all_limit_list_df.copy()
    print('sltp : unfiltered_df >>>', unfiltered_df) 
    #df.drop(df.index , inplace=True)
    
    filtered_df = unfiltered_df.drop(unfiltered_df.index)
    #filtered_df
    
    if all_filters_df.empty:
        filtered_df = unfiltered_df
    else:
        for index, row in all_filters_df.iterrows():
            #print(row['variable'], row['value'])
            matching_records = unfiltered_df[unfiltered_df['experiment'] == 'empty']
            if row['data_type'] == 'number':
                matching_records = unfiltered_df[unfiltered_df[row['variable']] == int(row['value'])]
            elif row['data_type'] == 'text':
                matching_records = unfiltered_df[unfiltered_df[row['variable']] == row['value']]
            elif row['data_type'] == 'boolean':
                if row['value'] == 1:
                    matching_records = unfiltered_df[unfiltered_df[row['variable']] == True]
            else:
                    a = 1
            filtered_df = pd.concat([filtered_df, matching_records])
            #filtered_df = matching_records
            #filtered_df = filtered_df[filtered_df[row['variable']] == row['value']] 
    
    filtered_df = filtered_df.drop_duplicates()
    #filtered_df
   
    data1 = all_filters_df.to_dict("records")
    data2 = filtered_df.to_dict("records")
    #print(data1)
    #data1=dff2.to_dict("records")
    #list_output = str(selectedcontinent_list) if selectedcontinent_list else "Click the table"
    return data2 #, list_output


@callback(
    Output(page_name+'limits_to_plot_table', 'data'),
    [Input(page_name + 'main_limits_table', 'active_cell'),Input(page_name+'limits_to_plot_table', 'active_cell')],
    [State(page_name+'limits_to_plot_table', 'data')])
def trigger_fork(active_cell_exp,active_cell_plot,data_in):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #print(triggered_id)
    if triggered_id == page_name + 'main_limits_table':
        all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits(dmtool_userid)  
        selected_rowid = active_cell_exp['row_id']
        selected_row = all_limit_list_df[all_limit_list_df['id']==active_cell_exp['row_id']]
        selected_row  = selected_row[['id','limit_id','data_reference','data_label']]
        selected_row['plot_id'] = 'plot_id here'
        #data_out=plots_todo_df.to_dict("records")
        record=selected_row.to_dict("records")[0]
        #print(type(record))
        #print(record)
        #record = {columns[i]: arg for i, arg in enumerate(list(args))}
        # If the record (identified by user_key) already exists, update it.
        #try:
        #    #record_index = [record[selected_rowid] for record in data_in].index(record[selected_rowid])
        #    record_index = [record[selected_rowid] for record in data_in].index(record[selected_rowid])
        #    data_in[record_index] = record
        # Otherwise, append it.
        #except ValueError:
        #    data_in[selected_rowid] = record
        #dictlen = len(data_in)
        #data_in[selected_rowid] = record
        data_in.append(record)
        #data_in = record
        # Return the updated data.
        #return data

        #selected_row = limits_table_df[limits_table_df['expid']==active_cell['row_id']]
        #plots_todo_df= selected_row.copy()
        #data_out=plots_todo_df.to_dict("records")
        #data_out=selected_row.to_dict("records")

    elif triggered_id == page_name+'limits_to_plot_table':
        #selected_rowid = active_cell_plot['row']
        #print(data_in[selected_rowid])
        #print(active_cell_plot)
        #data_in = data_in.pop(active_cell_plot['row'])
        #print(data_in)
        a = 1
    
    return data_in


@callback(
    [Output(page_name+'url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
     Output(page_name+'limit_list','children')],
    [
    Input(page_name + "new_button_id", "n_clicks"),
    Input(page_name + "save_button_id", "n_clicks"),
    Input(page_name + "cancel_button_id", "n_clicks"),
    Input(page_name + "home_button_id", "n_clicks"),
    Input(page_name + "list_button_id","n_clicks"),
        ],[State(page_name +'limits_to_plot_table', 'data')],
        prevent_initial_call=True
)
def button_click(button1,button2,button3,button4,button5,plot_table_in):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print('plot_table_in >>>>>>>>>>>>>>>>' ,plot_table_in)
    #plots_to_do_df = pd.DataFrame(plot_table_in)
    plots_to_do_df = pd.DataFrame.from_dict(plot_table_in)
    plots_to_do_df['all'] = 'all'
    plots_to_do_df['limit_id'] = plots_to_do_df['limit_id'].astype(str)
    limits_to_plot = plots_to_do_df[['limit_id','all']]
    print('limits_to_plot >>>>>>', limits_to_plot)
    
    #limits_to_plot['limit_ids'] = limits_to_plot[['all']].groupby(['all'])['limit_id'].transform(lambda x: ','.join(x))
    #print(limit_ids)  
    new_df = limits_to_plot.groupby(['all'])['limit_id'].apply('|'.join).reset_index()
    #print('new_df >>>>>>>>' ,new_df)
    limit_ids = new_df['limit_id'].values[0]
    #print('limit_ids >>>>>>>>' ,limit_ids)
            
    #msg = prop_id
    if page_name + "new_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        #href_return = dash.page_registry['pages.style_plot_and_traces']['path']
        href_return = '/application/baseapp/style_plot_and_traces'
        return [href_return,'']
    elif page_name + "new_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/application/baseapp/create_new_plot'
        return  [href_return,'']
    elif page_name + "cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/application/baseapp/homepage'
        return  [href_return,'']
    elif page_name + "home_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/application/baseapp/homepage'
        return  [href_return,'']
    elif page_name + "list_button_id" == prop_id:
        #msg = "Button 3 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        #href_return = '/app/baseapp/select_limits_to_plot'
        href_return = '/application/baseapp/style_plot_and_traces?limit_id=' + limit_ids
        return [href_return,limit_ids]
    else:
        href_return = '/app/baseapp/select_limits_to_plot'
        return href_return

###

##



'''
@callback(Output(page_name +'_plot_name_id', 'children'),
              [Input(page_name +'url', 'href')])
def set_plot_name(href: str):
    f = furl(href)
    plot_name = f.args['plot_name']
    plot_id = f.args['plot_id']
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX select limits to plot XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    session_key = request.cookies.get('session')
    print('selecf limits to plot : session key >>',session_key)
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
    print('dmtool_userid in sltp >>>' ,decoded_val['dmtool_userid'])
    print('=======================================')
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    
    return html.H1(children=plot_id + ' - ' + plot_name) 
    '''
    ## see https://github.com/plotly/dash/issues/61
    ## including the call backs in the class
