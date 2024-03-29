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



data=[{'c-{}'.format(i): (j + (i-1)*5) for i in range(1, 15)} for j in range(25)]
column_names_dict = [{'name': 'c-{}'.format(i),'id': 'c-{}'.format(i)} for i in range(1,15)]
column_names_list= ['c-{}'.format(i) for i in range(1,15)]
bottom_df_full = pd.DataFrame.from_dict(data)
print(bottom_df_full)
bottom_df_empty = pd.DataFrame(data=[], columns=column_names_list)
print(bottom_df_empty)

def get_bottom_table(bottom_df_in,page_size_in):
    
    bottom_table_width = int(page_size_in.get('width'))
    #bottom_table_height = int(page_size_in.get('height')) * 0.45
    bottom_table_height = str(int((int(page_size_in.get('height')) - 33 - 60)/2)) + 'px'
    bottom_table_width = 1000
    bottom_row_height = '12px'
    bottom_font_height = '11px'
    bottom_table_table_style = {'height': bottom_table_height,'width' : bottom_table_width, 'overflowX': 'auto', 'overflowY': 'auto'}

  
    bottom_table_cell_style = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': bottom_font_height,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': bottom_row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }

    bottom_table_ret = dash_table.DataTable(
                                id=page_name + 'bottom_table_datatable',
                                data=bottom_df_in.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in bottom_df_in.columns],
                                fixed_rows={'headers': True},
                                virtualization=True,
                                style_cell=bottom_table_cell_style,
                                style_table=bottom_table_table_style,
                                css=css_row_heights,
                                )
    return bottom_table_ret

page_size = {"width":375,"height":667}
#page_size_json = json.loads(page_size)
#width = page_size_json['width']
page_size_json = json.dumps(page_size) 

bottom_table = get_bottom_table(bottom_df_empty, page_size)

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

##top_table_height = '300px'
##top_table_width = '1000px'

def get_top_table(top_df_in, page_size_in):
    print("get tt page_size_in >>", type(page_size_in), page_size_in)
    #top_table_width = str(page_size_in['width']) + 'px'
    top_table_width = '1000px'
    screen_height = int(page_size_in.get('height'))
    #top_table_height = str(screen_height * 0.45) + 'px'
    top_table_height = str(int((int(page_size_in.get('height')) - 33 - 60)/2)) + 'px'
    top_row_height = '12px'
    top_font_height = '11px'
    top_table_table_style = {'height': top_table_height,'width' : top_table_width, 'overflowX': 'auto', 'overflowY': 'auto'}

  
    top_table_cell_style = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': top_font_height,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': top_row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
  
    top_table_ret = dash_table.DataTable(
                                       id=page_name+'top_table_datatable',
                                       data=top_df_in.to_dict('records'),
                                       columns=[{"name": i, "id": i} for i in top_df_in.columns],
                                       fixed_rows={'headers': True},
                                       virtualization=True,
                                       style_cell = top_table_cell_style,
                                       style_table= top_table_table_style,
                                       css=css_row_heights)
    return top_table_ret

page_size = {"width":'375',"height":'667'}

top_table_1 = get_top_table(top_df_empty, page_size)

'''
top_table_div_style =  {'position':'absolute','top': '33px','padding':'0','margins':'0','left':'0','border':'5px solid red',
                            'background-color':'green','height':'300px', 'width':'600px', 'overflow-y': 'scroll'}

bottom_table_div_style =  {'position':'absolute','top': '333px','padding':'0','margins':'0','left':'0','border':'5px solid black',
                            'background-color':'blue','height':'300px', 'width':'600px', 'overflow-y': 'scroll'}


'''

'''

def get_top_table_div(page_size_in,top_df_in):
    top_row_height = '12px'
    top_font_height = '11px'
    screen_height = page_size_in['height']
    screen_width = page_size_in['width']
    top_div_height = str(int(screen_height * 0.45)) + 'px'
    top_div_width = str(int(screen_width * 1)) + 'px'
    top_table_cell_style = {'textAlign': 'left',
                                          'padding': '0px',
                                          'font_size': top_font_height,
                                          'overflow': 'hidden',
                                          'textOverflow': 'ellipsis',
                                          'border': '1px solid black',
                                          'height': top_row_height,
                                          'overflow': 'hidden',
                                          'maxWidth': 0 ## made things work!!
                                         }
    top_table_div_style =  {'position':'absolute','top': '33px','padding':'0','margins':'0','left':'0','border':'5px solid red',
                            'background-color':'green','height':top_div_height, 'width':top_div_width, 'overflow-y': 'scroll'}
    top_table_style_table= {'height': top_div_height,'width' : '1000px', 'overflowX': 'auto', 'overflowY': 'auto'},
    top_table_ret = dash_table.DataTable(
                                       id='top_table_datatable',
                                       data=top_df_in.to_dict('records'),
                                       columns=[{"name": i, "id": i} for i in top_df_in.columns],
                                       fixed_rows={'headers': True},
                                       virtualization=True,
                                       style_cell = top_table_cell_style,
                                       style_table=top_table_style_table,
                                       css=css_row_heights)

'''

