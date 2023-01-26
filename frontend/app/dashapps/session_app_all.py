import flask
from flask import Flask, flash, render_template, session
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, no_update

server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/session_app/'
)

app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash',),
    html.H1(
        id='div3',
        children='Input',),
   html.H1(
        id='store_client_id',
        children='Session ID Here'),
])

## that session is then available inside callbacks.

app.callback(
   [Output('store_client_id', 'data')],
   [Input('div3', 'children')])
def update_user(children):
    try:
         s = session.get('sessionid', None)
         return s
    except:
        return -10
