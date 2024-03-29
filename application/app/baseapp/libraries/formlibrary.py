import dash
from dash import dcc
from dash import html
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
from datetime import datetime
import requests


#######################################################

## def PopulateFilterDataFrames(self):
#do some parsing
dropdown_route = 'metadata/dropdown_valuepair'
fastapi_url = "http://container_fastapi_about_1:8014/dmtool/fastapi_data/internal/"
fastapi_get_dropdown = fastapi_url + dropdown_route + "?variable_in="


## experiment drop down table ##
experiments_req_url = fastapi_get_dropdown + 'experiment'
print("experiments_req_url >>>>>>>>>>>>",experiments_req_url)
r = requests.get(experiments_req_url)
experiments_response_data = r.json()
print("experiments_response_data >>>>>>>>>>>>" ,experiments_response_data)

experiments_df = pd.DataFrame.from_dict(experiments_response_data)
experiments_df.reset_index(drop=True, inplace=True)

## result type drop down table ##

result_types_req_url = fastapi_get_dropdown + 'result_type'
r = requests.get(result_types_req_url)
result_types_response_data = r.json()

result_types_df  = pd.DataFrame.from_dict(result_types_response_data)

result_types_df.reset_index(drop=True, inplace=True)

## spin dependency drop down table ##

spin_dependency_req_url = fastapi_get_dropdown + 'spin_dependency'
r = requests.get(spin_dependency_req_url)
spin_dependency_response_data = r.json()

spin_dependency_df  =  pd.DataFrame.from_dict(spin_dependency_response_data)

spin_dependency_df.reset_index(drop=True, inplace=True)

## result type drop down table ##

greatest_hit_req_url = fastapi_get_dropdown + 'greatest_hit'
r = requests.get(greatest_hit_req_url)
greatest_hit_response_data = r.json()

greatest_hit_df = pd.DataFrame.from_dict(greatest_hit_response_data)

#self.greatest_hit_df.reset_index(drop=True, inplace=True)

official_req_url = fastapi_get_dropdown + 'official'
r = requests.get(official_req_url)
official_response_data = r.json()

official_df = pd.DataFrame.from_dict(official_response_data)

#self.official_df.reset_index(drop=True, inplace=True)

year_req_url = fastapi_get_dropdown + 'year'
r = requests.get(year_req_url)
year_response_data = r.json()

years_df = pd.DataFrame.from_dict(year_response_data)

########################################

symbols_value_list = ['circle','square','diamond','x','triangle']
symbols_label_list = ['○','□','◇','x','△']        
symbols_lol = []
for p in (range(0,5)):
    l = [symbols_label_list[p],symbols_value_list[p]]
    symbols_lol.append(l)
#print("symbols_lol >>>>>>>>>>>", symbols_lol)
symbol_options=[{'label': item[0], 'value' : item[1]} for item in symbols_lol]
print("symbol_options >>>>>>>>>>>", symbol_options)

palette_color_list = ['black','red','orange','yellow' 'green','blue', 'purple', 'brown']
palette_color_abreviations = ['BK','RD','OR','YL','GN', 'BL', 'PR', 'BR']
palette_color_squares = ['⬛','🟥','🟧','🟨','🟩', '🟦', '🟪', '🟫']

colors_lol = []
for p in (range(0,7)):
    l = [palette_color_squares[p],palette_color_list[p]]
    colors_lol.append(l)

#print("self.symbols_lol >>>>>>>>>>>", self.symbols_lol)

color_options=[{'label': item[0], 'value' : item[1]} for item in colors_lol]
print("color_options >>>>>>>>>>>", color_options)

line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
line_styles_lines = ['__', '...', '---', '__ __', '_.', '__.']

line_styles_lol = []
for p in (range(0,5)):
    l = [line_styles_lines[p],line_styles_list[p]]
    line_styles_lol.append(l)

