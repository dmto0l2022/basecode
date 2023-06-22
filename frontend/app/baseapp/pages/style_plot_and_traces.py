import os
import requests
from urllib.parse import urlparse, parse_qs

cwd = os.getcwd()

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
                className="col col-lg-6"
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
palette = cycle(px.colors.qualitative.Bold)
#palette = cycle(['black', 'grey', 'red', 'blue'])

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
    
    rowofbuttons = html.Div([
        html.Button('Save', id='btn-nclicks-1', n_clicks=0),
        html.Button('Revert', id='btn-nclicks-2', n_clicks=0),
        html.Button('Cancel', id='btn-nclicks-3', n_clicks=0),
        html.Div(id='container-button-timestamp')
    ])

    next_button =  html.Div(dbc.Button("Next",  id="style_plot_and_traces_next_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")
    
    cancel_button =  html.Div(dbc.Button("Cancel",  id="style_plot_and_traces_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")
   
    
    ## all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict
    
    graph_fig = cg.CreateGraph(limits_in, all_trace_list_df, all_limit_data_df)
    
    graph_out = dcc.Graph(figure=graph_fig,
                                  id='graph_out_id',
                                  config=dict(responsive=True),
                                  className='h-100'
                                  #style={'width': '100%', 'height': '100%'}
                                  )
    
    chart_in = graph_out
    
    column_chart = GetChart(chart_in)
    
    twocolumns =  html.Div(className="row g-0 ALL_ROW NOPADDING",
                           children=[
                                    default_column_chart,
                                    default_styleandlegendcolumn,
                                    rowofbuttons,
                                    next_button,
                               cancel_button
                                    ],)
    
    layout_out = html.Div([twocolumns],
                       className="container-fluid DASHBOARD_CONTAINER_STYLE",
                      )
    return layout_out


#layout = style_plot_and_traces_form_form

layout = create_layout(default_limits)

'''
@app.callback(Output('content', 'children'),
              [Input('url', 'href')])
def _content(href: str):
    f = furl(href)
    param1= f.args['param1']
    param2= f.args['param2']

    return html.H1(children=param1: {param1} param2: {param2}' )
'''

'''
## woking

layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='layout-div'),
    html.Div(id='content')
])

@callback(Output('content', 'children'), [Input('url', 'pathname'),Input('url', 'search') ,Input('url', 'href')])
def display_page(pathname,search,href):
    original_search_string = search
    just_list = original_search_string.split('=')
    o = urlparse(href)
    just_list = o.query.split('=')[1]
    list_of_limits = just_list.split('|')
    return html.Div([
        dcc.Input(id='input', value='hello world'),
        html.Div(children=pathname, id='pathname'),
        html.Div(children=search, id='search'),
        html.Div(children=href, id='href'),
        html.Div(children=o.query, id='params'),
        html.Div(children=list_of_limits, id='lol'),
    ])
'''

@callback(
    [Output("graph_out_id","figure"),Output("legend_out_id","figure"),],
    [Input('format_table_id', 'data')],
    [State("format_table_id", "data")])
def update_output(table_data, table_data_in):
    fig_out = ug.UpdateGraph(table_data_in)
    legend_out = ul.UpdateLegendFig(table_data_in)
    
    return fig_out, legend_out

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("style_plot_and_traces_next_button_id", "n_clicks"),
    Input("style_plot_and_traces_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "style_plot_and_traces_next_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.show_plot']['path']
        return href_return
    elif "style_plot_and_traces_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return


'''
#### style plot and traces
    
    style_plot_and_traces_form_title = html.Div(html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE"))
    
    style_plot_and_traces_form_content  = dbc.Row(
        [
            dbc.Col(
                [
                    html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE")
                ],
                width=6,
            )
        ],
        className="g-3",
    )
style_plot_and_traces_form_form = html.Div(
        #[newplot_title,newplot_input3],
        [dcc.Location(id="url", refresh=True),
         style_plot_and_traces_form_title,
         style_plot_and_traces_form_content,
         next_button, cancel_button],
        className = "NOPADDING_CONTENT CENTRE_FORM"
    )
'''
