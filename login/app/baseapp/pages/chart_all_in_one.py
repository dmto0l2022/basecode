## a version of the DMTOOLS chart with everything in one file

import dash
import json
import requests
import pathlib
import sqlalchemy
from sqlalchemy import text
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dash_table
from dash import dcc, callback, html
from dash import Input, Output, State

from itertools import cycle

# colors
palette = cycle(px.colors.qualitative.Bold)

dash.register_page(__name__, path='/chart_all_in_one')

## takes the full limits table and
## splits all the data including the data_values field into 3 dataframes
## 1. simple list of limits
## 2. list of traces within the limits
## 3. trace data

def parse_series_and_values(limits_dataframe_in):
    limit_data = []
    for index, row in limits_dataframe_in.iterrows():
        #print(row['id'], row['data_values'])
        data_label = row[['data_label']].iloc[0]
        data_string = row[['data_values']].iloc[0]
        data_string = data_string.replace("{[", "")
        data_string = data_string.replace("]}", "")
        #print(data_string)
        data_series = data_string.split("]")
        #print(len(data_series))
        for l in range(0,len(data_series)):
            next_colour = next(palette)
            single_set = data_series[l]
            set_list = single_set.split(";")
            for i in set_list:
                z = i.split(" ");
                new_x = z[0].replace(",[", "")
                try:
                    appendthis = [row['id'],data_label,l,new_x,z[1],next_colour]
                except:
                    appendthis = [row['id'],'data_label',l,0,0]
                limit_data.append(appendthis)
        #lol
    #print('parsed limit data >>>>',limit_data) 
    
    ## the datatable needed a unique id
    ## the id of the limit table was renamed to limit_id
    ## a new column was created called id
    
    limit_data_df_out = pd.DataFrame(data=limit_data,columns=['id','data_label','trace_id','raw_x','raw_y','trace_color_default'])
    limit_data_df_out['masses'] = limit_data_df_out['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')
    limit_data_df_out['cross_sections'] = limit_data_df_out['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')
    limit_data_df_out = limit_data_df_out.rename(columns={"id": "limit_id" })
    limit_data_df_out = limit_data_df_out.reset_index()
    limit_data_df_out['id'] = limit_data_df_out.index
    limit_data_df_out.set_index('id', inplace=True, drop=False)
    
    #columns=['id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']

    limit_list_df_out = limit_data_df_out[['limit_id','data_label']].copy()
    limit_list_df_out.drop_duplicates(inplace=True)
    limit_list_df_out = limit_list_df_out.reset_index()
    limit_list_df_out['id'] = limit_list_df_out.index
    limit_list_df_out.set_index('id', inplace=True, drop=False)
    
    trace_list_df_out = limit_data_df_out[['limit_id','data_label','trace_id','trace_color_default']]
    trace_list_df_out.drop_duplicates(inplace=True)
    trace_list_df_out = trace_list_df_out.reset_index()
    trace_list_df_out['id'] = trace_list_df_out.index
    trace_list_df_out.set_index('id', inplace=True, drop=False)
        
    return limit_list_df_out, trace_list_df_out, limit_data_df_out
       

fastapi_url_limits = "http://container_fastapi_alembic_1:8014/alembic/limits" ## multiple limit operations
fastapi_url_limit = "http://container_fastapi_alembic_1:8014/alembic/limit/" ## single limit operations



def GetLimit(limit_id_in):
    url = fastapi_url_limit + str(limit_id_in)
    r = requests.get(url)
    response_data = r.json()
    #print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
    column_names=['id','data_label','data_comment','data_values']
    limit_columns = ['id','limit_id','data_label']
    trace_columns = ['id','limit_id','data_label','trace_id','trace_color_default']
    limit_data_columns = ['id','limit_id','data_label','trace_id','raw_x','raw_y','trace_color_default','masses','cross_sections']
    #print('limit_list_df >>', limit_list_df_resp)
    #print('trace_list_df >>', trace_list_df_resp)
    #print('limit_data_df >>', limit_data_df_resp)

    
    if response_data_frame.empty:
        
        limit_empty_data = [['id','limit_id','data_label']]
        trace_empty_data = [['id','limit_id','data_label','trace_id','trace_color']]
        limit_data_empty_data = [['id','limit_id','data_label','trace_id','raw_x','raw_y','trace_color_default','masses','cross_sections']]
        
        limit_list_df_ret = pd.DataFrame(columns=limit_columns)
        trace_list_df_ret = pd.DataFrame(columns=trace_columns)
        limit_data_df_ret = pd.DataFrame(columns=limit_data_columns)
        
        limit_list_dict_ret = limit_list_df.to_dict('records')
    else:
        limit_list_df_ret = limit_list_df_resp
        trace_list_df_ret = trace_list_df_resp
        limit_data_df_ret = limit_data_df_resp
        limit_list_dict_ret = limit_list_df_ret.to_dict('records')

    return limit_list_df_ret, trace_list_df_ret, limit_data_df_ret, limit_list_dict_ret, limit_columns, limit_data_columns, trace_columns

