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


###########################################################
# Should only need to change the following:

page_name = "list_all_plots"
page_title = 'List All Plots'
table_meta_data_data = [
                        ['id', '2%'],
                        ['user_id', '2%'],
                        ['name', '18%'],
                        ['created_at', '5%'],
                        ['updated_at', '5%'],
                        ['ceased_at', '5%']
                       ]

single_api = 'plot'
multiple_api = 'plots'

##########################################################
baseapp_prefix = '/application/baseapp'
plot_table_id = page_name + '_plot_table'
dash.register_page(__name__, path='/'+page_name)

#fastapi_url = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/"
#fastapi_url_all = fastapi_url + multiple_api ## multiple limit operations
#fastapi_url_one = fastapi_url + single_api + "/" ## single limit operations

button_styling_1 = {'font-size': '12px',
                  'width': '70px',
                  'display': 'inline-block', 
                  'margin-bottom': '1px',
                  'margin-right': '0px',
                  'margin-top': '1px',
                  'height':'19px',
                  'verticalAlign': 'center'}


row_height = '13px'
table_font_size = '12px'



empty_dash_table = dash_table.DataTable(id=plot_table_id)
######################################################

def get_layout():    
  
    debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                      html.Div(id=page_name+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                      html.Div(id=page_name+"button-output-div", children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                      className="PAGE_DEBUG_CONTENT")

    ##dmtool_user_id = gdu.dmtool_userid
    ## the callback triggers first time the page opens and the actual user is retrieved from the header
    dmtool_user_id = '0' ### default - no user should be given 0
    internal_header={'dmtool-userid':'1'}

    ## create an empty table to be refreshed by the callback

    #set_table_height("80%")
    table_height_in = "80%"
    plot_table = pt.get_table(page_title,plot_table_id, table_meta_data_data,table_height_in,row_height,table_font_size,dmtool_user_id)
    
  
    table_layout = html.Div(
        [
            dcc.Location(id= page_name + "url", refresh=True), ## important to allow redirects
            html.Div(children= page_title, className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(id=page_name + "plot_table_div",
                [
                    plot_table.dash_table
                ],
                className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT"
            ),
            debug_output
        ],
        className="row NOPADDING_CONTENT"
    )

    return table_layout
    

layout = get_layout

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
        Output(page_name + 'screen_size_store', 'data'),
        Input(page_name + 'url', 'href')
    )

callback([Output(page_name + "plot_table_div", 'children')],
              Input(page_name +'url', 'href'), State(page_name + 'screen_size_store', 'data'))
def set_plot_name(href: str, page_size_in):
    page_size_as_string = json.dumps(page_size_in)
    print('sltp : set plot name callback triggered ---- page size >>>>>>>' + page_size_as_string)
    screen_height = page_size_in['height']
    print('screen_height >>>>>>>>>>', screen_height)
    plots_table_height = str(screen_height * 0.7) + 'px'
    ## get user id from cookie
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    
    plot_table.set_dmtool_userid(dmtool_userid)
    plot_table.set_table_height(plots_table_height)
    plot_table.RefreshTableData()
    return plot_table.dash_table
