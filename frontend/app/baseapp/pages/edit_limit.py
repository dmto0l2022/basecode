import dash
from dash import html, dcc

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/edit_limit')

newplot_row = fl.newplot_form

layout = newplot_row