def GetLimits():
    url = fastapi_url_limits
    r = requests.get(url)
    response_data = r.json()
    print("+++++++++ response data ++++++++++++")
    print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    print("+++++++++++ response_data_frame ++++++++++++")
    print(response_data_frame)
    limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
    column_names=['id','data_label','data_comment','data_values']

    #print('limit_list_df >>', limit_list_df_resp)
    #print('trace_list_df >>', trace_list_df_resp)
    #print('limit_data_df >>', limit_data_df_resp)

    
    if response_data_frame.empty:
        limit_columns = ['id','limit_id','data_label']
        limit_empty_data = [['id','limit_id','data_label']]
        trace_columns = ['id','limit_id','data_label','trace_id','trace_color_default']
        trace_empty_data = [['id','limit_id','data_label','trace_id','trace_color_default']]
        limit_data_columns = ['id','limit_id','data_label','trace_id','raw_x','raw_y','trace_color','masses','cross_sections']
        limit_data_empty_data = [['id','limit_id','data_label','trace_id','raw_x','raw_y','trace_color','masses','cross_sections']]
        #limit_list_df_ret = pd.DataFrame(data=limit_empty_data, columns=limit_columns)
        #trace_list_df_ret = pd.DataFrame(data=trace_empty_data, columns=trace_columns)
        #limit_data_df_ret = pd.DataFrame(data=limit_data_empty_data, columns=limit_data_columns)
        limit_list_df_ret = pd.DataFrame(columns=limit_columns)
        trace_list_df_ret = pd.DataFrame(columns=trace_columns)
        limit_data_df_ret = pd.DataFrame(columns=limit_data_columns)
        
        limit_list_dict_ret = trace_list_df_ret.to_dict('records')
    else:
        limit_list_df_ret = limit_list_df_resp
        trace_list_df_ret = trace_list_df_resp
        limit_data_df_ret = limit_data_df_resp
        limit_list_dict_ret = limit_list_df_ret.to_dict('records')

    return limit_list_df_ret, trace_list_df_ret, limit_data_df_ret, limit_list_dict_ret, limit_columns, limit_data_columns, trace_columns


LIMIT_COLUMNS = [
    {"id": "id", "name": "id"},
    {"id": "limit_id", "name": "id"},
    {"id": "data_label", "name": "Label"},
    {"id": "data_reference", "name": "Reference"}
]

#LIMIT_TABLE_PAGE_SIZE = 100
#column_width = f"{100/len(LIMIT_COLUMNS)}%"

#limit_list_df, trace_list_df, limit_data_df, limit_list_dict = GetLimits()

def GetLimitDict():
    limit_list_df, trace_list_df, limit_data_df, limit_list_dict, limit_columns, limit_data_columns, trace_columns = GetLimits()
    return limit_list_dict, limit_columns

# The css is needed to maintain a fixed column width after filtering