line_style_options=[{'label': item[0], 'value' : item[1]} for item in line_styles_lol]


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
lines_tyle_form_field_id
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
'''

#######################################################


#######################################################
## form variables

label_column_width = 4
data_column_width = 4
example_column_width = 3
show_example = 1

######################### fields ######################


# Plot Name - Text
def get_example_column(show_example_in):
    return_val =  dbc.Col()
    if show_example_in == 1:
        return_val = dbc.Col(dcc.Input(id='plot_name_example_field_id',
                                          type='text',
                                          value='example',
                                          readOnly=True,
                                          className='FORM_COLUMN_EXAMPLE'),
                            className='FORM_EXAMPLE_COLUMN',
                            width=example_column_width)
    else:
        return_val = dbc.Col(className='FORM_EXAMPLE_COLUMN',width=example_column_width)
    return return_val

example_column = get_example_column(show_example)

plot_name_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Plot Name :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='plot_name_form_field_id',
                              type='text',maxLength=40,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = data_column_width
                ),
                example_column,        
                dbc.Popover(
                    dbc.PopoverBody('enter plot unique name'),
                    target="plot_name_example_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Plot of Experiment M'),
                    target="plot_name_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW '),
    ]
)


# X Range: Lower Bound - Text

x_range_lower_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('X Range Lower :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='x_range_lower_form_field_id',
                              type='text',
                              maxLength=10,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='x_range_lower_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter lower bound X'),
                    target="x_range_lower_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('12345'),
                    target="x_range_lower_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Upper Bound - Text

x_range_upper_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('X Range Upper :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='x_range_upper_form_field_id',
                              type='text',
                              maxLength=10,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = data_column_width
                ),

                dbc.Col(dcc.Input(id='x_range_upper_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter upper bound X'),
                    target="x_range_upper_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('12345'),
                    target="x_range_upper_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)



# Scale - Dropdown

BARN_CM2 = 1e-24

scale_lol = [
["b", BARN_CM2],
["mb",1e-3*BARN_CM2],
["ub",1e-6*BARN_CM2],
["nb", 1e-9*BARN_CM2],
["pb", 1e-12*BARN_CM2],
["fb",  1e-15*BARN_CM2],
["ab", 1e-18*BARN_CM2],
["zb", 1e-21*BARN_CM2],
["yb",1e-24*BARN_CM2],
["1",1]
]

scaleDict = {item[0]: item[1] for item in scale_lol}

scale_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Scale :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='scale_form_field_id',
                        options=[{'label': k, 'value': v} for k, v in scaleDict.items()],
                        ##className='FORM_COLUMN_SCALE',
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_SCALE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='scale_example_field_id',
                                  type='text', 
                                  value='scale example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                dbc.Popover(
                    dbc.PopoverBody('enter scale'),
                    target="scale_form_field_id",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="scale_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Trace Trace ID - Integer

trace_id_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace ID :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='trace_id_form_field_id', type='number',
                                  #className='FORM_COLUMN_TRACEID',
                                  className='FORM_COLUMN_DATA',
                                  ),
                    #className='FORM_TRACEID_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='trace_id_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                dbc.Popover(
                    dbc.PopoverBody('enter traceid'),
                    target="trace_id_form_field_id",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="trace_id_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Trace Name - Text

trace_name_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Name :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='trace_name_form_field_id', type='text',maxLength=10,
                                  #className='FORM_COLUMN_TEXTINPUT',
                                  className='FORM_COLUMN_DATA',
                                  ),
                    #className='FORM_TEXTINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='trace_name_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width
                    ),
                
                dbc.Popover(
                    dbc.PopoverBody('enter trace name'),
                    target="trace_name_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Plot of Experiment M'),
                    target="trace_name_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Trace Color - Dropdown Trace

trace_color_css = [{"selector": ".form-select", "rule": "padding':0 !important"}, {"selector": ".form-select", "rule": "margin : 0 !important"}]

trace_color_dropdown = dbc.Col(dbc.Select(
                                options=color_options,
                                id='year_form_field_id_3',
                                style={'width':'100%','height':'24px', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

trace_color_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Color :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                trace_color_dropdown,                
                dbc.Col(dcc.Input(id='trace_color_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter color'),
                    target="trace_color_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('red'),
                    target="trace_color_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Symbol - Dropdown

symbols_list = ['circle','square','diamond','x','triangle']
symbols_df = pd.DataFrame({'c' : symbols_list})
labels_list = [
           html.Span([dcc.Markdown('&#9675')]),
           html.Span([dcc.Markdown('&#9643')]),
           html.Span([dcc.Markdown('&#9671')]),
           html.Span([dcc.Markdown('&#9747')]),
           html.Span([dcc.Markdown('&#9661')])
          ]
#symbols_df = pd.DataFrame({'c' : symbols_list})
#labels_df = pd.DataFrame({'c' : labels_list})
#labels_df
lol = []
for p in (range(0,5)):
    l = [labels_list[p],symbols_list[p]]
    lol.append(l)
    
itemDict = {item[0]: item[1] for item in lol}

symboldd = dcc.Dropdown(
        id='symbol_form_field_id',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()]
    )

symbol_dropdown = dbc.Col(dbc.Select(options=symbol_options,
                                     id='year_form_field_id_3',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

symbol_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Symbol :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                symbol_dropdown,
                dbc.Col(dcc.Input(id='symbol_input_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="symbol_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="symbol_input_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Trace Line Style - Dropdown

linestyle_list = ['solid','dash','dot','dashdot']
linestyle_df = pd.DataFrame({'c' : symbols_list})
labels_list = [
           html.Span([dcc.Markdown('&#9473')]),
           html.Span([dcc.Markdown('&#9476')]),
           html.Span([dcc.Markdown('&#8226')]),
           html.Span([dcc.Markdown('&#9476 &#8226')])
          ]

lol = []
for p in (range(0,4)):
    l = [labels_list[p],linestyle_list[p]]
    lol.append(l)
    
itemDict = {item[0]: item[1] for item in lol}

linestyledd = dcc.Dropdown(
        id='line_style_form_field_id',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()],
        style={'height': '14px', 'width': '100%'}
    )


line_style_dropdown = dbc.Col(dbc.Select(
                        options=line_style_options,
                        id='year_form_field_id_3',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)


line_style_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Line Style :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                line_style_dropdown,                
                dbc.Col(dcc.Input(id='line_style_input_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="line_style_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="line_style_input_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Trace Fill Color - Dropdown

trace_fill_color_dropdown = dbc.Col(dbc.Select(
                                options=color_options,
                                id='year_form_field_id_3',
                                style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

trace_fill_color_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Fill Color :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                trace_fill_color_dropdown,                
                dbc.Col(dcc.Input(id='trace_fill_color_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter color'),
                    target="trace_fill_color_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('red'),
                    target="trace_fill_color_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Remove Site Address Check Box

remove_site_address_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Remove Site Address :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                
                dbc.Col(
                    dcc.Checklist(
                            id='remove_site_address_form_field_id',
                            options=[
                                   ##{'label': 'New York City', 'value': 'New York City'},
                                   {'label': 'Remove', 'value': 'Remove'}
                                   ##{'label': 'San Francisco', 'value': 'San Francisco'},
                               ],
                            value=['Remove'],
                            #className='FORM_COLUMN_CHECKBOXINPUT',
                            className='FORM_COLUMN_DATA',
                            labelStyle={'display': 'block'} ,
                                        ),
                    #className='FORM_CHECKBOXINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='remove_site_address_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle checkbox'),
                    target="remove_site_address_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="remove_site_address_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Upload XML File - Select File

style_form_select_file = {
    'line-height': '20px',
    'text-align': 'left',
    'color': 'purple',
    'font-size': '13px',
    'font-weight': 'bold'
}

upload_xml_file_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Upload XML File :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                      dcc.Upload(
                          id = 'upload_xml_file_form_field_id',
                          children= [
                                    'Drop or ',
                                    html.A('Select',style=style_form_select_file)
                                    ],
                       #className='FORM_COLUMN_UPLOAD',
                       className='FORM_COLUMN_DATA',
                                        ),
                    #className='FORM_UPLOAD_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='upload_xml_file_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('upload xml file'),
                    target="upload_xml_file_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Drag or Drop File here'),
                    target="upload_xml_file_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Load Limit from Uploaded File

# Help on XML File and Examples

# Data Label - Text - < 60 chars

data_label_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Data Label :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='data_label_form_field_id',
                              type='text',
                              maxLength=60,
                              #className='FORM_COLUMN_TEXTINPUT'),
                              className='FORM_COLUMN_DATA'),
                    #className='FORM_TEXTINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='data_label_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter data label'),
                    target="data_label_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('example_datalabel'),
                    target="data_label_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Data Reference - Big Text

data_reference_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Data Reference :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                
                dbc.Col(
                    dcc.Textarea(
                            id='data_reference_form_field_id',
                            value='Data Reference',
                            rows=1,
                            #className='FORM_COLUMN_TEXTAREAINPUT'
                            className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_TEXTAREAINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='data_reference_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="data_reference_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="data_reference_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Data Comment - Big Text

data_comment_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Data Comment :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                
                dbc.Col(
                    dcc.Textarea(
                            id='data_comment_form_field_id',
                            value='Data Comment',
                            rows=1,
                            #className='FORM_COLUMN_TEXTAREAINPUT'
                            className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_TEXTAREAINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='data_comment_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="data_comment_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="data_comment_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Experiment - Dropdown
'''
experiments_list = [
"CDMS I (SUF)","CDMS II (Soudan)","SuperCDMS","LUX","XENON10",
"XENON100","XENON1T","ZEPLIN I","ZEPLIN II","ZEPLIN III","ZEPLIN IV",
"COSME","CUORICINO","DAMA","KIMS DMRC","ELEGANT V","Edelweiss",
"GEDEON","Genius","Genino","Heidelberg","IGEX","KIMS","MIBETA",
"Modane NaI","NAIAD","PICASSO","ROSEBUD","SIMPLE","Saclay",
"SuperK","TOKYO","UKDMC","WARP","Theory","Heidelberg-Moscow",
"Cuore","DAMA Xe","TEXONO","XMASS","IceCube","DMTPC","DEAP CLEAN",
"DAMA/LIBRA","CoGeNT","COUPP","LUX-ZEPLIN","Fermi","DarkSide","DAMIC",
"EURECA","DEAP-3600","PICO","PandaX","LHC","DRIFT","GAMBIT",
"CDEX-10","NEWS-G","XENONnT","CRESST"
]
'''

#experiments_df = pd.DataFrame({'c' : experiments_list})
#experiments_df_dict = experiments_df.to_dict('records')
experiments_labels = experiments_df[['label','value']]
experiments_labels_dict = experiments_labels.to_dict('records')

#options=[{'label': i['name'], 'value': i['ip']} for i in available_rpi],

experiment_dropdown = dbc.Col(dbc.Select(
                        options=[{'label': i['label'], 'value': i['value']} for i in experiments_labels_dict],id='year_form_field_id_3',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)


experiment_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Experiment :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                experiment_dropdown,
                dbc.Col(dcc.Input(id='experiment_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter experiment'),
                    target="experiment_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('example experiment'),
                    target="experiment_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Date of Announcement - Date

#dbc.Input(id="input", placeholder="Type something...", type="text"),

date_of_announcement_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Announcement Date :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dbc.Input(id='date_of_announcement_form_field_id', placeholder=datetime.now(), type="date",className='FORM_COLUMN_DATA'),
                    #className='FORM_SINGLEDATE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='date_of_announcement_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter date of announcement'),
                    target="date_of_announcement_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="date_of_announcement_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)



# Date of Run Start - Date

date_of_run_start_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Run Start Date :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dbc.Input(id='date_of_run_start_form_field_id', placeholder=datetime.now(), type="date",className='FORM_COLUMN_DATA'),
                    #className='FORM_SINGLEDATE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='date_of_run_start_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter date of run start'),
                    target="date_of_run_start_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="date_of_run_start_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Date of Run End - Date

date_of_run_end_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Run End Date :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dbc.Input(id='date_of_run_end_form_field_id', placeholder=datetime.now(), type="date",className='FORM_COLUMN_DATA'),
                    #className='FORM_SINGLEDATE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='date_of_run_end_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter date of run end'),
                    target="date_of_run_end_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="date_of_run_end_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Year - Dropdown - Integer

years = range(2010,2031)
years_list = list(years)
years_list
#years_df = pd.DataFrame({'c' : years_list})
#years_df

year_labels = years_df[['label','value']]
year_labels_dict = year_labels.to_dict('records')

'''dd = dcc.Dropdown(
        id='yearid',
        options=[
            {'label':i, 'value':i} for i in years_df['c'].unique()
        ],
    )
