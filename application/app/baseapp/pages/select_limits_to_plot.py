import dash
from dash import Dash
import dash_bootstrap_components as dbc
from flask import session
from furl import furl
from flask import request

#import formlibrary as fl
import requests
import json
import redis
import pickle

#r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
dmtool_userid = 16384 ## testing

dash.register_page(__name__, path='/select_limits_to_plot')
page_name = 'select_limits_to_plot'

#### select limits to plot

from dash import dcc
from dash import html
from dash import callback
from dash import Output, Input, State
from dash import callback_context
from dash import dash_table

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_bootstrap_components as dbc

import pandas as pd

import plotly.express as px
from itertools import cycle

# colors
# palette = cycle(px.colors.qualitative.Bold)

from app.baseapp.dashboard_libraries import all_data_tables as adt

from app.baseapp.dashboard_libraries import get_limit_data as gld

#from app.baseapp.dashboard_libraries import get_dmtool_user as gdu

from app.baseapp.libraries import main_table_editor as mte

dash.register_page(__name__, path='/select_limits_to_plot')

#guid = gdu.GetUserID()

#print("guid.dmtool_userid >>>>>>>>>>>>>>>>", guid.dmtool_userid)

dashdataandtables = adt.DashDataAndTables(dmtool_userid)

#####

