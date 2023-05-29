import dash
from dash import dcc
from dash import html
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date

#######################################################

'''
ID List
========
plotnameid
xrangelowerid
xrangeupperid
scaleid
traceidid
tracenameid
tracecolorid
symbolid
linestyleid
tracefillcolorid
removesiteaddressid
uploadxmlfileid
datalabelid
datareferenceid
datacommentid
experimentid
dateofannouncementid
dateofrunstartid
dateofrunendid
yearid
rescalexid
rescaleyid
yunitid
xunitid
datavaluesid
resulttypeid
limittypeid
spindependencyid
measurementtypeid
publiclimitid
otherusersid
officialid
greatesthitid
'''

#######################################################


#######################################################
## form variables

label_column_width = 2
data_column_width = 2

######################### fields ######################


# Plot Name - Text

plotname_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Plot Name :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='plotnameid',
                              type='text',maxLength=40,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='example_plotname',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter plot unique name'),
                    target="plotnameid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Plot of Experiment M'),
                    target="example_plotname",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# X Range: Lower Bound - Text

xrangelower_input_row = html.Div(
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
                    dcc.Input(id='xrangelowerid',
                              type='text',
                              maxLength=10,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_textinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter lower bound X'),
                    target="textinput",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('12345'),
                    target="example_textinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Upper Bound - Text

xrangeupper_input_row = html.Div(
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
                    dcc.Input(id='xrangeupperid',
                              type='text',
                              maxLength=10,
                              className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width = data_column_width
                ),

                dbc.Col(dcc.Input(id='example_xrangeupper', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter upper bound X'),
                    target="xrangeupperid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('12345'),
                    target="example_xrangeupper",trigger="click"), 
                
            ],
        className='g-0'),
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
                        id='scaleid',
                        options=[{'label': k, 'value': v} for k, v in scaleDict.items()],
                        ##className='FORM_COLUMN_SCALE',
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_SCALE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='example_scale',
                                  type='text', 
                                  value='scale example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter scale'),
                    target="scaleid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_scale",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Trace Trace ID - Integer

traceid_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace ID :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='traceidid', type='number',
                                  #className='FORM_COLUMN_TRACEID',
                                  className='FORM_COLUMN_DATA',
                                  ),
                    #className='FORM_TRACEID_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='example_traceid',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter traceid'),
                    target="traceidid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_traceid",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Trace Name - Text

tracename_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Name :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='tracenameid', type='text',maxLength=10,
                                  #className='FORM_COLUMN_TEXTINPUT',
                                  className='FORM_COLUMN_DATA',
                                  ),
                    #className='FORM_TEXTINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='example_tracename',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1
                    ),
                
                dbc.Popover(
                    dbc.PopoverBody('enter trace name'),
                    target="tracenameid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Plot of Experiment M'),
                    target="example_tracename",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Trace Color - Dropdown Trace

tracecolor_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Color :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                     dbc.Input(
                        type="color",
                        id="tracecolorid",
                        value="#000000",
                     #className='FORM_COLUMN_COLOR',
                     className='FORM_COLUMN_DATA'
                    ),
                    # className='FORM_COLOR_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_tracecolor',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter color'),
                    target="tracecolorid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('red'),
                    target="example_tracecolor",trigger="click"), 
                
            ],
        className='g-0'),
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
        id='symbolid',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()]
    )


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
                
                dbc.Col(
                    symboldd,
                    #className='FORM_COLOR_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_symbolinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="symbolid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_symbolinput",trigger="click"), 
                
            ],
        className='g-0'),
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
        id='linestyleid',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()]
    )


linestyle_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Trace Line Style :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    linestyledd,
                    #className='FORM_COLOR_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_linestyleinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="linestyleid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_linestyleinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Trace Fill Color - Dropdown

tracefillcolor_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Fill Color :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                     dbc.Input(
                        type="color",
                        id="tracefillcolorid",
                        value="#000000",
                     #className='FORM_COLUMN_COLOR',
                     className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_COLOR_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_tracefillcolor',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter color'),
                    target="tracefillcolorid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('red'),
                    target="example_tracefillcolor",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Remove Site Address Check Box

