import os
import requests

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
dashdataandtables = adt.DashDataAndTables()

from app.baseapp.dashboard_libraries import scaling as sc
#sf = sc.get_scale_factor('ub')
#sf

####################################


def get_plotid():
    plotid_datetime = datetime.now()
    plotid = plotid_datetime.strftime('%Y%m%d%H%M%S%f%z')
    return plotid

####################################

# colors
palette = cycle(px.colors.qualitative.Bold)
#palette = cycle(['black', 'grey', 'red', 'blue'])

#####################################

## create plot series

def CreatePlotSeries(limits_in):
    plotseries_df = dashdataandtables.limits_traces_df[dashdataandtables.limits_traces_df['limit_id'].isin(limits_in)].copy()
    plotseries_df = plotseries_df.drop_duplicates()
    plotseries_df = plotseries_df.reset_index(drop=True)
    
    return plotseries_df

default_results = [1000]
plotseries = CreatePlotSeries(default_results)
#plotseries

from app.baseapp.dashboard_libraries import formattingtable as ft

default_limit = [1000]
default_traces = dashdataandtables.limits_traces_df[dashdataandtables.limits_traces_df['limit_id']\
                                                    .isin(default_limit)].copy()

default_styledatatable = ft.CreateFormatTable(default_traces)

plotseries_default = CreatePlotSeries([1000])
plotseries_default.head(5)

from app.baseapp.dashboard_libraries import createlegend as cl

default_limit = [1000]
default_traces = dashdataandtables.limits_traces_df[dashdataandtables.limits_traces_df['limit_id']\
                                                    .isin(default_limit)].copy()
default_legend_fig = cl.CreateLegendFig(default_limit,dashdataandtables.limits_traces_df)

default_legend_out_graph = dcc.Graph(figure=default_legend_fig,id='legend_out_id',
                             style={'width': '100%', 'height': '100%'})

from app.baseapp.dashboard_libraries import updatelegend as ul
from app.baseapp.dashboard_libraries import getstyleandlegend as gsal
default_styleandlegendcolumn = gsal.GetStyleAndLegendColumn(default_styledatatable,default_legend_out_graph)

from app.baseapp.dashboard_libraries import creategraph as cg

rowofbuttons = html.Div([
    html.Button('Save', id='btn-nclicks-1', n_clicks=0),
    html.Button('Revert', id='btn-nclicks-2', n_clicks=0),
    html.Button('Cancel', id='btn-nclicks-3', n_clicks=0),
    html.Div(id='container-button-timestamp')
])

default_limit = [1000]
default_traces = dashdataandtables.limits_traces_df[dashdataandtables.limits_traces_df['limit_id'].isin(default_limit)].copy()
print('default_limit')
print(default_limit)
print('dashdataandtables.limits_traces_df')
print(dashdataandtables.limits_traces_df)
print('dashdataandtables.limits_data_df')
print(dashdataandtables.limits_data_df)

default_graph_fig = cg.CreateGraph(default_limit, dashdataandtables.limits_traces_df, dashdataandtables.limits_data_df)

from app.baseapp.dashboard_libraries import updategraph as ug

default_graph_out = dcc.Graph(figure=default_graph_fig,id='graph_out_id',
                            config=dict(responsive=True),
                            className='h-100'
                            #style={'width': '100%', 'height': '100%'}
                           )

chart_in = default_graph_out

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

default_column_chart = GetChart(chart_in)


dash.register_page(__name__, path='/show_plots_and_legend')

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

next_button =  html.Div(dbc.Button("Next",  id="style_plot_and_traces_next_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="style_plot_and_traces_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

style_plot_and_traces_form_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     style_plot_and_traces_form_title,
     style_plot_and_traces_form_content,
     next_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

#layout = style_plot_and_traces_form_form

twocolumns =  html.Div(className="row g-0 ALL_ROW NOPADDING",children=[
                                                                    default_column_chart,
                                                                    default_styleandlegendcolumn,
                                                                    rowofbuttons,
                                                                    next_button, cancel_button
                                                                      ],)

layout2 = html.Div([twocolumns],
                   className="container-fluid DASHBOARD_CONTAINER_STYLE",
                  )


#layout = style_plot_and_traces_form_form
layout = layout2

@callback(
    [Output("graph_out_id","figure"),Output("legend_out_id","figure"),],
    [Input('format_table_id', 'data')],
    [State("format_table_id", "data")])
def update_output(table_data, table_data_in):
    fig_out = ug.UpdateGraph(dashdataandtables, table_data_in)
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
