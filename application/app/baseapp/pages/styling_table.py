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


class StylingTable():

    def __init__(self,pagename_in):
        self.page_name = pagename_in
        self.data = []
        self.data_df = pd.DataFrame()
        self.table_row  =  dbc.Row()
        self.layout = html.Div()
        self.Create()
        self.Update()

  
    def Create(self):
        self.TableFormat = dash_table.DataTable(
            id=self.page_name + 'format_table_id',
            columns=[
                {'id': 'limit_id', 'name': 'limit_id'},
                {'id': 'trace_id', 'name': 'trace_id'},
                {'id': 'trace_name', 'name': 'trace_name'},
                {'id': 'line_color', 'name': 'line_color', 'presentation': 'dropdown'},
                {'id': 'line', 'name': 'line', 'presentation': 'dropdown'},
                {'id': 'fill_color', 'name': 'fill_color', 'presentation': 'dropdown'},
                {'id': 'symbol', 'name': 'symbol', 'presentation': 'dropdown'},
                {'id': 'symbol_color', 'name': 'symbol_color', 'presentation': 'dropdown'},
            ],
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

    def Update(self):
      
        #limits_traces_copy = limits_traces_in.copy()
        #print("format table : trace_list_df.columns >> " , self.limit_data.trace_list_df.columns)
        #print("format table : trace_list_df 5 >> " , self.limit_data.trace_list_df.head(5))
        trace_1 = {'limit_id' : 1, 'trace_id' : 1, 'line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 1}
        trace_2 = {'limit_id' : 1, 'trace_id' : 2, 'line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 2}
        trace_3 = {'limit_id' : 1, 'trace_id' : 3, 'line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 3}
        data = [trace_1, trace_2, trace_3]
        data_df = pd.DataFrame.from_dict(data)
        palette_list = ['black','red','orange','yellow' 'green','blue', 'purple', 'grey', 'pink']
        palette_abr = ['BK','RD','OR','YL','GN', 'BL', 'PR', 'GY', 'PK']
        cycle_colors = itertools.cycle(palette_list)
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
        
        
        line_color_list = palette_abr
        
        fill_color_list = palette_abr
        
        symbol_color_list = palette_abr 
        
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

    def Layout(self):
        self.table_row  =  dbc.Row(
                [
                    dbc.Col(id= self.page_name+'table_div', children=[self.TableFormat], width=6, sm=12, md=12, className="PAGE_TABLE_CONTENT_TOP_RIGHT"),
                ], style={'width': '100%', 'height': '50%','border': '2px solid black'})
        
        self.layout = html.Div([
            dcc.Location(id=page_name+'url',refresh=True),
            html.Div(id=page_name+'content',children=self.table_row,className="DASHBOARD_CONTAINER_STYLE"),
        ],className="PAGE_CONTENT")
    

page_name = 'styling_table'
dbl = StylingTable(page_name)
dbl.Layout()
layout = dbl.layout
