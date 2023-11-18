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

fastapi_url_all = "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limits" ## multiple limit operations
fastapi_url_one= "http://container_fastapi_data_1:8014/dmtool/fastapi_data/internal/data/limit" ## single limit operations

dash.register_page(__name__, path='/list_all_limits')
baseapp_prefix = '/application/baseapp'

page_name = "list_all_limits"
page_title = 'List All Limits'
main_table_id = page_name + '_main_table_id'

table_meta_data_data = [
                        ['id', '3%'],
                        ['experiment', '3%'],
                        ['data_comment', '44%'],
                        ['data_label', '44%'],
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

button_styling_1 = {'font-size': '12px',
                  'width': '70px',
                  'display': 'inline-block', 
                  'margin-bottom': '1px',
                  'margin-right': '0px',
                  'margin-top': '1px',
                  'height':'19px',
                  'verticalAlign': 'center'}

new_button =  html.Button("New", id= page_name + "new_button_id", style=button_styling_1)
save_button =  html.Button("Save", id= page_name + "save_button_id", style=button_styling_1)
cancel_button =  html.Button("Cancel",  id=page_name + "cancel_button_id", style=button_styling_1)
home_button =  html.Button("Home",  id=page_name + "home_button_id", style=button_styling_1)


##########################################################

table_height = '100vh'
page_size = 54 ## rows of data
row_height = '13px'
table_font_size = '12px'

dmtool_user_id = '1' ### default - no user should be given 0
internal_header={'dmtool-userid':'1'}

## create an empty table to be refreshed by the callback
main_table_1 = mte.get_main_table(page_title,
                                 main_table_id,
                                 table_meta_data_data,
                                 table_height,
                                 page_size,
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

debug_output = html.Div(children=[html.Div(children="Debug Output", className="NOPADDING_CONTENT OUTPUT_CELL_TITLE"),
                                      html.Div(id=page_name+"cell-output-div", children="Cell Output Here", className="NOPADDING_CONTENT OUTPUT_CELL"),
                                      html.Div(id=page_name+"button-output-div", children="Button Output Here", className="NOPADDING_CONTENT OUTPUT_CELL")],
                                      className="PAGE_DEBUG_CONTENT")


###########################################################################

def get_layout():

    style_header_var={ 'backgroundColor': 'black','color': 'white'}
    dmtool_user_id = 1
    main_table_1 = mte.get_main_table(page_title,
                                 main_table_id,
                                 table_meta_data_data,
                                 table_height,
                                 page_size,
                                 row_height,
                                 table_font_size,
                                 fastapi_url_all,
                                 fastapi_url_one,
                                 dmtool_user_id)
  
    #main_table_1.RefreshTableData()
    
    table_layout_1 = html.Div(
        [
            dcc.Location(id= page_name + "url", refresh=True), ## important to allow redirects
            html.Div(children= page_title, className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(
                [
                    main_table_1.dash_table_main
                ],
                className="NOPADDING_CONTENT PAGE_FULL_TABLE_CONTENT"
            ),
            debug_output,
            html.Div(id= page_name + "page_buttons", children=[new_button,save_button,cancel_button,home_button], className="PAGE_FOOTER_BUTTONS"),
        ],
        className="NOPADDING_CONTENT"
    )

    #table_layout = main_table_1.dash_table_main
    table_layout = table_layout_1
  
    return table_layout
    
#no_output = html.Div([limits_table], className="NOPADDING_CONTENT")
        
##className="PAGE_CONTENT",)

layout = get_layout


#layout = table_layout
#layout = list_all_limits_form

#layout = no_output


@callback(
    [Output(page_name+"cell-output-div", "children"), Output(main_table_id,'data')], Input(main_table_id, "active_cell"),
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
