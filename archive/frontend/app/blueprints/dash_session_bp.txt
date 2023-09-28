# https://community.plotly.com/t/use-flask-session/17949/4
# For other user reference:

from flask import Blueprint, render_template, redirect, request, session

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password

from flask_security.models import fsqla_v3 as fsqla

from flask_login import current_user

dash_session_bp = Blueprint('dash_session_bp', __name__)

def create_layout():
    layout02 = html.Div([
    html.H3(‘App 1’),
    dcc.Dropdown(
        id=‘app-1-dropdown’,
        options=[
        {‘label’: ‘App 1 - {}’.format(i), ‘value’: i} for i in [
        ‘NYC’, ‘MTL’, ‘LA’
        ]
        ],
        value=session[‘app-1-display-val-session’]
        ),
    html.Div(id=‘app-1-display-value’)
    ])
    return layout02

@dash_session_bp.server.route(’/’)

