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

#api_container = "container_api_1:8004"
fastapi_orm_url = "http://35.214.16.124:8008"
fastapi_orm_url_api = fastapi_orm_url +"/apiorm"

dash.register_page(__name__, path='/list_all_limits')


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

def DeleteRow(limit_in):
    url = fastapi_orm_url_api + "/limit/"
    delete_url = fastapi_orm_url_api + "/limit/" + str(limit_in)
    requests.delete(delete_url)

def RefreshTableData():
    url = fastapi_orm_url_api + "/limit/"
    r = requests.get(url)
    response_data = r.json()
    print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    lst = ['id','experiment','data_comment']
    updated_data_frame = response_data_frame[response_data_frame.columns.intersection(lst)]
    updated_data_frame = updated_data_frame[lst]
    updated_data_frame['create'] = "create"
    updated_data_frame['read'] = "read"
    updated_data_frame['update'] = "update"
    updated_data_frame['delete'] = "delete"
    updated_data_ret = updated_data_frame.to_dict('records')
    return updated_data_ret


##data_request = requests.get('/plots/getall')
#url = "http://10.154.0.20:8004/plots/getall/"
#url = "http://localhost:8002/todo/list/1"
#data_request = requests.get(url="http://0.0.0.0:8002/todo/list/1")
##url = "http://dev4.dmtools.info:8002/todo/list/1"
#url = "http://10.154.0.20:8004/todo/list/1"
##10.154.0.20

url = fastapi_orm_url_api + "/limit/"
r = requests.get(url)
response_data = r.json()
response_data_frame = pd.DataFrame(response_data)
lst = ['id','experiment','data_comment']
table_dataframe = response_data_frame[response_data_frame.columns.intersection(lst)]
table_dataframe = table_dataframe[lst]

print(table_dataframe)

#data_request = requests.get(url=url)
#text = json.dumps(data_request, sort_keys=True, indent=4)
#print(text)
#MakeApiCall().get_data(url)
##data_request = requests.get(url)
#print(data_request)
#data_frame = pd.read_json(response_data, orient='records')
#data_frame = pd.DataFrame(response_data)
##print(data_frame)
dff = table_dataframe.copy()
##df = px.data.gapminder()
##df["id"] = df.index
#dff["id"] = dff.index
# print(df.head(15))
##dff = df[df.year == 2007].copy()
dff['create'] = "create"
dff['read'] = "read"
dff['update'] = "update"
dff['delete'] = "delete"
#columns = ["country", "continent", "lifeExp", "pop", "gdpPercap", "create", "read", "update", "delete"]
columns = ["id", "experiment ", "data_comment", "create", "read", "update", "delete"]
#initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}
initial_active_cell = {"row": 0, "column": 0, "column_id": "plotid", "row_id": 0}

###########################################################

list_all_limits_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_all_limits_form_title,
     list_all_limits_form_content,
     edit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


table_layout = html.Div(
    [
        html.Div(
            [
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": c, "id": c} for c in columns],
                    data=dff.to_dict("records"),
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

layout = table_layout

@callback(
    [Output("output-div", "children"), Output('table','data')], Input("table", "active_cell"),
)
def cell_clicked(active_cell):
    
    updated_data = RefreshTableData()
    
    if active_cell is None:
        return no_update

    #row = active_cell["row_id"]
    row_id = active_cell["row_id"]
    print(f"row_id: {row_id}")
    
    #row = active_cell["row_id"]
    column_id = active_cell["column_id"]
    print(f"column_id: {column_id}")
    
    row = active_cell["row"]
    print(f"row: {row}")

    #country = df.at[row, "country"]
    #print(country)
    id = dff.at[row, "id"]
    print(id)

    column = active_cell["column"]
    print(f"column: {column}")
    print("---------------------")
    
    cell_value = dff.iat[active_cell['row'], active_cell['column']]

    print("cell_value > ", cell_value)

    print("---------------------")

    print("table data frame")
    print("---------------------")

    print(dff)

    print("---------------------")

    
    if cell_value == 'delete':
        DeleteRow(id)
        updated_data = RefreshTableData()
            
    ##http://127.0.0.1:5000/query-example?plotid=Python
    return_data = row, " ", column, " ",cell_value, " ", id
    return return_data, updated_data ##country

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