class SelectLimitsToPlotDashBoardLayout():
    def __init__(self,pagename_in, dmtool_userid_in,  listoflimits_in):
        self.page_name = pagename_in
        self.data_table_id =  self.page_name + "data_table_id"
        #self.table_meta_data_data = [
                        ['id', '3%'],
                        ['experiment', '3%'],
                        ['data_comment', '44%'],
                        ['data_label', '44%'],
                       ]
        
        self.row_height = '12px'
        self.table_font_size = '11px'

        self.data_table_cell_styles = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': self.table_font_size,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
        
        self.data_table_css_row_heights = [ {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                                    ]

         self.limits_to_plot_table_cell_styles = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': self.table_font_size,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
        
        self.limits_to_plot_table_css_row_heights = [ {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                                    ]

        self.button_styling_1 = {'font-size': '12px',
                          'width': '70px',
                          'display': 'inline-block', 
                          'margin-bottom': '1px',
                          'margin-right': '0px',
                          'margin-top': '1px',
                          'height':'19px',
                          'verticalAlign': 'center'}

        self.internal_header={'dmtool-userid':'0'}

        self.fastapi_url = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/"
        self.fastapi_url_all_limits = fastapi_url + multiple_api ## multiple limit operations
        self.fastapi_url_one_limit = fastapi_url + single_api + "/" ## single limit operations
        self.style_header_var={ 'backgroundColor': 'black','color': 'white'}
        main_data_table = mte.get_main_table(page_title,
                                             main_table_id,
                                             table_meta_data_data,
                                             row_height,
                                             table_font_size,
                                             fastapi_url_all,
                                             fastapi_url_one,
                                             dmtool_userid)


        self.limits_to_plot_df = pd.DataFrame()
        self.RowLimitsToPlot = dbc.Row()

    def CreateLimitsToPlot():

        ## creates empty limits to plot table and sets the unique id
        
        self.limits_to_plot_df = pd.DataFrame(data=None, columns=['id','plot_id','limit_id','data_reference','data_label'])
        
        style_header_var={ 'backgroundColor': 'black','color': 'white'}
        
        self.limits_to_plot_table = dash_table.DataTable(
            id=page_name+'limits_to_plot_table',
            data=limits_to_plot_df.to_dict('records'),
            columns=[{'name': 'id', 'id': 'id'},
                     {'name': 'limit_id', 'id': 'limit_id'},
                     {'name': 'data_reference', 'id': 'data_reference'},
                     {'name': 'data_label', 'id': 'data_label'}
                     ],
            #fixed_rows={'headers': True},
            page_size=7,
            style_cell=self.limits_to_plot_table_cell_styles,
            css=self.limits_to_plot_table_css_row_heights,
            #sort_action='native',
            #sort_mode='multi',
            #sort_as_null=['', 'No'],
            #sort_by=[{'column_id': 'expid', 'direction': 'desc'}],
            filter_action='none',
            row_deletable=True,
            #row_selectable='multi',
            #selected_rows=[],
            style_table={'height': '25vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'id'},
                 'width': '5%'},
                {'if': {'column_id': 'limit_id'},
                 'width': '10%'},
                {'if': {'column_id': 'data_reference'},
                 'width': '25%'},
                {'if': {'column_id': 'data_label'},
                 'width': '55%'},
            ],
            style_data={
                'whiteSpace': 'nowrap'
            },
            style_header=style_header_var,
        ) 

        self.RowLimitsToPlot = dbc.Row([dbc.Col(
                [
                     limits_to_plot_table
                ],
                width=12,)],
                    className ="TABLE_ROW NOPADDING")

    
    def CreateFilters():

        self.RowFilters =  dbc.Row([
                dbc.Col(
                    [
                        dashdataandtables.official_table
                    ],
                    width=2,
                    ),
                dbc.Col(
                    [
                        dashdataandtables.experiments_table
                    ],
                    width=2,
                    ),
                dbc.Col(
                    [
                        dashdataandtables.result_types_table
                    ],
                    width=2,
                    ),
                dbc.Col(
                    [
                        dashdataandtables.spin_dependency_table
                    ],
                    width=2,
                    ),
               dbc.Col(
                    [
                        dashdataandtables.years_table
                    ],
                    width=2,
                    ),
               dbc.Col(
                    [
                        dashdataandtables.greatest_hit_table
                    ],
                    width=2,
                    ),
        ])
    
    def GetDebugTable():
        row2_debug_ret = dbc.Row([dbc.Col(
                    [
                        dashdataandtables.debug_dropdown_table
                    ],
                    width=12,),
                       ])
    
        row3_1_debug_ret = dbc.Row([dbc.Col(
                    [
                        dashdataandtables.debug_dropdown_table
                    ],
                    width=12,),
                       ], className ="TABLE_ROW NOPADDING")
        
        #row3 = dbc.Row([dbc.Col(html.Div('List Here',id='tbl_out'),width=12,),])
        return row2_debug_ret, row3_1_debug_ret

    
    def CreateLayout():

        self.DivPlotName = html.Div(children='Plot Name Here',id=page_name +'_plot_name_id')
        
        
        
        new_button =  html.Button("New", id= page_name + "new_button_id", style=self.button_styling_1)
        save_button =  html.Button("Save", id= page_name + "save_button_id", style=self.button_styling_1)
        cancel_button =  html.Button("Cancel",  id=page_name + "cancel_button_id", style=self.button_styling_1)
        home_button =  html.Button("Home",  id=page_name + "home_button_id", style=self.button_styling_1)
        list_button =  html.Button("List",  id=page_name + "list_button_id", style=self.button_styling_1)
        self.DivRowOfButtons = html.Div(id= page_name + "page_buttons", children=[new_button,save_button,cancel_button,home_button,list_button], className="PAGE_FOOTER_BUTTONS"),
        
        
        self.RowLimits = dbc.Row([dbc.Col(
                            [ main_limits_table.dash_table_main],
                            width=12,)],
                            className ="NOPADDING_CONTENT")

        self.RowListOfLimits = dbc.Row([html.P(children='List of limits appear here',id=page_name+'limit_list')])
        
        maincolumn = dbc.Col(
                    [
                        dcc.Location(id=page_name+'url',refresh=True),
                        self.DivPlotName,
                        self.RowFilters,
                        self.RowLimits,
                        self.RowLimitsToPlot,
                        self.DivRowOfButtons,
                        self.RowListOfLimits
                    ],
                    width=12,)
        
        self.layout = html.Div(id=page_name+'content',children=[maincolumn],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
        
###

##

def get_layout():
    layout_out = html.Div(id=page_name+'content',children=[maincolumn],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
    #layout_out = html.Div(id=page_name+'content',children=[main_table_1.dash_table_main],className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT")
    
    return layout_out
        
##className="PAGE_CONTENT",)
sltpdb = SelectLimitsToPlotDashBoardLayout()
layout = sltpdb.layout

'''
@callback(Output(page_name +'_plot_name_id', 'children'),
              [Input(page_name +'url', 'href')])
def set_plot_name(href: str):
    f = furl(href)
    plot_name = f.args['plot_name']
    plot_id = f.args['plot_id']
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX select limits to plot XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    session_key = request.cookies.get('session')
    print('selecf limits to plot : session key >>',session_key)
    redis_session_key = "session:"+session_key

    val = r.get(redis_session_key)
    print(redis_session_key)
    print('---------val------------------------------')
    print(val)
    print('--------- decoded val------------------------------')
    decoded_val = pickle.loads(val)
    print(decoded_val)
    dmtool_userid = decoded_val['dmtool_userid']
    dmtool_authorised = decoded_val['dmtool_authorised']
    print('dmtool_userid in sltp >>>' ,decoded_val['dmtool_userid'])
    print('=======================================')
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    
    return html.H1(children=plot_id + ' - ' + plot_name) 
'''
## see https://github.com/plotly/dash/issues/61
## including the call backs in the class

@callback(
    Output(page_name + 'main_limits_table', 'data'),
    #Output('debug_dropdown_table', 'data'),
    #Output(component_id='tbl_out', component_property='children'),
    #
    Input('years_table', 'active_cell'),
    Input('years_table', 'derived_virtual_selected_rows'),
    #
    Input('official_table', 'active_cell'),
    Input('official_table', 'derived_virtual_selected_rows'),
    #
    Input('experiments_table', 'active_cell'),
    Input('experiments_table', 'derived_virtual_selected_rows'),
    #
    Input('result_types_table', 'active_cell'),
    Input('result_types_table', 'derived_virtual_selected_rows'),
    #
    Input('spin_dependency_table', 'active_cell'),
    Input('spin_dependency_table', 'derived_virtual_selected_rows'),
    #
    Input('greatest_hit_table', 'active_cell'),
    Input('greatest_hit_table', 'derived_virtual_selected_rows'),
    )
def update_graphs(
    active_cell_years,
    derived_virtual_selected_rows_years,
    #
    active_cell_official,
    derived_virtual_selected_rows_official,
    #
    active_cell_experiments,
    derived_virtual_selected_rows_experiments,
    #
    active_cell_resulttypes,
    derived_virtual_selected_rows_result_types,
    #
    active_cell_spin_dependency,
    derived_virtual_selected_rows_spin_dependency,
    #
    active_cell_greatest_hit,
    derived_virtual_selected_rows_greatest_hit,
    
):
    
    try:
        dfs = [
            dashdataandtables.years_df.loc[derived_virtual_selected_rows_years],
            dashdataandtables.experiments_df.loc[derived_virtual_selected_rows_experiments],
            dashdataandtables.result_types_df.loc[derived_virtual_selected_rows_result_types],
            dashdataandtables.spin_dependency_df.loc[derived_virtual_selected_rows_spin_dependency],
            dashdataandtables.official_df.loc[derived_virtual_selected_rows_official],
            dashdataandtables.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit],
        ]
        non_empty_dfs = [df for df in dfs if not df.empty]
        all_filters_df = pd.concat(non_empty_dfs)
    except:
        all_filters_df = pd.DataFrame()

    # print('sltp : all filters >>>>> ', all_filters_df)
    ## boolean filters
    #   dashdataandtables.official_df.loc[derived_virtual_selected_rows_official]
    #   dashdataandtables.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit]
            
    # https://stackoverflow.com/questions/60964165/ignore-empty-dataframe-when-merging

    all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits(dmtool_userid) 
    
    unfiltered_df = all_limit_list_df.copy()
    print('sltp : unfiltered_df >>>', unfiltered_df) 
    #df.drop(df.index , inplace=True)
    
    filtered_df = unfiltered_df.drop(unfiltered_df.index)
    #filtered_df
    
    if all_filters_df.empty:
        filtered_df = unfiltered_df
    else:
        for index, row in all_filters_df.iterrows():
            #print(row['variable'], row['value'])
            matching_records = unfiltered_df[unfiltered_df['experiment'] == 'empty']
            if row['data_type'] == 'number':
                matching_records = unfiltered_df[unfiltered_df[row['variable']] == int(row['value'])]
            elif row['data_type'] == 'text':
                matching_records = unfiltered_df[unfiltered_df[row['variable']] == row['value']]
            elif row['data_type'] == 'boolean':
                if row['value'] == 1:
                    matching_records = unfiltered_df[unfiltered_df[row['variable']] == True]
            else:
                    a = 1
            filtered_df = pd.concat([filtered_df, matching_records])
            #filtered_df = matching_records
            #filtered_df = filtered_df[filtered_df[row['variable']] == row['value']] 
    
    filtered_df = filtered_df.drop_duplicates()
    #filtered_df
   
    data1 = all_filters_df.to_dict("records")
    data2 = filtered_df.to_dict("records")
    #print(data1)
    #data1=dff2.to_dict("records")
    #list_output = str(selectedcontinent_list) if selectedcontinent_list else "Click the table"
    return data2 #, list_output


@callback(
    Output(page_name+'limits_to_plot_table', 'data'),
    [Input(page_name + 'main_limits_table', 'active_cell'),Input(page_name+'limits_to_plot_table', 'active_cell')],
    [State(page_name+'limits_to_plot_table', 'data')])
def trigger_fork(active_cell_exp,active_cell_plot,data_in):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #print(triggered_id)
    if triggered_id == page_name + 'main_limits_table':
        all_limit_list_df, all_trace_list_df, all_limit_data_df, all_limit_list_dict = gld.GetLimits(dmtool_userid)  
        selected_rowid = active_cell_exp['row_id']
        selected_row = all_limit_list_df[all_limit_list_df['id']==active_cell_exp['row_id']]
        selected_row  = selected_row[['id','limit_id','data_reference','data_label']]
        selected_row['plot_id'] = 'plot_id here'
        #data_out=plots_todo_df.to_dict("records")
        record=selected_row.to_dict("records")[0]
        #print(type(record))
        #print(record)
        #record = {columns[i]: arg for i, arg in enumerate(list(args))}
        # If the record (identified by user_key) already exists, update it.
        #try:
        #    #record_index = [record[selected_rowid] for record in data_in].index(record[selected_rowid])
        #    record_index = [record[selected_rowid] for record in data_in].index(record[selected_rowid])
        #    data_in[record_index] = record
        # Otherwise, append it.
        #except ValueError:
        #    data_in[selected_rowid] = record
        #dictlen = len(data_in)
        #data_in[selected_rowid] = record
        data_in.append(record)
        #data_in = record
        # Return the updated data.
        #return data

        #selected_row = limits_table_df[limits_table_df['expid']==active_cell['row_id']]
        #plots_todo_df= selected_row.copy()
        #data_out=plots_todo_df.to_dict("records")
        #data_out=selected_row.to_dict("records")

    elif triggered_id == page_name+'limits_to_plot_table':
        #selected_rowid = active_cell_plot['row']
        #print(data_in[selected_rowid])
        #print(active_cell_plot)
        #data_in = data_in.pop(active_cell_plot['row'])
        #print(data_in)
        a = 1
    
    return data_in




@callback(
    [Output(page_name+'url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
     Output(page_name+'limit_list','children')],
    [
    Input(page_name + "new_button_id", "n_clicks"),
    Input(page_name + "save_button_id", "n_clicks"),
    Input(page_name + "cancel_button_id", "n_clicks"),
    Input(page_name + "home_button_id", "n_clicks"),
    Input(page_name + "list_button_id","n_clicks"),
        ],[State(page_name +'limits_to_plot_table', 'data')],
        prevent_initial_call=True
)
def button_click(button1,button2,button3,button4,button5,plot_table_in):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print('plot_table_in >>>>>>>>>>>>>>>>' ,plot_table_in)
    #plots_to_do_df = pd.DataFrame(plot_table_in)
    plots_to_do_df = pd.DataFrame.from_dict(plot_table_in)
    plots_to_do_df['all'] = 'all'
    plots_to_do_df['limit_id'] = plots_to_do_df['limit_id'].astype(str)
    limits_to_plot = plots_to_do_df[['limit_id','all']]
    print('limits_to_plot >>>>>>', limits_to_plot)
    
    #limits_to_plot['limit_ids'] = limits_to_plot[['all']].groupby(['all'])['limit_id'].transform(lambda x: ','.join(x))
    #print(limit_ids)  
    new_df = limits_to_plot.groupby(['all'])['limit_id'].apply('|'.join).reset_index()
    #print('new_df >>>>>>>>' ,new_df)
    limit_ids = new_df['limit_id'].values[0]
    #print('limit_ids >>>>>>>>' ,limit_ids)
            
    #msg = prop_id
    if page_name + "new_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        #href_return = dash.page_registry['pages.style_plot_and_traces']['path']
        href_return = '/application/baseapp/style_plot_and_traces'
        return [href_return,'']
    elif page_name + "new_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/application/baseapp/create_new_plot'
        return  [href_return,'']
    elif page_name + "cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/application/baseapp/homepage'
        return  [href_return,'']
    elif page_name + "home_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/application/baseapp/homepage'
        return  [href_return,'']
    elif page_name + "list_button_id" == prop_id:
        #msg = "Button 3 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        #href_return = '/app/baseapp/select_limits_to_plot'
        href_return = '/application/baseapp/style_plot_and_traces?limit_id=' + limit_ids
        return [href_return,limit_ids]
    else:
        href_return = '/app/baseapp/select_limits_to_plot'
        return href_return

