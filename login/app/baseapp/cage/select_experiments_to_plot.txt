import dash

from dash import dcc
from dash import html
from dash import callback
from dash import Output, Input
from dash import callback_context
from dash import dash_table

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, Input, Output, callback, State

#from jupyter_dash import JupyterDash

import dash_bootstrap_components as dbc

import pandas as pd

import plotly.express as px
from itertools import cycle

# colors
palette = cycle(px.colors.qualitative.Bold)

from app.baseapp.dashboard_libraries import all_data_tables as adt

#from dashboard_libraries import all_data_tables as adt
dashdataandtables = adt.DashDataAndTables()

dashdataandtables.limits_table_df.set_index('id', inplace=True, drop=False)
#dashdataandtables.limits_table_df['expid'] = dashdataandtables.limits_table_df['limit_id'] 
#dashdataandtables.limits_table_df

#####

row1 =  dbc.Row([
        dbc.Col(
            [
                dashdataandtables.limit_types_table
            ],
            width=2,
            ),
        dbc.Col(
            [
                dashdataandtables.experiments_table
            ],
            width=2,
            ),
        dbc.Col(
            [
                dashdataandtables.result_types_table
            ],
            width=2,
            ),
        dbc.Col(
            [
                dashdataandtables.spin_dependency_table
            ],
            width=2,
            ),
       dbc.Col(
            [
                dashdataandtables.years_table
            ],
            width=2,
            ),
       dbc.Col(
            [
                dashdataandtables.greatest_hit_table
            ],
            width=2,
            ),
])
    

row2 = dbc.Row([dbc.Col(
            [
                dashdataandtables.limits_table
            ],
            width=12,),
               ])

row2_debug = dbc.Row([dbc.Col(
            [
                dashdataandtables.debug_dropdown_table
            ],
            width=12,),
               ])

#row3 = dbc.Row([dbc.Col(html.Div('List Here',id='tbl_out'),width=12,),])

row3_1 = dbc.Row([dbc.Col(
            [
                dashdataandtables.limits_table
            ],
            width=10,),
               ], className ="TABLE_ROW NOPADDING")


row3_1_debug = dbc.Row([dbc.Col(
            [
                dashdataandtables.debug_dropdown_table
            ],
            width=10,),
               ], className ="TABLE_ROW NOPADDING")

row3_2 = dbc.Row([dbc.Col(
            [
                dashdataandtables.plots_table
            ],
            width=10,),
               ],className ="TABLE_ROW NOPADDING")

row4 = html.Div([dcc.Store(id='plot_expids')])
'''
form = dbc.Container(
    children=[dbc.Row(
    [
        row1,
        row2,
        #row2_debug,
        row3_1,
        row4
    ])],
    
)
'''

#####

#import formlibrary as fl

dash.register_page(__name__, path='/select_experiments_to_plot')

#### select experiments to plot

