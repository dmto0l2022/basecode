# This Code was written by Ann Marie - a Plotly Forum Moderator
from dash import Dash, dcc, html, Input, Output, dash_table, no_update  # Dash version >= 2.0.0
import pandas as pd
import plotly.express as px
import json
import requests
###

import requests
import json

api_container = "container_api_backend_1:8004"

class MakeApiCall():

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

    '''def get_user_data(self, api, parameters):
        response = requests.get(f"{api}", params=parameters)
        if response.status_code == 200:
            print("sucessfully fetched the data with parameters provided")
            self.formatted_print(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
    '''
    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
    '''
    def __init__(self, api):
        # self.get_data(api)

        parameters = {
            "username": "kedark"
        }
        self.get_user_data(api, parameters)
    '''
###

def DeleteRow(plotid_in):
    params = {'plotid': plotid_in}
    url = "http://" + api_container + "/plots/delete/"
    requests.post(url, params=params)

def RefreshTableData():
    url = "http://" + api_container + "/plots/getall/"
    r = requests.get(url,headers={'Accept': 'application/json'})
    response_data = r.json()
    updated_data_frame = pd.DataFrame(response_data)
    updated_data_frame['create'] = "create"
    updated_data_frame['read'] = "read"
    updated_data_frame['update'] = "update"
    updated_data_frame['delete'] = "delete"
    updated_data_ret = updated_data_frame.to_dict('records')
    return updated_data_ret
    

app = Dash(__name__, requests_pathname_prefix='/wsgi_app2/')

##data_request = requests.get('/plots/getall')
#url = "http://10.154.0.20:8004/plots/getall/"
#url = "http://localhost:8002/todo/list/1"
#data_request = requests.get(url="http://0.0.0.0:8002/todo/list/1")
##url = "http://dev4.dmtools.info:8002/todo/list/1"
#url = "http://10.154.0.20:8004/todo/list/1"
##10.154.0.20

url = "http://" + api_container + "/plots/getall/"
r = requests.get(url, 
                 headers={'Accept': 'application/json'})
response_data = r.json()
data_frame = pd.DataFrame(response_data)
#data_request = requests.get(url=url)
#text = json.dumps(data_request, sort_keys=True, indent=4)
#print(text)
#MakeApiCall().get_data(url)
##data_request = requests.get(url)
#print(data_request)
#data_frame = pd.read_json(response_data, orient='records')
#data_frame = pd.DataFrame(response_data)
##print(data_frame)
dff = data_frame.copy()
##df = px.data.gapminder()
##df["id"] = df.index
dff["id"] = dff.index
# print(df.head(15))
##dff = df[df.year == 2007].copy()
dff['create'] = "create"
dff['read'] = "read"
dff['update'] = "update"
dff['delete'] = "delete"
#columns = ["country", "continent", "lifeExp", "pop", "gdpPercap", "create", "read", "update", "delete"]
columns = ["id", "plotid", "name", "create", "read", "update", "delete"]
#initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}
initial_active_cell = {"row": 0, "column": 0, "column_id": "plotid", "row_id": 0}

app.layout = html.Div(
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


@app.callback(
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
    plotid = dff.at[row, "plotid"]
    print(plotid)

    column = active_cell["column"]
    print(f"column: {column}")
    print("---------------------")
    
    cell_value = dff.iat[active_cell['row'], active_cell['column']]
    
    if cell_value == 'delete':
        DeleteRow(plotid)
        updated_data = RefreshTableData()
            
    ##http://127.0.0.1:5000/query-example?plotid=Python
    return_data = row, " ", column, " ",cell_value, " ", plotid
    return return_data, updated_data ##country

##json.dumps(list(active_cell))