'''

dbc_select_col = dbc.Col(dbc.Select(
    options=[
                {"label": "Option 1", "value": "1"},
                {"label": "Option 2", "value": "2"},
                {"label": "Disabled option", "value": "3", "disabled": True},
            ],id='year_form_field_id_3',style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
            ,width = data_column_width)


dbc_select_col_1 = dbc.Col(dbc.Select(
                        options=[{'label': i['label'], 'value': i['value']} for i in year_labels_dict],id='year_form_field_id_3',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

year_dropdown_col_2 = dbc.Col(dbc.Select(options=[
    {'label': 'eeney', 'value': 'eeney'},
    {'label': 'meeney', 'value': 'meeney'},
    {'label': 'miney', 'value': 'miney'},
    {'label': 'mo', 'value': 'mo'},
], id='year_form_field_id_2',  style={'height': '25px','width':'100%','display': 'inline-block','padding':'0 !important','margin': '0 !important', 'border': '2px solid black'}),
                            width = data_column_width,
                            className='FORM_DATA_COLUMN',
                            style={'height': '100%'},
                             )

year_dropdown_col_3 = dbc.Col(dbc.Select(
                                        options=[{'label': i['label'], 'value': i['value']} for i in year_labels_dict],
                                        id='year_form_field_id_2',
                                        style={'height': '25px','width':'100%','display': 'inline-block','padding':'0 !important','margin': '0 !important', 'border': '2px solid black'}),
                            width = data_column_width,
                            className='FORM_DATA_COLUMN',
                            style={'height': '100%'},
                             )

year_dropdown_col_1 = dbc.Col(
                     dcc.Dropdown(
                        id='year_form_field_id',
                        options=[{'label': i['label'], 'value': i['value']} for i in year_labels_dict],
                        #className='FORM_COLUMN_YEARDROPDOWN'
                        className='FORM_COLUMN_DATA',
                        style={'height': '25px','width':'100%','display': 'inline-block','padding':'0 !important','margin': '0 !important', 'border': '2px solid black'},
                    ),
                    #className='FORM_YEARDROPDOWN_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width,
                    style={'height': '100%'},
                )

year_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Year :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc_select_col_1,
                dbc.Col(dcc.Input(id='year_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('select year'),
                    target="year_form_field_id_2",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('2023'),
                    target="year_form_field_id_2",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# X Rescale - Exponential

x_rescale_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('X Rescale :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(
                        id="x_rescale_form_field_id",
                        debounce=True,
                        placeholder="1e1",
                        type="text",
                        ##pattern=u"^(?:\d{3}|\(\d{3}\))([-/.])\d{3}\1\d{4}$",
                        #className='FORM_COLUMN_RESCALEX'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_RESCALEX_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='x_rescale_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter rescale x'),
                    target="x_rescale_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('example rescale'),
                    target="x_rescale_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Y Rescale - Exponential

y_rescale_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Y Rescale :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(
                        id="y_rescale_form_field_id",
                        debounce=True,
                        placeholder="1e1",
                        type="text",
                        ##pattern=u"^(?:\d{3}|\(\d{3}\))([-/.])\d{3}\1\d{4}$",
                        #className='FORM_COLUMN_RESCALEY'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_RESCALEY_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width,
                ),
                
                dbc.Col(dcc.Input(id='y_rescale_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter y rescale'),
                    target="y_rescale_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('rescale y example'),
                    target="y_rescale_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# X Unit

x_unit_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('X Unit :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(
                        id="x_unit_form_field_id",
                        debounce=True,
                        placeholder="1e1",
                        type="text",
                        ##pattern=u"^(?:\d{3}|\(\d{3}\))([-/.])\d{3}\1\d{4}$",
                        #className='FORM_COLUMN_RESCALEY'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_RESCALEY_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='x_unit_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter x unit'),
                    target="x_unit_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('x unit example'),
                    target="x_unit_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Y Unit

y_unit_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Y Unit :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(
                        id="y_unit_form_field_id",
                        debounce=True,
                        placeholder="1e1",
                        type="text",
                        ##pattern=u"^(?:\d{3}|\(\d{3}\))([-/.])\d{3}\1\d{4}$",
                        #className='FORM_COLUMN_RESCALEY'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_RESCALEY_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='y_unit_input_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter y unit'),
                    target="y_unit_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('y unit example'),
                    target="y_unit_input_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Data Values - big text field

data_values_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Data Values :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Textarea(
                            id='data_values_form_field_id',
                            value='Data Values',
                            rows=1,
                            className='FORM_COLUMN_DATA'
                    ),
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='data_values_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="data_values_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="data_values_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Data Formatting Help

# Result Type - Dropdown

resulttype_lol = [['Theory','Th'],['Project','Proj'],['Experiment','Exp']]
resulttype_lol

result_type_options=[{'label': item[0], 'value' : item[1]} for item in resulttype_lol]

result_type_dropdown = dbc.Col(dbc.Select(
                        options=result_type_options,
                        id='result_type_form_field_id',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

result_type_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Result Type :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                result_type_dropdown,                
                dbc.Col(dcc.Input(id='result_type_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter result type'),
                    target="result_type_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('result type example'),
                    target="result_type_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Limit Type

limit_type_lol = [['All',-1],['Official','1']]
#limit_type,All,-1
#limit_type,Official,"1"
limit_typeDict = {item[0]: item[1] for item in limit_type_lol}

limit_type_options=[{'label': item[0], 'value' : item[1]} for item in limit_type_lol]

limit_type_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Limit Type :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='limit_type_form_field_id',
                        options=[{'label': k, 'value': v} for k, v in limit_typeDict.items()],
                        #className='FORM_COLUMN_LIMITTYPE'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_LIMITTYPE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='limit_type_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="limit_type_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="limit_type_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Spin Dependency - Dropdown

spin_lol = [['All','All'],['spin-dependent','SD'],['spin-independent','SI']]

spin_dependency_options=[{'label': item[0], 'value' : item[1]} for item in spin_lol]

spin_dependency_dropdown = dbc.Col(dbc.Select(
                        options=spin_dependency_options,
                        id='result_type_form_field_id',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

spin_dependency_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Spin Dependency :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                spin_dependency_dropdown,
                dbc.Col(dcc.Input(id='spin_dependency_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="spin_dependency_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="spin_dependency_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Measurement Type - Dropdown

measurementtype_lol = [['All','All'],['Direct','Dir']]
measurementtypeDict = {item[0]: item[1] for item in measurementtype_lol}

measurement_type_options=[{'label': item[0], 'value' : item[1]} for item in measurementtype_lol]

measurement_type_dropdown = dbc.Col(dbc.Select(
                        options=measurement_type_options,
                        id='result_type_form_field_id',
                        style={'width':'100%','height':'24px','line-height': '80%', 'font-size': '12px','padding':'0 !important','margin': '0 !important', 'border': '1px solid black'})
                        ,width = data_column_width)

measurement_type_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Measurement Type :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                measurement_type_dropdown,
                dbc.Col(dcc.Input(id='measurement_type_example_field_id',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="measurement_type_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="measurement_type_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Public Limit - Checkbox
'''
<label class="switch">
  <input type="checkbox">
  <span class="slider round"></span>
