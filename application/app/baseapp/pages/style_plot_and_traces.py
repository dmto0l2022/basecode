import os
import requests
from urllib.parse import urlparse, parse_qs

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
#from app.baseapp.dashboard_libraries import creategraph as cg
#from app.baseapp.dashboard_libraries import updategraph as ug
#from app.baseapp.dashboard_libraries import data_graph as dg

####################################

dmtool_userid = '16384'


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


listoflimits = []

dash.register_page(__name__, path='/style_plot_and_traces')

## create plot series

class DashBoardLayout():
    def __init__(self,pagename_in, dmtools_userid_in,  listoflimits_in):
        self.button_styling_1 = {'font-size': '12px',
                          'width': '70px',
                          'display': 'inline-block', 
                          'margin-bottom': '1px',
                          'margin-right': '0px',
                          'margin-top': '1px',
                          'height':'19px',
                          'verticalAlign': 'center'}
        self.new_button =  html.Button("New", id= pagename_in + "new_button_id", style=button_styling_1)
        self.save_button =  html.Button("Save", id= pagename_in + "save_button_id", style=button_styling_1)
        self.cancel_button =  html.Button("Cancel",  id=pagename_in + "cancel_button_id", style=button_styling_1)
        self.home_button =  html.Button("Home",  id=pagename_in + "home_button_id", style=button_styling_1)
        self.row_of_buttons = html.Div(id= pagename_in + "page_buttons", children=[new_button,save_button,cancel_button,home_button], className="PAGE_FOOTER_BUTTONS")
          
        self.debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                              html.Div(id=pagename_in+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                              html.Div(id=pagename_in+'button-output-div', children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                              className="PAGE_DEBUG_CONTENT")
         
        self.dmtools_userid = dmtools_userid_in
        self.listoflimits = listoflimits_in
        self.limits_traces_df = pd.DataFrame()
        self.limits_data_df = pd.DataFrame()
        self.plot_series_df = pd.DataFrame()
        self.GraphFig = go.Figure()
        self.GraphClass = dg.DataGraph()
        self.GraphOut = dcc.Graph()
        self.layout = {}
        self.SetLayout()
        self.UpdateData()
        self.CreateGraph()

    def CreateLayout(self):
    
        self.limit_list_df, self.trace_list_df, self.limits_data_df, self.limits_list_dict = gld.GetListOfLimits(self.dmtools_userid, self.listoflimits)
        
        #traces = all_trace_list_df[all_trace_list_df['limit_id'].isin(limits_in)].copy()
        traces = trace_list_df
        
        print("traces >>>>>>", traces)
        
        styling_data_table = ft.CreateFormatTable(page_name,traces)
        
        legend_fig = cl.CreateLegendFig(limits_in,traces)
        
        legend_graph = dcc.Graph(figure=legend_fig,
                                 id= page_name + 'legend_out_id',
                                 style={'width': '100%', 'height': '100%'})
        
        #style_and_legend_column = gsal.GetStyleAndLegendColumn(styling_data_table,legend_graph)
        
        
        ## all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict
    
        self.GraphClass = dg.DataGraph(dmtool_userid, limits_in)
        
        self.GraphOut = dcc.Graph(figure=self.GraphClass.GraphFig,
                                  id=page_name + 'graph_out_id',
                                  config=dict(responsive=True),
                                  mathjax=True,
                                  #className='GRAPH'
                                  style={'width': '100%', 'height': '100%'}
                                      )
        
        ### this is to show how the page is laid out and structured
        
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
        
        ##layout_out = skeleton_container
    
        ######
        
        first_row_second_column =  dbc.Row(
                [
                    dbc.Col(children=[styling_data_table], className="col-sm-12 col-md-6 col-lg-6 PAGE_TABLE_CONTENT_TOP_RIGHT"),
                ], style={'width': '100%', 'height': '50%','border': '2px solid black'})
    
        second_row_second_column = dbc.Row(
                [
                    dbc.Col(children=[legend_graph], className="col-sm-12 col-md-6 col-lg-6 PAGE_TABLE_CONTENT_BOTTOM_RIGHT")
                ] , style={'width': '100%', 'height': '50%', 'border': '2px solid black'})
            
        dashboard_container = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(children=[self.GraphOut], className="col-sm-12 col-md-6 col-lg-6 PAGE_GRAPH_CONTENT", style={'border': '2px solid black'}),
                    dbc.Col(children=[first_row_second_column,second_row_second_column] , className="col-sm-12 col-md-6 col-lg-6")
                ], style={'height': '100%'} ##className = "CONTENT_ROW"
            ),
        ],  style={'height': '100%'} ##className="container-fluid DASHBOARD_CONTAINER_STYLE"
        )    
        
        #self.layout = dashboard_container
        
        
        #layout = style_plot_and_traces_form_form
        
        
    def SetLayout(self):
        self.layout = html.Div([
            dcc.Location(id=page_name+'url',refresh=True),
            ##html.Div(id=page_name+'layout-div'),
            html.Div(id=page_name+'content',children=self.CreateLayout(),className="DASHBOARD_CONTAINER_STYLE"),
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
    

      
    def UpdateData(self):
        self.limits_list_df, self.limits_traces_df, self.limits_data_df, self.limit_list_dict = gld.GetListOfLimits(self.dmtools_userid, self.listoflimits)

    def CreateGraph(self):
      
        self.GraphFig = go.Figure()
        
        self.GraphFig.update_layout(autosize=True)
        
        for index, row in self.limits_list_df.iterrows():
          
            trace_data = self.limits_data_df[(self.limits_data_df['limit_id']==row['limit_id'])
                                          & (self.limits_data_df['trace_id']==row['trace_id'])]
            
            trace2add = trace_data
            
            #trace_name = str(row['id']) + str(row['series'])
            trace_name = str(row['trace_name'])
            
            x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
            y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
            
            self.GraphFig.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'], ## scaled needs to be updated
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
            
            self.GraphFig.update(layout_showlegend=False)
            
            self.GraphFig.update_xaxes(
              title_text=x_title_text,
              type="log"
              #type="linear"
            )
            self.GraphFig.update_yaxes(
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
  
  
    def UpdateGraph(self, plotseries_table_in):
        #result_ids = [1,262]
        print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
        self.plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
        
        #result_ids_plot = plot_series_df['limit_id'].unique().tolist()
        
        limit_list_df, trace_list_df, limit_data_df, limit_list_dict = gld.GetListOfLimits(self.dmtools_userid_in, self.listoflimits)
        
        #plot_series_df = pd.DataFrame(plotseries_table_in)
        
        x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
        y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
        
        #plotseries_default, df_experiment_plot = CreatePlotSeries(result_ids_plot)
        #plotseries_default_plot = CreatePlotSeriesDefault(df_experiment_all_plot)
        
        # Create figure
        self.GraphFig = go.Figure()
        self.GraphFig.update_xaxes(
              title_text=x_title_text,
              type="log"
              #type="linear"
          )
        
        self.GraphFig.update_yaxes(
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
            
            self.GraphFig.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'],
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
            
            self.GraphFig.update(layout_showlegend=False)


dbl = DashBoardLayout(page_name, dmtool_userid,  listoflimits)

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


@callback(Output(page_name+'content', 'children'), [Input(page_name+'url', 'pathname'),Input(page_name+'url', 'search') ,Input(page_name+'url', 'href')])
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
    dbl = DashBoardLayout(pagename, dmtool_userid,  list_of_limits_int)
    layout_return = dbl.layout
    return layout_return

@callback(
    [Output(page_name+'graph_out_id','figure'),Output(page_name+'legend_out_id','figure'),],
    [Input(page_name+'format_table_id', 'data')],
    [State(page_name+'format_table_id', 'data')])
def update_output(table_data, table_data_in):
    print('spat : table_data_in >>>>>>>>>>',table_data_in)
    dbl.UpdateGraph(dmtool_userid,table_data_in)
    legend_out = ul.UpdateLegendFig(dmtool_userid, table_data_in)
    return dbl.GraphFig, legend_out

