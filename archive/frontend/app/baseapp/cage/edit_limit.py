import dash
from dash import html, dcc

#import libraries.formlibrary as fl
from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/edit_limit')

new_plot_row = fl.new_plot_form

layout = new_plot_row
