import os
import requests
from urllib.parse import urlparse, parse_qs
import pandas as pd
import itertools

cwd = os.getcwd()

page_name = 'styling_table'
baseapp_prefix = '/application/baseapp'

from datetime import datetime

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Dash
from dash import Input, Output,State
from dash import callback

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


dash.register_page(__name__, path='/styling_table')

## color abreviations from
## https://technicallibrary.midmark.com/Global/Global-GB-00003.htm

class StylingTable():

    def __init__(self,pagename_in):
        self.page_name = pagename_in
        self.data_table_id =  self.page_name + "data_table_id"
        self.format_data_table_row_height = '12px'
        self.row_height = '12px'
        self.table_height = '600px'
        self.format_data_table_font_size = '11px'
        self.format_data_table_style_table={
                #'maxHeight': '50ex',
                #'minHeight': '40vh',
                ##'height': '44vh', ## does not know any detail about parent container
                ##'overflowY': 'scroll', # 'auto'
                ##'overflowX': 'scroll',
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
        
        '''
        self.format_table_css = [{"selector": ".Select-menu-outer", "rule": "display: block !important"},
                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of header
                    {"selector": ".dash-spreadsheet-inner tr td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-spreadsheet tr td th", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of body rows
                    {"selector": ".dash-spreadsheet tr th td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of header
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr td th", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-cell tr th td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"}, 
                    {"selector": ".dash-header tr th td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".Select-option", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    ]
        
        
        self.format_table_css = [{'selector':'.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr', 'rule':'min-height: 10px;height: 10px;'}]

        '''
        
        self.format_table_css = [{"selector": ".Select-menu-outer", "rule": "display: block !important"},
                            {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                            {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                            {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-spreadsheet.dash-freeze-top, .dash-spreadsheet.dash-virtualized",  "rule": "max-height: inherit !important;" },
                            {"selector": ".dash-table-container" ,  "rule":  "max-height: calc(" + self.table_height + " - 100px);"},]
    
        self.table_columns =[
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
        
        self.data = []
        self.table_data = 'table data'
        self.table_div = html.Div()
        self.data_df = pd.DataFrame()
        self.table_df = pd.DataFrame()
        self.table_row  =  dbc.Row()
        self.layout = html.Div()
        self.ExampleTable = dash_table.DataTable()
        self.ExampleTableFormat  = dash_table.DataTable()
        self.Create()
        self.Update()
        self.Example()
        self.generate_html_table()

  
    def Create(self):
        self.TableFormat = dash_table.DataTable(
            id=self.page_name + 'format_table_id',
            columns=self.table_columns,
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

    def Update(self):
      
        #limits_traces_copy = limits_traces_in.copy()
        #print("format table : trace_list_df.columns >> " , self.limit_data.trace_list_df.columns)
        #print("format table : trace_list_df 5 >> " , self.limit_data.trace_list_df.head(5))
        trace_1 = {'limit_id' : 1,'data_label' : 'data_label_1', 'trace_id' : 1, 'trace_name' : '1_trace_name','line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 1}
        trace_2 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 2, 'trace_name' : '2_trace_name','line_color': 'red', 'symbol_color': 'red', 'fill_color': 'red', 'line': 'dot', 'symbol': 'circle', 'id': 2}
        trace_3 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 3, 'trace_name' : '3_trace_name','line_color': 'blue', 'symbol_color': 'blue', 'fill_color': 'blue', 'line': 'dash', 'symbol': 'circle', 'id': 3}
        self.data = [trace_1, trace_2, trace_3]
        self.data_df = pd.DataFrame.from_dict(self.data)
        cycle_colors = itertools.cycle(self.palette_color_list)
        append_this = []
        #colored_limits = pd.DataFrame(data=None, columns=limits_traces_in.columns, index=limits_traces_in.index)
        colored_limits_list =[]
        #for index, row in self.limit_data.trace_list_df.iterrows():
        for index, row in self.data_df.iterrows():
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
        
        colored_limits = pd.DataFrame(data=colored_limits_list, columns=self.data_df.columns)
        
        
        #print("formatting table >>>> colored_limits >>>", colored_limits)
        
        
        #line_color_list = self.palette_abr
        
        #fill_color_list = self.palette_abr
        
        #symbol_color_list = self.palette_abr 
        
        #line_color_options=[{'label': i, 'value': i} for i in line_color_list]
        
        #fill_color_options=[{'label': i, 'value': i} for i in fill_color_list]
        
        #symbol_color_options=[{'label': i, 'value': i} for i in symbol_color_list]
        
        line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
        line_styles_list = ['__', '...', '---', '__ __', '_._', '___ .']
        
        line_styles_options=[{'label': i, 'value': i} for i in line_styles_list]
        
        #symbol_list = ['circle','square','diamond','cross','x','hexagon','pentagon','octagon','star','asterisk','hash']
        
        #symbol_options=[{'label': i, 'value': i} for i in symbol_list]
        
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
              #virtualization=TrueInput(self.page_name +'url', 'href'),
              data=colored_limits.to_dict('records'),
              columns=self.table_columns,
              editable=True,
              ##css=self.format_table_css,
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
        print('-------------------------------------')
        print("self.format_table_css >>>>>>" , self.format_table_css)
        print('-------------------------------------')
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
            css= self.format_table_css
        )
        self.ExampleTableFormat = self.ExampleTable


    def generate_html_table(self):
        data = {'Column:Cap' : ['Data A', 'Data B', 'Data C', ], 'Column:non-Cap' : ['Data a','Data b','Data c', ]}
        max_rows = 12
        df = pd.DataFrame(data)
        self.generated_table = html.Table(id=self.page_name + 'generated_table',
            # Header
            children=[html.Tr([html.Th(col) for col in df.columns]) ] +
            # Body
            [html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))]
        )
    
    
    def Layout(self):
        self.table_div =  html.Div(id= self.page_name+'table_div', children=[self.generated_table], style={'width': '100%', 'height': '200px','border': '2px solid black'})
        
        self.layout = html.Div([
            dcc.Location(id=self.page_name+'url',refresh=True),
            dcc.Store(id= self.page_name + 'screen_size_store', storage_type='local'),
            html.Div(id=self.page_name+'content',children=[self.table_div], style = {'position':'absolute', 'top':'0px', 'width':'100px'}),
            html.Div(id=self.page_name+'response',children="table content", style = {'position':'absolute', 'top':'200px', 'width':'100px'}),
            html.Div(id=self.page_name+'button-output-div',children="button message", style={'position':'absolute', 'top':'225px', 'width':'100px'}),
            html.Button('Submit', id=self.page_name+'save_plot_button', n_clicks=0, style={'position':'absolute', 'top':'250px', 'width':'100px'}),
        ])
    

    def page_refresh_callback(self):
        @callback(Output(self.page_name+'response','children'),
                          Input(self.page_name +'url', 'href'),
                          State(self.page_name+'generated_table', 'children'))
        def get_table_children(url_in,table_div_in):
            print("styling table callback triggered")
            print(table_div_in)
    
    def button_callback(self):
        @callback(
                    Output(self.page_name+'button-output-div', 'children'),
                    Input(self.page_name+"save_plot_button", 'n_clicks'),
                    State(self.page_name+'generated_table', 'children')
                )
        def displayClick1_1(btn1,table_in):
            msg = "None of the buttons have been clicked yet"
            prop_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
            if page_name+'save_plot_button' == prop_id:
                msg = "save_plot_button pressed"
                row_count = len(table_in)
                print("table row count >>>>", row_count)
                column_count = len(table_in[0]['props']['children'])
                print("column_count >>>>>>", column_count)
                table_columns = []
                for c in range(0,column_count):
                    append_this = table_in[0]['props']['children'][c]['props']['children']
                    table_columns.append(append_this)
                print("table_columns >>>>>", table_columns)
                #column_1 = table_in[0]['props']['children'][0]['props']['children']
                #column_2 = table_in[0]['props']['children'][1]['props']['children']
                print(msg)
                #print(table_in[0]['props'])
                #print("column_1, column_2 >>>>>>>>>>>" , column_1, column_2)

                #row_count = len(table_in[1]['props']['children'])
                row_data = []
                table_data_raw = []
                for r in range(1, row_count):
                    row_data = []
                    for c in range(0,column_count):
                        print(r,c,table_in[r]['props']['children'][c]['props']['children'])
                        append_this = table_in[r]['props']['children'][c]['props']['children']
                        row_data.append(append_this)
                    table_data_raw.append(row_data)
                #print('data_1 >>>>>>>>>' , data_1)
                #self.table_data = data_1
                #print("self.table_data >>>>" , self.table_data)
                print("table_data_raw >>>>" , table_data_raw)
                self.table_df = pd.DataFrame(data=table_data_raw, columns=table_columns)
                print("self.table_df >>>>>>>", self.table_df)
            else:
                msg = "No Button Pressed"
            return html.Div(msg)


page_name = 'styling_table'
dbl = StylingTable(page_name)
dbl.Layout()
layout = dbl.layout
dbl.button_callback()

'''
@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(relative_pathname):
    dbl.Layout()
    layout_return = dbl.layout
    return layout_return
'''
