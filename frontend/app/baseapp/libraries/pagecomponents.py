import dash
from dash import dcc
from dash import html
from dash import Dash, html
from dash import Input, Output, State
from dash import dash_table

import dash_bootstrap_components as dbc
'''

"margin": "0px", "position": "absolute","top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"


page_header_0 =  dbc.Row(
            [
                dbc.Col(
                    html.P("DM Tools Plotter", className="HEADER_TEXT"),
                    width=12,
                    className = "HEADER_COLUMN",
                ),
            ] , ##className="PAGE_HEADER_0",
                justify="center",
        )

'''


page_header_0 = dbc.Row(
            [
                dbc.Col(html.Div("One of three columns",className="HEADER_TEXT"), width=4,className = "HEADER_COLUMN"),
                dbc.Col(
                    html.Div("DM Tools Plotter", className="HEADER_TEXT"), width=4, className = "HEADER_COLUMN"
                        ),
                dbc.Col(html.Div("One of three columns",className="HEADER_TEXT"), width=4, className = "HEADER_COLUMN"),
            ],
    className="PAGE_HEADER_0",
        )





##header1 = html.Div(
page_header_1 =  dbc.Row(
            [
                dbc.Col(
                    html.P("Need Help", className="HEADER_TEXT"),
                    width=3,
                    className = "HEADER_COLUMN",
                ),
                dbc.Col(
                    html.P("FAQ",className="HEADER_TEXT"),
                    width=3,
                    className = "HEADER_COLUMN",
                ),
                dbc.Col(
                    html.P("Found A Bug", className="HEADER_TEXT"),
                    width=3,
                    className = "HEADER_COLUMN",
                ),
                dbc.Col(
                    html.P("What's New", className="HEADER_TEXT"),
                    width=3,
                    className = "HEADER_COLUMN",
                ),
            ],
            className="PAGE_HEADER_1",
        )

#header2 = html.Div(
page_header_2 = dbc.Row(
            [
                dbc.Col(
                    html.P("Plots", className="HEADER_TEXT"),
                    width=3,
                    className = "HEADER_COLUMN",
                ),
                dbc.Col(
                    html.P("Data",  className="HEADER_TEXT"),
                    width=3,
                    className = "HEADER_COLUMN",
                ),
                 dbc.Col(
                    html.P("Logged in as pauser (log out)", className="HEADER_TEXT"),
                    width=6,
                    className = "HEADER_COLUMN",
                 ),
            ],
            className="PAGE_HEADER_2",
        )

#header2 = html.Div(
page_footer_1 = dbc.Row(
            [
                dbc.Col(
                    html.P("ACG", className="FOOTER_TEXT"),
                    width=4,
                    className = "FOOTER_COLUMN",
                ),
                dbc.Col(
                    html.P("Brown",  className="FOOTER_TEXT"),
                    width=4,
                    className = "FOOTER_COLUMN",
                ),
                 dbc.Col(
                    html.P("Version 0", className="FOOTER_TEXT"),
                    width=4,
                    className = "FOOTER_COLUMN",
                 ),
            ],
            className="PAGE_FOOTER",
        )

