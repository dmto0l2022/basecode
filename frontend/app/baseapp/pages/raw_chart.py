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
    lol = []
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
                lol.append(appendthis)
        #lol
        df_experiment = pd.DataFrame(data=lol,columns=['id','data_label','series','raw_x','raw_y','series_color'])
        
        df_experiment['masses'] = df_experiment['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')
        df_experiment['cross_sections'] = df_experiment['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')

        columns=['id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']
        
        return df_experiment, columns
       

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


#api_container = "container_api_1:8004"
fastapi_orm_url = "http://35.214.16.124:8008"
fastapi_orm_url_api = fastapi_orm_url +"/apiorm"

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

def GetLimits():
    url = fastapi_orm_url_api + "/limit/"
    r = requests.get(url)
    response_data = r.json()
    print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    column_names=['id','data_label','data_comment','data_values']
    if response_data_frame.empty:
        empty_data = [['id','data_label','data_comment','data_values']]
        updated_data_frame_ret = pd.DataFrame(data=empty_data, columns=column_names)
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
        experiment_data_ret = pd.DataFrame(data=empty_data, columns=column_names)
    else:
        lst = ['id','data_label','data_comment','data_values']
        updated_data_frame_ret = response_data_frame[response_data_frame.columns.intersection(lst)]
        updated_data_frame_ret = updated_data_frame_ret[lst]
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
        experiment_data_ret = parse_series_and_values(updated_data_frame_ret)
    return updated_data_dict_ret, updated_data_frame_ret, column_names, experiment_data_ret

LIMIT_COLUMNS = [
    {"id": "id", "name": "ID"},
    {"id": "data_label", "name": "Label"},
    {"id": "data_reference", "name": "Reference"}
]

LIMIT_TABLE_PAGE_SIZE = 100
column_width = f"{100/len(LIMIT_COLUMNS)}%"

limits_data_dict, limits_data_frame, column_names, experiment_data = GetLimits()

# The css is needed to maintain a fixed column width after filtering
limits_table = dash_table.DataTable(
    id='limits-table',
    data=limits_data_dict,
    columns=LIMIT_COLUMNS,
    row_selectable="multi",
    cell_selectable=False,
    filter_action="native",
    page_size=LIMIT_TABLE_PAGE_SIZE,
    css=[{"selector": "table", "rule": "table-layout: fixed"}],
    style_table={
        "height": "300px",
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

layout = html.Div(
    [
        limits_table,
        add_limits_div,
        plot_container_div,
    ]
)


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

        limits_data_dict, limits_data_frame, column_names, experiment_df = GetLimits()
    
        for row in selected_rows:
            limit_id = limits_data_frame.iloc[row]["id"]
            updated_data_dict, updated_data_frame, column_names, experiment_df = GetLimit(limit_id)
            
            trace_id = 0
            
            for result in experiment_df:
                trace_id = trace_id + 1
        
                result['series_name'] = result['data_label'] + '_' + result['series'].astype(str)
                series_name = result['series_name'][0]
                series_color = result['series_color'][0]
                fig.add_trace(
                    go.Scatter(
                        x=result['masses'],
                        y=result['cross_sections'],
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
