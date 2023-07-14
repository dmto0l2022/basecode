import dash
from dash import html, dcc, callback, Output, Input
from dash import dash_table, no_update
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import json
import requests

api_container = "container_api_1:8004"


#import formlibrary as fl


#############

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

dash.register_page(__name__, path='/list_user_plots')

#### list user plots

list_user_plots_form_title = html.Div(html.P(children='List User Plots', className = "NOPADDING_CONTENT FORM_TITLE"))

list_user_plots_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='List User Plots', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

next_button =  html.Div(dbc.Button("Next",  id="list_user_plots_next_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="list_user_plots_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")


list_user_plots_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_user_plots_form_title,
     list_user_plots_form_content,
     next_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

##########################################



###

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
#print(data_frame)

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

layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
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
        next_button,
        cancel_button
    ],
    className="row"
)


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



#########################################
@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("list_user_plots_next_button_id", "n_clicks"),
    Input("list_user_plots_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    #msg = prop_id
    if "list_user_plots_next_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        href_return = dash.page_registry['pages.show_user_plot']['path']
        return href_return
    elif "list_user_plots_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        href_return = dash.page_registry['pages.home']['path']
        return href_return
    else:
        href_return = dash.page_registry['pages.home']['path']
        return href_return
