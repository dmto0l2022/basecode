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

import requests
import json

fastapi_url_all = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/user_api_keys" ## multiple limit operations
fastapi_url_one = "http://container_fastapi_about_1:8016/dmtool/fastapi_about/internal/about/user_api_key/" ## single limit operations
internal_header={'dmtool-userid':'999'}

dash.register_page(__name__, path='/list_all_keys')
page_name = "list_all_keys"
page_title = 'List All Keys'
baseapp_prefix = '/application/baseapp'

### table data
table_column_names=['id','user_id','api_key','public_key', 'created_at','modified_at','ceased_at','edit','cease','delete']
main_table_id = 'user_api_keys_table_main'

## table_format
conditional_column_widths = [{'if': {'column_id': 'id'},
             'width': '2%'},
            {'if': {'column_id': 'user_id'},
             'width': '2%'},
            {'if': {'column_id': 'api_key'},
             'width': '25%'},
            {'if': {'column_id': 'public_key'},
             'width': '25%'},
            {'if': {'column_id': 'created_at'},
             'width': '5%'},
            {'if': {'column_id': 'modified_at'},
             'width': '5%'},
            {'if': {'column_id': 'ceased_at'},
             'width': '5%'},
            {'if': {'column_id': 'edit'},
             'width': '2%'},
            {'if': {'column_id': 'cease'},
             'width': '2%'},
            {'if': {'column_id': 'delete'},
             'width': '2'}]

#### list all keys

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#edit_button =  html.Div(dbc.Button("Edit", id="list_all_limits_edit_button_id", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="list_all_limits_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

##########################################################

table_heights = 120
row_height = '13px'
font_size = '12px'

'''
class MakeApiCall():

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
            
    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
'''
###

def DeleteRow(key_in):
    delete_url = fastapi_url_one + str(key_in)
    requests.delete(delete_url, headers=internal_header)

def CeaseRow(key_in):
    cease_url = fastapi_url_one + str(key_in)
    print('cease >>' + str(key_in))
    requests.put(cease_url, headers=internal_header)


def RefreshTableData():
    url = fastapi_url_all
    response_data_frame = pd.DataFrame()
    try:
        r = requests.get(url, headers=internal_header)
        response_data = r.json()
        print('response data')
        print('===================')
        print(response_data)
        print('===================')
        response_data_frame = pd.DataFrame(response_data)
    except:
        a = 1
    
    if response_data_frame.empty:
        empty_data = [table_column_names]
        updated_data_frame_ret = pd.DataFrame(data=empty_data, columns=table_column_names)
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
    else:
        lst = table_column_names
        updated_data_frame_ret = response_data_frame[response_data_frame.columns.intersection(lst)]
        updated_data_frame_ret = updated_data_frame_ret[lst]
        #updated_data_frame_ret['create'] = "create"
        updated_data_frame_ret['edit'] = "edit"
        updated_data_frame_ret['cease'] = "cease"
        #updated_data_frame_ret['update'] = "update"
        updated_data_frame_ret['delete'] = "delete"
        updated_data_dict_ret = updated_data_frame_ret.to_dict('records')
    return updated_data_dict_ret, updated_data_frame_ret, column_names


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

    table_data_dict, table_data_frame, table_column_names = RefreshTableData()
    
    user_api_keys_table = dash_table.DataTable(
        id= main_table_id,
        data=table_data_dict,
        columns=[{"name": c, "id": c} for c in table_column_names],
        fixed_rows={'headers': True},
        #fixed_rows={'headers': True},
        #page_size=5,
        filter_action='none',
        #row_selectable='multi',
        #selected_rows=[],
    
        style_cell={'textAlign': 'left','padding': '0px','font_size': font_size,
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'border': '1px solid black',
                        #'height': 'auto'
                        'height': row_height,
                    },
         css=[
                    {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of body rows
                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"}
                    ],
        
        #style_table={'height': '75vh',},
        ## 'user_id','secret_key','public_key', 'created_at','modified_at','ceased_at'
        style_cell_conditional=conditional_column_widths,
        #style_data={
        #    'whiteSpace': 'normal',
        #    'height': 'auto',
        #},
        #style_header=style_header_var,
        #tooltip_data=[
        #    {
        #        column: {'value': str(value), 'type': 'markdown'}
        #        for column, value in row.items()
        #    } for row in data
        #],
        tooltip_duration=None,
        )
    
    ##########################
    #{
    #        'selector': '.dash-spreadsheet td div',
    #        'rule': '''
    #            line-height: 12px;
    #            max-height: 12px; min-height: 12px; height: 12px;
    #            display: block;
    #            overflow-y: hidden;
    #        '''
    #    },
    
    ##########################
    
    
    '''
    table_layout = html.Div(
        [
            html.Div(
                [
                    dash_table.DataTable(
                        id="table",
                        columns=[{"name": c, "id": c} for c in column_names],
                        data=table_data_frame_initial.to_dict("records"),
                        page_size=10,
                        sort_action="native",
                        active_cell=initial_active_cell,
                    ),
                ],
                style={"margin": 50},
                className="five columns"
            ),
            html.Div(id="output-div", className="six columns"),
        ],
        className="row"
    )
    '''
    
    table_layout = html.Div(
        [
            html.Div(children="Table Title", className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(
                [
                    user_api_keys_table
                ],
                className="NOPADDING_CONTENT"
            ),
            html.Div(children="Debug Output", className="NOPADDING_CONTENT TABLE_TITLE"),
            html.Div(id=page_name+"output-div", children="Debug Output Here", className="NOPADDING_CONTENT"),
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
    [Output(page_name+"output-div", "children"), Output('user_api_keys_table_main','data')], Input("user_api_keys_table_main", "active_cell"),
)
def cell_clicked(active_cell):
    
    updated_data_dict, updated_data_frame, column_names = RefreshTableData()
    
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
        DeleteRow(id)
        updated_data_dict, updated_data_frame, column_names = RefreshTableData()

    if cell_value == 'cease':
        CeaseRow(id)
        updated_data_dict, updated_data_frame, column_names = RefreshTableData()
            
    ##http://127.0.0.1:5000/query-example?plotid=Python
    return_data = row, " ", column, " ",cell_value, " ", id
    return return_data, updated_data_dict

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
