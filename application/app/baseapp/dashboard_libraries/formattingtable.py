from dash import dash_table
import itertools
import pandas as pd
row_height = '12px'
font_size = '11px'

style_table={
                #'maxHeight': '50ex',
                #'minHeight': '40vh',
                ##'height': '44vh', ## does not know any detail about parent container
                ##'overflowY': 'scroll', # 'auto'
                ##'overflowX': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            }

table_style_cell = {'textAlign': 'left',
                                  'padding': '0px',
                                  'font_size': font_size,
                                  'overflow': 'hidden',
                                  'textOverflow': 'ellipsis',
                                  ##'border': '1px solid black',
                                  'height': row_height,
                                  'overflow': 'hidden',
                                  'maxWidth': 0 ## made things work!!
                                 }

table_css = [{"selector": ".Select-menu-outer", "rule": "display: block !important"},
            {"selector": "p", "rule" :"margin: 0px; padding:0px"},
            {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
            {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
            {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of body rows
            {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"}
            ]

def CreateFormatTable(page_name_in, limits_traces_in):

    #limits_traces_copy = limits_traces_in.copy()
    print("format table : limits_traces_in.columns >> " , limits_traces_in.columns)
    palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
    cycle_colors = itertools.cycle(palette_list)

    #colored_limits = pd.DataFrame(data=None, columns=limits_traces_in.columns, index=limits_traces_in.index)
    colored_limits_list =[]
    for index, row in limits_traces_in.iterrows():
        #print(row['c1'], row['c2'])
        copy_row = row.copy()
        color = next(cycle_colors)
        copy_row['line_color'] = color
        copy_row['symbol_color'] = color
        copy_row['fill_color'] = color
        append_this = [copy_row['id'], copy_row['limit_id'], copy_row['data_label'],
                       copy_row['trace_id'],copy_row['trace_name'],
                       copy_row['line_color'],copy_row['symbol_color'],copy_row['fill_color'],
                       copy_row['line'],copy_row['symbol']]
        print(append_this)
        colored_limits_list.append(append_this)

    #Index(['id', 'limit_id', 'data_label', 'trace_id', 'trace_name', 'line_color',
    #   'symbol_color', 'fill_color', 'line', 'symbol'],

    colored_limits = pd.DataFrame(data=colored_limits_list, columns=limits_traces_in.columns, index=limits_traces_in.index)
    
  
    print("formatting table >>>> colored_limits >>>", colored_limits)
  
  
    line_color_list = palette_list
    
    fill_color_list = palette_list
    
    symbol_color_list = palette_list 
  
    line_color_options=[{'label': i, 'value': i} for i in line_color_list]
    
    fill_color_options=[{'label': i, 'value': i} for i in fill_color_list]
    
    symbol_color_options=[{'label': i, 'value': i} for i in symbol_color_list]
    
    line_styles_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    
    line_styles_options=[{'label': i, 'value': i} for i in line_styles_list]
    
    symbol_list = ['circle','square','diamond','cross','x','hexagon','pentagon','octagon','star','asterisk','hash']
    
    symbol_options=[{'label': i, 'value': i} for i in symbol_list]
    
    format_datatable_out = dash_table.DataTable(
            id=page_name_in + 'format_table_id',
            #row_deletable=True,
            # Add this line
            #fixed_rows={'headers': True},
            #style_table=style_table,  # defaults to 500
            #style_cell={'fontSize':10,'height':11} ,
            style_cell=table_style_cell,
            #fill_width=True,
            #style_table={'overflowY': 'auto'},
            #virtualization=True
            data=colored_limits.to_dict('records'),
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
            css=table_css,
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
                 'width': '5%'},
                #{'if': {'column_id': 'data_label'},
                # 'width': '40%'},
                {'if': {'column_id': 'trace_id'},
                 'width': '5%'},
                {'if': {'column_id': 'trace_name'},
                 'width': '40%'},
                {'if': {'column_id': 'line_color'},
                 'width': '10%'},
                {'if': {'column_id': 'line'},
                 'width': '10%'},
                {'if': {'column_id': 'fill_color'},
                 'width': '10%'},
                {'if': {'column_id': 'symbol'},
                 'width': '10%'},
                {'if': {'column_id': 'symbol_color'},
                 'width': '10%'}],
        )

    return format_datatable_out