</label>

https://getbootstrap.com/docs/5.1/forms/checks-radios/
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckChecked" checked>
  <label class="form-check-label" for="flexSwitchCheckChecked">Checked switch checkbox input</label>
</div>

<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckChecked" checked>
  <label class="form-check-label" for="flexSwitchCheckChecked">Checked switch checkbox input</label>
</div>

'''

public_checkbox =  dbc.Col(html.Div(className='form-check form-switch', children=[dcc.Input(className="form-check-input", type="checkbox", id="flexSwitchCheckChecked")]),
                               className='FORM_DATA_COLUMN',
                               width = data_column_width
                           )

boolean = dbc.Col(
                    daq.BooleanSwitch(id='public_limit_form_field_id',
                                      on=False,
                                      className='FORM_COLUMN_DATA'
                                        ),
                    #className='FORM_CHECKBOXINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                )

public_limit_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Public Limit :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                public_checkbox,                
                dbc.Col(dcc.Input(id='public_limit_example_field_id',
                                  type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle check box'),
                    target="public_limit_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Yes'),
                    target="public_limit_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Other Users - CSV of Users

other_users_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Other Users :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                
                dbc.Col(
                    dcc.Textarea(
                            id='other_users_form_field_id',
                            value='Textarea content',
                            rows=1,
                            #className='FORM_COLUMN_TEXTAREAINPUT'
                            className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_TEXTAREAINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='other_users_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('enter list of users'),
                    target="other_users_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('user1, user2, user3'),
                    target="other_users_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)


# Official - Dropdown

official_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Official Limit :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Checklist(
                            id='official_form_field_id',
                            options=[
                                   ##{'label': 'New York City', 'value': 'New York City'},
                                   {'label': 'Yes', 'value': 'Yes'}
                                   ##{'label': 'San Francisco', 'value': 'San Francisco'},
                               ],
                            value=['Yes'],
                            #className='FORM_COLUMN_CHECKBOXINPUT',
                            className='FORM_COLUMN_DATA',
                            labelStyle={'display': 'block'} ,
                                        ),
                    #className='FORM_CHECKBOXINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='official_limit_example_field_id',
                                  type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle checkbox'),
                    target="official_form_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Yes'),
                    target="official_limit_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

# Experiment Type - Dropdown ???

# Greatest Hits - Dropdown

greatest_hits_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Greates Hit :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Checklist(
                            id='greatest_hit_form_field_id',
                            options=[
                                   ##{'label': 'New York City', 'value': 'New York City'},
                                   {'label': 'Yes', 'value': 'Yes'}
                                   ##{'label': 'San Francisco', 'value': 'San Francisco'},
                               ],
                            value=['Yes'],
                            #className='FORM_COLUMN_CHECKBOXINPUT',
                            className='FORM_COLUMN_DATA',
                            labelStyle={'display': 'block'} ,
                                        ),
                    #className='FORM_CHECKBOXINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='greatest_hit_example_field_id', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=example_column_width),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle checkbox'),
                    target="greatest_hit_example_field_id",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Yes'),
                    target="greatest_hit_example_field_id",trigger="click"), 
                
            ],
        className='g-0 FORM_ROW'),
    ]
)

##########################

############################################
# BUTTONS
############################################

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save", color="primary"), className = "FORM_SAVE_BUTN")

#create_button =  html.Div(dbc.Button("Create", color="primary"), className = "FORM_CREATE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
button_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    create_button,
                    className='FORM_BUTTON_COLUMN',
                    width= 1
                ),

                dbc.Col(
                    save_button,
                    className='FORM_BUTTON_COLUMN',
                    width= 1
                ),

                dbc.Col(
                    submit_button,
                    className='FORM_BUTTON_COLUMN',
                    width= 1
                ),
                
                dbc.Col(
                    cancel_button,
                    className='FORM_BUTTON_COLUMN',
                    width= 1
                ),
                
            ],
        className='g-0'),
    ]
)'''


