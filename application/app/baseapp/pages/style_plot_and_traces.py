import os
import requests
from urllib.parse import urlparse, parse_qs
import pandas as pd
import itertools

cwd = os.getcwd()

page_name = 'style_plot_and_traces'
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

import redis

r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
dmtool_userid = 16384 ## testing

# import formlibrary as fl

#from app.baseapp.libraries import formlibrary as fl

#from app.baseapp.dashboard_libraries import all_data_tables as adt
#dashdataandtables = adt.DashDataAndTables()

from app.baseapp.dashboard_libraries import scaling as sc
#sf = sc.get_scale_factor('ub')
#sf

####################################
#from app.baseapp.dashboard_libraries import formattingtable as ft
#from app.baseapp.dashboard_libraries import createlegend as cl
#from app.baseapp.dashboard_libraries import updatelegend as ul
#from app.baseapp.dashboard_libraries import getstyleandlegend as gsal
#from app.baseapp.dashboard_libraries import creategraph as cg
#from app.baseapp.dashboard_libraries import updategraph as ug
#from app.baseapp.dashboard_libraries import data_graph as dg

####################################

dmtool_userid = '16384'

'''
def GetChart(chart_in):

    chartdiv = html.Div([chart_in], className="CHART_DIV NOPADDING")

    chart_col =  html.Div(children=[chartdiv],className="col col-lg-12 NOPADDING")

    chart_row = html.Div([chart_col],
                    className="row CHART_ROW NOPADDING")

    column_chart_out = html.Div(
                [chart_row]  ,
                className="col col-lg-6 PAGE_GRAPH_COLUMN_CONTENT_LEFT",
            )
    return column_chart_out
'''
###########

from app.baseapp.dashboard_libraries import get_limit_data as gld

##############################################
'''
def get_plotid():
    plotid_datetime = datetime.now()
    plotid = plotid_datetime.strftime('%Y%m%d%H%M%S%f%z')
    return plotid
'''

############
## default_limits = [45]

####################################

# colors
#palette = cycle(px.colors.qualitative.Bold)
#palette = cycle(['black', 'grey', 'red', 'blue'])

palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
palette = cycle(palette_list)

#####################################


listoflimits = []

dash.register_page(__name__, path='/style_plot_and_traces')

## create plot series

