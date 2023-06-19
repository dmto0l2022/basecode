# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
import pathlib
import sqlalchemy
from sqlalchemy import text
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dash_table, dcc, html, Input, Output, State

app = Dash(__name__)

def parse_values(limit_query_result):
    data = limit_query_result.data_values.replace("{[", "").replace("]}", "")
    values = data.split(";")
    masses = [value.split()[0] for value in values]
    cross_sections = [value.split()[1] for value in values]

    return masses, cross_sections

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

with open(BASE_DIR / "secrets.json") as s:
    secrets = json.load(s)
db_info = secrets["DATABASES"]["default"]

engine = sqlalchemy.create_engine(
    f"mariadb+mariadbconnector://"
    f"{db_info['USER']}:{db_info['PASSWORD']}@"
    f"{db_info['HOST']}:{db_info['PORT']}/"
    f"{db_info['NAME']}"
)

with engine.connect() as connection:
    limits = pd.read_sql("SELECT id, data_label, data_reference from limits",
                         connection)

LIMIT_COLUMNS = [
    {"id": "data_label", "name": "Label"},
    {"id": "data_reference", "name": "Reference"}
]
LIMIT_TABLE_PAGE_SIZE = 100
column_width = f"{100/len(LIMIT_COLUMNS)}%"

# The css is needed to maintain a fixed column width after filtering
limits_table = dash_table.DataTable(
    id='limits-table',
    data=limits.to_dict('records'),
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

@app.callback(
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
        with engine.connect() as connection:
            for row in selected_rows:
                limit_id = limits.iloc[row]["id"]
                query = text(f"SELECT * FROM limits WHERE id={limit_id}")
                result = connection.execute(query).fetchone()

                mass, cross_section = parse_values(result)
                results.append(
                    {
                        "mass": mass,
                        "cross_section": cross_section,
                        "label": result.data_label
                    }
                )

            for result in results:
                fig.add_trace(
                    go.Scatter(
                        x=result["mass"],
                        y=result["cross_section"],
                        mode='lines',
                        name=result["label"],
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

app.layout = html.Div(
    [
        limits_table,
        add_limits_div,
        plot_container_div,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
