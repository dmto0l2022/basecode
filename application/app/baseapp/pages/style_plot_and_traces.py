import os
import requests
from urllib.parse import urlparse, parse_qs

cwd = os.getcwd()

page_name = 'style_plot_and_traces'
baseapp_prefix = '/login/baseapp'

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

# import formlibrary as fl

#from app.baseapp.libraries import formlibrary as fl

from app.baseapp.dashboard_libraries import all_data_tables as adt
#dashdataandtables = adt.DashDataAndTables()

from app.baseapp.dashboard_libraries import scaling as sc
#sf = sc.get_scale_factor('ub')
#sf

####################################
from app.baseapp.dashboard_libraries import formattingtable as ft
from app.baseapp.dashboard_libraries import createlegend as cl
from app.baseapp.dashboard_libraries import updatelegend as ul
from app.baseapp.dashboard_libraries import getstyleandlegend as gsal
from app.baseapp.dashboard_libraries import creategraph as cg
from app.baseapp.dashboard_libraries import updategraph as ug

####################################

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

###########
from app.baseapp.dashboard_libraries import get_limit_data as gld

##############################################
def get_plotid():
    plotid_datetime = datetime.now()
    plotid = plotid_datetime.strftime('%Y%m%d%H%M%S%f%z')
    return plotid

############
default_limits = [45]

####################################

# colors
#palette = cycle(px.colors.qualitative.Bold)
#palette = cycle(['black', 'grey', 'red', 'blue'])

palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
palette = cycle(palette_list)

#####################################

dash.register_page(__name__, path='/style_plot_and_traces')

## create plot series

def create_layout(limits_in):

    all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits()
    
    traces = all_trace_list_df[all_trace_list_df['limit_id'].isin(limits_in)].copy()
    
    styling_data_table = ft.CreateFormatTable(traces)
    
    legend_fig = cl.CreateLegendFig(limits_in,all_trace_list_df)
    
    legend_graph = dcc.Graph(figure=legend_fig,
                             id='legend_out_id',
                             style={'width': '100%', 'height': '100%'})
    
    style_and_legend_column = gsal.GetStyleAndLegendColumn(styling_data_table,legend_graph)
    
    
    ## all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict
    
    graph_fig = cg.CreateGraph(limits_in, all_trace_list_df, all_limit_data_df)
    
    graph_out = dcc.Graph(figure=graph_fig,
                                  id='graph_out_id',
                                  config=dict(responsive=True),
                                  className='GRAPH'
                                  #style={'width': '100%', 'height': '100%'}
                                  )
    
    chart_in = graph_out
    
    column_chart = GetChart(chart_in)
    
    two_columns =  html.Div(className="row g-0 ALL_ROW NOPADDING",
                           children=[
                                    column_chart,
                                    style_and_legend_column,
                                    ],)
    
    #layout_out = html.Div(
    #                   [two_columns],
    #                   className="container-fluid DASHBOARD_CONTAINER_STYLE",
    #                  )
    layout_out = two_columns
    return layout_out


#layout = style_plot_and_traces_form_form

row_of_buttons = html.Div([
        html.Button('Save', id=page_name+'btn-nclicks-1_1', n_clicks=0),
        html.Button('Revert', id=page_name+'btn-nclicks-2_1', n_clicks=0),
        html.Button('Cancel', id=page_name+'btn-nclicks-3_1', n_clicks=0),
        html.Div(id=page_name+'container-button-output')
    ])
  

layout = html.Div([
    dcc.Location(id='url',refresh=True),
    html.Div(id='layout-div'),
    html.Div(id='content',children=create_layout(default_limits),className="PAGE_GRAPH_CONTENT"),
    html.Div(id=page_name+"rowofbuttons", children=[row_of_buttons], className="BUTTONS_ON_PAGE_LEFT"),
    html.Div(id=page_name+'button_presses',children='button here',className="DIV_ON_PAGE_RIGHT")
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

@callback(
    Output(page_name+'container-button-output', 'children'),
    Input(page_name+'btn-nclicks-1_1', 'n_clicks'),
    Input(page_name+'btn-nclicks-2_1', 'n_clicks'),
    Input(page_name+'btn-nclicks-3_1', 'n_clicks')
)
def displayClick1_1(btn1, btn2, btn3):
    msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if page_name+"btn-nclicks-1_1" == prop_id:
        msg = "Button 1 was most recently clicked"
    elif page_name+"btn-nclicks-2_1" == prop_id:
        msg = "Button 2 was most recently clicked"
    elif page_name+"btn-nclicks-3_1" == prop_id:
        msg = "Button 3 was most recently clicked"
    return html.Div(msg)


@callback(Output('content', 'children'), [Input('url', 'pathname'),Input('url', 'search') ,Input('url', 'href')])
def display_page(pathname,search,href):
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
    
    print('spat : list_of_limits >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', list_of_limits_int)
    #list_of_limits = [33]
    layout_return = create_layout(list_of_limits_int)
    return layout_return

@callback(
    [Output('graph_out_id','figure'),Output('legend_out_id','figure'),],
    [Input('format_table_id', 'data')],
    [State('format_table_id', 'data')])
def update_output(table_data, table_data_in):
    print('spat : table_data_in >>>>>>>>>>',table_data_in)
    fig_out = ug.UpdateGraph(table_data_in)
    legend_out = ul.UpdateLegendFig(table_data_in)
    
    return fig_out, legend_out