################################################
## NEW PLOT FORM
################################################

'''
new_plot_form = html.Div([
                plot_name_input_row,
                button_input_row])
'''

'''
newplot_input = html.Div(
    [
        dbc.Label("New Plot"),
        dbc.Input(type="text", id="newplot-input1", placeholder="Enter New Plot Name"),
        dbc.FormText(
            "Enter unique name for your plot",
            color="secondary",
        ),
    ],
)


newplot_input2 = dbc.Row(
    [
        html.Div(children="New Plot", className="FORM_TEXT"),
        dbc.Col([
            dbc.Label("Name", width=2),
            dbc.Input(
                type="text",
                id="newplot-input2",
                placeholder="Enter New Plot Name",
                style={"width": "25vh", "height": "5vh", "color": "blue"},
            ),]
        ),
    ],
)


#######################################


newplot_title = html.Div(html.P(children='New Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

label_1 = html.Div(dbc.Label("Name", align="center", className="FORM_TEXT"))

newplot_input3 = html.Div(
    [
        dbc.Col(dbc.Label("Name", align="end", className="FORM_TEXT"),width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="newplot-input3",
                placeholder="Enter New Plot Name",
            ),
            width=4,
        ),
    ],
    className="row",
)

#newplotform = html.Div([newplot_title , newplot_input3], style={"padding":"0px", "margin":"0px", "background-color":"red"})

newplotform = html.Div(
    [newplot_title,newplot_input3],
    #[newplot_title, label_1],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

################################################

newplot_input = dbc.Row(
    [
        dbc.Label("New Plot", width=2),
        dbc.Col(
            [dbc.Input(
                type="text", id="newplot_input", placeholder="Enter New Plot Name"
            ),
            dbc.FormText("Enter unique name for your plot",color="secondary")],
            width=10,
            style={"height": "100%","background-color": "blue", "padding":"0px", "margin":"0px"},
        ),
    ],
style={"height": "50%"},
)
'''