home_top_table_div_style =  {'position':'absolute','top': '33px','padding':'0','margins':'0','left':'0','border':'5px solid red',
                            'background-color':'green','height':'300px', 'width':'600px', 'overflow-y': 'scroll'}

home_bottom_table_div_style =  {'position':'absolute','top': '333px','padding':'0','margins':'0','left':'0','border':'5px solid black',
                            'background-color':'blue','height':'300px', 'width':'600px', 'overflow-y': 'scroll'}

TopTableTitleDiv = html.Div(id=page_name+'top_table_div_title', children="Top Table Title",
                       ##style=home_top_table_div_style,
                       className='home_top_table_title_div_class')

TopTableDiv = html.Div(id=page_name+'top_table_div', children=[top_table_1],
                       ##style=home_top_table_div_style,
                       className='home_top_table_div_class')

BottomTableTitleDiv = html.Div(id=page_name+'bottom_table_div',children="Bottom Table Title",
                          ##style=home_bottom_table_div_style,
                          className='home_bottom_table_title_div_class')

BottomTableDiv = html.Div(id=page_name+'bottom_table_div',children=[bottom_table],
                          ##style=home_bottom_table_div_style,
                          className='home_bottom_table_div_class')

action_feedback_div_style =  {'position':'absolute','top': '633px','padding':'0','margins':'0','left':'0','border':'5px solid green',
                            'background-color':'pink','height':'30px', 'width':'600px', 'overflow-y': 'scroll'}

ActionFeedBackDiv = html.Div(id=page_name + "action_feedback", children=['Action Feedback'],className='home_page_action_feedback_div_class')

##------------------------------------

def get_layout():
    layout_out = html.Div(id=page_name + 'layout_div',
      children=[
        dcc.Interval(id= page_name + 'interval-component',interval=1000,n_intervals=0),
        dcc.Location(id=page_name + "url", refresh=True), ## important to allow redirects
        dcc.Store(id= page_name + 'screen_size_store', storage_type='local'),
        app_page_menu,
        TopTableTitleDiv,
        TopTableDiv,
        BottomTableTitleDiv,
        BottomTableDiv,
        ActionFeedBackDiv
        ])
    return layout_out

layout = get_layout


clientside_callback(
        """
        function(href) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            var width_text = w.toString();
            var height_text = h.toString();
            const page_size_dict = {width: width_text, height: height_text};
            return page_size_dict;
        }
        """,
        Output(page_name + 'screen_size_store', 'data'),
        Input(page_name + 'url', 'href')
    )
'''
@callback([Output(page_name + 'layout_div', 'children')],       
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
    #top_table_dict = top_df_full_x.to_dict('records')
    #bottom_table_dict = bottom_df_full.to_dict('records')

    return TopTableDiv, BottomTableDiv
'''

@callback([Output(page_name+'top_table_div','children'),
          Output(page_name + 'bottom_table_div','children')
          ],       
          Input(page_name +'url', 'href'),
          State(page_name + 'screen_size_store', 'data')
         )
def get_owned_data(href: str, page_size_in):
    if page_size_in is None:
       page_size_in = {"width":"375","height":"667"}
    print(type(page_size_in), page_size_in)
    #print('home : get_user_owned_data callback triggered ---- page size >>>>>>>' + page_size_as_string)
    screen_height = page_size_in.get('height')
    print('screen_height >>>>>>>>>>', screen_height)
    #plots_table_height = str(int(screen_height) * 0.5) + 'px'
    ## get user id from cookie
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid

    top_df_full = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
    column_names = ['state','plants','capacity','average','generation']
    top_df_full.columns=column_names
    top_df_full_x = pd.concat([top_df_full,top_df_full,top_df_full,top_df_full])
  
    data=[{'c-{}'.format(i): (j + (i-1)*5) for i in range(1, 15)} for j in range(25)]
    column_names_dict = [{'name': 'c-{}'.format(i),'id': 'c-{}'.format(i)} for i in range(1,15)]
    column_names_list= ['c-{}'.format(i) for i in range(1,15)]
    bottom_df_full = pd.DataFrame.from_dict(data)
  
    top_table_ret = get_top_table(top_df_full_x, page_size_in)
    bottom_table_ret = get_bottom_table(bottom_df_full, page_size_in)
  
    return [top_table_ret, bottom_table_ret]


## prevent_initial_call=True

@callback(
    [Output(page_name + 'url', 'href'),
    Output(page_name + "action_feedback", 'children')],
    Input(page_name+"home_button",'n_clicks'),
    prevent_initial_call=True
)
def button_click_do_something(button0):
    msg = "None of the buttons have been clicked yet"
    prop_id = dash.callback_context.triggered[0]["prop_id"].split('.')[0]
    dmtooluser_cls = gdu.GetUserID()
    dmtool_userid = dmtooluser_cls.dmtool_userid
    #msg = prop_id
    if page_name+"home_button" == prop_id :
        msg = "button pressed " + prop_id
        request_header = {'dmtool-userid': str(dmtool_userid)}
        fastapi_about_url = "http://container_fastapi_data_1:8014/"
        href_return = baseapp_prefix + '/'
        return href_return, msg
    else:
        href_return = baseapp_prefix + '/'
        return href_return, msg
