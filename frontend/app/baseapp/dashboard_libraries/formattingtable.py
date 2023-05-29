from dash import dash_table

style_table={
                #'maxHeight': '50ex',
                'height': '44vh', ## does not know any detail about parent container
                'overflowY': 'scroll', # 'auto'
                'overflowX': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            }

# style cell
style_cell={
    'fontFamily': 'Open Sans',
    'textAlign': 'center',
    #'height': '60px',
    #'padding': '2px 22px',
    ##'height': '11px', ### this did not have any impact, see css in DataTable Definition
    'padding': '0px 0px',
    'whiteSpace': 'inherit',
    #'overflow': 'hidden',
    #'textOverflow': 'ellipsis',
    "padding-left": 0,
     "padding-right":0,
     "margin-left":0,
     "margin-right": 0,
     "fontSize":10,
}

def CreateFormatTable(limits_traces_in):

    default_plotseries_df = limits_traces_in
    
    line_color_list = ['black','red','orange','yellow','lime green', 'green', 'cyan',
              'sky blue', 'blue', 'purple', 'magenta', 'pink']
    
    fill_color_list = ['LightGrey','black','red','orange','yellow','lime green', 'green', 'cyan',
              'sky blue', 'blue', 'purple', 'magenta', 'pink']
    
    symbol_color_list = ['LightGrey','black','red','orange','yellow','lime green', 'green', 'cyan',
              'sky blue', 'blue', 'purple', 'magenta', 'pink']
    
    line_color_options=[{'label': i, 'value': i} for i in line_color_list]
    
    fill_color_options=[{'label': i, 'value': i} for i in fill_color_list]
    
    symbol_color_options=[{'label': i, 'value': i} for i in symbol_color_list]
    
    line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    
    line_styles_options=[{'label': i, 'value': i} for i in line_styles_list]
    
    symbol_list = ['circle','square','diamond','cross','x','hexagon','pentagon','octagon','star','asterisk','hash']
    
    symbol_options=[{'label': i, 'value': i} for i in symbol_list]
    
    format_datatable_out = dash_table.DataTable(
            id='format_table_id',
            #row_deletable=True,
            # Add this line
            fixed_rows={'headers': True},
            style_table=style_table,  # defaults to 500
            #style_cell={'fontSize':10,'height':11} ,
            style_cell=style_cell,
            fill_width=True,
            #style_table={'overflowY': 'auto'},
            #virtualization=True
            data=default_plotseries_df.to_dict('records'),
            columns=[
                {'id': 'limit_id', 'name': 'limit_id'},
                ##{'id': 'data_label', 'name': 'data_label'},
                {'id': 'trace_id', 'name': 'trace_id'},
                {'id': 'trace_name', 'name': 'trace_name'},
                {'id': 'line_color', 'name': 'line_color', 'presentation': 'dropdown'},
                {'id': 'line', 'name': 'line', 'presentation': 'dropdown'},
                {'id': 'fill_color', 'name': 'fill_color', 'presentation': 'dropdown'},
                {'id': 'symbol', 'name': 'symbol', 'presentation': 'dropdown'},
                {'id': 'symbol_color', 'name': 'symbol_color', 'presentation': 'dropdown'},
            ],

            editable=True,
            css=[
                {"selector": ".Select-menu-outer", "rule": "display: block !important"}
                #{"selector": ".dash-spreadsheet tr th", "rule": "height: 5px;"},  # set height of header
                #{"selector": ".dash-spreadsheet tr td", "rule": "height: 5px;"}  # set height of body rows
                ],

            dropdown={
                'line_color': {
                    'options': [
                        {'label': i, 'value': i}
                        for i in line_color_list
                    ]
                },
                'line': {
                     'options': [
                        {'label': i, 'value': i}
                        for i in line_styles_list
                    ]
                },
                'fill_color': {
                    'options': [
                        {'label': i, 'value': i}
                        for i in fill_color_list
                    ]
                },
                'symbol': {
                     'options': [
                        {'label': i, 'value': i}
                        for i in symbol_list
                    ]
                },
                 'symbol_color': {
                     'options': [
                        {'label': i, 'value': i}
                        for i in symbol_color_list
                    ]
                }
            },
            style_cell_conditional=[
                {'if': {'column_id': 'limit_id'},
                 'width': '10%'},
                #{'if': {'column_id': 'data_label'},
                # 'width': '40%'},
                {'if': {'column_id': 'trace_id'},
                 'width': '10%'},
                {'if': {'column_id': 'trace_name'},
                 'width': '15%'},
                {'if': {'column_id': 'line_color'},
                 'width': '5%'},
                {'if': {'column_id': 'line'},
                 'width': '5%'},
                {'if': {'column_id': 'fill_color'},
                 'width': '5%'},
                {'if': {'column_id': 'symbol'},
                 'width': '5%'},
                {'if': {'column_id': 'symbol_color'},
                 'width': '5%'}],
        )

    return format_datatable_out