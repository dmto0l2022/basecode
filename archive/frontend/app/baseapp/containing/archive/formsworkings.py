#import dash_bootstrap_components as dbc
#from dash import html
import pandas as pd


popovers = html.Div(
    [
        # First example - using dbc.PopoverBody
        dbc.Button(
            "popover-target",
            id="popover-target",
            className="me-1",
        ),
        dbc.Popover(dbc.PopoverBody('dd'))
        #dbc.Popover(
        #    dbc.PopoverBody("My `target` is `popover-target`."),
        #    target="popover-target",
        #    trigger="click",
        #),
        # Second example - using body=True
        dbc.Button(
            "popover-alt-target",
            id="popover-alt-target",
            className="me-1",
        ),
        #dbc.Popover(
        #    "My `target` is `popover-alt-target`.",
        #    #body=True,
        #    target="popover-alt-target",
        #    trigger="click",
        #),
    ]
)


from datetime import daterow = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Range :',
                               style={"text-align":"right","padding":"0 !important",
                                      "margin": "0 !important","border-style": "solid",
                                     "width": "100%",}),
                    style={"padding":"0 !important",
                           "margin": "0 !important", "border-style": "solid", "width": "1"},
                    width=2
                ),
                dbc.Col(dcc.Input(id='rangeinput', type='number', min=2, max=10, step=1,
                                  style={"font":"bold", "font-size": "14px", "width":"140px"}),
                        style={"padding":"0 !important", "margin": "0 !important", "border-style": "solid"},
                        width=1),
                dbc.Col(dcc.Input(id='example1', type='text', value='example', readOnly=True,
                  style={"font":"bold", "font-size": "12px",
                         "border-style": "none", "height":"18px", "width":"50px",
                        "text-decoration": "underline"}),
                        style={"padding":"0 !important", "margin": "0 !important", "border-style": "solid"},
                        width=1),
                dbc.Popover(dbc.PopoverBody('enter number between 2 and 10'),
                            target="rangeinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('3'),target="example1",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


range_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Range :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Input(id='rangeinput', type='number', min=2, max=10, step=1,
                                  className='FORM_COLUMN_RANGEINPUT'),
                    className='FORM_RANGEINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example1', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number between 2 and 10'),
                    target="rangeinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('3'),
                    target="example1",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

text_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Text :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Input(id='textinput', type='text',maxLength=10,
                                  className='FORM_COLUMN_TEXTINPUT'),
                    className='FORM_TEXTINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_textinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter text'),
                    target="textinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('3'),
                    target="example_textinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

# Define scale factors
def get_scale_factor(unit):
    BARN_CM2= 1e-24
    
    if (unit == "b"):
        return BARN_CM
    elif (unit == "mb"):
        return 1e-3*BARN_CM2
    elif (unit == "ub"):
        return 1e-6*BARN_CM2
    elif (unit == "nb"):
        return 1e-9*BARN_CM2
    elif (unit == "pb"):
        return 1e-12*BARN_CM2
    elif (unit == "fb"):
        return 1e-15*BARN_CM2
    elif (unit == "ab"):
        return 1e-18*BARN_CM2
    elif (unit == "zb"):
        return 1e-21*BARN_CM2
    elif (unit == "yb"):
        return 1e-24*BARN_CM2
    else: 
        return 1

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
scale_loldd = dcc.Dropdown(
        id='scaleid',
        options=[{'label': k, 'value': v} for k, v in scaleDict.items()]
    )

scale_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Scale :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='scaleid',
                        options=[{'label': k, 'value': v} for k, v in scaleDict.items()],
                        className='FORM_COLUMN_SCALE'
                        ),
                    className='FORM_SCALE_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_scale', type='text', value='example', readOnly=True,
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

 ta = dcc.Textarea(
        id='textarea-example',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 300},
    )
    
textarea_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Text :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Textarea(
                            id='textarea-example',
                            value='Textarea content',
                            rows=1,
                            className='FORM_COLUMN_TEXTAREAINPUT'
                    ),
                    className='FORM_TEXTAREAINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_textareainput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter multiple lined text'),
                    target="textareainput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('Textarea example content\nwith multiple lines of text'),
                    target="example_textareainput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