############################################
## LOAD LIMIT FILE
############################################

'''
data_values_form_field_id
data_comment_form_field_id
data_label_form_field_id
data_reference_form_field_id
date_of_announcement_form_field_id
date_of_runstart_form_field_id
date_of_runend_form_field_id
trace_color_form_field_id
line_style_form_field_id
experiment_form_field_id
public_limit_form_field_id
result_type_form_field_id
spin_dependency_form_field_id
rescale_x_form_field_id
x_unit_form_field_id
rescale_y_form_field_id
y_unit_form_field_id
year_form_field_id
'''            

load_limit_file_form = html.Div(
        [upload_xml_file_input_row,
        data_values_input_row,
        data_comment_input_row,
        data_label_input_row,
        data_reference_input_row,
        date_of_announcement_input_row,
        date_of_run_start_input_row,
        date_of_run_end_input_row,
        trace_color_input_row,
        line_style_input_row,
        experiment_input_row,
        public_limit_input_row,
        result_type_input_row,
        spin_dependency_input_row,
        x_rescale_input_row,
        x_unit_input_row,
        y_rescale_input_row,
        y_unit_input_row,
        year_input_row
    ])



############################################
## EDIT LIMIT FORM
############################################

edit_limit_form = html.Div(
        [upload_xml_file_input_row,
        data_label_input_row,
        data_reference_input_row,
        data_comment_input_row,
        data_values_input_row,
        experiment_input_row,
        date_of_announcement_input_row,
        year_input_row,
        y_rescale_input_row,
        x_rescale_input_row])


