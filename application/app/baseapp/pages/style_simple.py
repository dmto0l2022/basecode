import os
import requests
import json
from urllib.parse import urlparse, parse_qs
import pandas as pd
import numpy as np
import itertools

cwd = os.getcwd()

page_name = 'style_simple'
baseapp_prefix = '/application/baseapp'

from datetime import datetime

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Dash
from dash import Input, Output,State
from dash import callback

from dash_extensions import EventListener

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



dash.register_page(__name__, path='/style_simple')

## color abreviations from
## https://technicallibrary.midmark.com/Global/Global-GB-00003.htm

class StylingTable():

    def __init__(self,pagename_in):
        self.page_name = pagename_in
        self.data_table_id =  self.page_name + "data_table_id"
        self.format_data_table_row_height = '11px'
        self.row_height = '11px'
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
        
        self.event = {'event': 'click', 'props': ['timeStamp', 'button','type', 'srcElement.className', 'srcElement.innerText', 'srcElement.value', 'srcElement.id']}
        self.previous_clickevent = 'None'
        
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
        self.formatting_table = html.Table()
        self.data_df = pd.DataFrame()
        self.data_df_melt = pd.DataFrame()
        self.table_df = pd.DataFrame()
        self.table_row  =  dbc.Row()
        self.layout = html.Div()
        self.dropdown_test = html.Div()
        self.simple_table = html.Table()
        self.Update()

    

    def Update(self):
        ## limit_id #1
        trace_1_1 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 1, 'trace_name' : '1_trace_name','line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 1}
        trace_1_2 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 2, 'trace_name' : '2_trace_name','line_color': 'red', 'symbol_color': 'red', 'fill_color': 'red', 'line': 'dot', 'symbol': 'circle', 'id': 2}
        trace_1_3 = {'limit_id' : 1, 'data_label' : 'data_label_1', 'trace_id' : 3, 'trace_name' : '3_trace_name','line_color': 'blue', 'symbol_color': 'blue', 'fill_color': 'blue', 'line': 'dash', 'symbol': 'circle', 'id': 3}
        ## limit_id #2
        trace_2_1 = {'limit_id' : 2, 'data_label' : 'data_label_1', 'trace_id' : 1, 'trace_name' : '1_trace_name','line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 1}
        trace_2_2 = {'limit_id' : 2, 'data_label' : 'data_label_1', 'trace_id' : 2, 'trace_name' : '2_trace_name','line_color': 'red', 'symbol_color': 'red', 'fill_color': 'red', 'line': 'dot', 'symbol': 'circle', 'id': 2}
        trace_2_3 = {'limit_id' : 2, 'data_label' : 'data_label_1', 'trace_id' : 3, 'trace_name' : '3_trace_name','line_color': 'blue', 'symbol_color': 'blue', 'fill_color': 'blue', 'line': 'dash', 'symbol': 'circle', 'id': 3}
        ## limit_id #3
        trace_3_1 = {'limit_id' : 3, 'data_label' : 'data_label_1', 'trace_id' : 1, 'trace_name' : '1_trace_name','line_color': 'black', 'symbol_color': 'black', 'fill_color': 'black', 'line': 'solid', 'symbol': 'circle', 'id': 1}
        trace_3_2 = {'limit_id' : 3, 'data_label' : 'data_label_1', 'trace_id' : 2, 'trace_name' : '2_trace_name','line_color': 'red', 'symbol_color': 'red', 'fill_color': 'red', 'line': 'dot', 'symbol': 'circle', 'id': 2}
        trace_3_3 = {'limit_id' : 3, 'data_label' : 'data_label_1', 'trace_id' : 3, 'trace_name' : '3_trace_name','line_color': 'blue', 'symbol_color': 'blue', 'fill_color': 'blue', 'line': 'dash', 'symbol': 'circle', 'id': 3}
        
        
        self.data = [trace_1_1, trace_1_2, trace_1_3, trace_2_1, trace_2_2, trace_2_3 , trace_3_1, trace_3_2, trace_3_3]
        self.data_df = pd.DataFrame.from_dict(self.data)

        self.data_df_melt = pd.melt(self.data_df, id_vars=['limit_id','trace_id'], value_vars=['line_color', 'symbol_color','fill_color', 'line', 'symbol'])
        print('melted >>>>>>>>>>>',self.data_df_melt)
        
        
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
          
        self.colored_limits_df = pd.DataFrame(data=colored_limits_list, columns=self.data_df.columns)

        self.format_table_df = self.colored_limits_df[['limit_id', 'trace_id','trace_name','line','line_color','symbol','symbol_color','fill_color']]

        self.format_table_df.columns = ['ds','tc','description','ls','lc','ss','sc','fc']
        
        self.formatting_table = self.generate_html_formatting_table_from_df(self.format_table_df, 'formatting_table')

        self.values_table = self.generate_html_general_table_from_df(self.data_df_melt, 'values_table')
              
    def get_color_dropdown(self, limit_id_in, trace_id_in, of_what_in, default_value_in):
        palette_color_squares_1 = ['⬛','🟥','🟧','🟨','🟩', '🟦', '🟪', '🟫']
        palette_color_list_1 = ['black','red','orange','yellow','green','blue', 'purple', 'brown']
        palette_color_abreviations_1 = ['BK','RD','OR','YL','GN', 'BL', 'PR', 'BR']
        counter = 0
        children_color = []
        for pc in palette_color_squares_1:
            color_value = palette_color_list_1[counter]
            #print(counter,color_value)
            if color_value == default_value_in:
                selected_flag = True
            else:
                selected_flag = False
            option_id = "{'color_option':'" + str(counter) + "','limit_id':'" + str(limit_id_in) + "','trace_id':'" + str(trace_id_in) + "','variable':'" + of_what_in +"'}"
            option_value = '{\"limit_id":\"' + str(limit_id_in) + '\",\"trace_id\":\"' + str(trace_id_in) + '\",\"variable\":\"' + of_what_in +'\",\"value\":\"'+color_value+'\"}'
            palette_option_append = html.Option(pc, id=option_id , value=option_value,
                                                selected=selected_flag,
                                                style={'width':'100%','margin':'0 !important',
                                                       'padding':'0 !important',
                                                       'line-height':'12px','font-size' : '12px',
                                                       'min-height': '12px', 'display': 'block', 'background':'lightblue', 'border':'none'})
            children_color.append(palette_option_append)
            counter += 1

        
        select_out = html.Select(children=children_color,
                               id=self.page_name + "color_selection, limit_id:" + str(limit_id_in) + ",trace_id:" + str(trace_id_in),
                               style={'width':'100%','margin':'0','padding':'0','appearance':'none', 'background':'lightblue', 'border':'none'})

        return select_out

    def get_line_styles(self, limit_id_in, trace_id_in,default_value_in):
        line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
        line_styles_lines = ['__', '...', '---', '_ _', '_.', '__.']
        counter = 0
        children_line_styles = []
        for ls in line_styles_lines:
            line_value = line_styles_list[counter]
            #print(counter,color_value)
            if line_value == default_value_in:
                selected_flag = True
            else:
                selected_flag = False
            palette_option_append = html.Option(ls, id="line_style_option:" + str(counter) + ",limit_id:" + str(limit_id_in) + ",trace_id:" + str(trace_id_in),
                                                value=line_value,
                                                selected=False,
                                                style={'width':'100%','margin':'0 !important',
                                                       'padding':'0 !important',
                                                       'line-height':'12px','font-size' : '12px',
                                                       'min-height': '12px', 'display': 'block', 'background':'lightblue', 'border':'none'})
            children_line_styles.append(palette_option_append)
            counter += 1

        select_out = html.Select(children=children_line_styles,
                               id=self.page_name + "line_style_selection" + ", limit_id:" + str(limit_id_in) + ",trace_id:" + str(trace_id_in),
                               style={'width':'100%','margin':'0','padding':'0','appearance':'none', 'background':'lightblue', 'border':'none'})

        return select_out


    def get_symbols(self, limit_id_in, trace_id_in,default_value_in):

        symbols_value_list = ['circle','square','diamond','x','triangle']
        symbols_label_list = ['○','□','◇','x','△']
        counter = 0
        children_symbols = []
        for sl in symbols_label_list:
            symbol_value = symbols_value_list[counter]
            if sl == default_value_in:
                selected_flag = True
            else:
                selected_flag = False
            palette_option_append = html.Option(sl, id="symbol_option:" + str(counter) + ",limit_id:" + str(limit_id_in) + ",trace_id:" + str(trace_id_in),
                                                value=symbol_value,
                                                selected=selected_flag,
                                                style={'width':'100%','margin':'0 !important',
                                                       'padding':'0 !important',
                                                       'line-height':'12px','font-size' : '12px',
                                                       'min-height': '12px', 'display': 'block'})
            children_symbols.append(palette_option_append)
            counter += 1

        select_out = html.Select(children=children_symbols,
                               id=self.page_name + "symbol_selection" + "-" + str(limit_id_in) + "-" + str(trace_id_in),
                               style={'width':'100%','margin':'0','padding':'0','appearance':'none',  'background':'lightblue', 'border':'none'})

        return select_out

    
    def select_beginnings(self):

        heading_1 = html.Th(className='th', children='Column 1', style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})

        heading_2 = html.Th(className='th', children='Column 2', style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})

        heading_3 = html.Th(className='th', children='Column 3', style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})

        heading_4 = html.Th(className='th', children='Column 4', style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})
        
        cell_1 = html.Td(className='td', children='Emil', style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})
        cell_2 = html.Td(className='td', children='Tobias', style={'margin':'0','padding':'0','border':'1px solid black',
                                                                     'font-size':'8px', 'line-height':'8px', 'height':'8px', 'min-height':'8px'})
        cell_3 = html.Td(className='td', children='Linus',style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})
        
            
        option_1 = html.Option("Server Option 1", id="Server , 1, 1", value="Server Option 1 Selected", style={'width':'100%','margin':'0','padding':'0','border':'1px solid black'})
        option_2 = html.Option("Server Option 2", id="Server, 1, 2", value="Server Option 2 Selected", style={'width':'100%','margin':'0','padding':'0','border':'1px solid black'})

        palette_color_squares_1 = ['⬛','🟥','🟧','🟨','🟩', '🟦', '🟪', '🟫']

        palette_options = ["X"] * 10
        counter = 0
        children_color = []
        for pc in palette_color_squares_1:
            palette_option_append = html.Option(pc, id="color " + str(counter), value="color " + str(counter),
                                                style={'width':'100%','margin':'0 !important',
                                                       'padding':'0 !important',
                                                       'line-height':'12px','font-size' : '12px',
                                                       'min-height': '12px', 'display': 'block'})
            children_color.append(palette_option_append)
            counter += 1

        
        select_1 = html.Select(children=children_color,
                               id="connections",
                               style={'width':'100%','margin':'0','padding':'0','border':'1px solid black','appearance':'none'})  

        cell_4 = html.Td(className='td', children=select_1,style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})

        cell_10 = html.Td(className='td', children="hello",style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})
        
        ##cell_5 = dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown')

        style_1={'font-size' : '11px', 'line-height':'12px', 'padding':'0', 'margin':'0', 'height':'12px !important',
                                     'max-height':'12px !important', 'min-height':'12px !important','display': 'inline-block'}
        
        flex_style = {'height': '12px', 'display': 'flex', 'justify-content': 'flex-end',
                      'flex-direction': 'row', 'align-items': 'center','padding':'0 !important', 'margin':'0',
                     }

        dropdown_1 = dcc.Dropdown(['New York', 'Montreal', 'Paris', 'London', 'Amsterdam', 'Berlin', 'Rome'],'Paris',
                              style=style_1,
                              id='option-height-example-dropdown')

        dropdown_nostyle = dcc.Dropdown(['New York', 'Montreal', 'Paris', 'London', 'Amsterdam', 'Berlin', 'Rome'],'Paris',
                              id='option1')
        
        #cell_5 = html.Td(className='td', children=dropdown_1, style={'margin':'0','padding':'0','border':'1px solid black',
        #                                                           'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})

        cell_5 = html.Td(className='td', children=dropdown_nostyle,style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})
        
        options = [html.Option(value=x) for x in ["Chocolate", "Coconut", "Mint", "Strawberry"]]

        cell_8 = html.Div(children=cell_5, style={'height':'12px', 'width':'50px', 'background-color':'blue', 'font-size':'11px'})
        
        cell_6 = html.Div(
                [
                    html.Datalist(id="ice-cream-flavors", children=options),
                    dcc.Input(
                        id="ice-cream-choice", list="ice-cream-flavors", name="ice-cream-choice",
                    ),
                ]
            )

        
        '''
         <div class="dropdown">
          <button class="dropbtn">Dropdown</button>
          <div class="dropdown-content">
            <a href="#">Link 1</a>
            <a href="#">Link 2</a>
            <a href="#">Link 3</a>
          </div>
        </div> 
        '''
        '''
        option1 = html.Div('option1')
        option2 = html.Div('option2')
        dropdown_content = html.Div(className=
        cell_6 = html.Div(className='dropdown',children=['option1','option2'] id='dropdown1')
        '''

        cell_7 = dbc.Select(id="select",options=[{"label": "Option 1", "value": "1"},
                                                 {"label": "Option 2", "value": "2"},
                                                 {"label": "Disabled option", "value": "3", "disabled": True}],
                            style={'font-size' : '11px', 'line-height':'12px !important', 'padding':'0', 'margin':'0', 'height':'12px !important',
                                     'max-height':'12px !important', 'min-height':'12px !important','display': 'inline-block'})

        ##'display': 'inline-block'}


        dd_div = html.Div(className='custom-dropdown-style-2', children=[dcc.Dropdown(
            options=[
                {'label': 'Option 4', 'value': 4},
                {'label': 'Option 5', 'value': 5},
                {'label': 'Option 6', 'value': 6}
            ],
            value=4,
            className='dropdown-class-2'
        )
        ])

        cell_11 = html.Td(className='td', children=dd_div,style={'margin':'0','padding':'0','border':'1px solid black',
                                                                   'font-size':'8px', 'line-height':'8px','height':'8px', 'min-height':'8px'})
        
        
        heading_row = html.Tr(className='tr', children=[heading_1,heading_2,heading_3,heading_4], style={'width':'100%','margin':'0','padding':'0','border':'1px solid black'})
        table_row = html.Tr(className='tr', children=[cell_1,cell_2,cell_3,cell_4], style={'width':'100%','margin':'0','padding':'0','border':'1px solid black'})
        
        self.simple_table = html.Table(className='table', id=self.page_name + "simple_table", children=[heading_row, table_row],
                                       style={'width':'100%','margin':'0','padding':'0','border':'1px solid black'})


    def generate_html_general_table_from_df(self, df_in, id_in):
        df = df_in
        count_row = df_in.shape[0]  # Gives number of rows
        count_col = df_in.shape[1]  # Gives number of columns

        table_headings = [html.Tr([html.Th(col) for col in df.columns])]
        table_body = []
        for i in range(min(len(df), count_row)):
            table_row = []
            datacell_style = {'background-color': 'lightblue'}
            for col in df.columns:
                append_cell = html.Td(df.iloc[i][col])
                table_row.append(append_cell)
            table_body.append(html.Tr(table_row, style=datacell_style))
        
        generated_table_from_df = html.Table(id=self.page_name + id_in,
           children= table_headings + table_body
        )
        return generated_table_from_df
    
    def generate_html_formatting_table_from_df(self, df_in, id_in):
        df = df_in
        count_row = df_in.shape[0]  # Gives number of rows
        count_col = df_in.shape[1]  # Gives number of columns

        table_headings = [html.Tr([html.Th(col) for col in df.columns])]
        table_body = []
        for i in range(min(len(df), count_row)):
            table_row = []
            datacell_style = {'background-color': 'lightblue'}
            for col in df.columns:
                dataset_id = df.iloc[i]['ds']
                trace_id = df.iloc[i]['tc']
                if col == 'lc':
                    of_what = 'line_color'
                elif col == 'sc':
                    of_what = 'symbol_color'
                elif col == 'fc':
                    of_what = 'fill_color'
                else:
                    of_what = ''
                if col in ( 'lc', 'sc', 'fc'):
                    cdr = self.get_color_dropdown(dataset_id, trace_id, of_what, df.iloc[i][col])
                    append_cell = html.Td(cdr, style=datacell_style)
                elif col in ('ls'):
                    ls = self.get_line_styles(dataset_id, trace_id, df.iloc[i][col])
                    append_cell = html.Td(ls, style=datacell_style)
                elif col in ('ss'):
                    ss = self.get_symbols(dataset_id, trace_id, df.iloc[i][col])
                    append_cell = html.Td(ss, style=datacell_style)
                else:
                    append_cell = html.Td(df.iloc[i][col])
                table_row.append(append_cell)
            table_body.append(html.Tr(table_row, style=datacell_style))
        
        generated_table_from_df = html.Table(id=self.page_name + id_in,
           children= table_headings + table_body
        )
        return generated_table_from_df
    
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
    
    def html_table_to_df(self, html_table_in):

        row_count = len(html_table_in)
        print("table row count >>>>", row_count)
        column_count = len(html_table_in[0]['props']['children'])
        print("column_count >>>>>>", column_count)
        table_columns = []
        for c in range(0,column_count):
            append_this = html_table_in[0]['props']['children'][c]['props']['children']
            table_columns.append(append_this)
        print("table_columns >>>>>", table_columns)
        #column_1 = table_in[0]['props']['children'][0]['props']['children']
        #column_2 = table_in[0]['props']['children'][1]['props']['children']
        #print(table_in[0]['props'])
        #print("column_1, column_2 >>>>>>>>>>>" , column_1, column_2)

        #row_count = len(table_in[1]['props']['children'])
        row_data = []
        table_data_raw = []
        for r in range(1, row_count):
            row_data = []
            for c in range(0,column_count):
                try:
                    print(r,c,html_table_in[r]['props']['children'][c]['props']['children'])
                    append_this = html_table_in[r]['props']['children'][c]['props']['children']
                except:
                    #print(html_table_in[r]['props']['children'][c]['props']['children'])
                    append_this = 'error'
                row_data.append(append_this)
            table_data_raw.append(row_data)
        #print('data_1 >>>>>>>>>' , data_1)
        #self.table_data = data_1
        #print("self.table_data >>>>" , self.table_data)
        print("table_data_raw >>>>" , table_data_raw)
        table_df = pd.DataFrame(data=table_data_raw, columns=table_columns)
        print("table_df >>>>>>>", table_df)
        return table_df
        
    def Layout(self):
        #self.table_div =  html.Div(id= self.page_name+'table_div', children=[self.generated_table], style={'width': '100%', 'height': '200px','border': '2px solid black'})

        #self.table_div =  html.Div(id= self.page_name+'table_div', children=[self.simple_table], style={'width': '100%', 'height': '200px','border': '2px solid black'})
        #self.table_div =  html.Div(id= self.page_name+'table_div', children=[self.TableFormat], style={'width': '100%', 'height': '200px','border': '2px solid black'})

        #self.table_div =  html.Div(id= self.page_name+'table_div', children=[self.dropdown_test], style={'width': '100%', 'height': '200px','border': '2px solid black'})
        self.table_div =  html.Div(id= self.page_name+'table_div', children=[self.formatting_table],
                                   style={'width': '100%', 'height': '200px'})


        self.values_table_div =  html.Div(id= self.page_name+'values_div', children=[self.values_table],
                                   style={'width': '100%', 'height': '600px'})

      
        listen2this = html.Div(children=
            [html.Div(id=self.page_name+'content',children=[self.table_div],
                      style = {'position':'absolute', 'top':'0px', 'width':'300px',  'overflow': 'auto'}),
            html.Div(id=self.page_name+'content',children=[self.values_table_div],
                      style = {'position':'absolute', 'top':'0px','left': '400px', 'width':'300px',  'overflow': 'auto'}),
            html.Div(id=self.page_name+'response',children="table content", style = {'position':'absolute', 'top':'200px', 'width':'300px'}),
            html.Div(id=self.page_name+'button-output-div',children="button message", style={'position':'absolute', 'top':'225px', 'width':'300px'}),
            html.Button('Submit', id=self.page_name+'save_plot_button', n_clicks=0, style={'position':'absolute', 'top':'250px', 'width':'100px'})]
        )
        
        ## https://www.dash-extensions.com/components/event_listener
        
        self.layout = html.Div([
            dcc.Location(id=self.page_name+'url',refresh=True),
            dcc.Store(id= self.page_name + 'screen_size_store', storage_type='local'),
            EventListener(
            listen2this,
            events=[self.event], logging=True, id=self.page_name +"el"
            ),
            html.Div(id=self.page_name + "log", style={'position':'absolute', 'top':'300px', 'width':'100px'})
        ])
    

    def page_refresh_callback(self):
        @callback(Output(self.page_name+'response','children'),
                          Input(self.page_name +'url', 'href'),
                          State(self.page_name+'generated_table', 'children'))
        def get_table_children(url_in,table_div_in):
            print("styling table callback triggered")
            print(table_div_in)

    def ListenerCallback(self):

        @callback(Output(self.page_name + "log", "children"),
                  Output(self.page_name + "values_div", "children"),
                  Input(self.page_name +"el", "n_events"),
                  State(self.page_name +"el", "event"))
        def click_event(n_events, e):
            #print("srcElement.id>>>>", e['srcElement.id'])
            #print("previous_clickevent>>>>>", self.previous_clickevent)
            #if e['srcElement.id'] == self.previous_clickevent:
            if e is None:
                raise PreventUpdate()
            print('e >>>>>>>>', e)
            return_string = ",".join(f"{prop} is '{e[prop]}' " for prop in self.event["props"]) + f" (number of clicks is {n_events})"
            field_value = e['srcElement.value']
            field_value_json = json.loads(field_value)
            print("field_value_json >>>>>>", field_value_json)
            limit_id_value = field_value_json['limit_id']
            trace_id_value = field_value_json['trace_id']
            variable_value = field_value_json['variable']
            value_value = field_value_json['value']
            print("limit_id_value >>> " , limit_id_value)
            print("trace_id_value >>> " , trace_id_value)
            print("variable_value >>> " , variable_value)
            print("value_value >>> " , value_value)
            print(self.data_df_melt)
            ## mask = df['ID'].eq('AA') & df['Date'].isin(['Q2.22', 'Q1.22'])
            ## df.loc[mask, ['stat', 'en']] = ['', 0]

            mask = (self.data_df_melt['limit_id'].astype(str) == limit_id_value) & (self.data_df_melt['trace_id'].astype(str) == trace_id_value) \
                        & (self.data_df_melt['variable'] == variable_value)
            print(mask)

            # limit_id  trace_id      variable   value
            #self.data_df_melt['value'] = np.where((self.data_df_melt['limit_id'] == limit_id_value) &
            #                                      (self.data_df_melt['trace_id'] == trace_id_value) &
            #                                      (self.data_df_melt['variable'] == variable_value)
            #                                      , value_value, self.data_df_melt['value'])

            #self.data_df_melt[mask,['value']] = [value_value]

            self.data_df_melt['value'].mask((self.data_df_melt['limit_id'].astype(str) == limit_id_value) &
                                                 (self.data_df_melt['trace_id'].astype(str) == trace_id_value) &
                                                 (self.data_df_melt['variable'] == variable_value), value_value, inplace=True)

            self.values_table = self.generate_html_general_table_from_df(self.data_df_melt, 'values_table')
            
            return [return_string, self.values_table]
    
    def button_callback(self):
        @callback(
                    Output(self.page_name+'button-output-div', 'children'),
                    Input(self.page_name+"save_plot_button", 'n_clicks'),
                    ##State(self.page_name+'generated_table', 'children')
                    State(self.page_name+'simple_table', 'children')
                )
        def displayClick1_1(btn1,table_in):
            msg = "None of the buttons have been clicked yet"
            prop_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
            if page_name+'save_plot_button' == prop_id:
                msg = "save_plot_button pressed"
                self.table_df = self.html_table_to_df(table_in)
                '''
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
                '''
            else:
                msg = "No Button Pressed"
            return html.Div(msg)


page_name = 'style_simple'
dbl = StylingTable(page_name)
dbl.Layout()
layout = dbl.layout
#dbl.button_callback()
dbl.ListenerCallback()

'''
@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(relative_pathname):
    dbl.Layout()
    layout_return = dbl.layout
    return layout_return
'''