number_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Enter Number :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Input(id='numberinput', type='number',
                                  className='FORM_COLUMN_NUMBERINPUT'),
                    className='FORM_NUMBERINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

dropdown_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                           options=[
                               {'label': 'New York City', 'value': 'New York City'},
                               {'label': 'Montreal', 'value': 'Montreal'},
                               {'label': 'San Francisco', 'value': 'San Francisco'},
                           ],
                           value='Montreal',
                           className='FORM_COLUMN_DROPDOWNINPUT',
                        ),
                    className='FORM_DROPDOWNINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

checkbox_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Checklist(
                            id='checklistid',
                            options=[
                                   ##{'label': 'New York City', 'value': 'New York City'},
                                   {'label': 'Montreal', 'value': 'Montreal'}
                                   ##{'label': 'San Francisco', 'value': 'San Francisco'},
                               ],
                            value=['Montreal'],
                            className='FORM_COLUMN_CHECKBOXINPUT',
                            labelStyle={'display': 'block'} ,
                                        ),
                    className='FORM_CHECKBOXINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

radioitem_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.RadioItems(
                        id = 'radioitemid',
                           options=[
                               {'label': 'New York City', 'value': 'New York City'},
                               {'label': 'Montreal', 'value': 'Montreal'},
                               {'label': 'San Francisco', 'value': 'San Francisco'},
                           ],
                           value='Montreal',
                       className='FORM_COLUMN_RADIOINPUT',
                       labelStyle={'display': 'block'} ,
                                        ),
                    className='FORM_RADIOINPUT_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

upload_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                      dcc.Upload(children=[
                        'Drag and Drop or ',
                            html.A('Select a File',className='FORM_SELECTFILE')
                        ],
                       className='FORM_COLUMN_UPLOAD',
                                        ),
                    className='FORM_UPLOAD_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

singledate_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                     dcc.DatePickerSingle(
                        id='my-date-picker-single',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2023, 5, 7),
                        initial_visible_month=date(2023, 1, 1),
                        date=date(2023, 1, 1),
                       className='FORM_COLUMN_SINGLEDATE',
                                        ),
                    className='FORM_SINGLEDATE_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

years = range(2010,2031)
years_list = list(years)
years_list
years_df = pd.DataFrame({'c' : years_list})
years_df

dd = dcc.Dropdown(
        id='yearsdropdown',
        options=[
            {'label':i, 'value':i} for i in years_df['c'].unique()
        ],
    )

years = range(2010,2031)
years_list = list(years)
years_list
years_df = pd.DataFrame({'c' : years_list})
years_df

dd = dcc.Dropdown(
        id='yearsdropdown',
        options=[
            {'label':i, 'value':i} for i in years_df['c'].unique()
        ],
    )


year_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                     dcc.Dropdown(
                        id='yearsdropdown',
                        options=[
                            {'label':i, 'value':i} for i in years_df['c'].unique()
                        ],
                        className='FORM_COLUMN_YEARDROPDOWN'
                    ),
                    className='FORM_YEARDROPDOWN_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

color_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                     dbc.Input(
                        type="color",
                        id="colorpicker",
                        value="#000000",
                     className='FORM_COLUMN_COLOR'
                    ),
                    className='FORM_COLOR_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

#circle, 9675	25CB	 
#square, 	9643	25AB
#diamond, 9671	25C7	 
#x, 9747	2613
#triangle, 9661	25BD	

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
itemDict

itemDict = {item[0]: item[1] for item in lol}
itemDict
symboldd = dcc.Dropdown(
        id='dropdownid',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()]
    )

symbol_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    symboldd,
                    className='FORM_COLOR_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

linestyle_list = ['solid','dash','dot','dashdot']
['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']

linestyle_df = pd.DataFrame({'c' : symbols_list})
labels_list = [
           html.Span([dcc.Markdown('&#9473')]),
           html.Span([dcc.Markdown('&#9476')]),
           html.Span([dcc.Markdown('&#8226')]),
           html.Span([dcc.Markdown('&#9476 &#8226')])
          ]
#symbols_df = pd.DataFrame({'c' : symbols_list})
#labels_df = pd.DataFrame({'c' : labels_list})
#labels_df
lol = []
for p in (range(0,4)):
    l = [labels_list[p],linestyle_list[p]]
    lol.append(l)
    