limits_table = dash_table.DataTable(
        id='limits_table_select',
        data=GetLimitDict()[0],
        columns=[{"name": c, "id": c} for c in GetLimitDict()[1]],
        fixed_rows={'headers': True},
        #fixed_rows={'headers': True},
        #page_size=5,
        filter_action='none',
        #row_selectable='multi',
        #selected_rows=[],
    
        style_cell={'textAlign': 'left','padding': '0px','font_size': font_size,
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'border': '1px solid black',
                        #'height': 'auto'
                        'height': row_height,
                    },
         css=[
                    {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of body rows
                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"}
                    ],
        
        #style_table={'height': '75vh',},
        style_cell_conditional=[
            {'if': {'column_id': 'id'},
             'width': '2%'},
            {'if': {'column_id': 'data_label'},
             'width': '25%'},
            {'if': {'column_id': 'data_reference'},
             'width': '25%'},
        ],
        #style_data={
        #    'whiteSpace': 'normal',
        #    'height': 'auto',
        #},
        #style_header=style_header_var,
        #tooltip_data=[
        #    {
        #        column: {'value': str(value), 'type': 'markdown'}
        #        for column, value in row.items()
        #    } for row in data
        #],
        tooltip_duration=None,
        )
    


add_limits_div = html.Div(
    [
        html.Button(
            id="add-button",
            children="Add Selected Limit(s)",
            style={
                "margin": "auto",
            }
        )
    ],
    style={
        "text-align": "center",
    }
)

plot_container_div = html.Div(id="limit-plot-container")

def serve_layout():
    layout_out = html.Div(
        [
            #limits_table,
            dash_table.DataTable(
                id='limits-table',
                data=GetLimitDict()[0],
                columns=[{"name": c, "id": c} for c in GetLimitDict()[1]],
                row_selectable="multi",
                cell_selectable=False,
                filter_action="native",
                page_size=12,
                css=[{"selector": "table", "rule": "table-layout: fixed"}],
                style_table={
                    "height": "40vh",
                    "overflowY": "auto",
                },
                style_header={
                    "fontWeight": "bold",
                    "textAlign": "left"
                },
                style_cell={
                    "overflow": "hidden",
                    "textAlign": "left",
                    "textOverflow": "ellipsis",
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'id'},
                     'width': '2%'},
                    {'if': {'column_id': 'data_label'},
                     'width': '25%'},
                    {'if': {'column_id': 'data_reference'},
                     'width': '25%'},
        ],
            ),
            add_limits_div,
            plot_container_div,
        ]
    )
    return layout_out

layout = serve_layout

#Output('datatable-row-ids-container', 'children'),
#Input('datatable-row-ids', 'derived_virtual_row_ids'),
#Input('datatable-row-ids', 'selected_row_ids'),
#Input('datatable-row-ids', 'active_cell'))

@callback(
    Output(component_id="limit-plot-container", component_property="children"),
    Input(component_id="add-button", component_property="n_clicks"),
    State(component_id="limits-table", component_property="selected_rows"),
)
def add_limits(n_clicks, selected_rows):
    x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
    y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"

    # Default to an empty graph
    if (
        n_clicks is None
        or selected_rows is None
    ):
        fig = go.Figure(data=[go.Scatter(x=[], y=[])])
        fig.update_xaxes(
            title_text=x_title_text,
            #type="log"
            type="linear"
        )
        fig.update_yaxes(
            title_text=y_title_text,
            #type="log"
            type="linear"
        )
    # Handle the case of de-selecting rows
    elif len(selected_rows) == 0:
        fig = go.Figure(data=[go.Scatter(x=[], y=[])])
        fig.update_xaxes(
            title_text=x_title_text,
            #type="log"
            type="linear"
        )
        fig.update_yaxes(
            title_text=y_title_text,
            #type="log"
            type="linear"
        )
    # Populate the graph
    else:
        fig = go.Figure()

        results = []

        limit_all_df, trace_all_df, limit_data_all_df, limit_all_dict ,limit_columns, limit_data_columns, trace_columns = GetLimits()
    
        for row in selected_rows:
            limit_id = limit_all_df.iloc[row]["limit_id"]
            print('selected limit >>', limit_id)
            limit_selected_df = limit_all_df[limit_all_df['limit_id']==limit_id]
            trace_selected_df = trace_all_df[trace_all_df['limit_id']==limit_id]
            limit_data_selected_df = limit_data_all_df[limit_data_all_df['limit_id']==limit_id]
            trace_id = 0
            # df[(df.year == 2013) & (df.country.isin(['US', 'FR', 'ES']))]
            for index, row in trace_selected_df.iterrows():
                trace_data = limit_data_selected_df[(limit_data_selected_df['limit_id']==row['limit_id']) \
                                                & (limit_data_selected_df['trace_id']==row['trace_id'])]
                print("trace_data >>>>" , trace_data)
                trace_name = row['data_label'] + '_' + str(row['trace_id'])
                trace_color_default = row['trace_color_default']
                fig.add_trace(
                    go.Scatter(
                        x=trace_data['masses'],
                        y=trace_data['cross_sections'],
                        name=trace_name,
                        line=dict(color=trace_color_default),
                        mode='lines',
                    )
                )

        fig.update_xaxes(
            title_text=x_title_text,
            #type="log"
            type="linear"
        )
        fig.update_yaxes(
            title_text=y_title_text,
            #type="log"
            type="linear"
        )
        fig.update_layout(showlegend=True)

    graph = dcc.Graph(
        figure=fig,
        id="limit-plot",
        style={
            "width": "50%",
            "margin": "auto"
        },
        mathjax=True,
    )
    return graph
