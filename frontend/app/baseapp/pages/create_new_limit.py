import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import json
import requests

import base64

import pandas as pd

from app.baseapp.libraries import formlibrary as fl

import xml.etree.ElementTree as ET

dash.register_page(__name__, path='/create_new_limit')

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
        
    def f(self):
        return 'hello world'

#save_button =  html.Div(dbc.Button("Save",  id="create_new_limit_save_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")
save_button =  html.Div(dbc.Button("Save",  id="9876_new_limit_save_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")


#cancel_button =  html.Div(dbc.Button("Cancel",  id="create_new_limit_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")
cancel_button =  html.Div(dbc.Button("Cancel",  id="9876_new_limit_cancel_button_id", color="secondary"), className = "FORM_CANCEL_BUTN")

#### create new Limit form

create_new_limit_form_title = html.Div(html.P(children='Create New Limit', className = "NOPADDING_CONTENT FORM_TITLE"))

Limit = Limit_class

load_limit_file_form = html.Div(
        [fl.uploadxmlfile_input_row,
        fl.datavalues_input_row,
        fl.datacomment_input_row,
        fl.datalabel_input_row,
        fl.datareference_input_row,
        fl.dateofannouncement_input_row,
        fl.dateofrunstart_input_row,
        fl.dateofrunend_input_row,
        fl.tracecolor_input_row,
        fl.linestyle_input_row,
        fl.experiment_input_row,
        fl.publiclimit_input_row,
        fl.resulttype_input_row,
        fl.spindependency_input_row,
        fl.rescalex_input_row,
        fl.xunit_input_row,
        fl.rescaley_input_row,
        fl.yunit_input_row,
        fl.year_input_row,
        save_button,
        cancel_button,
        html.Div(id='container')
    ])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    stringToXML = ET.ElementTree(ET.fromstring(decoded))
    DMToolLimit = Limit_class()
    DMToolLimit.set_values(stringToXML)
    data_reference_out = DMToolLimit.data_reference
    #print(stringToXML)
    #data_reference_out = find_xml_text(stringToXML,'data-reference')
    print(DMToolLimit)
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
            Output('datavaluesid', 'value'),
            Output('datacommentid', 'value'),
            Output('datalabelid', 'value'),
            Output('datareferenceid', 'value'),
            Output('dateofannouncementid', 'initial_visible_month'),
            Output('dateofrunstartid', 'initial_visible_month'),
            Output('dateofrunendid', 'initial_visible_month'),
            Output('tracecolorid', 'value'),
            Output('linestyleid', 'value'),
            Output('experimentid', 'value'),
            Output('publiclimitid', 'on'),
            Output('resulttypeid', 'value'),
            Output('spindependencyid', 'value'),
            Output('rescalexid', 'value'),
            Output('xunitid', 'value'),
            Output('rescaleyid', 'value'),
            Output('yunitid', 'value'),
            Output('yearid', 'value'),
            Input('uploadxmlfileid', 'contents')
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
'''
@callback(
    Output('url', 'href',allow_duplicate=True), ## duplicate set as all callbacks tartgetting url
    [
    Input("9876_new_limit_save_button_id", "n_clicks"),
    Input("9876_new_limit_cancel_button_id", "n_clicks")
        ],
        prevent_initial_call=True
)
def button_click(button1,button2):
    #msg = "None of the buttons have been clicked yet"
    
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    print('-------------- prop id ---------------------')
    
    print(prop_id)
    
    #msg = prop_id
    if "9876_new_limit_save_button_id" == prop_id :
        #msg = "Button 1 was most recently clicked"
        print("save button pressed")
        #href_return = dash.page_registry['pages.list_all_limits']['path']
        
        new_limit_txt = {
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
          "date_of_announcement": "2023-06-13",
          "public": 2147483647,
          "official": 2147483647,
          "date_official": "2023-06-13",
          "greatest_hit": 2147483647,
          "date_of_run_start": "2023-06-13",
          "date_of_run_end": "2023-06-13",
          "year": 2147483647
        }
        
        new_limit_json = json.dumps(new_limit_txt)
        
        
        #url = 'https://www.w3schools.com/python/demopage.php'
        url = 'http://35.214.16.124:8008/apiorm/limit'
        #url = 'http://container_fastapi_orm_1:8008/apiorm/limit'
        #myobj = {'somekey': 'somevalue'}

        #x = requests.post(url, json = new_limit_txt)

        #print(x.text)
        
        
        href_return = '/app/baseapp/list_all_limits'
        
        return href_return
    
    elif "9876_new_limit_cancel_button_id" == prop_id:
        #msg = "Button 2 was most recently clicked"
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/app/baseapp/homepage'
        return href_return
    else:
        #href_return = dash.page_registry['pages.home']['path']
        href_return = '/app/baseapp/homepage'
        return href_return
    '''
@app.callback(Output('container', 'children'),
              [Input('9876_new_limit_save_button_id', 'n_clicks_timestamp'),
               Input('9876_new_limit_cancel_button_id', 'n_clicks_timestamp')])
def display(btn1, btn2):
    if int(btn1) > int(btn2):
        msg = 'Save was most recently clicked'
    elif int(btn2) > int(btn1):
        msg = 'Cancel was most recently clicked'
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div([
        html.Div('btn1: {}'.format(btn1)),
        html.Div('btn2: {}'.format(btn2)),
        html.Div(msg)
    ])