############################################
## EDIT EXISTING LIMIT FORM
############################################

edit_existing_limit_form = html.Div(
        [x_rescale_input_row,
        data_values_input_row,
        result_type_input_row,
        spin_dependency_input_row,
        measurement_type_input_row,
        public_limit_input_row,
        other_users_input_row
        ])


#############################################
## LOGIN
#############################################

email_input = html.Div(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
        dbc.FormText(
            "Are you on email? You simply have to be these days",
            color="secondary",
        ),
    ],
)

password_input = html.Div(
    [
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="example-password",
            placeholder="Enter password",
        ),
        dbc.FormText(
            "A password stops mean people taking your stuff", color="secondary"
        ),
    ],
    className="mb-3",
)

#### email & password form

email_form_title = html.Div(html.P(children='Please Login', className = "NOPADDING_CONTENT FORM_TITLE"))


enter_email_and_password  = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Label("Email", html_for="example-email-grid", className="FORM_TEXT"),
                dbc.Input(
                    type="email",
                    id="example-email-grid",
                    placeholder="Enter email",
                ),
            ],
            width=6,
        ),
        dbc.Col(
            [
                dbc.Label("Password", html_for="example-password-grid", className="FORM_TEXT"),
                dbc.Input(
                    type="password",
                    id="example-password-grid",
                    placeholder="Enter password",
                ),
            ],
            width=6,
        ),
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
login_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     email_form_title, enter_email_and_password,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''


