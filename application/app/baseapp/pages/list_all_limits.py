import dash

from dash import Dash
from dash import dcc, html
from dash import Input, Output, callback
from dash import dash_table, no_update  # Dash version >= 2.0.0
import pandas as pd
import plotly.express as px
import json
import requests
import dash_bootstrap_components as dbc

from app.baseapp.libraries import formlibrary as fl
from app.baseapp.libraries import main_table_editor as mte

#from app.baseapp.dashboard_libraries import get_limit_data as gld


import requests
import json

fastapi_url_limits = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limits" ## multiple limit operations
fastapi_url_limit = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limit" ## single limit operations

dash.register_page(__name__, path='/list_all_limits')
page_name = "list_all_limits"
baseapp_prefix = '/application/baseapp'

page_name = "list_all_limits"
page_title = 'List All Limits'

table_meta_data_data = [
                        ['id', '2%'],
                        ['experiment', '2%'],
                        ['data_comment', '18%'],
                        ['data_label', '18%'],
                       ]

single_api = 'limit'
multiple_api = 'limits'

#### list all limits

list_all_limits_form_title = html.Div(html.P(children='List All Limits', className = "NOPADDING_CONTENT FORM_TITLE"))

list_all_limits_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='List All Limits', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

edit_button =  html.Div(dbc.Button("Edit", id="list_all_limits_edit_button_id", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="list_all_limits_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

##########################################################

table_heights = 120
row_height = '13px'
font_size = '12px'

dmtool_user_id = '0' ### default - no user should be given 0
internal_header={'dmtool-userid':'0'}

## create an empty table to be refreshed by the callback
main_table_1 = mte.get_main_table(page_title,
                                 main_table_id,
                                 table_meta_data_data,
                                 row_height,
                                 table_font_size,
                                 fastapi_url_all,
                                 fastapi_url_one,
                                 dmtool_user_id)



def DeleteRow(limit_in):
    delete_url = fastapi_url_limit + "/" + str(limit_in)
    requests.delete(delete_url)




#table_data_dict_initial, table_data_frame_initial, column_names = RefreshTableData()
initial_active_cell = {"row": 0, "column": 0, "column_id": "id", "row_id": 0}

###########################################################

'''
list_all_limits_form = html.Div(
    [dcc.Location(id="url", refresh=True),
     list_all_limits_form_title,
     list_all_limits_form_content,
     edit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''
    
# limits_df = pd.read_sql_query(limits_sql, self.engine)
# limits_df['rowid'] = self.limits_df.index

# limits_table_df = limits_df[['id','limit_id','spin_dependency',
#                         'experiment','official','greatest_hit','data_label',
#                         'result_type','data_reference','year']].copy()


###########################################################################

def get_layout():

    style_header_var={ 'backgroundColor': 'black','color': 'white'}
    dmtool_user_id = 16384
    main_table_1 = mte.get_main_table(page_title,
                                 main_table_id,
                                 table_meta_data_data,
                                 row_height,
                                 table_font_size,
                                 fastapi_url_all,
                                 fastapi_url_one,
                                 dmtool_user_id)
  
    #main_table_1.RefreshTableData()
    
    table_layout = html.Div(
        [
            html.Div(children="Table Title", className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(
                [
                    main_table_1.dash_table_main
                ],
                className="NOPADDING_CONTENT"
            ),
            html.Div(children="Debug Output", className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(id="output-div", children="Debug Output Here", className="NOPADDING_CONTENT"),
        ],
        className="row NOPADDING_CONTENT"
    )

    return table_layout
    
#no_output = html.Div([limits_table], className="NOPADDING_CONTENT")
        
##className="PAGE_CONTENT",)

layout = get_layout


#layout = table_layout
#layout = list_all_limits_form

#layout = no_output


@callback(
    [Output("output-div", "children"), Output('limits_table_main','data')], Input("limits_table_main", "active_cell"),
)
def cell_clicked(active_cell):
    
    main_table_1.RefreshTableData()
    
    if active_cell is None:
        return no_update

    #row = active_cell["row_id"]
    row_id = active_cell["row_id"]
    #print(f"row_id: {row_id}")
    
    #row = active_cell["row_id"]
    column_id = active_cell["column_id"]
    #print(f"column_id: {column_id}")
    
    row = active_cell["row"]
    #print(f"row: {row}")

    #country = df.at[row, "country"]
    #print(country)
    id = updated_data_frame.at[row, "id"]
    #print("id >> ", id)

    column = active_cell["column"]
    #print(f"column: {column}")
    #print("---------------------")
    
    cell_value = updated_data_frame.iat[active_cell['row'], active_cell['column']]

    #print("cell_value > ", cell_value)

    #print("---------------------")

    #print("table data frame")
    #print("---------------------")

    #print(updated_data_frame)

    #print("---------------------")

    
    if cell_value == 'delete':
        main_table_1.DeleteRow(id)
            
    ##http://127.0.0.1:5000/query-example?plotid=Python
    return_data = row, " ", column, " ",cell_value, " ", id
    return return_data, main_table_1.main_table_data_dict

##json.dumps(list(active_cell))


'''

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("list_all_limits_edit_button_id", "n_clicks"),
    Input("list_all_limits_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "list_all_limits_edit_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.show_limit']['path']
        return href_return
    elif "list_all_limits_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
'''
