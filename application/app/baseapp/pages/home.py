import dash
from dash import html, dcc, callback
from dash import Input, Output, State
from dash import clientside_callback
import dash_bootstrap_components as dbc
from dash import dash_table
import json
import pandas as pd


dash.register_page(__name__, path='/') ## path='/' makes it the home page for the pages app

page_name = 'home'
baseapp_prefix = '/application/baseapp'

from app.baseapp.dashboard_libraries import get_dmtool_user as gdu
from app.baseapp.libraries import page_menu as page_menu

create_plot_button = html.Button("Create Plot", id=page_name+"create_plot_button", className="btn btn-primary",type="button")

dropdown_button = html.Button(id=page_name + "dropdown_button", type="button",
                           className = "btn btn-danger dropdown-toggle dropdown-toggle-split",
                           **{
                            'data-toggle' : 'dropdown',
                            'aria-haspopup' : 'true',
                            'aria-expanded' : 'false',
                            },
                            children=html.Span(className="sr-only", children=['Create Plot Menu'])
                          )

drop_down_create =  html.A(id=page_name + "dropdown_action", children=['New'], href=baseapp_prefix + '/create_new_plot', className="dropdown-item")
drop_down_edit =  html.A(id=page_name + "dropdown_action", children=['Edit'], href=baseapp_prefix + '/edit_existing_plot', className="dropdown-item")
drop_down_list =  html.A(id=page_name + "dropdown_action", children=['List'], href=baseapp_prefix + '/list_all_plots', className="dropdown-item")
drop_down_exit =  html.A(id=page_name + "dropdown_action", children=['Exit'], href=baseapp_prefix + '/plot_menu', className="dropdown-item")

dropdown_menu = html.Div(id=page_name + "dropdown_menu", children = [drop_down_create,drop_down_edit,drop_down_list, drop_down_exit], className = "dropdown-menu")

relevant_dropdowns = [drop_down_create,drop_down_edit,drop_down_list,drop_down_exit] 

button_padding = {'height':'33px','padding-left':'12px','padding-right':'12px' ,
                          'padding-top':'0px',
                          'padding-bottom':'0px',
                          'margin':'0', 'border': '0', 'vertical-align':'middle'}

action_button = html.Button("Home",
                                       id=page_name+"home_button",
                                       className="btn btn-primary",type="button",
                                       style=button_padding)

app_page_menu = page_menu.page_top_menu(page_name,action_button,relevant_dropdowns)

##-------------------------------------

## css_row_height = self.row_height
css_row_height = '12px'


css_row_heights = [ {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                                    {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                                    {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + css_row_height + "; height: " + css_row_height + ";line-height: " + css_row_height + ";max-height: " + css_row_height + ";"},  # set height of header
                                    {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + css_row_height + "; height: " + css_row_height + ";line-height: " + css_row_height + ";max-height: " + css_row_height + ";"},
                                    {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + css_row_height + "; height: " + css_row_height + ";line-height: " + css_row_height + ";max-height: " + css_row_height + ";"},  # set height of body rows
                                    {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + css_row_height + "; height: " + css_row_height + ";line-height: " + css_row_height + ";max-height: " + css_row_height + ";"},  # set height of header
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + css_row_height + "; height: " + css_row_height + ";line-height: " + css_row_height + ";max-height: " + css_row_height + ";"},
                                    {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + css_row_height + "; height: " + css_row_height + ";line-height: " + css_row_height + ";max-height: " + css_row_height + ";"}
                                    ]

## create bottom table

#bottom_table_height = str(int(300)) + 'px'
#bottom_table_width = str(int(1000)) + 'px'
bottom_table_height = '300px'
bottom_table_width = '1000px'

bottom_table_cell_style = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': '11px',
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': '12px',
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }

bottom_table_table_style = {'height': bottom_table_height,'width' : bottom_table_width, 'overflowX': 'auto', 'overflowY': 'auto'}

data=[{'c-{}'.format(i): (j + (i-1)*5) for i in range(1, 15)} for j in range(25)]
column_names_dict = [{'name': 'c-{}'.format(i),'id': 'c-{}'.format(i)} for i in range(1,15)]
column_names_list= ['c-{}'.format(i) for i in range(1,15)]
bottom_df_full = pd.DataFrame.from_dict(data)
print(bottom_df_full)
bottom_df_empty = pd.DataFrame(data=[], columns=column_names_list)
print(bottom_df_empty)

def get_bottom_table(bottom_df_in):

    bottom_table_ret = dash_table.DataTable(
                                id='bottom_table_datatable',
                                data=bottom_df_in.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in bottom_df_in.columns],
                                fixed_rows={'headers': True},
                                virtualization=True,
                                style_cell=bottom_table_cell_style,
                                style_table=bottom_table_table_style,
                                css=css_row_heights,
                                )
    return bottom_table_ret