itemDict = {item[0]: item[1] for item in lol}
itemDict

linestyle_list = ['line','dash','dot','dashdot']
linestyle_df = pd.DataFrame({'c' : symbols_list})
labels_list = [
           html.Span([dcc.Markdown('&#9473')]),
           html.Span([dcc.Markdown('&#9476')]),
           html.Span([dcc.Markdown('&#8226')]),
           html.Span([dcc.Markdown('&#9476 &#8226')])
          ]
#symbols_df = pd.DataFrame({'c' : symbols_list})
#labels_df = pd.DataFrame({'c' : labels_list})
#labels_df
lol = []
for p in (range(0,4)):
    l = [labels_list[p],linestyle_list[p]]
    lol.append(l)
    
itemDict = {item[0]: item[1] for item in lol}

limnestyledd = dcc.Dropdown(
        id='dropdownid',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()]
    )

linestyle_list = ['line','dash','dot','dashdot']
linestyle_df = pd.DataFrame({'c' : symbols_list})
labels_list = [
           html.Span([dcc.Markdown('&#9473')]),
           html.Span([dcc.Markdown('&#9476')]),
           html.Span([dcc.Markdown('&#8226')]),
           html.Span([dcc.Markdown('&#9476 &#8226')])
          ]
#symbols_df = pd.DataFrame({'c' : symbols_list})
#labels_df = pd.DataFrame({'c' : labels_list})
#labels_df
lol = []
for p in (range(0,4)):
    l = [labels_list[p],linestyle_list[p]]
    lol.append(l)
    
itemDict = {item[0]: item[1] for item in lol}

limnestyledd = dcc.Dropdown(
        id='dropdownid',
        options=[{'label': k, 'value': v} for k, v in itemDict.items()]
    )


linestyle_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    limnestyledd,
                    className='FORM_COLOR_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_numberinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="radioitemid",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

cd = dcc.Dropdown(id = 'cdid',
    options=[
        {
            "label": html.Span(children=['Montreal']),
            "value": "Montreal",
        },
        {
            "label": html.Span(children=['NYC']),
            "value": "NYC",
        },
        {
            "label": html.Span(children=['London']),
            "value": "London",
        },
    ]
)

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
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                            id='experimentdropdown',
                            options=[
                                {'label':i, 'value':i} for i in experiments_df['c'].unique()
                            ],className='FORM_COLUMN_EXPERIMENTDROPDOWN',
                        ),
                    className='FORM_EXPERIMENTDROPDOWN_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

rescalex_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Input(
                        id="rescalexid",
                        debounce=True,
                        placeholder="1e1",
                        type="text",
                        ##pattern=u"^(?:\d{3}|\(\d{3}\))([-/.])\d{3}\1\d{4}$",
                        className='FORM_COLUMN_RESCALEX'
                        ),
                    className='FORM_RESCALEX_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

rescaley_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Input(
                        id="rescalexid",
                        debounce=True,
                        placeholder="1e1",
                        type="text",
                        ##pattern=u"^(?:\d{3}|\(\d{3}\))([-/.])\d{3}\1\d{4}$",
                        className='FORM_COLUMN_RESCALEY'
                        ),
                    className='FORM_RESCALEY_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

limit_type_lol = [['All',-1],['Official','1']]
#limit_type,All,-1
#limit_type,Official,"1"
limit_typeDict = {item[0]: item[1] for item in limit_type_lol}
limit_typedd = dcc.Dropdown(
        id='llimitypeid',
        options=[{'label': k, 'value': v} for k, v in limit_typeDict.items()]
    )

limit_type_lol = [['All',-1],['Official','1']]
#limit_type,All,-1
#limit_type,Official,"1"
limit_typeDict = {item[0]: item[1] for item in limit_type_lol}

limittype_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='llimitypeid',
                        options=[{'label': k, 'value': v} for k, v in limit_typeDict.items()],
                        className='FORM_COLUMN_LIMITTYPE'
                        ),
                    className='FORM_LIMITTYPE_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

resulttype_lol = [['Theory','Th'],['Project','Proj'],['Experiment','Exp']]
resulttype_lol
resulttypeDict = {item[0]: item[1] for item in resulttype_lol}
resulttypedd = dcc.Dropdown(
        id='resulttypeid',
        options=[{'label': k, 'value': v} for k, v in resulttypeDict.items()]
    )

