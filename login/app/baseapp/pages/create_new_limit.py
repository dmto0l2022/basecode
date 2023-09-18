import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import json
import requests

import base64

import pandas as pd

from app.baseapp.libraries import formlibrary as fl

import xml.etree.ElementTree as ET

baseapp_prefix = '/login/baseapp'

dash.register_page(__name__, path='/create_new_limit')

fastapi_url = "http://container_fastapi_alembic_1:8014/alembic/limit"

'''
ID List
========
plot_name_form_field_id
x_range_lower_form_field_id
x_range_upper_form_field_id
scale_form_field_id
trace_id_form_field_id
trace_name_form_field_id
trace_color_form_field_id
symbol_form_field_id
line_style_form_field_id
trace_fill_color_form_field_id
remove_site_address_form_field_id
upload_xml_file_form_field_id
data_label_form_field_id
data_reference_form_field_id
data_comment_form_field_id
experiment_form_field_id
date_of_announcement_form_field_id
date_of_run_start_form_field_id
date_of_run_end_form_field_id
year_form_field_id
x_rescale_form_field_id
y_rescale_form_field_id
y_unit_form_field_id
x_unit_form_field_id
data_values_form_field_id
result_type_form_field_id
limit_type_form_field_id
spin_dependency_form_field_id
measurement_type_form_field_id
public_limit_form_field_id
other_users_form_field_id
official_form_field_id
greatest_hit_form_field_id
upload_xml_file_form_field_id
'''

#### New Limit Class

class Limit_class:
    i = 12345
    def __init__(self):
        self.data = []
        self.data_values = ''
        self.data_comment = ''
        self.data_label = ''
        self.data_reference = ''
        self.date_of_announcement = ''
        self.date_of_run_end = ''
        self.date_of_run_start = ''
        self.default_color = ''
        self.default_style = ''
        self.experiment = ''
        self.public = ''
        self.result_type = ''
        self.spin_dependency = ''
        self.x_rescale = ''
        self.x_units = ''
        self.y_rescale = ''
        self.y_units = ''
        self.year = ''
        ##self.json_put = ''
    
    def find_xml_text(self,root_in,tag_in):
        dv_find = root_in.findall(tag_in)
        return dv_find[0].text
    
    def set_values(self,root_in):
        self.data_values = self.find_xml_text(root_in,'data-values')
        self.data_comment = self.find_xml_text(root_in,'data-comment')
        self.data_label = self.find_xml_text(root_in,'data-label')
        self.data_reference = self.find_xml_text(root_in,'data-reference')
        self.date_of_announcement = self.find_xml_text(root_in,'date-of-announcement')
        self.date_of_run_end = self.find_xml_text(root_in,'date-of-run-end')
        self.date_of_run_start = self.find_xml_text(root_in,'date-of-run-start')
        self.default_color = self.find_xml_text(root_in,'default-color')
        self.default_style = self.find_xml_text(root_in,'default-style')
        self.experiment = self.find_xml_text(root_in,'experiment')
        self.public = self.find_xml_text(root_in,'public')
        self.result_type = self.find_xml_text(root_in,'result-type')
        self.spin_dependency = self.find_xml_text(root_in,'spin-dependency')
        self.x_rescale = self.find_xml_text(root_in,'x-rescale')
        self.x_units = self.find_xml_text(root_in,'x-units')
        self.y_rescale = self.find_xml_text(root_in,'y-rescale')
        self.y_units = self.find_xml_text(root_in,'y-units')
        self.year = self.find_xml_text(root_in,'year')
        #self.json_put = self.create_json()
    
    def f(self):
        return 'hello world'
    
    '''
    def create_json(self):
        json_str = {
          "spin_dependency": self.spin_dependency,
          "result_type": self.result_type,
          "measurement_type": "string",
          "nomhash": "string",
          "x_units":  self.x_units,
          "y_units": self.y_units,
          "x_rescale": self.x_rescale,
          "y_rescale": self.y_rescale,
          "default_color": self.default_color,
          "default_style": self.default_style,
          "data_values": self.data_values,
          "data_label": self.data_label,
          "file_name": "string",
          "data_comment":self.data_comment,
          "data_reference": self.data_reference,
          "creator_id": 2147483647,
          "experiment": self.experiment,
          "rating": 2147483647,
          "date_of_announcement":  self.date_of_announcement ,
          "public": self.public,
          "official":  self.official,
          "date_official": self.date_official,
          "greatest_hit": self.greatest_hit,
          "date_of_run_start": self.date_of_run_start,
          "date_of_run_end": self.date_of_run_end,
          "year": self.year
        }
        return json_str
        '''
    
      

