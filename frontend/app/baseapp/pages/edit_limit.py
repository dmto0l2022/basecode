import dash
from dash import html, dcc

import libraries.formlibrary as fl

dash.register_page(__name__, path='/app/edit_limit')

newplot_row = fl.newplot_form

layout = newplot_row
