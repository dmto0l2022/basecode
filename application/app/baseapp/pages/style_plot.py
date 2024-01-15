import os
import requests
from urllib.parse import urlparse, parse_qs
from furl import furl
import pandas as pd
import itertools

cwd = os.getcwd()

page_name = 'style_plot'
baseapp_prefix = '/application/baseapp'

from datetime import datetime

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Dash
from dash import Input, Output,State
from dash import callback
from dash import clientside_callback

from dash.exceptions import PreventUpdate

from collections import OrderedDict

import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from plotly.subplots import make_subplots

import plotly.express as px

import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate

from collections import OrderedDict

from itertools import cycle

import redis

from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

from app.baseapp.dashboard_libraries import get_limit_data_cls as gldc

from app.baseapp.dashboard_libraries import scaling as sc

dmtool_userid = '1'

from app.baseapp.libraries import page_menu as page_menu

palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
palette = cycle(palette_list)

listoflimits = []

dash.register_page(__name__, path='/style_plot')

## create plot series

class StylePlotAndTracesDashBoardLayout():
    def __init__(self,pagename_in, dmtool_userid_in):
        self.page_name = pagename_in
        self.data_table_id =  self.page_name + "data_table_id"
        #self.table_meta_data_data = table_meta_data_data_in
        ### format style table

        self.format_data_table_row_height = '12px'
        self.format_data_table_font_size = '11px'
        self.format_data_table_style_table={
                'width': '100%',
                'minWidth': '100%',
            }

        self.format_table_style_cell = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': self.format_data_table_font_size,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          ##'border': '1px solid black',
                                          'height': self.format_data_table_row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }

       
        self.format_table_css = [{"selector": ".Select-menu-outer", "rule": "display: block !important"},
                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of header
                    {"selector": ".dash-spreadsheet-inner tr td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-spreadsheet tr td th", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of body rows
                    {"selector": ".dash-spreadsheet tr th td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of header
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr td th", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-cell tr th td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"}, 
                    {"selector": ".Select-option", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".data-dash-column tr td th", "rule": "min-height: " + self.format_data_table_row_height + ";height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    ]
        
        ##  {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                   
        
        self.dropdown_button = html.Button(id=page_name + "dropdown_button", type="button",
                           className = "btn btn-danger dropdown-toggle dropdown-toggle-split",
                           **{
                            'data-toggle' : 'dropdown',
                            'aria-haspopup' : 'true',
                            'aria-expanded' : 'false',
                            },
                            children=html.Span(className="sr-only", children=['Create Plot Menu'])
                          )

        self.drop_down_save =  html.A(id=page_name + "dropdown_action", children=['Save Styled Plot'], href=baseapp_prefix + '/save_styled_plot', className="dropdown-item")

        #self.dropdown_menu = html.Div(id=page_name + "dropdown_menu", children = [self.drop_down_save], className = "dropdown-menu")

        self.relevant_dropdowns = [self.drop_down_save] 

        self.button_padding = {'height':'33px','padding-left':'12px','padding-right':'12px' ,
                                  'padding-top':'0px',
                                  'padding-bottom':'0px',
                                  'margin':'0', 'border': '0', 'vertical-align':'middle'}

        self.action_button = html.Button("Save Plot",
                                               id=self.page_name+"save_plot_button",
                                               className="btn btn-primary",type="button",
                                               style=self.button_padding)

        self.app_page_menu = page_menu.page_top_menu(self.page_name,self.action_button,self.relevant_dropdowns)
          
        self.debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                              html.Div(id=self.page_name+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                              html.Div(id=self.page_name+'button-output-div', children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                              className="PAGE_DEBUG_CONTENT")

        self.format_table_columns =[
                {'id': 'limit_id', 'name': ['','limit_id']},
                {'id': 'trace_id', 'name': ['','trace_id']},
                {'id': 'trace_name', 'name': ['','trace_name']},
                {'id': 'line_color', 'name': ['line','c'], 'presentation': 'dropdown'},
                {'id': 'line', 'name': ['line','s'], 'presentation': 'dropdown'},
                {'id': 'fill_color', 'name': ['fill','c'], 'presentation': 'dropdown'},
                {'id': 'symbol', 'name': ['symbol','s'], 'presentation': 'dropdown'},
                {'id': 'symbol_color', 'name': ['symbol','c'], 'presentation': 'dropdown'},
            ]

        self.symbols_value_list = ['circle','square','diamond','x','triangle']
        self.symbols_label_list = ['○','□','◇','x','△']        
        self.symbols_lol = []
        for p in (range(0,5)):
            l = [self.symbols_label_list[p],self.symbols_value_list[p]]
            self.symbols_lol.append(l)
        #print("self.symbols_lol >>>>>>>>>>>", self.symbols_lol)
        self.symbol_options=[{'label': item[0], 'value' : item[1]} for item in self.symbols_lol]
        print("self.symbol_options >>>>>>>>>>>", self.symbol_options)

        self.palette_color_list = ['black','red','orange','yellow' 'green','blue', 'purple', 'brown']
        self.palette_color_abreviations = ['BK','RD','OR','YL','GN', 'BL', 'PR', 'BR']
        self.palette_color_squares = ['⬛','🟥','🟧','🟨','🟩', '🟦', '🟪', '🟫']
        
        self.colors_lol = []
        for p in (range(0,7)):
            l = [self.palette_color_squares[p],self.palette_color_list[p]]
            self.colors_lol.append(l)

        #print("self.symbols_lol >>>>>>>>>>>", self.symbols_lol)
        
        self.color_options=[{'label': item[0], 'value' : item[1]} for item in self.colors_lol]
        print("self.color_options >>>>>>>>>>>", self.color_options)

        self.line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
        self.line_styles_lines = ['__', '...', '---', '__ __', '_.', '__.']

        self.line_styles_lol = []
        for p in (range(0,5)):
            l = [self.line_styles_lines[p],self.line_styles_list[p]]
            self.line_styles_lol.append(l)
        
        self.line_style_options=[{'label': item[0], 'value' : item[1]} for item in self.line_styles_lol]
        self.simple_table = html.Div()
        self.dmtool_userid = dmtool_userid_in
        self.limits_list_df = pd.DataFrame()
        self.limits_traces_df = pd.DataFrame()
        self.limits_data_df = pd.DataFrame()
        self.limits_list_dict = {}
        self.plot_series_df = pd.DataFrame()
        self.FigChart = go.Figure()
        self.FigLegend = go.Figure()
        self.TableFormat = dash_table.DataTable()
        self.GraphClass = None
        self.GraphChart = dcc.Graph()
        self.GraphLegend = dcc.Graph()
        self.layout = {}
        self.CreateLegend()
        self.CreateChart()
        self.CreateFormat()
        self.CreateSimpleTable()

        '''
        self.data = []
        self.data_df = pd.DataFrame()
        self.table_row  =  dbc.Row()
        self.layout = html.Div()
        self.ExampleTable = dash_table.DataTable()
        self.Create()
        self.Update()
        #self.Example()
        '''
        
    def SetListOfLimits(self, listoflimits_in):
        self.listoflimits = listoflimits_in
        
    def UpdateData(self):
        #self.limits_list_df, self.limits_traces_df, self.limits_data_df, self.limits_list_dict = gld.GetListOfLimits(self.dmtool_userid, listoflimits_in)
        self.limit_data = gldc.LimitData(self.dmtool_userid, 0, self.listoflimits)
        self.limit_data.PopulateLimitData()
        print("<<<<<<<< ---------- Updating Data ---------------- >>>>>>")
        print("limit_list_df >>>>>", self.limit_data.limit_list_df)
        print("trace_list_df >>>>>",self.limit_data.trace_list_df)
        print("limit_data_df >>>>>", self.limit_data.limit_data_df.head(5)) 

    def CreateLayout(self):
    
        #self.limit_list_df, self.trace_list_df, self.limits_data_df, self.limits_list_dict = gld.GetListOfLimits(self.dmtools_userid, self.listoflimits)
        
        #traces = all_trace_list_df[all_trace_list_df['limit_id'].isin(limits_in)].copy()
        #traces = self.trace_list_df
        
        #print("traces >>>>>>", traces)
        
        #styling_data_table = self.FormatDataTable
        
        #legend_fig = FigLegend
        
        self.GraphLegend = dcc.Graph(figure=self.FigLegend,
                                 id= self.page_name + 'graph_legend_id',
                                 style={'width': '100%', 'height': '100%'})
        
        #style_and_legend_column = gsal.GetStyleAndLegendColumn(styling_data_table,legend_graph)
        
        
        ## all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict
    
        #self.GraphClass = dg.DataGraph(dmtool_userid, limits_in)
        
        self.GraphChart = dcc.Graph(figure=self.FigChart,
                                  id=self.page_name + 'graph_chart_id',
                                  config=dict(responsive=True),
                                  mathjax=True,
                                  #className='GRAPH'
                                  style={'width': '100%', 'height': '100%'}
                                      )
        
        ### this is to show how the page is laid out and structured
        '''
        first_row_second_column =  dbc.Row(
                [
                    dbc.Col(html.Div("1st Row of Second columns"), className="col-sm-12 col-md-6 col-lg-6 PAGE_TABLE_CONTENT_TOP_RIGHT"),
                ], style={'width': '100%', 'height': '50%','border': '2px solid black'})
    
        second_row_second_column = dbc.Row(
                [
                    dbc.Col(html.Div("2nd Row of Second columns"), className="col-sm-12 col-md-6 col-lg-6 PAGE_TABLE_CONTENT_BOTTOM_RIGHT")
                ] , style={'width': '100%', 'height': '50%', 'border': '2px solid black'})
            
        skeleton_container = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div("1st of two columns"), className="col-sm-12 col-md-6 col-lg-6 PAGE_GRAPH_CONTENT", style={'border': '2px solid black'}),
                    dbc.Col(children=[first_row_second_column,second_row_second_column] , className="col-sm-12 col-md-6 col-lg-6")
                ], style={'height': '100%'} ##className = "CONTENT_ROW"
            ),
        ],  style={'height': '100%'} ##className="container-fluid DASHBOARD_CONTAINER_STYLE"
        )    
        '''
        
        ##layout_out = skeleton_container
    
        ######
        
        first_row_second_column = html.Div(id= self.page_name+'table_div', children=[self.TableFormat],
                                style={'width': '100%', 'height': '100%','border': '2px solid black', 'padding' : '0', 'margin' : '0'})

        simple_table_div = html.Div(id= self.page_name+'table_div', children=[self.simple_table],
                                style={'width': '100%', 'height': '100%','border': '2px solid black', 'padding' : '0', 'margin' : '0'})

       
        '''
        second_row_second_column = dbc.Row(
                [
                    dbc.Col(id= self.page_name+'legend_div', children=[self.GraphLegend], width=6, sm=12, md=12, className="PAGE_TABLE_CONTENT_BOTTOM_RIGHT")
                ] , style={'width': '100%', 'height': '50%', 'border': '2px solid black'})
        '''
        
        
        self.dashboard_container = html.Div(id=self.page_name+'content',
            children=[
                html.Div(
                    children=[
                        html.Div(id= self.page_name+'chart_div', children=[self.GraphChart],
                                 style={'border': '2px solid black', 'height': '500px', 'width': '500px', 'padding' : '0', 'margin' : '0'}),
                        html.Div(children=[simple_table_div] , style={'height': '200px', 'width': '500px','border': '2px solid black'})
                    ], style={'height': '100%',  'width' : '100%', 'padding' : '0', 'margin' : '0'} ##className = "CONTENT_ROW"
                ),
            ],  style={'height': '100%', 'width' : '100%', 'padding' : '0', 'margin' : '0'}
            )    
        
        #self.layout = dashboard_container
        
        
        #layout = style_plot_and_traces_form_form
        
        self.layout = html.Div([
                                dcc.Location(id=self.page_name+'url',refresh=True),
                                dcc.Store(id= self.page_name + 'screen_size_store', storage_type='local'),
                                ##html.Div(id=self.page_name+'layout-div'),
                                self.app_page_menu,
                                self.dashboard_container
                                #self.debug_output
                                ])

        
        '''
        @callback(Output('container-button-timestamp_1', 'children'),
            Input('btn-nclicks-1_1', 'n_clicks_timestamp'),
            Input('btn-nclicks-2_1', 'n_clicks_timestamp'))
        def display(btn1, btn2):
            if btn1 == None:
                btn1 = 0
            if btn2 == None:
                btn2 = 0
            prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
            if int(btn1) > int(btn2):
                msg = 'Save was most recently clicked  > ' + prop_id
            elif int(btn2) > int(btn1):
                msg = 'Cancel was most recently clicked  > ' + prop_id
            else:
                msg = 'None of the buttons have been clicked yet'
            return html.Div([
                html.Div('btn1: {}'.format(btn1)),
                html.Div('btn2: {}'.format(btn2)),
                html.Div(msg)
            ]) 
        '''
    
    def UpdateFormat(self):
      
        #limits_traces_copy = limits_traces_in.copy()
        #print("format table : trace_list_df.columns >> " , self.limit_data.trace_list_df.columns)
        #print("format table : trace_list_df 5 >> " , self.limit_data.trace_list_df.head(5))
        #trace_1 = {'limit_id' : 1,'data_label' : 'data_label_1', 'trace_id' : 1, 'trace_name' : '1_trace_name','line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 1}
        #trace_2 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 2, 'trace_name' : '2_trace_name','line_color': 'red', 'symbol_color': 'red', 'fill_color': 'red', 'line': 'dot', 'symbol': 'circle', 'id': 2}
        #trace_3 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 3, 'trace_name' : '3_trace_name','line_color': 'blue', 'symbol_color': 'blue', 'fill_color': 'blue', 'line': 'dash', 'symbol': 'circle', 'id': 3}
        #self.data = [trace_1, trace_2, trace_3]
        #self.data_df = pd.DataFrame.from_dict(self.data)
        cycle_colors = itertools.cycle(self.palette_color_list)
        append_this = []
        #colored_limits = pd.DataFrame(data=None, columns=limits_traces_in.columns, index=limits_traces_in.index)
        colored_limits_list =[]
        #for index, row in self.limit_data.trace_list_df.iterrows():
        for index, row in self.limit_data.trace_list_df.iterrows():
            #print(row['c1'], row['c2'])
            copy_row = row.copy()
            #color = next(cycle_colors)
            #copy_row['line_color'] = color
            #copy_row['symbol_color'] = color
            #copy_row['fill_color'] = color
            append_this = [copy_row['limit_id'], copy_row['data_label'],
                         copy_row['trace_id'],copy_row['trace_name'],
                         copy_row['line_color'],copy_row['symbol_color'],copy_row['fill_color'],
                         copy_row['line'],copy_row['symbol'],copy_row['id']]
            print(append_this)
            colored_limits_list.append(append_this)
        
        #Index(['id', 'limit_id', 'data_label', 'trace_id', 'trace_name', 'line_color',
        #   'symbol_color', 'fill_color', 'line', 'symbol'],
        
        print("append_this >>>>", append_this)
        #print("self.limit_data.trace_list_df.columns >>>>>>", self.limit_data.trace_list_df.columns)
        
        colored_limits = pd.DataFrame(data=colored_limits_list, columns=self.limit_data.trace_list_df.columns)
        
        #print("formatting table >>>> colored_limits >>>", colored_limits)
        
        self.TableFormat = dash_table.DataTable(
              id=self.page_name + 'format_table_id',
              #row_deletable=True,
              # Add this line
              #fixed_rows={'headers': True},
              #style_table=style_table,  # defaults to 500
              #style_cell={'fontSize':10,'height':11} ,
              style_cell=self.format_table_style_cell,
              #fill_width=True,
              #style_table={'overflowY': 'auto'},
              #virtualization=True
              data=colored_limits.to_dict('records'),
              columns=self.format_table_columns,
              editable=True,
              css=self.format_table_css,
              dropdown={
                  'line_color': {
                      'options': self.color_options,
                      'searchable' : False,
                      'clearable' : False,
                  },
                  'line': {
                       'options': self.line_style_options,
                       'searchable' : False
                  },
                  'fill_color': {
                      'options': self.color_options,
                      'searchable' : False,
                      'clearable' : False,
                  },
                  'symbol': {
                       'options': self.symbol_options,
                       'searchable' : False,
                      'clearable' : False,
                  },
                   'symbol_color': {
                       'options': self.color_options,
                       'searchable' : False,
                       'clearable' : False,
                  }
              },
              style_cell_conditional=[
                  {'if': {'column_id': 'limit_id'},
                   'width': '5%'},
                  #{'if': {'column_id': 'data_label'},
                  # 'width': '40%'},
                  {'if': {'column_id': 'trace_id'},
                   'width': '5%'},
                  {'if': {'column_id': 'trace_name'},
                   'width': '40%'},
                  {'if': {'column_id': 'line_color'},
                   'width': '10%'},
                  {'if': {'column_id': 'line'},
                   'width': '10%'},
                  {'if': {'column_id': 'fill_color'},
                   'width': '10%'},
                  {'if': {'column_id': 'symbol'},
                   'width': '10%'},
                  {'if': {'column_id': 'symbol_color'},
                   'width': '10%'}],
            merge_duplicate_headers=True,
          )

    def Example(self):
        self.ExampleTable = dash_table.DataTable(
            columns=[
                {"name": ["", "Year"], "id": "year"},
                {"name": ["City", "Montreal"], "id": "montreal"},
                {"name": ["City", "Toronto"], "id": "toronto"},
                {"name": ["City", "Ottawa"], "id": "ottawa"},
                {"name": ["City", "Vancouver"], "id": "vancouver"},
                {"name": ["Climate", "Temperature"], "id": "temp"},
                {"name": ["Climate", "Humidity"], "id": "humidity"},
            ],
            data=[
                {
                    "year": i,
                    "montreal": i * 10,
                    "toronto": i * 100,
                    "ottawa": i * -1,
                    "vancouver": i * -10,
                    "temp": i * -100,
                    "humidity": i * 5,
                }
                for i in range(10)
            ],
            merge_duplicate_headers=True,
        )
        self.TableFormat = self.ExampleTable


    def CreateSimpleTable(self):
        '''
        <table style="width:100%">
          <tr>
            <td>Emil</td>
            <td>Tobias</td>
            <td>Linus</td>
          </tr>
        </table>
        '''
        cell_1 = html.Div(className='td', children=['Emil'])
        cell_2 = html.Div(className='td', children=['Tobias'])
        cell_3 = html.Div(className='td', children=['Linus'])
        table_row = html.Div(className='tr', children=[cell_1,cell_2,cell_3], style={'width':'100%'})
        self.simple_table = html.Div(className='table', children=[table_row], style={'width':'100%'})
    
    def CreateFormat(self):
         self.TableFormat = dash_table.DataTable(
            id=self.page_name + 'format_table_id',
            columns=self.format_table_columns,
            style_cell_conditional=[
                {'if': {'column_id': 'limit_id'},
                 'width': '5%'},
                #{'if': {'column_id': 'data_label'},
                # 'width': '40%'},
                {'if': {'column_id': 'trace_id'},
                 'width': '5%'},
                {'if': {'column_id': 'trace_name'},
                 'width': '40%'},
                {'if': {'column_id': 'line_color'},
                 'width': '10%'},
                {'if': {'column_id': 'line'},
                 'width': '10%'},
                {'if': {'column_id': 'fill_color'},
                 'width': '10%'},
                {'if': {'column_id': 'symbol'},
                 'width': '10%'},
                {'if': {'column_id': 'symbol_color'},
                 'width': '10%'}],
            merge_duplicate_headers=True,
        )

    
    def UpdateFormatOld(self):
    
        #limits_traces_copy = limits_traces_in.copy()
        print("format table : trace_list_df.columns >> " , self.limit_data.trace_list_df.columns)
        print("format table : trace_list_df 5 >> " , self.limit_data.trace_list_df.head(5))
        palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
        cycle_colors = itertools.cycle(palette_list)
        append_this = []
        #colored_limits = pd.DataFrame(data=None, columns=limits_traces_in.columns, index=limits_traces_in.index)
        colored_limits_list =[]
        for index, row in self.limit_data.trace_list_df.iterrows():
            #print(row['c1'], row['c2'])
            copy_row = row.copy()
            #color = next(cycle_colors)
            #copy_row['line_color'] = color
            #copy_row['symbol_color'] = color
            #copy_row['fill_color'] = color
            append_this = [copy_row['limit_id'], copy_row['data_label'],
                           copy_row['trace_id'],copy_row['trace_name'],
                           copy_row['line_color'],copy_row['symbol_color'],copy_row['fill_color'],
                           copy_row['line'],copy_row['symbol'],copy_row['id']]
            print(append_this)
            colored_limits_list.append(append_this)
    
        #Index(['id', 'limit_id', 'data_label', 'trace_id', 'trace_name', 'line_color',
        #   'symbol_color', 'fill_color', 'line', 'symbol'],
        
        print("append_this >>>>", append_this)
        print("self.limit_data.trace_list_df.columns >>>>>>", self.limit_data.trace_list_df.columns)
    
        colored_limits = pd.DataFrame(data=colored_limits_list, columns=self.limit_data.trace_list_df.columns)##, index=self.limit_data.trace_list_df.index)
        
      
        print("formatting table >>>> colored_limits >>>", colored_limits)
      
      
        line_color_list = palette_list
        
        fill_color_list = palette_list
        
        symbol_color_list = palette_list 
      
        line_color_options=[{'label': i, 'value': i} for i in line_color_list]
        
        fill_color_options=[{'label': i, 'value': i} for i in fill_color_list]
        
        symbol_color_options=[{'label': i, 'value': i} for i in symbol_color_list]
        
        line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
        
        line_styles_options=[{'label': i, 'value': i} for i in line_styles_list]
        
        symbol_list = ['circle','square','diamond','cross','x','hexagon','pentagon','octagon','star','asterisk','hash']
        
        symbol_options=[{'label': i, 'value': i} for i in symbol_list]
        
        self.TableFormat = dash_table.DataTable(
                id=self.page_name + 'format_table_id',
                #row_deletable=True,
                # Add this line
                #fixed_rows={'headers': True},
                #style_table=style_table,  # defaults to 500
                #style_cell={'fontSize':10,'height':11} ,
                style_cell=self.format_table_style_cell,
                #fill_width=True,
                #style_table={'overflowY': 'auto'},
                #virtualization=True
                data=colored_limits.to_dict('records'),
                columns=[
                    {'id': 'limit_id', 'name': 'limit_id'},
                    ##{'id': 'data_label', 'name': 'data_label'},
                    {'id': 'trace_id', 'name': 'trace_id'},
                    {'id': 'trace_name', 'name': 'trace_name'},
                    {'id': 'line_color', 'name': 'line_color', 'presentation': 'dropdown'},
                    {'id': 'line', 'name': 'line', 'presentation': 'dropdown'},
                    {'id': 'fill_color', 'name': 'fill_color', 'presentation': 'dropdown'},
                    {'id': 'symbol', 'name': 'symbol', 'presentation': 'dropdown'},
                    {'id': 'symbol_color', 'name': 'symbol_color', 'presentation': 'dropdown'},
                ],
    
                editable=True,
                css=self.format_table_css,
                dropdown={
                    'line_color': {
                        'options': [
                            {'label': i, 'value': i}
                            for i in line_color_list
                        ]
                    },
                    'line': {
                         'options': [
                            {'label': i, 'value': i}
                            for i in line_styles_list
                        ]
                    },
                    'fill_color': {
                        'options': [
                            {'label': i, 'value': i}
                            for i in fill_color_list
                        ]
                    },
                    'symbol': {
                         'options': [
                            {'label': i, 'value': i}
                            for i in symbol_list
                        ]
                    },
                     'symbol_color': {
                         'options': [
                            {'label': i, 'value': i}
                            for i in symbol_color_list
                        ]
                    }
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'limit_id'},
                     'width': '5%'},
                    #{'if': {'column_id': 'data_label'},
                    # 'width': '40%'},
                    {'if': {'column_id': 'trace_id'},
                     'width': '5%'},
                    {'if': {'column_id': 'trace_name'},
                     'width': '40%'},
                    {'if': {'column_id': 'line_color'},
                     'width': '10%'},
                    {'if': {'column_id': 'line'},
                     'width': '10%'},
                    {'if': {'column_id': 'fill_color'},
                     'width': '10%'},
                    {'if': {'column_id': 'symbol'},
                     'width': '10%'},
                    {'if': {'column_id': 'symbol_color'},
                     'width': '10%'}],
            )

    
    def CreateLegend(self):
    
        #limit_id = [1]
        
        #legend_plotseries = self.limits_traces_df[self.limits_traces_df['limit_id'].isin(self.listoflimits)].copy()
        
        ##plotseries_default = CreatePlotSeries(limit_id)
        
        rows_list = list(range(1,6))
        cols_list = list(range(1,6))
        
        table_rows=12
        table_cols=5
        
        self.FigLegend = make_subplots(
        column_titles = ['limit_id','trace_id','trace_name','line', 'symbol'],
        rows=table_rows,
        cols=table_cols,
        horizontal_spacing = 0.00,
        vertical_spacing = 0.00,
        #subplot_titles=(titles)
        column_widths=[0.1,0.1,0.6,0.1, 0.1],)
        
        
        #fig_legend_out.update_xaxes(matches=None, showticklabels=True)
        #fig_legend_out.update_yaxes(matches=None, showticklabels=True)
        
        #fig_legend_out.update_layout(xaxis_range=[1,2])
    
        
        self.FigLegend.update_layout(
        #    autosize=False,
        #    width=800,
        #    height=200,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=20,
                pad=0
            ),
            paper_bgcolor="LightSteelBlue",
        )        
        
        self.GraphLegend = dcc.Graph(figure=self.FigLegend,
                                 id= self.page_name + 'graph_legend_id',
                                 style={'width': '100%', 'height': '100%'})

    def UpdateLegend(self):
        #result_ids = [1,262]
        
        #print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
        #self.plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
        
        #result_ids_plot = self.plot_series_df['limit_id'].unique().tolist()
        rows_list = list(range(1,6))
        cols_list = list(range(1,6))
        
        table_rows=12
        table_cols=5

        self.FigLegend = make_subplots(
        column_titles = ['limit_id','trace_id','trace_name','line', 'symbol'],
        rows=table_rows,
        cols=table_cols,
        horizontal_spacing = 0.00,
        vertical_spacing = 0.00,
        #subplot_titles=(titles)
        column_widths=[0.1,0.1,0.6,0.1, 0.1],)
        
        
        #fig_legend_out.update_xaxes(matches=None, showticklabels=True)
        #fig_legend_out.update_yaxes(matches=None, showticklabels=True)
        
        #fig_legend_out.update_layout(xaxis_range=[1,2])
    
        
        self.FigLegend.update_layout(autosize=True,
        #    width=100%,
        #    height=200,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=20,
                pad=0
            ),
            paper_bgcolor="LightSteelBlue",
        )
        
        rowloop = 0
        
        for index, row in self.limit_data.trace_list_df.iterrows():
            #print(row['c1'], row['c2'])
            rowloop +=1
            for c in cols_list: #enumerate here to get access to i
                # STEP 2, notice position of arguments!
                table_column_names = ['limit_id','trace_id','trace_name','line','symbol']
                scatter_mode_list = ['text-number','text-number','text-text','lines','markers']
                current_column = table_column_names[c-1]
                current_mode = scatter_mode_list[c-1]
                if current_mode =='lines':
                    self.FigLegend.add_trace(go.Scatter(x=[1,2],
                                             y=[1,1],
                                             mode=current_mode,
                                             #text=row[current_column],
                                             line=dict(width=4,dash=row['line'],color=row['line_color']),
                                            ),
                                  row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                                  col=c)
                if current_mode =='text-text':
                    self.FigLegend.add_trace(go.Scatter(x=[1,2], 
                                             textposition='middle right',
                                             y=[1,1],
                                             mode='text',
                                             text=[row[current_column],'']
                                            ),
                                  row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                                  col=c)
                
                if current_mode =='text-number':
                    self.FigLegend.add_trace(go.Scatter(x=[1], 
                                             textposition='middle right',
                                             y=[1],
                                             mode='text',
                                             text=row[current_column]
                                            ),
                                  row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                                  col=c)
                if current_mode =='markers':
                    self.FigLegend.add_trace(go.Scatter(x=[1], 
                                            y=[1],
                                            mode=current_mode,
                                            #text=row[current_column],
                                            marker_symbol=row['symbol'],
                                            marker=dict(
                                            size=10,
                                            color=row['symbol_color'],#set color equal to a variable
                                            colorscale='Viridis', # one of plotly colorscales
                                            showscale=False,
                                            )
                                            ),
                                  row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                                  col=c)
                    
                self.FigLegend.update_xaxes(showgrid=False)
                self.FigLegend.update_yaxes(showgrid=False)
                #legend
                self.FigLegend.update_layout(showlegend=False)
                #x axis
                self.FigLegend.update_xaxes(visible=False)
                #y axis    
                self.FigLegend.update_yaxes(visible=False)
        
        self.GraphLegend = dcc.Graph(figure=self.FigLegend,
                                 id= self.page_name + 'graph_legend_id',
                                 style={'width': '100%', 'height': '100%'})
    
    def CreateChart(self):
      
        self.FigChart = go.Figure()
        
        self.FigChart.update_layout(autosize=True)
        
        self.GraphChart = dcc.Graph(figure=self.FigChart,
                                  id=self.page_name + 'graph_chart_id',
                                  config=dict(responsive=True),
                                  mathjax=True,
                                  #className='GRAPH'
                                  style={'width': '100%', 'height': '100%'}
                                      )
    
    def UpdateChart(self):
        #result_ids = [1,262]
        #print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
        #self.plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
        
        #result_ids_plot = plot_series_df['limit_id'].unique().tolist()
        
        #limit_list_df, trace_list_df, limit_data_df, limit_list_dict = gld.GetListOfLimits(self.dmtool_userid, self.listoflimits)
        #print("limit_list_df >>>>>", self.limit_data.limit_list_df)
        #print("trace_list_df >>>>>",self.limit_data.trace_list_df)
        #print("limit_data_df >>>>>", self.limit_data.limit_data_df.head(5))
        #plot_series_df = pd.DataFrame(plotseries_table_in)
        
        x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
        y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
        
        #plotseries_default, df_experiment_plot = CreatePlotSeries(result_ids_plot)
        #plotseries_default_plot = CreatePlotSeriesDefault(df_experiment_all_plot)
        
        # Create figure
        self.FigChart = go.Figure()
        self.FigChart.update_xaxes(
              title_text=x_title_text,
              type="log"
              #type="linear"
          )
        
        self.FigChart.update_yaxes(
              title_text=y_title_text,
              #type="log"
              type="linear"
          )

        for index, row in self.limit_data.trace_list_df.iterrows():
            trace_data = self.limit_data.limit_data_df[(self.limit_data.limit_data_df['limit_id']==row['limit_id'])
                                          & (self.limit_data.limit_data_df['trace_id']==row['trace_id'])]
            
            # print('trace_data>>>>', trace_data)
            
            trace2add = trace_data.sort_index()
            
            trace_name = str(row['trace_name'])
            
            self.FigChart.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'],
                              mode='lines+markers', # 'lines' or 'markers'
                              line=dict(width=4,dash=row['line'],color=row['line_color']),
                              #showscale=False,
                              text=row['trace_name'],
                              fill='toself',
                              fillcolor = row['fill_color'],
                              marker_symbol=row['symbol'],
                                   marker=dict(
                                  size=10,
                                  color=row['symbol_color'],#set color equal to a variable
                                  #colorscale='Viridis', # one of plotly colorscales
                                  showscale=False,
                              ),
                              legendgroup=str(row['limit_id']),  # this can be any string, not just "group"
                              legendgrouptitle_text=str(row['limit_id']),
                              name=str(row['trace_name'])
                                   ))
            
            self.FigChart.update(layout_showlegend=False)

    def UpdateAppearances(self, newformats_dict):
        self.limit_data.trace_list_df = pd.DataFrame()
        self.limit_data.trace_list_df = pd.DataFrame.from_dict(newformats_dict).copy()

    def RespondToButtonCallBackSPAT(self):
        @callback(
            Output(self.page_name+'button-output-div', 'children'),
            Input(self.page_name+"save_plot_button", 'n_clicks')
        )
        def displayClick1_1(btn1):
            msg = "None of the buttons have been clicked yet"
            prop_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
            if self.page_name+'save_plot_button' == prop_id:
                msg = "save_plot_button pressed"
            else:
                msg = "No Button Pressed"
            return html.Div(msg)

    def UpdateChartsForPlot(self):
        @callback(Output(page_name+'chart_div','children'),
                  Output(page_name+'table_div', 'children'),
                  Input(self.page_name +'url', 'href'),
                  State(self.page_name + 'screen_size_store', 'data'))
        def set_plot_name(url_in,page_size_in):
            ## get user id from cookie
            dmtooluser_cls = gdu.GetUserID()
            self.dmtool_userid = dmtooluser_cls.dmtool_userid
            self.request_header = {'dmtool-userid':str(self.dmtool_userid)}
            ## get plot name from url
            f = furl(url_in)
            self.plot_id = f.args['plot_id']
            ## get about data
            container_url = 'http://container_fastapi_data_1:8014'
            api_url = '/dmtool/fastapi_data/internal/data/data_about?plot_id_in=' + str(self.plot_id)
            full_url = container_url + api_url
            r = requests.get(full_url,  headers=self.request_header)
            response_data = r.json()
            print('response_data >>>>>>>>>', response_data)
            lol = []
            for x in response_data:
                append_this = x['Data_about']
                lol.append(append_this)
                
            response_data_frame = pd.DataFrame.from_dict(lol)
            limits_list = response_data_frame['limit_id'].tolist()
            print(limits_list)
            
            #https://dev1.dmtool.info/dmtool/fastapi_data/internal/data/data_about?plot_id_in=3181
            ## get limit data
            ##def GetListOfLimits(dmtool_userid,listoflimits_in):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> get list of limits called <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            
            fastapi_url_listoflimits = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/listoflimits" ## multiple limit operations
           
            response_data_frame = pd.DataFrame()
                
            #try:
            print("get limits - list of limits ", limits_list)
            listoflimits_json = {"limit_ids": limits_list}
            
            r = requests.post(fastapi_url_listoflimits,json=listoflimits_json,headers=self.request_header)
            response_data = r.json()
            #print("list of limits request response >>>>>>>>>>>>>>>>>>>>> " ,response_data)
        
            #print('response data')
            #print('===================')
            #print(response_data)
            print('===== response data frame ==============')
            response_data_frame = pd.DataFrame.from_dict(response_data['limits'])
            #print('===== response data frame ==============')
            
            #print("gld : library response_data_frame >>>>>" , response_data_frame)
            
            #limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
            #column_names=['id','data_label','data_comment','data_values']

            self.limits_dataframe = response_data_frame
            ## create appearance data
            

            ## create data data

            ## get data data
            
            
            ##print('spat callback: list_of_limits >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', list_of_limits_int)
            #list_of_limits = [33]
            #dbl = DashBoardLayout(page_name, dmtool_userid,  list_of_limits_int)
            self.SetListOfLimits(limits_list)
            self.UpdateData()
            ##self.UpdateLegend()
            self.UpdateFormat()
            self.UpdateChart()
            
            
            return self.GraphChart, self.TableFormat
    
    def UpdateChartAndLegendAppearanceCallBackSPAT(self):
        @callback(
            [Output(page_name+'graph_chart_id','figure')],
            [Input(page_name+'format_table_id', 'data')],
            [State(page_name+'format_table_id', 'data')])
        def update_output(table_data, table_data_in):
            
            print('spat : update data call back triggered')
            print('spat : table_data_in >>>>>>>>>>',table_data_in,"  type >> ", type(table_data_in) )
            self.UpdateAppearances(table_data_in)
            self.UpdateChart()
            self.UpdateLegend()
            return [self.FigChart]
    def page_size_callback(self):
        clientside_callback(
            """
            function(href) {
                var w = window.innerWidth;
                var h = window.innerHeight;
                var width_text = w.toString();
                var height_text = h.toString();
                const page_size_dict = {width: width_text, height: height_text};
                return page_size_dict;
            }
            """,
            Output(self.page_name + 'screen_size_store', 'data'),
            Input(self.page_name + 'url', 'href')
        )
        


dbl = StylePlotAndTracesDashBoardLayout(page_name, dmtool_userid)
dbl.CreateLayout()
layout = dbl.layout
dbl.page_size_callback()
#dbl.RespondToButtonCallBackSPAT()
#dbl.UpdateChartsForPlot()
#dbl.UpdateChartAndLegendAppearanceCallBackSPAT()
