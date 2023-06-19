# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# https://github.com/BrownParticleAstro/dmtools/blob/develop-dash/dash/app.py

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

dash.register_page(__name__, path='/will_chart')

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
        empty_data = [['id','data_values']]
        updated_data_frame_ret = pd.DataFrame(data=empty_data, columns=column_names)
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
    else:
        lst = ['id','data_label','data_values']
        updated_data_frame_ret = response_data_frame[response_data_frame.columns.intersection(lst)]
        updated_data_frame_ret = updated_data_frame_ret[lst]
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
    return updated_data_dict_ret, updated_data_frame_ret, column_names, masses, cross_sections

def GetLimits():
    url = fastapi_orm_url_api + "/limit/"
    r = requests.get(url)
    response_data = r.json()
    print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    column_names=['id','experiment','data_comment','create', 'read', 'update', 'delete']
    if response_data_frame.empty:
        empty_data = [['id','experiment','data_comment','create', 'read', 'update', 'delete']]
        updated_data_frame_ret = pd.DataFrame(data=empty_data, columns=column_names)
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
    else:
        lst = ['id','experiment','data_label','data_comment']
        updated_data_frame_ret = response_data_frame[response_data_frame.columns.intersection(lst)]
        updated_data_frame_ret = updated_data_frame_ret[lst]
        updated_data_frame_ret['create'] = "create"
        updated_data_frame_ret['read'] = "read"
        updated_data_frame_ret['update'] = "update"
        updated_data_frame_ret['delete'] = "delete"
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
    return updated_data_dict_ret, updated_data_frame_ret, column_names

LIMIT_COLUMNS = [
    {"id": "id", "name": "ID"},
    {"id": "experiment", "name": "Experiment"},
    {"id": "data_label", "name": "Label"},
    {"id": "data_reference", "name": "Reference"}
]

LIMIT_TABLE_PAGE_SIZE = 100
column_width = f"{100/len(LIMIT_COLUMNS)}%"

limits_data_dict, limits_data_frame, column_names = GetLimits()

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
            type="log"
        )
        fig.update_yaxes(
            title_text=y_title_text,
            type="log"
        )
    # Handle the case of de-selecting rows
    elif len(selected_rows) == 0:
        fig = go.Figure(data=[go.Scatter(x=[], y=[])])
        fig.update_xaxes(
            title_text=x_title_text,
            type="log"
        )
        fig.update_yaxes(
            title_text=y_title_text,
            type="log"
        )
    # Populate the graph
    else:
        fig = go.Figure()

        results = []

        limits_data_dict, limits_data_frame, column_names = GetLimits()
    
        for row in selected_rows:
            limit_id = limits_data_frame.iloc[row]["id"]
            updated_data_dict, updated_data_frame, column_names, masses, cross_sections = GetLimit(limit_id)
            results.append(
                {
                    "mass": masses ,
                    "cross_section": cross_sections ,
                    "label": updated_data_frame['data_label'].astype('string')
                }
            )

        for result in results:
            fig.add_trace(
                go.Scatter(
                    x=masses,
                    y=cross_sections,
                    mode='lines',
                    name=updated_data_frame["data_label"].astype('string')
                )
            )

        fig.update_xaxes(
            title_text=x_title_text,
            type="log"
        )
        fig.update_yaxes(
            title_text=y_title_text,
            type="log"
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