bottom_table = get_bottom_table(bottom_df_empty)

## create top table

top_table_cell_style = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': '11px',
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': '12px',
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }

top_df_full = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
column_names = ['state','plants','capacity','average','generation']
top_df_full.columns = column_names

top_df_empty = pd.DataFrame(data=[],columns=column_names)

print("solar columns : ", top_df_full.columns)
## State,Number of Solar Plants,Installed Capacity (MW),Average MW Per Plant,Generation (GWh)

print('top_df_full >>>>>>>>>>>>' ,top_df_full)

top_df_full_x = pd.concat([top_df_full,top_df_full,top_df_full,top_df_full])

top_table_height = '300px'
top_table_width = '1000px'

def get_top_table(top_df_in):
    top_table_ret = dash_table.DataTable(
                                       id='top_table_datatable',
                                       data=top_df_in.to_dict('records'),
                                       columns=[{"name": i, "id": i} for i in top_df_in.columns],
                                       fixed_rows={'headers': True},
                                       virtualization=True,
                                       style_cell = top_table_cell_style,
                                       style_table={'height': top_table_height,'width' : top_table_width, 'overflowX': 'auto', 'overflowY': 'auto'},
                                       css=css_row_heights)
    return top_table_ret

top_table_1 = get_top_table(top_df_empty)

top_table_div_style =  {'position':'absolute','top': '33px','padding':'0','margins':'0','left':'0','border':'5px solid red',
                            'background-color':'green','height':'300px', 'width':'600px', 'overflow-y': 'scroll'}

bottom_table_div_style =  {'position':'absolute','top': '333px','padding':'0','margins':'0','left':'0','border':'5px solid black',
                            'background-color':'blue','height':'300px', 'width':'600px', 'overflow-y': 'scroll'}

TopTableDiv = html.Div(children=[top_table_1],style=top_table_div_style)
BottomTableDiv = html.Div(children=[bottom_table], style=bottom_table_div_style)

TopRowTable = dbc.Row([dbc.Col(id=page_name+"top_table_div",
                            children=[top_table_1],
                            width=12,)],
                            style=top_table_div_style,
                            className =page_name + "top_table_class")
        

BottonRowTable = dbc.Row([dbc.Col(id=page_name+'bottom_table_div', 
                              children=[bottom_table],
                              width=12,)],
                              style=bottom_table_div_style,
                              className = page_name + "bottom_table_class")

##------------------------------------

def get_layout():
    layout_out = html.Div([
        dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
        dcc.Store(id= page_name + 'screen_size_store', storage_type='local'),
        app_page_menu,
        TopTableDiv,
        BottomTableDiv,
        html.Div(id=page_name + "action_feedback", children=['Action Feedback'])
        ])
    return layout_out

layout = get_layout


clientside_callback(
        """
        function(href) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            var jsn = {width: w, height: h};
            const myJSON = JSON.stringify(jsn); 
            return jsn;
        }
        """,
        Output(page_name + 'screen_size_store', 'data'),
        Input(page_name + 'url', 'href')
    )

@callback([Output('top_table_datatable','data'),
          Output('bottom_table_datatable','data')],       
          Input(page_name +'url', 'href'),
          State(page_name + 'screen_size_store', 'data')
         )
def get_owned_data(href: str, page_size_in):
    page_size_as_string = json.dumps(page_size_in)
    print('home : get_user_owned_data callback triggered ---- page size >>>>>>>' + page_size_as_string)
    screen_height = page_size_in['height']
    print('screen_height >>>>>>>>>>', screen_height)
    plots_table_height = str(screen_height * 0.5) + 'px'
    ## get user id from cookie
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    top_table_dict = top_df_full_x.to_dict('records')
    bottom_table_dict = bottom_df_full.to_dict('records')

    return [top_table_dict, bottom_table_dict]

## prevent_initial_call=True

@callback(
    [Output(page_name + 'url', 'href'),
    Output(page_name + "action_feedback", 'children')],
    Input(page_name+"home_button",'n_clicks'),
    prevent_initial_call=True
)
def button_click_do_something(button0):
    #msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    #msg = prop_id
    if page_name+"home_button" == prop_id :
        request_header = {'dmtool-userid': str(dmtool_userid)}
        fastapi_about_url = "http://container_fastapi_data_1:8014/"
        href_return = baseapp_prefix + '/'
        return href_return, ''
    else:
        href_return = baseapp_prefix + '/'
        return href_return, ''