class DashBoardLayout():
    def __init__(self,pagename_in, dmtool_userid_in,  listoflimits_in):
        self.page_name = pagename_in
        self.data_table_id =  self.page_name + "data_table_id"
        #self.table_meta_data_data = table_meta_data_data_in
        self.format_data_table_row_height = '12px'
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
        
        self.format_table_css = [{"selector": ".Select-menu-outer", "rule": "display: block !important"},
                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of header
                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of body rows
                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},  # set height of header
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    {"selector": ".dash-cell tr th td", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"}, 
                    {"selector": ".Select-option", "rule": "min-height: " + self.format_data_table_row_height + "; height: " + self.format_data_table_row_height + ";line-height: " + self.format_data_table_row_height + ";max-height: " + self.format_data_table_row_height + ";"},
                    ]

        
        
        self.button_styling_1 = {'font-size': '12px',
                          'width': '70px',
                          'display': 'inline-block', 
                          'margin-bottom': '1px',
                          'margin-right': '0px',
                          'margin-top': '1px',
                          'height':'19px',
                          'verticalAlign': 'center'}
        
        self.new_button =  html.Button("New", id= pagename_in + "new_button_id", style=self.button_styling_1)
        self.save_button =  html.Button("Save", id= pagename_in + "save_button_id", style=self.button_styling_1)
        self.cancel_button =  html.Button("Cancel",  id=pagename_in + "cancel_button_id", style=self.button_styling_1)
        self.home_button =  html.Button("Home",  id=pagename_in + "home_button_id", style=self.button_styling_1)
        self.row_of_buttons = html.Div(id= pagename_in + "page_buttons", children=[self.new_button,self.save_button,self.cancel_button,self.home_button], className="PAGE_FOOTER_BUTTONS")
          
        self.debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                              html.Div(id=pagename_in+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                              html.Div(id=pagename_in+'button-output-div', children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                              className="PAGE_DEBUG_CONTENT")
         
        self.dmtool_userid = dmtool_userid_in
        self.listoflimits = listoflimits_in
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
        self.UpdateData([1])
        self.CreateChart()
        self.CreateFormat()
        self.CreateLegend()

    def UpdateData(self, listoflimits_in):
        self.limits_list_df, self.limits_traces_df, self.limits_data_df, self.limits_list_dict = gld.GetListOfLimits(self.dmtool_userid, listoflimits_in)

    def CreateLayout(self):
    
        #self.limit_list_df, self.trace_list_df, self.limits_data_df, self.limits_list_dict = gld.GetListOfLimits(self.dmtools_userid, self.listoflimits)
        
        #traces = all_trace_list_df[all_trace_list_df['limit_id'].isin(limits_in)].copy()
        #traces = self.trace_list_df
        
        #print("traces >>>>>>", traces)
        
        #styling_data_table = self.FormatDataTable
        
        #legend_fig = FigLegend
        
        legend_graph = dcc.Graph(figure=self.FigLegend,
                                 id= self.page_name + 'legend_id',
                                 style={'width': '100%', 'height': '100%'})
        
        #style_and_legend_column = gsal.GetStyleAndLegendColumn(styling_data_table,legend_graph)
        
        
        ## all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict
    
        #self.GraphClass = dg.DataGraph(dmtool_userid, limits_in)
        
        self.GraphChart = dcc.Graph(figure=self.FigChart,
                                  id=self.page_name + 'chart_id',
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
        
        first_row_second_column =  dbc.Row(
                [
                    dbc.Col(id= self.page_name+'table_div', children=[self.TableFormat], className="col-sm-12 col-md-6 col-lg-6 PAGE_TABLE_CONTENT_TOP_RIGHT"),
                ], style={'width': '100%', 'height': '50%','border': '2px solid black'})
    
        second_row_second_column = dbc.Row(
                [
                    dbc.Col(id= self.page_name+'legend_div', children=[legend_graph], className="col-sm-12 col-md-6 col-lg-6 PAGE_TABLE_CONTENT_BOTTOM_RIGHT")
                ] , style={'width': '100%', 'height': '50%', 'border': '2px solid black'})
            
        dashboard_container = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(id= self.page_name+'graph_div', children=[self.GraphChart], className="col-sm-12 col-md-6 col-lg-6 PAGE_GRAPH_CONTENT", style={'border': '2px solid black'}),
                    dbc.Col(children=[first_row_second_column,second_row_second_column] , className="col-sm-12 col-md-6 col-lg-6")
                ], style={'height': '100%'} ##className = "CONTENT_ROW"
            ),
        ],  style={'height': '100%'} ##className="container-fluid DASHBOARD_CONTAINER_STYLE"
        )    
        
        #self.layout = dashboard_container
        
        
        #layout = style_plot_and_traces_form_form
        
        self.layout = html.Div([
            dcc.Location(id=page_name+'url',refresh=True),
            ##html.Div(id=page_name+'layout-div'),
            html.Div(id=page_name+'content',children=dashboard_container,className="DASHBOARD_CONTAINER_STYLE"),
            self.row_of_buttons,
            self.debug_output
        ],className="PAGE_CONTENT")

        
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
    
    ################
    
    def CreateFormat(self):
    
        #limits_traces_copy = limits_traces_in.copy()
        print("format table : limits_traces_df.columns >> " , self.limits_traces_df.columns)
        palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
        cycle_colors = itertools.cycle(palette_list)
    
        #colored_limits = pd.DataFrame(data=None, columns=limits_traces_in.columns, index=limits_traces_in.index)
        colored_limits_list =[]
        for index, row in self.limits_traces_df.iterrows():
            #print(row['c1'], row['c2'])
            copy_row = row.copy()
            color = next(cycle_colors)
            copy_row['line_color'] = color
            copy_row['symbol_color'] = color
            copy_row['fill_color'] = color
            append_this = [copy_row['id'], copy_row['limit_id'], copy_row['data_label'],
                           copy_row['trace_id'],copy_row['trace_name'],
                           copy_row['line_color'],copy_row['symbol_color'],copy_row['fill_color'],
                           copy_row['line'],copy_row['symbol']]
            print(append_this)
            colored_limits_list.append(append_this)
    
        #Index(['id', 'limit_id', 'data_label', 'trace_id', 'trace_name', 'line_color',
        #   'symbol_color', 'fill_color', 'line', 'symbol'],
    
        colored_limits = pd.DataFrame(data=colored_limits_list, columns=self.limits_traces_df.columns, index=self.limits_traces_df.index)
        
      
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
        
        rowloop = 0
    
        for index, row in self.limits_traces_df.iterrows():
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

        self.LegendGraph = dcc.Graph(figure=self.FigLegend,
                                 id= self.page_name + 'legend_id',
                                 style={'width': '100%', 'height': '100%'})

    def UpdateLegendFig(self, plotseries_table_in):
        #result_ids = [1,262]
        
        print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
        self.plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
        
        result_ids_plot = self.plot_series_df['limit_id'].unique().tolist()
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
    
        for index, row in self.plot_series_df.iterrows():
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

    
    def CreateChart(self):
      
        self.FigChart = go.Figure()
        
        self.FigChart.update_layout(autosize=True)
        
        for index, row in self.limits_data_df.iterrows():
          
            trace_data = self.limits_data_df[(self.limits_data_df['id']==row['id'])
                                          & (self.limits_data_df['trace_id']==row['trace_id'])]
            
            trace2add = trace_data
            
            #trace_name = str(row['id']) + str(row['series'])
            trace_name = str(row['trace_name'])
            
            x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
            y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
            
            self.FigChart.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'], ## scaled needs to be updated
                              mode='lines+markers', # 'lines' or 'markers'
                              line=dict(width=4,dash=row['line'],color=row['line_color']),
                              #showscale=False,
                              fill='toself',
                              fillcolor = row['fill_color'],
                              text=row['trace_name'],
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
            #fig3.add_trace(go.Scatter(x=trace2add['x'], y=trace2add['scaled_y'],
            #                   mode='markers', # 'lines' or 'markers'
            #                    marker_symbol=row['symbol'],
            #                         marker=dict(
            #                        size=10,
            #                        color=row['color'],#set color equal to a variable
            #                        #colorscale='Viridis', # one of plotly colorscales
            #                        showscale=False,
            #                    ),
            #                    name=str(row['id'])))
  
        self.GraphChart = dcc.Graph(figure=self.FigChart,
                                  id=self.page_name + 'chart_id',
                                  config=dict(responsive=True),
                                  mathjax=True,
                                  #className='GRAPH'
                                  style={'width': '100%', 'height': '100%'}
                                      )
    
    def UpdateChart(self, plotseries_table_in):
        #result_ids = [1,262]
        print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
        self.plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
        
        #result_ids_plot = plot_series_df['limit_id'].unique().tolist()
        
        limit_list_df, trace_list_df, limit_data_df, limit_list_dict = gld.GetListOfLimits(self.dmtool_userid, self.listoflimits)
        
        #plot_series_df = pd.DataFrame(plotseries_table_in)
        
        x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
        y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
        
        #plotseries_default, df_experiment_plot = CreatePlotSeries(result_ids_plot)
        #plotseries_default_plot = CreatePlotSeriesDefault(df_experiment_all_plot)
        
        # Create figure
        self.ChartFig = go.Figure()
        self.ChartFig.update_xaxes(
              title_text=x_title_text,
              type="log"
              #type="linear"
          )
        
        self.ChartFig.update_yaxes(
              title_text=y_title_text,
              #type="log"
              type="linear"
          )

        for index, row in self.plot_series_df.iterrows():
            trace_data = self.limits_data_df[(self.limits_data_df['limit_id']==row['limit_id'])
                                          & (self.limits_data_df['trace_id']==row['trace_id'])]
            
            # print('trace_data>>>>', trace_data)
            
            trace2add = trace_data.sort_index()
            
            trace_name = str(row['trace_name'])
            
            self.ChartFig.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'],
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
            
            self.ChartFig.update(layout_showlegend=False)


