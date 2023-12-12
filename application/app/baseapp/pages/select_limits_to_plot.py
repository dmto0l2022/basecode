import dash
from dash import Dash
import dash_bootstrap_components as dbc
from flask import session
from furl import furl
from flask import request

#import formlibrary as fl
import requests
import json
from json import loads, dumps
import redis
import pickle

#r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)


dash.register_page(__name__, path='/select_limits_to_plot')
dmtool_userid = 1 ## testing
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

##from app.baseapp.dashboard_libraries import get_limit_data as gld

from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

from app.baseapp.libraries import main_table_editor as mte

dash.register_page(__name__, path='/select_limits_to_plot')

#guid = gdu.GetUserID()

#print("guid.dmtool_userid >>>>>>>>>>>>>>>>", guid.dmtool_userid)

dashdataandtables = adt.DashDataAndTables(dmtool_userid)

#####

class SelectLimitsToPlotDashBoardLayout():
    def __init__(self,pagename_in,  listoflimits_in):
        self.page_name = pagename_in
        self.page_title = pagename_in
        self.plot_id = 0
        self.dmtool_userid = 0
        self.main_table_id =  "main_limits_table"
        self.table_meta_data_main_table = [
                                        #['id', '5%'],
                                        #['experiment', '5%'],
                                        ['data_label', '100%']
                                    ]
        #self.table_height = '50vh'
        #self.page_size = 26
        self.row_height = '12px'
        self.table_font_size = '11px'
        self.filter_table_heights = '60px'

        self.page_content_style = {'top': '0px','padding':'0','margins':'0',
				   'height':'100%', 'width':'100%',
				   'left': '0','background-color': 'green',
                                   'overflow-y': 'scroll'}
        
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
        
        self.main_data_table = dash_table.DataTable(
            id = self.page_name + self.main_table_id
            )
        
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

        self.ClsMainDataTable = None
        
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
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
                dbc.Col(
                    [
                        self.experiments_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
                dbc.Col(
                    [
                        self.result_types_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
                dbc.Col(
                    [
                        self.spin_dependency_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
               dbc.Col(
                    [
                        self.years_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
               dbc.Col(
                    [
                        self.greatest_hit_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
        ])

    def PopulateMainDataTable(self):
        self.ClsMainDataTable = mte.get_main_table(self.page_title,
                                             self.page_name + self.main_table_id,
                                             self.table_meta_data_main_table,
                                             self.table_height,
                                             self.page_size,
                                             self.row_height,
                                             self.table_font_size,
                                             self.fastapi_url_all_limits,
                                             self.fastapi_url_one_limit,
                                             self.dmtool_userid)
        
        self.main_data_table = self.ClsMainDataTable.dash_table_main

    
    def CreateLimitsToPlot(self):

        ## creates empty limits to plot table and sets the unique id
        
        self.limits_to_plot_df = pd.DataFrame(data=[], columns=['id','plot_id','limit_id','data_reference','data_label'])
        
        style_header_var={ 'backgroundColor': 'black','color': 'white'}
        
        self.limits_to_plot_table = dash_table.DataTable(
            id=self.page_name+'limits_to_plot_table',
            data=self.limits_to_plot_df.to_dict('records'),
            columns=[{'name': 'id', 'id': 'id'},
                     {'name': 'limit_id', 'id': 'limit_id'},
                     #{'name': 'data_reference', 'id': 'data_reference'},
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
                #{'if': {'column_id': 'data_reference'},
                # 'width': '25%'},
                {'if': {'column_id': 'data_label'},
                 'width': '85%'},
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
                    className ="NOPADDING")

    
   
    
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
        page_content_style_1 =  {'position':'relative', 'width':'100vw', 'height':'100vh','top': '0px','padding':'0','margins':'0',
				                 'left': '0',
				                 'background-color': 'lightgreen'}
        plot_name_style = {'position':'absolute','top': '0px','padding':'0','margins':'0','left':'0',
			               'background-color':'purple','height':'20px', 'width' : '100%'}
        row_filters_style = {'position':'absolute','top': '20px','padding':'0','margins':'0','left':'0',
			                'background-color':'blue','height':'200px', 'width':'100%'}
        row_limits_style = {'position':'absolute','top': '220px','padding':'0','margins':'0','left':'0',
			                'background-color':'green','height':'300px', 'width':'100%'}
        main_style = {'position':'absolute','top': '0px','padding':'0','margins':'0','left':'0','height':'100%','width':'100%',
		              'background-color':'red'}
	    
        self.DivPlotName = html.Div(children='Plot Name Here',id=page_name +'_plot_name_id',style=plot_name_style)
        
        self.RowFilters =  dbc.Row([
                dbc.Col(
                    [
                        self.official_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
                dbc.Col(
                    [
                        self.experiments_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
                dbc.Col(
                    [
                        self.result_types_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
                dbc.Col(
                    [
                        self.spin_dependency_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
               dbc.Col(
                    [
                        self.years_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
               dbc.Col(
                    [
                        self.greatest_hit_table
                    ],
                    width=2,xs=6, sm=6, md=4, lg=2, xl=2, xxl=2,
                    ),
        ], style=row_filters_style)
        
        new_button =  html.Button("New", id= self.page_name + "new_button_id", style=self.button_styling_1)
        save_button =  html.Button("Save", id= self.page_name + "save_button_id", style=self.button_styling_1)
        cancel_button = html.Button("Cancel",  id=self.page_name + "cancel_button_id", style=self.button_styling_1)
        home_button =  html.Button("Home",  id=self.page_name + "home_button_id", style=self.button_styling_1)
        list_button =  html.Button("List",  id=self.page_name + "list_button_id", style=self.button_styling_1)
        
        self.DivOfButtons = html.Div(id= self.page_name + "page_buttons",
				     children=[new_button,save_button,cancel_button,home_button,list_button],
				     className="PAGE_FOOTER_BUTTONS")
        
        #self.RowLimits = dbc.Row([dbc.Col(id=self.page_name+"main_table_div",
        #                    children=[self.main_data_table],
        #                    width=12,)],
        #                    className ="NOPADDING_CONTENT")
	    
        #self.RowLimits = dbc.Row([dbc.Col(id=self.page_name+"main_table_div",width=12,)],style=row_limits_style)
        
        self.RowLimits = dbc.Row([dbc.Col(children=[html.Div(children='Data Starts')], id=self.page_name+"main_table_div_xxx",width=12,)],style=row_limits_style)
	    
        self.RowListOfLimits = dbc.Row(html.Div(children=['List of limits appear here'],id=self.page_name+'limit_list'))
        
        maincolumn = html.Div(
                        [dcc.Location(id=page_name+'url',refresh=True),
                        self.DivPlotName,
                        self.RowFilters,
                        self.RowLimits,
                        #self.RowLimitsToPlot,
                        #self.DivOfButtons,
                        #self.RowListOfLimits
			], style=main_style)
        
        self.layout = html.Div(id=page_name+'content',children=maincolumn,className="container-fluid",style=page_content_style_1)

    def SetPlotNameCallback(self):
        @callback([Output(self.page_name +'_plot_name_id', 'children'), Output(self.page_name+'main_table_div','children')],
              [Input(self.page_name +'url', 'href')])
        def set_plot_name(href: str):
            ## get user id from cookie
            dmtooluser_cls = gdu.GetUserID()
            self.dmtool_userid = dmtooluser_cls.dmtool_userid
            ## get plot name from url
            f = furl(href)
            self.plot_name = f.args['plot_name']
            self.plot_id = f.args['plot_id']
            #####
            '''
            curl -X 'GET' \
              'https://dev1.dmtool.info/dmtool/fastapi_data/internal/data/plot?plot_id=3119' \
              -H 'accept: application/json' \
              -H 'dmtool-userid: 1'
            '''
            #####
            
            request_header = {'dmtool-userid': str(self.dmtool_userid)}
            fastapi_data_url = "http://container_fastapi_data_1:8014/"
            
            get_plot_api = "dmtool/fastapi_data/internal/data/plot?plot_id=" + self.plot_id
            get_plot_api_url = fastapi_data_url + get_plot_api
            
            get_plot_response = requests.get(get_plot_api_url, headers=request_header)
            json_data = json.loads(get_plot_response.text)
            print("json_data sltp >>>>>>>>>", json_data)
            print("select limits to plot status code >>>> " , get_plot_response.status_code)
            new_plot_id = json_data['Plot']['id']
            new_plot_name = json_data['Plot']['name']
            print("create_new_plot_req plot id from api >>>> " , new_plot_id)

            #####
            ## populate data=self.limits_to_plot_df.to_dict('records'),
            ## if the plot is in progress or being edited there will be limits already chosen
            
            request_header = {'dmtool-userid': str(self.dmtool_userid)}
            fastapi_data_url = "http://container_fastapi_data_1:8014/"
        
            get_limits_to_plot_api = "dmtool/fastapi_data/internal/data/data_about?plot_id_in=" + str(new_plot_id)
            
            get_limits_to_plot_api_url = fastapi_data_url + get_limits_to_plot_api

            get_limits_to_plot_response = requests.get(get_limits_to_plot_api_url, headers=request_header)
            json_data_response = json.loads(get_limits_to_plot_response.text)
            
            lol = []
            for j in json_data_response:
                record = j['Data_about']
                lol.append(record)
            
            self.limits_to_plot_df = pd.DataFrame.from_dict(lol)

            print("self.limits_to_plot_df >>>>>>>>", self.limits_to_plot_df)
            
            #print("json_data sltp add initial limits to plot >>>>>>>>>", json_data_response)
            #print("select limits to plot - add limit to plot - status code >>>> " , get_limits_to_plot_response.status_code)
            
            #self.limits_to_plot_df = pd.json_normalize(json_data_response)

            #########################
            self.PopulateMainDataTable()
            
            return [html.H1(children=str(new_plot_id) + ' - ' + new_plot_name) , self.main_data_table]
    
    def ApplyFiltersCallback(self):
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
            derived_virtual_selected_rows_greatest_hit):

            print("call back triggered")
            
            try:
                dfs = [
                    self.years_df.loc[derived_virtual_selected_rows_years],
                    self.experiments_df.loc[derived_virtual_selected_rows_experiments],
                    self.result_types_df.loc[derived_virtual_selected_rows_result_types],
                    self.spin_dependency_df.loc[derived_virtual_selected_rows_spin_dependency],
                    self.official_df.loc[derived_virtual_selected_rows_official],
                    self.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit],
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
        
            #all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits(dmtool_userid) 
            
            self.PopulateMainDataTable()
            
            unfiltered_df = self.ClsMainDataTable.limit_data.limit_list_df.copy()
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

    def MoveLimitToLimitsToPlotCallback(self):
        @callback(
            Output(self.page_name+'limits_to_plot_table', 'data'),
            [Input(self.page_name + 'main_limits_table', 'active_cell'),Input(self.page_name+'limits_to_plot_table', 'active_cell')],
            [State(self.page_name+'limits_to_plot_table', 'data')])
        def trigger_fork(active_cell_exp,active_cell_plot,data_in):
            ctx = dash.callback_context
            triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
            #print(triggered_id)
            if triggered_id == self.page_name + 'main_limits_table':
                all_limit_list_df = self.ClsMainDataTable.limit_data.limit_list_df.copy()
                selected_rowid = active_cell_exp['row_id']
                selected_limit = all_limit_list_df[all_limit_list_df['id']==active_cell_exp['row_id']]
                print("selected limit columns >>>>>>>>>", selected_limit.columns)
                selected_row  = selected_limit[['id','limit_id','data_reference','data_label']].copy()
                #selected_row['plot_id'] = self.plot_id
                #data_out=plots_todo_df.to_dict("records")
                
                record=selected_row.to_dict("records")[0]
                
                request_header = {'dmtool-userid': str(self.dmtool_userid)}
                fastapi_data_url = "http://container_fastapi_data_1:8014/"
            
                add_limit_to_plot_api = "dmtool/fastapi_data/internal/data/data_about"
                add_limit_to_plot_api_url = fastapi_data_url + add_limit_to_plot_api
                
                df_to_json = selected_limit[["limit_id", "data_label", "data_reference", "data_comment", "x_units", "y_units",
                      "x_rescale", "y_rescale", "year", "experiment", "spin_dependency", "result_type", "official", "greatest_hit"]].copy()
                
                df_to_json["plot_id"] =  str(self.plot_id)
                ####
                '''
                json_data = {
                      "limit_id": str(selected_limit["limit_id"].iloc[0]),
                      "plot_id": str(self.plot_id),
                      "data_label": selected_limit["data_label"].iloc[0],
                      "data_reference": selected_limit["data_reference"].iloc[0],
                      "data_comment": selected_limit["data_comment"].iloc[0],
                      "x_units": selected_limit["x_units"].iloc[0],
                      "y_units": selected_limit["y_units"].iloc[0],
                      "x_rescale": '1', ##str(selected_limit["x_rescale"].iloc[0]),
                      "y_rescale": '1', ##str(selected_limit["y_rescale"].iloc[0]),
                      "year": str(int(selected_limit["year"].iloc[0])),
                      "experiment": selected_limit["experiment"].iloc[0],
                      "spin_dependency": selected_limit["spin_dependency"].iloc[0],
                      "result_type": selected_limit["result_type"].iloc[0],
                      "official": str(selected_limit["official"].iloc[0]),
                      "greatest_hit": str(selected_limit["greatest_hit"].iloc[0])
                    }
                '''
                
                json_data_1 = df_to_json.to_json(orient="records")
                #result = df.to_json(orient="records")

                parsed = loads(json_data_1)
                print("print(dumps(parsed, indent=4))")
                #print(dumps(parsed, indent=4))
                print("parsed[0]  >>>", parsed[0])
                
                ##df.loc[i].to_json

                ####

                #print(json_data)
                #print("json_data_1 >>>>>>>>>>>", json_data_1)
                
                ####
                
                add_limit_to_plot_api_response = requests.post(add_limit_to_plot_api_url, json=parsed[0], headers=request_header)
                json_data_response = json.loads(add_limit_to_plot_api_response.text)
                print("json_data sltp add limit to plot >>>>>>>>>", json_data_response)
                print("select limits to plot - add limit to plot - status code >>>> " , add_limit_to_plot_api_response.status_code)

                #print(data_in)

                record_data=selected_limit.to_dict("records")[0]
                data_in.append(record_data)
                print("data_out >>>>>>>>>", data_in)
                #data_in = record
                # Return the updated data.
                #return data

                
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
            
                #selected_row = limits_table_df[limits_table_df['expid']==active_cell['row_id']]
                #plots_todo_df= selected_row.copy()
                #data_out=plots_todo_df.to_dict("records")
                #data_out=selected_row.to_dict("records")
        
            elif triggered_id == self.page_name+'limits_to_plot_table':
                #selected_rowid = active_cell_plot['row']
                #print(data_in[selected_rowid])
                #print(active_cell_plot)
                #data_in = data_in.pop(active_cell_plot['row'])
                #print(data_in)
                a = 1
            
            return data_in
    
    
    def RespondToButtonsCallback(self):
        @callback(
            [Output(self.page_name+'url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
             Output(self.page_name+'limit_list','children')],
            [
            Input(self.page_name + "new_button_id", "n_clicks"),
            Input(self.page_name + "save_button_id", "n_clicks"),
            Input(self.page_name + "cancel_button_id", "n_clicks"),
            Input(self.page_name + "home_button_id", "n_clicks"),
            Input(self.page_name + "list_button_id","n_clicks"),
                ],[State(self.page_name +'limits_to_plot_table', 'data')],
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
                href_return = '/application/baseapp/select_limits_to_plot'
                return href_return
	

#def get_layout():
#    layout_out = html.Div(id=page_name+'content',children=[maincolumn],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
#    #layout_out = html.Div(id=page_name+'content',children=[main_table_1.dash_table_main],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
#    
#    return layout_out

sltpdb = SelectLimitsToPlotDashBoardLayout(page_name, listoflimits)
sltpdb.CreateLayout()
layout = sltpdb.layout
sltpdb.SetPlotNameCallback() ## sets the dmtool user id
#sltpdb.CreateLimitsToPlot() ## this populates if there is a previous plot
#sltpdb.ApplyFiltersCallback()
#sltpdb.MoveLimitToLimitsToPlotCallback()
#sltpdb.RespondToButtonsCallback()
#sltpdb.PopulateMainDataTable()

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