select_experiments_to_plot_form_title = html.Div(html.P(children='Select Experiments to Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

select_experiments_to_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Select Experiments to Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

next_button =  html.Div(dbc.Button("Next",  id="next_button_select_experiments_to_plot_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button_select_experiments_to_plot_id", color="secondary"), className = "FORM_CANCEL_BUTN")


select_limits_to_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     select_experiments_to_plot_form_title,
     select_experiments_to_plot_form_content,
     next_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

maincolumn = dbc.Col(
            [
                row1,
                row3_1,
                #row3_1_debug,
                row3_2,
                next_button,
                cancel_button
            ],
            width=10,)

maindiv =  html.Div(className="row ALL_ROW NOPADDING",children=[maincolumn])

layout4 = html.Div([maindiv],
                   className="container-fluid MASTER_CONTAINER_STYLE",
                  )

layout = layout4

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("next_button_select_experiments_to_plot_id", "n_clicks"),
    Input("cancel_button_select_experiments_to_plot_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "next_button_select_experiments_to_plot_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.style_plot_and_traces']['path']
        return href_return
    elif "cancel_button_select_experiments_to_plot_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return

@callback(
    Output('limits_table_main', 'data'),
    #Output('debug_dropdown_table', 'data'),
    #Output(component_id='tbl_out', component_property='children'),
    #
    Input('years_table', 'active_cell'),
    Input('years_table', 'derived_virtual_selected_rows'),
    #
    Input('limit_types_table', 'active_cell'),
    Input('limit_types_table', 'derived_virtual_selected_rows'),
    #
    Input('experiments_table', 'active_cell'),
    Input('experiments_table', 'derived_virtual_selected_rows'),
    #
    Input('result_types_table', 'active_cell'),
    Input('result_types_table', 'derived_virtual_selected_rows'),
    #
    Input('spin_dependency_table', 'active_cell'),
    Input('spin_dependency_table', 'derived_virtual_selected_rows'),
    #
    Input('greatest_hit_table', 'active_cell'),
    Input('greatest_hit_table', 'derived_virtual_selected_rows'),
    )
def update_graphs(
    active_cell_years,
    derived_virtual_selected_rows_years,
    #
    active_cell_limit_types,
    derived_virtual_selected_rows_limit_types,
    #
    active_cell_experiments,
    derived_virtual_selected_rows_experiments,
    #
    active_cell_resulttypes,
    derived_virtual_selected_rows_result_types,
    #
    active_cell_spin_dependency,
    derived_virtual_selected_rows_spin_dependence,
    #
    active_cell_greatest_hit,
    derived_virtual_selected_rows_greatest_hit,
    
):
    
    try:
        dfs = [
            dashdataandtables.years_df.loc[derived_virtual_selected_rows_years],
            dashdataandtables.limit_types_df.loc[derived_virtual_selected_rows_limit_types],
            dashdataandtables.experiments_df.loc[derived_virtual_selected_rows_experiments],
            dashdataandtables.result_types_df.loc[derived_virtual_selected_rows_result_types],
            dashdataandtables.spin_dependence_df.loc[derived_virtual_selected_rows_spin_dependence],
            dashdataandtables.greatest_hit_df.loc[derived_virtual_selected_rows_greatest_hit]
        ]
        non_empty_dfs = [df for df in dfs if not df.empty]
        all_filters_df = pd.concat(non_empty_dfs)
    except:
        all_filters_df = pd.DataFrame()
    
    # https://stackoverflow.com/questions/60964165/ignore-empty-dataframe-when-merging
    
    unfiltered_df = dashdataandtables.limits_table_df.copy()
    #df.drop(df.index , inplace=True)
    
    filtered_df = unfiltered_df.drop(unfiltered_df.index)
    #filtered_df
    
    if all_filters_df.empty:
        filtered_df = unfiltered_df
    else:
        for index, row in all_filters_df.iterrows():
            #print(row['variable'], row['value'])
            matching_records = unfiltered_df[unfiltered_df[row['variable']] == row['value']]
            filtered_df = pd.concat([filtered_df, matching_records])
            #filtered_df = matching_records
            #filtered_df = filtered_df[filtered_df[row['variable']] == row['value']] 
    
    filtered_df = filtered_df.drop_duplicates()
    #filtered_df
   
    data1 = all_filters_df.to_dict("records")
    data2 = filtered_df.to_dict("records")
    print(data1)
    #data1=dff2.to_dict("records")
    #list_output = str(selectedcontinent_list) if selectedcontinent_list else "Click the table"
    return data2 #, list_output


@callback(
    Output('plots_table', 'data'),
    [Input('limits_table_main', 'active_cell'),Input('plots_table', 'active_cell')],
    [State('plots_table', 'data')])
def trigger_fork(active_cell_exp,active_cell_plot,data_in):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_id)
    if triggered_id == 'limits_table_main':

        selected_rowid = active_cell_exp['row_id']
        selected_row = dashdataandtables.\
                limits_table_df[dashdataandtables.limits_table_df['id']==active_cell_exp['row_id']]
        selected_row  = selected_row[['id','data_reference','data_reference','data_label']]
        #data_out=plots_todo_df.to_dict("records")
        record=selected_row.to_dict("records")[0]
        #print(type(record))
        #print(record)
        #record = {columns[i]: arg for i, arg in enumerate(list(args))}
        # If the record (identified by user_key) already exists, update it.
        #try:
        #    #record_index = [record[selected_rowid] for record in data_in].index(record[selected_rowid])
        #    record_index = [record[selected_rowid] for record in data_in].index(record[selected_rowid])
        #    data_in[record_index] = record
        # Otherwise, append it.
        #except ValueError:
        #    data_in[selected_rowid] = record
        #dictlen = len(data_in)
        #data_in[selected_rowid] = record
        data_in.append(record)
        #data_in = record
        # Return the updated data.
        #return data

        #selected_row = limits_table_df[limits_table_df['expid']==active_cell['row_id']]
        #plots_todo_df= selected_row.copy()
        #data_out=plots_todo_df.to_dict("records")
        #data_out=selected_row.to_dict("records")

    elif triggered_id == 'plots_table':
        #selected_rowid = active_cell_plot['row']
        #print(data_in[selected_rowid])
        print(active_cell_plot)
        #data_in = data_in.pop(active_cell_plot['row'])
        print(data_in)
    
    return data_in