###############

#### create new Limit form

create_new_limit_form_title = html.Div(html.P(children='Create New Limit', className = "NOPADDING_CONTENT FORM_TITLE"))


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

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
create_new_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_limit_form_title,
     create_new_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''
###############

#### edit existing limit form

edit_existing_limit_form_title = html.Div(html.P(children='Edit Existing Limit', className = "NOPADDING_CONTENT FORM_TITLE"))


edit_existing_limit_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Edit Existing Limit', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
edit_existing_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_limit_form_title,
     create_new_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''

###############

#### create new plot form

create_new_plot_form_title = html.Div(html.P(children='Create New Plot', className = "NOPADDING_CONTENT FORM_TITLE"))


create_new_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Create New Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
create_new_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_plot_form_title,
     create_new_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''

###############

#### edit existing plot form

edit_existing_plot_form_title = html.Div(html.P(children='Edit Existing Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

edit_existing_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Edit Existing Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
edit_existing_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_existing_plot_form_title,
     edit_existing_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''
###############

###############

#### select limits to plot

select_limits_to_plot_form_title = html.Div(html.P(children='Select Limits to Plot', className = "NOPADDING_CONTENT FORM_TITLE"))

select_limits_to_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Select Limits to Plot', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
select_limits_to_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_existing_plot_form_title,
     edit_existing_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''

#### style plot and traces

style_plot_and_traces_form_title = html.Div(html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE"))

style_plot_and_traces_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

'''
style_plot_and_traces_form_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     style_plot_and_traces_form_title,
     style_plot_and_traces_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''
#### show plot

show_plot_form_title = html.Div(html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE"))

show_plot_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")
'''
show_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     show_plot_form_title,
     show_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''
#### list user plots

list_user_plots_form_title = html.Div(html.P(children='List User Plots', className = "NOPADDING_CONTENT FORM_TITLE"))

list_user_plots_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Style Plot and Traces', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

'''
list_user_plots_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_user_plots_form_title,
     list_user_plots_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''


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

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

'''
list_all_limits_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_all_limits_form_title,
     list_all_limits_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''

#### show limit

show_limit_form_title = html.Div(html.P(children='Show Limit', className = "NOPADDING_CONTENT FORM_TITLE"))

show_limit_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Show Limit', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

'''
show_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     show_limit_form_title,
     show_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''

#### edit limit

edit_limit_form_title = html.Div(html.P(children='Edit Limit', className = "NOPADDING_CONTENT FORM_TITLE"))

edit_limit_form_content  = dbc.Row(
    [
        dbc.Col(
            [
                html.P(children='Edit Limit', className = "NOPADDING_CONTENT FORM_TITLE")
            ],
            width=6,
        )
    ],
    className="g-3",
)

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

#save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

#submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

#cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

'''
edit_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_limit_form_title,
     edit_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)
'''


'''
newplotform_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.P("New Plot"),
                    width=12,
                    style={"height": "100%","background-color": "red","padding":"0px", "margin":"0px"},
                ),
            ],
            #className="h-25",
            style={"height": "50%"},
        ),
        newplot_input,
    ],
    #style={"height": "600px","width": "700px","background-color": "green","padding":"0px", "margin":"auto"},
    #style={"height": "600px","width": "700px", "margin": "0px",\
    #       "position": "absolute","top": "50%", "left": "50%", \
    #       "transform": "translate(-50%, -50%)"},
    className = "CENTRE_FORM_CONTAINER",
)
'''


