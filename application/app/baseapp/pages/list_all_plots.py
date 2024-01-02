#####################################################
## Full Table Page to Edit Tables
#####################################################
## Version Journal
#####################################################

import dash
from dash import clientside_callback
from dash import Dash
from dash import dcc, html
from dash import Input, Output, State, callback
from dash import dash_table, no_update  # Dash version >= 2.0.0
import pandas as pd
import plotly.express as px
import json
import requests
import pickle
import dash_bootstrap_components as dbc

from flask import request, session

from app.baseapp.libraries import formlibrary as fl
from app.baseapp.libraries import plots_table as pt
from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

page_name = 'list_all_plots'
dash.register_page(__name__, path='/'+page_name)

###########################################################
# Should only need to change the following:
class ListAllPlotsDash():
    def __init__(self, page_name_in):
        self.page_name = "list_all_plots"
        self.page_title = 'List All Plots'
        self.dmtool_userid = '0' 
        self.plot_table_id = self.page_name + 'table_id'
        self.table_meta_data_data = [
                                ['id', '5%'],
                                ['user_id', '5%'],
                                ['name', '71%'],
                                ['created_at', '5%'],
                                ['updated_at', '5%'],
                                ['ceased_at', '5%']
                               ]
        self.baseapp_prefix = '/application/baseapp'
        self.plot_table_id = page_name + '_plot_table'


        self.page_content_style = {'top': '0px','padding':'0','margins':'0',
                                           'height':'100%', 'width':'100%',
                                           'left': '0','background-color': 'green',
                                           'overflow-y': 'scroll'}
        self.row_height = '13px'
        self.table_font_size = '12px'
        self.layout = html.Div()
        
        self.dash_table = dash_table.DataTable(id=self.plot_table_id)

    def get_layout(self):    
      
        debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                          html.Div(id=self.page_name+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                          html.Div(id=self.page_name+"button-output-div", children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                          className="PAGE_DEBUG_CONTENT")
    
        ##dmtool_user_id = gdu.dmtool_userid
        ## the callback triggers first time the page opens and the actual user is retrieved from the header
        self.dmtool_userid = '0' ### default - no user should be given 0
        internal_header={'dmtool-userid':self.dmtool_userid}
    
        ## create an empty table to be refreshed by the callback
    
        #set_table_height("80%")
        self.table_height = '1000px'
        self.plot_table = pt.get_table(self.page_title,self.plot_table_id, self.table_meta_data_data,self.table_height,self.row_height,self.table_font_size,self.dmtool_userid)
        
    
        self.row_plots = dbc.Row([dbc.Col(id=self.page_name + "plot_table_div",
                                children=[self.plot_table.dash_table],
                                width=12,)],
                                className ="list_all_plots_plots_class")
      
        self.table_layout = html.Div(
            [
                dcc.Location(id= self.page_name + "url", refresh=True), ## important to allow redirects,
                dcc.Store(id= self.page_name + 'screen_size_store', storage_type='local'), ## stores screen size
                ##html.Div(children= page_title, className="NOPADDING_CONTENT TABLE_TITLE"),
                self.row_plots,
                ## debug_output
            ],
            className='list_all_plots_main_class'
        )
    
        self.layout = html.Div(id=page_name+'content',children=[self.table_layout],className="container-fluid", style=self.page_content_style)
        
    def page_size_callback(self):
        clientside_callback(
                """
                function(href) {
                    var w = window.innerWidth;
                    var h = window.innerHeight;
                    var jsn = {width: w, height: h};
                    const myJSON = JSON.stringify(jsn); 
                    return jsn;
                }
                """,
                Output(self.page_name + 'screen_size_store', 'data'),
                Input(self.page_name + 'url', 'href')
            )
    def get_user_owned_plots(self):
        callback([Output(self.page_name + "plot_table_div", 'children')],
                      Input(self.page_name +'url', 'href'), State(self.page_name + 'screen_size_store', 'data'))
        def set_plot_name(href: str, page_size_in):
            page_size_as_string = json.dumps(page_size_in)
            print('sltp : list all plots callback triggered ---- page size >>>>>>>' + page_size_as_string)
            screen_height = page_size_in['height']
            print('screen_height >>>>>>>>>>', screen_height)
            plots_table_height = str(screen_height * 0.5) + 'px'
            ## get user id from cookie
            dmtooluser_cls = gdu.GetUserID()
            self.dmtool_userid = dmtooluser_cls.dmtool_userid
            self.plot_table.set_dmtool_userid(self.dmtool_userid)
            self.plot_table.set_table_height(plots_table_height)
            self.plot_table.get_dash_table()
            return self.plot_table.dash_table

dashboard = ListAllPlotsDash(page_name)
dashboard.get_layout()
layout = dashboard.layout
dashboard.page_size_callback()
dashboard.get_user_owned_plots()
    