save_button =  html.Div(dbc.Button("Save",  id="create_new_limit_save_button_id", color="secondary"), className = "FORM_CANCEL_BUTN",
                        n_clicks_timestamp=0)
#save_button =  html.Div(dbc.Button("Save",  id="9876_new_limit_save_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")


cancel_button =  html.Div(dbc.Button("Cancel",  id="create_new_limit_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN",
                          n_clicks_timestamp=0)
#cancel_button =  html.Div(dbc.Button("Cancel",  id="9876_new_limit_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#### create new Limit form

create_new_limit_form_title = html.Div(html.P(children='Create New Limit', className = "NOPADDING_CONTENT FORM_TITLE"))

Limit = Limit_class

load_limit_file_form = html.Div(
        [
        dcc.Location(id='url', refresh=True), ## very important for url output of callback
        fl.upload_xml_file_input_row,
        fl.data_values_input_row,
        fl.data_comment_input_row,
        fl.data_label_input_row,
        fl.data_reference_input_row,
        fl.date_of_announcement_input_row,
        fl.date_of_run_start_input_row,
        fl.date_of_run_end_input_row,
        fl.trace_color_input_row,
        fl.line_style_input_row,
        fl.experiment_input_row,
        fl.public_limit_input_row,
        fl.result_type_input_row,
        fl.spin_dependency_input_row,
        fl.x_rescale_input_row,
        fl.x_unit_input_row,
        fl.y_rescale_input_row,
        fl.y_unit_input_row,
        fl.year_input_row,
        save_button,
        cancel_button,
        html.Div(id='container', children='''here'''),
    ])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    stringToXML = ET.ElementTree(ET.fromstring(decoded))
    DMToolLimit = Limit_class()
    DMToolLimit.set_values(stringToXML)
    data_reference_out = DMToolLimit.data_reference
    print(stringToXML)
    #data_reference_out = find_xml_text(stringToXML,'data-reference')
    print(data_reference_out)
    return DMToolLimit

'''
create_new_limit_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Create New Limit', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

save_button =  html.Div(dbc.Button("Save",  id="create_new_limit_save_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="create_new_limit_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

create_new_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_limit_form_title,
     create_new_limit_form_content,
     save_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

layout = create_new_limit_form
'''

layout = load_limit_file_form

@callback(
            [Output('data_values_form_field_id', 'value'),
            Output('data_comment_form_field_id', 'value'),
            Output('data_label_form_field_id', 'value'),
            Output('data_reference_form_field_id', 'value'),
            Output('date_of_announcement_form_field_id', 'value'),
            Output('date_of_run_start_form_field_id', 'value'),
            Output('date_of_run_end_form_field_id', 'value'),
            Output('trace_color_form_field_id', 'value'),
            Output('line_style_form_field_id', 'value'),
            Output('experiment_form_field_id', 'value'),
            Output('public_limit_form_field_id', 'on'),
            Output('result_type_form_field_id', 'value'),
            Output('spin_dependency_form_field_id', 'value'),
            Output('x_rescale_form_field_id', 'value'),
            Output('x_unit_form_field_id', 'value'),
            Output('y_rescale_form_field_id', 'value'),
            Output('y_unit_form_field_id', 'value'),
            Output('year_form_field_id', 'value')],
            Input('upload_xml_file_form_field_id', 'contents')
            #State('upload-data', 'filename'),
            #State('upload-data', 'last_modified')
             )

def update_output(contents_in):
    print('hello during form update')
    #print(contents_in)
    #if list_of_contents is not None:
    #    children = [
    #        parse_contents(c, n, d) for c, n, d in
    #        zip(list_of_contents, list_of_names, list_of_dates)]
    try:
        DMToolLimit = parse_contents(contents_in)
    except:
        DMToolLimit = Limit_class() ## empty

    #print("Data Comment > " , DMToolLimit.data_comment)

    #print("Month of Announcement > ", DMToolLimit.date_of_announcement[0:7] + "01")
    
    return  [
            DMToolLimit.data_values,
            DMToolLimit.data_comment,
            DMToolLimit.data_label,
            DMToolLimit.data_reference,
            DMToolLimit.date_of_announcement,
            DMToolLimit.date_of_run_end,
            DMToolLimit.date_of_run_start,
            DMToolLimit.default_color,
            DMToolLimit.default_style,
            DMToolLimit.experiment,
            DMToolLimit.public,
            DMToolLimit.result_type,
            DMToolLimit.spin_dependency,
            DMToolLimit.x_rescale,
            DMToolLimit.x_units,
            DMToolLimit.y_rescale,
            DMToolLimit.y_units,
            DMToolLimit.year
        ]

@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input('data_values_form_field_id', 'value'),
    Input('data_comment_form_field_id', 'value'),
    Input('data_label_form_field_id', 'value'),
    Input('data_reference_form_field_id', 'value'),
    Input('date_of_announcement_form_field_id', 'value'),
    Input('date_of_run_start_form_field_id', 'value'),
    Input('date_of_run_end_form_field_id', 'value'),
    Input('trace_color_form_field_id', 'value'),
    Input('line_style_form_field_id', 'value'),
    Input('experiment_form_field_id', 'value'),
    Input('public_limit_form_field_id', 'on'),
    Input('result_type_form_field_id', 'value'),
    Input('spin_dependency_form_field_id', 'value'),
    Input('x_rescale_form_field_id', 'value'),
    Input('x_unit_form_field_id', 'value'),
    Input('y_rescale_form_field_id', 'value'),
    Input('y_unit_form_field_id', 'value'),
    Input('year_form_field_id', 'value'),
    Input("create_new_limit_save_button_id", "n_clicks"),
    Input("create_new_limit_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(
    data_values_in,
    data_comment_in,
    data_label_in,
    data_reference_in,
    date_of_announcement_in,
    date_of_run_start_in,
    date_of_run_end_in,
    trace_color_in,
    line_style_in,
    experiment_in,
    public_in,
    result_type_in,
    spin_dependency_in,
    x_rescale_in,
    x_units_in,
    y_rescale_in,
    y_units_in,
    year_in,
    button1,
    button2):
    #msg = "None of the buttons have been clicked yet"
    
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    '''
    print('-------------- prop id ---------------------')
    
    print(prop_id)

    print('data_values_in  >>',data_values_in)
    print('data_comment_in  >>',data_comment_in)
    print('data_label_in  >>',data_label_in)
    print('data_reference_in  >>',data_reference_in)
    print('date_of_announcement_in  >>',date_of_announcement_in)
    print('date_of_run_start_in  >>',date_of_run_start_in)
    print('date_of_run_end_in  >>',date_of_run_end_in)
    print('trace_color_in  >>',trace_color_in)
    print('line_style_in  >>',line_style_in)
    print('experiment_in  >>',experiment_in)
    print('public_in,  >>',public_in,)
    print('result_type_in  >>',result_type_in)
    print('spin_dependency_in  >>',spin_dependency_in)
    print('x_rescale_in  >>',x_rescale_in)
    print('x_units_in  >>',x_units_in)
    print('y_rescale_in  >>',y_rescale_in)
    print('y_units_in  >>',y_units_in)
    print('year_in  >>',year_in)
    '''
        
    '''
    data_comment_in  >> A descriptive comment
    data_label_in  >> What my data shows up under
    data_reference_in  >> where someone else can find the data 
    date_of_announcement_in  >> yyyy-mm-dd
    date_of_run_start_in  >> yyyy-mm-dd
    date_of_run_end_in  >> None
    trace_color_in  >> DkB
    line_style_in  >> Fill
    experiment_in  >> Your experiment's name as it shows up on the list or Theory
    public_in,  >> true
    result_type_in  >> Th or Exp
    spin_dependency_in  >> SI
    x_rescale_in  >> 1
    x_units_in  >> GeV
    y_rescale_in  >> 1e-36
    y_units_in  >> cm^2
    year_in  >> 2008
    '''
    #msg = prop_id
    if "create_new_limit_save_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        print("save button pressed")
        #href_return = dash.page_registry['pages.list_all_limits']['path']


        post_data = {
                  "spin_dependency": "string",
                  "result_type": "string",
                  "measurement_type": "string",
                  "nomhash": "string",
                  "x_units": "string",
                  "y_units": "string",
                  "x_rescale": "string",
                  "y_rescale": "string",
                  "default_color": "string",
                  "default_style": "string",
                  "data_values": "string",
                  "data_label": "string",
                  "file_name": "string",
                  "data_comment": "string",
                  "data_reference": "string",
                  "creator_id": 2147483647,
                  "experiment": "string",
                  "rating": 2147483647,
                  "date_of_announcement": "2023-09-06",
                  "public": True,
                  "official": True,
                  "date_official": "2023-09-06",
                  "greatest_hit": True,
                  "date_of_run_start": "2023-09-06",
                  "date_of_run_end": "2023-09-06",
                  "year": 2147483647
            }

        if public_in == "true":
            public_out = True
        else :
            public_out = False
        
        new_limit_txt = {
          "spin_dependency": spin_dependency_in,
          "result_type": result_type_in,
          "measurement_type": "measurement_type",
          "nomhash": "string",
          "x_units": x_units_in,
          "y_units": y_units_in,
          "x_rescale": x_rescale_in,
          "y_rescale": y_rescale_in,
          "default_color": trace_color_in,
          "default_style": line_style_in,
          "data_values": data_values_in,
          "data_label": data_label_in,
          "file_name": "string",
          "data_comment": data_comment_in,
          "data_reference": data_reference_in,
          "creator_id": 2147483647,
          "experiment": experiment_in,
          "rating": 2147483647,
          "date_of_announcement": date_of_announcement_in,
          "public": public_out,
          "official": False,
          "date_official": "2023-01-01",
          "greatest_hit": False,
          "date_of_run_start": date_of_run_start_in,
          "date_of_run_end": date_of_run_end_in,
          "year": year_in
        }
        
        new_limit_json = json.dumps(new_limit_txt)
        
        #x = requests.post(fastapi_url, json = post_data)
        x = requests.post(fastapi_url, json = new_limit_txt)
        
        #print("post data")
        #print("================")
        #print(post_data)

        print("new_limit_txt")
        print("================")
        print(new_limit_txt)

        print("request text")
        print("================")
        print(x.text)
        
        
        ## href_return = baseapp_prefix + '/list_all_limits'
        href_return = baseapp_prefix + '/homepage'
        
        return href_return
    
    elif "create_new_limit_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = baseapp_prefix + '/homepage'
        return href_return
        
'''
#### this works from here ####
@callback(Output('container', 'children'),
              [Input('create_new_limit_save_button_id', 'n_clicks_timestamp'),
               Input('create_new_limit_cancel_button_id', 'n_clicks_timestamp')])
def display(btn1, btn2):
    if btn1 == None:
        btn1 = 0
    if btn2 == None:
        btn2 = 0
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    if int(btn1) > int(btn2):
        msg = 'Save was most recently clicked  > ' + prop_id
    elif int(btn2) > int(btn1):
        msg = 'Cancel was most recently clicked  > ' + prop_id
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div([
        html.Div('btn1: {}'.format(btn1)),
        html.Div('btn2: {}'.format(btn2)),
        html.Div(msg)
    ]) 
### to here ######

### also now works having add Location to form #####

@callback(Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("create_new_limit_save_button_id", "n_clicks_timestamp"),
    Input("create_new_limit_cancel_button_id", "n_clicks_timestamp")
        ],
        prevent_initial_call=True)
def display(btn1, btn2):
    if btn1 == None:
        btn1 = 0
    if btn2 == None:
        btn2 = 0
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    if int(btn1) > int(btn2):
        msg = 'Save was most recently clicked' + prop_id
        print("save button pressed")
        href_return = '/app/baseapp/list_all_limits'
    elif int(btn2) > int(btn1):
        print("cancel button pressed")
        href_return = '/app/baseapp/homepage'
    else:
        msg = 'None of the buttons have been clicked yet'
        href_return = '/app/baseapp/create_new_limit'
    return href_return

'''