removesiteaddress_input_row = html.Div(
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
                            id='removesiteaddressid',
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
                
                dbc.Col(dcc.Input(id='example_removesiteaddress',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle checkbox'),
                    target="removesiteaddressid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_removesiteaddress",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Upload XML File - Select File

uploadxmlfile_input_row = html.Div(
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
                          id = 'uploadxmlfileid',
                          children= [
                                    'Drag and Drop or ',
                                    html.A('Select a File',className='FORM_SELECTFILE')
                                    ],
                       #className='FORM_COLUMN_UPLOAD',
                       className='FORM_COLUMN_DATA',
                                        ),
                    #className='FORM_UPLOAD_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_uploadinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('upload xml file'),
                    target="uploadxmlfileid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Drag or Drop File here'),
                    target="example_uploadinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Load Limit from Uploaded File

# Help on XML File and Examples

# Data Label - Text - < 60 chars

datalabel_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Data Label :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    dcc.Input(id='datalabelid',
                              type='text',
                              maxLength=60,
                              #className='FORM_COLUMN_TEXTINPUT'),
                              className='FORM_COLUMN_DATA'),
                    #className='FORM_TEXTINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_datalabel', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter data label'),
                    target="datalabelid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('example_datalabel'),
                    target="example_datalabel",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Data Reference - Big Text

datareference_input_row = html.Div(
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
                            id='datareferenceid',
                            value='Data Reference',
                            rows=1,
                            #className='FORM_COLUMN_TEXTAREAINPUT'
                            className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_TEXTAREAINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_datareferenceinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="datareferenceid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="example_datareferenceinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Data Comment - Big Text

datacomment_input_row = html.Div(
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
                            id='datacommentid',
                            value='Data Comment',
                            rows=1,
                            #className='FORM_COLUMN_TEXTAREAINPUT'
                            className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_TEXTAREAINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_datacommentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="datacommentid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="example_datacommentinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Experiment - Dropdown

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

experiments_df = pd.DataFrame({'c' : experiments_list})


experiment_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Experiment :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Dropdown(
                            id='experimentid',
                            options=[
                                {'label':i, 'value':i} for i in experiments_df['c'].unique()
                            ],
                            #className='FORM_COLUMN_EXPERIMENTDROPDOWN',
                            className='FORM_COLUMN_DATA',
                        ),
                    #className='FORM_EXPERIMENTDROPDOWN_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter experiment'),
                    target="experimentid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('example experiment'),
                    target="example_experimentinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Date of Announcement - Date

dateofannouncement_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Announcement Date :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                     dcc.DatePickerSingle(
                        id='dateofannouncementid',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2023, 5, 7),
                        initial_visible_month=date(2023, 1, 1),
                        date=date(2023, 1, 1),
                        #className='FORM_COLUMN_SINGLEDATE',
                        className='FORM_COLUMN_DATA',
                                        ),
                    #className='FORM_SINGLEDATE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_dateofannouncement',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter date of announcement'),
                    target="dateofannouncementid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_dateofannouncement",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Date of Run Start - Date

dateofrunstart_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Date of Run Start :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                     dcc.DatePickerSingle(
                        id='dateofrunstartid',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2023, 5, 7),
                        initial_visible_month=date(2023, 1, 1),
                        date=date(2023, 1, 1),
                        #className='FORM_COLUMN_SINGLEDATE',
                        className='FORM_COLUMN_DATA',
                                        ),
                    #className='FORM_SINGLEDATE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_dateofrunstart',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter date of run start'),
                    target="dateofrunstartid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_dateofrunstart",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Date of Run End - Date

dateofrunend_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Date of Run End :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                     dcc.DatePickerSingle(
                        id='dateofrunendid',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2023, 5, 7),
                        initial_visible_month=date(2023, 1, 1),
                        date=date(2023, 1, 1),
                        #className='FORM_COLUMN_SINGLEDATE',
                        className='FORM_COLUMN_DATA',
                                        ),
                    #className='FORM_SINGLEDATE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_dateofrunend',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter date of run end'),
                    target="dateofrunendid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_dateofrunend",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Year - Dropdown - Integer

years = range(2010,2031)
years_list = list(years)
years_list
years_df = pd.DataFrame({'c' : years_list})
years_df

'''dd = dcc.Dropdown(
        id='yearid',
        options=[
            {'label':i, 'value':i} for i in years_df['c'].unique()
        ],
    )
'''

year_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Year :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                     dcc.Dropdown(
                        id='yearid',
                        options=[
                            {'label':i, 'value':i} for i in years_df['c'].unique()
                        ],
                        #className='FORM_COLUMN_YEARDROPDOWN'
                        className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_YEARDROPDOWN_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                dbc.Col(dcc.Input(id='example_yearinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('select year'),
                    target="yearid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('2023'),
                    target="example_yearinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# X Rescale - Exponential

rescalex_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Rescale X :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(
                        id="rescalexid",
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
                dbc.Col(dcc.Input(id='example_rescalexinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter rescale x'),
                    target="rescalexid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('example rescale'),
                    target="example_rescalexinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Y Rescale - Exponential

rescaley_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Rescale Y :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Input(
                        id="rescaleyid",
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
                
                dbc.Col(dcc.Input(id='example_rescaleyinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter rescale y'),
                    target="rescaleyid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('rescale y example'),
                    target="example_rescaleyinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# X Unit

xunit_input_row = html.Div(
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
                        id="xunitid",
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
                
                dbc.Col(dcc.Input(id='example_xunitinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter x unit'),
                    target="yunitid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('x unit example'),
                    target="example_xunitinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Y Unit

yunit_input_row = html.Div(
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
                        id="yunitid",
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
                
                dbc.Col(dcc.Input(id='example_yunitinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter y unit'),
                    target="yunitid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('y unit example'),
                    target="example_yunitinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Data Values - big text field

datavalues_input_row = html.Div(
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
                            id='datavaluesid',
                            value='Data Values',
                            rows=1,
                            className='FORM_COLUMN_DATA'
                    ),
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_datavaluesinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="datavaluesid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="example_datavaluesinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Data Formatting Help

# Result Type - Dropdown

resulttype_lol = [['Theory','Th'],['Project','Proj'],['Experiment','Exp']]
resulttype_lol
resulttypeDict = {item[0]: item[1] for item in resulttype_lol}

resulttype_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Result Type :',
                               className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Dropdown(
                    id='resulttypeid',
                    options=[{'label': k, 'value': v} for k, v in resulttypeDict.items()],
                        #className='FORM_COLUMN_RESULTTYPE'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_RESULTTYPE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_resulttypeinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter result type'),
                    target="resulttypeid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('result type example'),
                    target="example_resulttypeinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Limit Type

limit_type_lol = [['All',-1],['Official','1']]
#limit_type,All,-1
#limit_type,Official,"1"
limit_typeDict = {item[0]: item[1] for item in limit_type_lol}

limittype_input_row = html.Div(
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
                        id='limittypeid',
                        options=[{'label': k, 'value': v} for k, v in limit_typeDict.items()],
                        #className='FORM_COLUMN_LIMITTYPE'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_LIMITTYPE_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_limittypeinput',
                                  type='text',
                                  value='example',
                                  readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="limittypeid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_limittypeinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Spin Dependency - Dropdown

spin_lol = [['All','All'],['spin-dependent','SD'],['spin-independent','SI']]
spinDict = {item[0]: item[1] for item in spin_lol}

spindependency_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Spin Dependency :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Dropdown(
                    id='spindependencyid',
                    options=[{'label': k, 'value': v} for k, v in spinDict.items()],
                        #className='FORM_COLUMN_SPIN'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_SPIN_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_spindependency', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="spindependencyid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_spindependency",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Measurement Type - Dropdown

measurementtype_lol = [['All','All'],['Direct','Dir']]
measurementtypeDict = {item[0]: item[1] for item in measurementtype_lol}

measurementtype_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Measurement Type :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width = label_column_width
                ),
                dbc.Col(
                    dcc.Dropdown(
                    id='measurementtypeid',
                    options=[{'label': k, 'value': v} for k, v in measurementtypeDict.items()],
                        #className='FORM_COLUMN_SPIN'
                        className='FORM_COLUMN_DATA'
                        ),
                    #className='FORM_SPIN_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_measurementtype', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="measurementtypeid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_measurementtype",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


# Public Limit - Checkbox

publiclimit_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Public Limit :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width= label_column_width
                ),
                dbc.Col(
                    daq.BooleanSwitch(id='publiclimitid',
                                      on=False,
                                      className='FORM_COLUMN_DATA'
                                        ),
                    #className='FORM_CHECKBOXINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_publiclimit', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle check box'),
                    target="publiclimitid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Yes'),
                    target="example_publiclimit",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Other Users - CSV of Users

otherusers_input_row = html.Div(
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
                            id='otherusersid',
                            value='Textarea content',
                            rows=1,
                            #className='FORM_COLUMN_TEXTAREAINPUT'
                            className='FORM_COLUMN_DATA'
                    ),
                    #className='FORM_TEXTAREAINPUT_COLUMN',
                    className='FORM_DATA_COLUMN',
                    width = data_column_width
                ),
                
                dbc.Col(dcc.Input(id='example_otherusersinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('enter list of users'),
                    target="otherusersid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('user1, user2, user3'),
                    target="example_otherusersinput",trigger="click"), 
                
            ],
        className='g-0'),
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
                            id='officialid',
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
                
                dbc.Col(dcc.Input(id='example_officiallimit', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle checkbox'),
                    target="officialid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Yes'),
                    target="example_officiallimit",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Experiment Type - Dropdown ???

# Greatest Hits - Dropdown

greatesthits_input_row = html.Div(
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
                            id='greatesthitid',
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
                
                dbc.Col(dcc.Input(id='example_greatesthit', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                
                dbc.Popover(
                    dbc.PopoverBody('toggle checkbox'),
                    target="greatesthitid",trigger="hover"),
                
                dbc.Popover(dbc.PopoverBody('Yes'),
                    target="example_greatesthit",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

##########################

############################################
# BUTTONS
############################################

#submit_button =  dbc.Col(dbc.Button("Submit", color="primary"), width="auto")

save_button =  html.Div(dbc.Button("Save", color="primary"), className = "FORM_SAVE_BUTN")

create_button =  html.Div(dbc.Button("Create", color="primary"), className = "FORM_CREATE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

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
)


################################################
## NEW PLOT FORM
################################################


newplot_form = html.Div([
                plotname_input_row,
                button_input_row])

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
datavaluesid
datacommentid
datalabelid
datareferenceid
dateofannouncementid
dateofrunstartid
dateofrunendid
tracecolorid
linestyleid
experimentid
publiclimitid
resulttypeid
spindependencyid
rescalexid
xunitid
rescaleyid
yunitid
yearid
'''            

load_limit_file_form = html.Div(
        [uploadxmlfile_input_row,
        datavalues_input_row,
        datacomment_input_row,
        datalabel_input_row,
        datareference_input_row,
        dateofannouncement_input_row,
        dateofrunstart_input_row,
        dateofrunend_input_row,
        tracecolor_input_row,
        linestyle_input_row,
        experiment_input_row,
        publiclimit_input_row,
        resulttype_input_row,
        spindependency_input_row,
        rescalex_input_row,
        xunit_input_row,
        rescaley_input_row,
        yunit_input_row,
        year_input_row
    ])



############################################
## EDIT LIMIT FORM
############################################

edit_limit_form = html.Div(
        [uploadxmlfile_input_row,
        datalabel_input_row,
        datareference_input_row,
        datacomment_input_row,
        datavalues_input_row,
        experiment_input_row,
        dateofannouncement_input_row,
        year_input_row,
        rescaley_input_row,
        rescalex_input_row])


############################################
## EDIT EXISTING LIMIT FORM
############################################

edit_existinglimit_form = html.Div(
        [rescalex_input_row,
        datavalues_input_row,
        resulttype_input_row,
        spindependency_input_row,
        measurementtype_input_row,
        publiclimit_input_row,
        otherusers_input_row
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

emailform_title = html.Div(html.P(children='Please Login', className = "NOPADDING_CONTENT FORM_TITLE"))


enter_emailandpassword  = dbc.Row(
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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

login_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     emailform_title, enter_emailandpassword,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

create_new_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_limit_form_title,
     create_new_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

edit_existing_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_limit_form_title,
     create_new_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

create_new_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     create_new_plot_form_title,
     create_new_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

edit_existing_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_existing_plot_form_title,
     edit_existing_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

select_limits_to_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_existing_plot_form_title,
     edit_existing_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

style_plot_and_traces_form_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     style_plot_and_traces_form_title,
     style_plot_and_traces_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

show_plot_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     show_plot_form_title,
     show_plot_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

list_user_plots_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_user_plots_form_title,
     list_user_plots_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

list_all_limits_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     list_all_limits_form_title,
     list_all_limits_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)

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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

show_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     show_limit_form_title,
     show_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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

save_button =  html.Div(dbc.Button("Save",id="save_button1", color="primary"), className = "FORM_SAVE_BUTN")

submit_button =  html.Div(dbc.Button("Submit", id="submit_button1", color="primary"), className = "FORM_SUBMIT_BUTN")

cancel_button =  html.Div(dbc.Button("Cancel",  id="cancel_button1", color="secondary"), className = "FORM_CANCEL_BUTN")

#cancel_button =  dbc.Col(dbc.Button("Cancel", color="secondary"), width="auto")

edit_limit_form = html.Div(
    #[newplot_title,newplot_input3],
    [dcc.Location(id="url", refresh=True),
     edit_limit_form_title,
     edit_limit_form_content,
     submit_button, cancel_button],
    className = "NOPADDING_CONTENT CENTRE_FORM"
)


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