dbl = DashBoardLayout(page_name, dmtool_userid,  listoflimits)
dbl.CreateLayout()
layout = dbl.layout

@callback(
    Output(page_name+'button-output-div', 'children'),
    Input(page_name+'new_button_id', 'n_clicks'),
    Input(page_name+'save_button_id', 'n_clicks'),
    Input(page_name+'cancel_button_id', 'n_clicks'),
    Input(page_name+'home_button_id', 'n_clicks'),
)
def displayClick1_1(btn1, btn2, btn3, btn4):
    msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if page_name+'new_button_id' == prop_id:
        msg = "Button 1 was most recently clicked"
    elif page_name+'save_button_id' == prop_id:
        msg = "Button 2 was most recently clicked"
    elif page_name+'cancel_button_id' == prop_id:
        msg = "Button 3 was most recently clicked"
    elif page_name+'home_button_id' == prop_id:
        msg = "Button 4 was most recently clicked"
    else:
        msg = "No Button Pressed"
    return html.Div(msg)


@callback(Output(page_name+'chart_div','children'),
          Output(page_name+'table_div', 'children'),
          Output(page_name+'legend_div','children'),
          [Input(page_name+'url', 'pathname'),Input(page_name+'url', 'search') ,Input(page_name+'url', 'href')])
def display_page(pathname,search,href):
    print('spat : 3 chart call vack triggered')
    original_search_string = search
    just_list = original_search_string.split('=')
    o = urlparse(href)
    print('query>>>>' ,o.query)
    
    try:
        just_list = o.query.split('=')[1]
        print("just_list >>>>>>",just_list)
        list_of_limits_str = just_list.split('|')
        list_of_limits_int = []
        for l in list_of_limits_str:
            list_of_limits_int.append(int(l))
        
    except:
        list_of_limits_int = [45]
    
    print('spat callback: list_of_limits >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', list_of_limits_int)
    #list_of_limits = [33]
    #dbl = DashBoardLayout(page_name, dmtool_userid,  list_of_limits_int)
    dbl.UpdateData(list_of_limits_int)
    dbl.CreateChart()
    dbl.CreateLegend()
    dbl.CreateFormat()
    return dbl.DataGraph, dbl.FormatDataTable, dbl.LegendGraph

@callback(
    [Output(page_name+'chart_id','figure'),Output(page_name+'legend_id','figure'),],
    [Input(page_name+'format_table_id', 'data')],
    [State(page_name+'format_table_id', 'data')])
def update_output(table_data, table_data_in):
    #print('spat : table_data_in >>>>>>>>>>',table_data_in)
    print('spat : update data call back triggered')
    dbl.UpdateChart(table_data_in)
    dbl.UpdateLegendFig(table_data_in)
    return dbl.GraphFig, dbl.LegendFig

