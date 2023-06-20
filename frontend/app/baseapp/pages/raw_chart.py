# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

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

dash.register_page(__name__, path='/raw_chart')

def parse_values(data_values_in):
    data = data_values_in[0].replace("{[", "").replace("]}", "")
    print('parse data before split')
    print(data)
    values = data.split(";")
    print('split values')
    print(values)
    masses = [value.split(" ")[0] for value in values]
    cross_sections = [value.split(" ")[1] for value in values]

    return masses, cross_sections

def parse_series_and_values(limits_dataframe_in):
    experiment_data = []
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
                experiment_data.append(appendthis)
        #lol
    experiment_data_df = pd.DataFrame(data=experiment_data,columns=['id','data_label','series','raw_x','raw_y','series_color'])
    
    experiment_data_df['masses'] = experiment_data_df['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')
    experiment_data_df['cross_sections'] = experiment_data_df['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')
    experiment_data_df = experiment_data_df.rename(columns={"id": "limit_id" })
    experiment_data_df = experiment_data_df.reset_index()
    experiment_data_df['id'] = experiment_data_df.index
    experiment_data_df.set_index('id', inplace=True, drop=False)
    
    #columns=['id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']

    experiment_list_df = experiment_data_df[['limit_id','data_label']].copy()
    #experiment_list_df.rename(columns={"id": "limit_id" })
    #experiment_list_df['limit_id'] = experiment_list_df['limit_id']
    experiment_list_df.drop_duplicates(inplace=True)
    experiment_list_df = experiment_list_df.reset_index()
    experiment_list_df['id'] = experiment_list_df.index
    experiment_list_df.set_index('id', inplace=True, drop=False)
    
    series_list_df = experiment_data_df[['limit_id','data_label','series','series_color']]
    #series_list_df.rename(columns={"id": "limit_id" })
    series_list_df.drop_duplicates(inplace=True)
    series_list_df = series_list_df.reset_index()
    series_list_df['id'] = series_list_df.index
    series_list_df.set_index('id', inplace=True, drop=False)
        
    return experiment_list_df, series_list_df, experiment_data_df
       

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


#api_container = "container_api_1:8004"
fastapi_orm_url = "http://35.214.16.124:8008"
fastapi_orm_url_api = fastapi_orm_url +"/apiorm"
'''
def GetLimit(limit_id_in):
    url = fastapi_orm_url_api + "/limit/" + str(limit_id_in)
    r = requests.get(url)
    response_data = r.json()
    print('get limit response data')
    print(response_data)
    response_data_frame = pd.DataFrame(response_data, index=[0])
    masses, cross_sections = parse_values(response_data_frame['data_values'])
    #response_data_frame['mass'] = mass
    #response_data_frame['cross_section'] = cross_section
    column_names=['id','data_label','data_values']
    if response_data_frame.empty:
        empty_data = [['id','data_label','data_values']]
        updated_data_frame_ret = pd.DataFrame(data=empty_data, columns=column_names)
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
        experiment_data_ret = pd.DataFrame(data=empty_data, columns=column_names)
    else:
        lst = ['id','data_label','data_values']
        updated_data_frame_ret = response_data_frame[response_data_frame.columns.intersection(lst)]
        updated_data_frame_ret = updated_data_frame_ret[lst]
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
        experiment_data_ret = parse_series_and_values(updated_data_frame_ret)
    return updated_data_dict_ret, updated_data_frame_ret, column_names, experiment_data_ret
'''

def GetLimits():
    url = fastapi_orm_url_api + "/limit/"
    r = requests.get(url)
    response_data = r.json()
    #print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    experiment_list_df, series_list_df, experiment_data_df = parse_series_and_values(response_data_frame)
    column_names=['id','data_label','data_comment','data_values']

    print('experiment_list_df >>', experiment_list_df)
    print('series_list_df >>', series_list_df)
    print('experiment_data_df >>',experiment_data_df)

    
    if response_data_frame.empty:
        experiment_columns = ['id','limit_id','data_label']
        experiment_empty_data = [['id','limit_id','data_label']]
        series_columns = ['id','limit_id','data_label','series','series_color']
        series_empty_data = [['id','limit_id','data_label','series','series_color']]
        experiment_data_columns = ['id','limit_id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']
        experiment_data_empty_data = [['id','limit_id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']]
        experiment_list_df_ret = pd.DataFrame(data=experiment_empty_data, columns=experiment_columns)
        series_list_df_ret = pd.DataFrame(data=series_empty_data, columns=series_columns)
        experiment_data_df_ret = pd.DataFrame(data=experiment_data_empty_data, columns=experiment_data_columns)
        
        experiment_list_dict_ret = experiment_list_df.to_dict('records')
    else:
        experiment_list_df_ret = experiment_list_df
        series_list_df_ret = series_list_df
        experiment_data_df_ret = experiment_data_df
        experiment_list_dict_ret = experiment_list_df_ret.to_dict('records')

    return experiment_list_df_ret, series_list_df_ret, experiment_data_df_ret, experiment_list_dict_ret


LIMIT_COLUMNS = [
    {"id": "id", "name": "id"},
    {"id": "limit_id", "name": "id"},
    {"id": "data_label", "name": "Label"},
    {"id": "data_reference", "name": "Reference"}
]

LIMIT_TABLE_PAGE_SIZE = 100
column_width = f"{100/len(LIMIT_COLUMNS)}%"

experiment_list_df, series_list_df, experiment_data_df, experiment_list_dict = GetLimits()

# The css is needed to maintain a fixed column width after filtering
limits_table = dash_table.DataTable(
    id='limits-table',
    data=experiment_list_dict,
    columns=[{"name": i, "id": i} for i in experiment_list_df.columns],
    row_selectable="multi",
    cell_selectable=False,
    filter_action="native",
    #page_size=LIMIT_TABLE_PAGE_SIZE,
    page_size=12,
    css=[{"selector": "table", "rule": "table-layout: fixed"}],
    style_table={
        "height": "600px",
        "overflowY": "auto",
    },
    style_header={
        "fontWeight": "bold",
        "textAlign": "left"
    },
    style_cell={
    	"width": f"{column_width}",
        "maxWidth": f"{column_width}",
        "overflow": "hidden",
        "textAlign": "left",
        "textOverflow": "ellipsis",
    },
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
            limits_table,
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

        experiment_all_df, series_all_df, experiment_data_all_df, experiment_all_dict = GetLimits()
    
        for row in selected_rows:
            limit_id = experiment_list_df.iloc[row]["limit_id"]
            experiment_selected_df = experiment_all_df[experiment_all_df['limit_id']==limit_id]
            series_selected_df = series_all_df[series_all_df['limit_id']==limit_id]
            experiment_data_selected_df = experiment_data_all_df[experiment_data_all_df['limit_id']==limit_id]
            trace_id = 0
            # df[(df.year == 2013) & (df.country.isin(['US', 'FR', 'ES']))]
            for index, row in series_selected_df.iterrows():
                series_data = experiment_data_selected_df[(experiment_data_selected_df['limit_id']==row['limit_id']) \
                                                & (experiment_data_selected_df['series']==row['series'])]
                series_name = row['data_label'] + '_' + str(row['series'])
                series_color = row['series_color']
                fig.add_trace(
                    go.Scatter(
                        x=series_data['masses'],
                        y=series_data['cross_sections'],
                        name=series_name,
                        line=dict(color=series_color),
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