resulttype_lol = [['Theory','Th'],['Project','Proj'],['Experiment','Exp']]
resulttype_lol
resulttypeDict = {item[0]: item[1] for item in resulttype_lol}

resultype_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                    id='resulttypeid',
                    options=[{'label': k, 'value': v} for k, v in resulttypeDict.items()],
                        className='FORM_COLUMN_RESULTTYPE'
                        ),
                    className='FORM_RESULTTYPE_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)

spin_lol = [['All','All'],['spin-dependent','SD'],['spin-independent','SI']]
spinDict = {item[0]: item[1] for item in spin_lol}
spindd = dcc.Dropdown(
        id='spinid',
        options=[{'label': k, 'value': v} for k, v in spinDict.items()]
    )

spin_lol = [['All','All'],['spin-dependent','SD'],['spin-independent','SI']]
spinDict = {item[0]: item[1] for item in spin_lol}

spin_input_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Label('Select Option :',className='FORM_COLUMN_LABEL'),
                    className='FORM_LABEL_COLUMN',
                    width=2
                ),
                dbc.Col(
                    dcc.Dropdown(
                    id='spinid',
                    options=[{'label': k, 'value': v} for k, v in spinDict.items()],
                        className='FORM_COLUMN_SPIN'
                        ),
                    className='FORM_SPIN_COLUMN',
                    width=1
                ),
                dbc.Col(dcc.Input(id='example_experimentinput', type='text', value='example', readOnly=True,
                                  className='FORM_COLUMN_EXAMPLE'),
                    className='FORM_EXAMPLE_COLUMN',
                    width=1),
                dbc.Popover(
                    dbc.PopoverBody('enter number'),
                    target="numberinput",trigger="hover"),
                dbc.Popover(dbc.PopoverBody('4'),
                    target="example_numberinput",trigger="click"), 
                
            ],
        className='g-0'),
    ]
)


################################################
## EDIT EXISTING
################################################

## X RESCALE
xrescale_input = html.Div(
    [
        dbc.Label("Xrescale", html_for="example-Xrescale"),
        dbc.Input(type="Xrescale", id="example-Xrescale", placeholder="Enter Xrescale"),
        dbc.FormText(
            "Enter XRescale",
            color="secondary",
        ),
    ],
)

## DATA VALUE
datavalue_input = html.Div(
    [
        dbc.Label("Data Value", html_for="example-datavalue"),
        dbc.Input(type="DataValue", id="example-DataValue", placeholder="Enter Data Value"),
        dbc.FormText(
            "Enter Data Value",
            color="secondary",
        ),
    ],
)

resultype_input = html.Div(
    [
        dbc.Label("Result Type", html_for="example-resultype"),
        dbc.Input(type="ResultType", id="example-resultype", placeholder="Enter Result Type"),
        dbc.FormText(
            "Enter Result Type",
            color="secondary",
        ),
    ],
)

spindependency_input = html.Div(
    [
        dbc.Label("Spin Dependency", html_for="example-spindependency"),
        dbc.Input(type="SpinDependency", id="example-spindependency", placeholder="Enter Spin Dependency"),
        dbc.FormText(
            "Enter Spin Dependency",
            color="secondary",
        ),
    ],
)

measuretype_input = html.Div(
    [
        dbc.Label("Measure Type", html_for="example-measuretype"),
        dbc.Input(type="MeasureType", id="example-measuretype", placeholder="Enter Measure Type"),
        dbc.FormText(
            "Enter Measure Type",
            color="secondary",
        ),
    ],
)


public_input = html.Div(
    [
        dbc.Label("Public", html_for="example-public"),
        dbc.Input(type="Public", id="example-public", placeholder="Enter Public"),
        dbc.FormText(
            "Enter Public",
            color="secondary",
        ),
    ],
)

otherusers_input = html.Div(
    [
        dbc.Label("Other Users", html_for="example-otherusers"),
        dbc.Input(type="Other Users", id="example-otherusers", placeholder="Enter Other Users"),
        dbc.FormText(
            "Enter Other Users",
            color="secondary",
        ),
    ],
)