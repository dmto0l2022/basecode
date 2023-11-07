from sqlalchemy import create_engine
import pandas as pd
from dash import dash_table

import os
from os import environ, path

from dotenv import load_dotenv

load_dotenv(".env")

#import mariadb
import requests

dropdown_api = 'dropdown_valuepair'

##########################################################


class DashDataAndTables():

    #import psycopg2
    #engine1 = create_engine(MARIADB_URI1)

    ##sqlquery = '''SELECT id, name FROM RubyDB.experiments;'''


    def __init__(self,dmtools_userid_in):
        self.experiments_df = None
        self.result_types_df = None
        self.spin_dependency_df = None
        self.greatest_hit_df = None
        self.limits_df = None
        self.limits_table_df = None
        self.limits_metadata_df = None
        self.limits_traces_df = None
        self.limits_data_df = None
        self.official_df = None
        self.years_df = None
        
        self.years_table = None
        self.official_table = None
        self.experiments_table = None
        self.result_types_table = None
        self.spin_dependency_table = None
        self.greatest_hit_table = None
        self.limits_table = None
        self.plots_table = None
        
        self.populate_dataframes(dmtools_userid_in)
        

    def populate_dataframes(self,dmtools_userid_in):
        #do some parsing
        dropdown_route = 'metadata/dropdown_valuepair'
        limit_route = 'data/limits'
        fastapi_url = "http://container_fastapi_about_1:8014/dmtool/fastapi_data/internal/"
        fastapi_get_dropdown = fastapi_url + dropdown_route + "?variable_in="
        fastapi_get_limits = fastapi_url + limit_route
        ##  'https://dev1.dmtool.info/dmtool/fastapi_data/internal/dropdown_valuepair?variable_in=year' \
        
        #r = requests.get(url, headers=headers)
        #response_data = r.json()
        #print('response data')
        #print('===================')
        #print(response_data)
        #print('===== response data frame ==============')
        #response_data_frame = pd.DataFrame(response_data)
        #response_data_frame = pd.DataFrame.from_dict(response_data['limits'])
        #print(response_data_frame)
        #print('===== response data frame ==============')
        
        
        #self.all_dropdown_pairs = \
        #    pd.read_sql('SELECT variable,label, value, data_type FROM dropdown_valuepairs', con=self.engine)

        experiments_req_url = fastapi_get_dropdown + 'experiment'
        print(experiments_req_url)
        r = requests.get(experiments_req_url)
        experiments_response_data = r.json()
        print("experiments_response_data: " ,experiments_response_data)
        
        self.experiments_df = pd.DataFrame.from_dict(experiments_response_data)
        self.experiments_df.reset_index(drop=True, inplace=True)

        result_types_req_url = fastapi_get_dropdown + 'result_type'
        r = requests.get(result_types_req_url)
        result_types_response_data = r.json()
        
        self.result_types_df  = pd.DataFrame.from_dict(result_types_response_data)
        
        self.result_types_df.reset_index(drop=True, inplace=True)

        spin_dependency_req_url = fastapi_get_dropdown + 'spin_dependency'
        r = requests.get(spin_dependency_req_url)
        spin_dependency_response_data = r.json()
        
        self.spin_dependency_df  =  pd.DataFrame.from_dict(spin_dependency_response_data)
        
        self.spin_dependency_df.reset_index(drop=True, inplace=True)

        greatest_hit_req_url = fastapi_get_dropdown + 'greatest_hit'
        r = requests.get(greatest_hit_req_url)
        greatest_hit_response_data = r.json()
        
        self.greatest_hit_df = pd.DataFrame.from_dict(greatest_hit_response_data)
        
        #self.greatest_hit_df.reset_index(drop=True, inplace=True)

        official_req_url = fastapi_get_dropdown + 'official'
        r = requests.get(official_req_url)
        official_response_data = r.json()
        
        self.official_df = pd.DataFrame.from_dict(official_response_data)
        
        #self.official_df.reset_index(drop=True, inplace=True)

        year_req_url = fastapi_get_dropdown + 'year'
        r = requests.get(year_req_url)
        year_response_data = r.json()
        
        self.years_df = pd.DataFrame.from_dict(year_response_data)
        
        #self.years_df.reset_index(drop=True, inplace=True)

        ## get limits
        fastapi_get_limits = fastapi_url + limit_route
        headers={"dmtool-userid":str(dmtools_userid_in)}
        r = requests.get(fastapi_get_limits, headers=headers)
        response_data = r.json()
        #print('response data')
        #print('===================')
        #print(response_data)
        print('===== response data frame ==============')
        #response_data_frame = pd.DataFrame(response_data)
        response_data_frame = pd.DataFrame.from_dict(response_data['limits'])

        #print('limits response df : ' , response_data_frame)
        
        limits_sql_old = '''SELECT
        id, spin_dependency, result_type, measurement_type, nomhash, x_units, y_units, x_rescale,
        y_rescale, default_color, default_style,
        data_values, data_label, file_name, data_comment,
        data_reference, created_at, updated_at, creator_id, experiment, rating, date_of_announcement,
        public, official, date_official, greatest_hit, date_of_run_start, date_of_run_end, `year`
        FROM RubyDB.limits;'''

        limits_sql = '''SELECT id, limit_id, spin_dependency, result_type, measurement_type, nomhash, x_units, y_units, x_rescale,
        y_rescale, default_color, default_style, data_label, file_name, data_comment,
        data_reference, created_at, updated_at, creator_id, experiment, rating, date_of_announcement,
        public, official, date_official, greatest_hit, date_of_run_start, date_of_run_end, `year`
        FROM test.limits_metadata;'''
        
        self.limits_df = response_data_frame.copy()
        
        self.limits_df['rowid'] = self.limits_df.index

        self.limits_table_df = self.limits_df[['id','spin_dependency',
                                     'experiment','official','greatest_hit','data_label',
                                     'result_type','data_reference','year']].copy()

        #self.limits_table_df['expid'] = self.limits_table_df['rowid']

        limits_metadata_sql = '''SELECT id, spin_dependency, result_type, measurement_type,
                                nomhash, x_units, y_units, x_rescale, y_rescale, default_color,
                                default_style, data_label, file_name, data_comment, data_reference,
                                created_at, updated_at, creator_id, experiment, rating,
                                date_of_announcement, public, official, date_official, greatest_hit,
                                date_of_run_start, date_of_run_end, `year` FROM
                                `test`.limits_metadata;'''

        #self.limits_metadata_df = pd.read_sql_query(limits_metadata_sql, self.engine)
        
        self.limits_metadata_df = self.limits_df[['id', 'spin_dependency', 'result_type', 'measurement_type',
                                'nomhash', 'x_units', 'y_units', 'x_rescale', 'y_rescale', 'default_color',
                                'default_style', 'data_label', 'file_name', 'data_comment', 'data_reference',
                                'created_at', 'updated_at', 'creator_id', 'experiment', 'rating',
                                'date_of_announcement', 'public', 'official', 'date_official', 'greatest_hit',
                                'date_of_run_start', 'date_of_run_end', 'year']].copy()
        
        #self.limits_metadata_df['rowid'] = self.limits_metadata_df.index

        #####

        #limits_traces_sql = '''SELECT distinct limit_id, trace_id, trace_name FROM `test`.limits_data;;'''
        #self.limits_traces_df = pd.read_sql_query(limits_traces_sql, self.engine)
        #self.limits_traces_df['rowid'] = self.limits_traces_df.index
        #self.limits_traces_df['line_color'] = 'black'
        #self.limits_traces_df['line'] = 'solid'
        #self.limits_traces_df['fill_color'] = 'LightGrey'
        #self.limits_traces_df['symbol'] = 'square'
        #self.limits_traces_df['symbol_color'] = 'blue'

        #limits_data_sql = '''SELECT id, limit_id, trace_id, trace_name, x, y FROM `test`.limits_data;'''

        #self.limits_data_df = pd.read_sql_query(limits_data_sql, self.engine)
        #self.limits_data_df['rowid'] = self.limits_data_df.index

        ###########################################################################

        
        table_heights = 60
        font_size = '11px'
        row_height = '12px'

        table_style_cell = {'textAlign': 'left',
                                  'padding': '0px',
                                  'font_size': font_size,
                                  'overflow': 'hidden',
                                  'textOverflow': 'ellipsis',
                                  'border': '1px solid black',
                                  'height': row_height,
                                  'overflow': 'hidden',
                                  'maxWidth': 0 ## made things work!!
                                 }
        
        table_css=  = [
                            {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                            {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                            {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of body rows
                            {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},  # set height of header
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"},
                            {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + self.row_height + "; height: " + self.row_height + ";line-height: " + self.row_height + ";max-height: " + self.row_height + ";"}
                            ]
        

        style_header_var={ 'backgroundColor': 'black','color': 'white'}

        self.years_table = dash_table.DataTable(
            id='years_table',
            columns=[
                {'name': 'year', 'id': 'label', 'type': 'text'},
            ],
            data=self.years_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            fixed_rows={'headers': True},
            #page_size=3,
            style_cell_conditional=[
                {'if': {'column_id': 'year'},
                 'width': '90%'},
            ],
            style_cell=table_style_cell,
            css=table_css,
            selected_rows=[],
            style_table={
                'height': table_heights,
            },
            style_header=style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.official_table = dash_table.DataTable(
            id='official_table',
            columns=[
                {'name': 'official', 'id': 'label', 'type': 'boolean'},
            ],
            data=self.official_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            fixed_rows={'headers': True},
            style_cell=table_style_cell,
            css=table_css,
            selected_rows=[],
            style_table={
                'height': table_heights,
            },
            style_header=style_header_var,
            #style_data={
             #   'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
             #   ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.experiments_table = dash_table.DataTable(
            id='experiments_table',
            columns=[
                {'name': 'experiment', 'id': 'label', 'type': 'text'},
            ],
            data=self.experiments_df.to_dict('records'),
           filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            fixed_rows={'headers': True},
            style_table={'height': table_heights},  # defaults to 500
            style_cell=table_style_cell,
            css=table_css,
            selected_rows=[],
            style_header=style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.result_types_table = dash_table.DataTable(
            id='result_types_table',
            columns=[
                {'name': 'result_type', 'id': 'label', 'type': 'text'},
            ],
            data=self.result_types_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            style_cell=table_style_cell,
            css=table_css,
            fixed_rows={'headers': True},
            selected_rows=[],
            style_table={
                'height': table_heights,
            },
            style_header=style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.spin_dependency_table = dash_table.DataTable(
            id='spin_dependency_table',
            columns=[
                {'name': 'spin_dependency', 'id': 'label', 'type': 'text'},
            ],
            data=self.spin_dependency_df.to_dict('records'),
            filter_action='none',
            row_selectable='multi',
            #page_size=5,
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
            style_cell=table_style_cell,
            css=table_css,
            fixed_rows={'headers': True},
            selected_rows=[],
            style_table={
                'height': table_heights,
            },
            style_header=style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
            #    ##'overflow': 'hidden',
            #    ##'textOverflow': 'ellipsis',
            #}
        )

        self.greatest_hit_table = dash_table.DataTable(
            id='greatest_hit_table',
            columns=[
                {'name': 'greatest_hit', 'id': 'label', 'type': 'text'},
            ],
            data=self.greatest_hit_df.to_dict('records'),
            #page_size=5,
            fixed_rows={'headers': True},
            filter_action='none',
            row_selectable='multi',
            selected_rows=[],
            style_cell_conditional=[
                {'if': {'column_id': 'label'},
                 'width': '90%'},
            ],
             style_cell=table_style_cell,
            css=table_css,
            style_table={'height': table_heights,},
            style_header=style_header_var,
            #style_data={
            #    'width': '25px', 'minWidth': '25px', 'maxWidth': '25px',
                ##'overflow': 'hidden',
                ##'textOverflow': 'ellipsis',
            #}
        )

        self.limits_table = dash_table.DataTable(
            id='limits_table_main',
            data=self.limits_table_df.to_dict('records'),
            columns=[{'name': 'id', 'id': 'id'},
                     {'name': 'data_reference', 'id': 'data_reference'},
                     {'name': 'data_label', 'id': 'data_label'},
                     #{'name': 'experiment', 'id': 'experiment'},
                     #{'name': 'spin_dependency', 'id': 'spin_dependency'},
                     #{'name': 'result_type', 'id': 'result_type'},
                     #{'name': 'year', 'id': 'year'},
                     ],
            #fixed_rows={'headers': True},
            page_size=5,
            filter_action='none',
            #row_selectable='multi',
            #selected_rows=[],
            style_cell=table_style_cell,
            css=table_css,
            style_table={'height': '25vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'id'},
                 'width': '5%'},
                {'if': {'column_id': 'data_reference'},
                 'width': '20%'},
                {'if': {'column_id': 'data_label'},
                 'width': '35%'},
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header=style_header_var,
            #tooltip_data=[
            #    {
            #        column: {'value': str(value), 'type': 'markdown'}
            #        for column, value in row.items()
            #    } for row in data
            #],
            tooltip_duration=None,
        )

        self.filter_table_df = pd.DataFrame(data=[],columns=['variable','label','value'])
        
        self.debug_dropdown_table = dash_table.DataTable(
            id='debug_dropdown_table',
            data=self.filter_table_df.to_dict('records'),
            columns=[{'name': 'variable', 'id': 'variable'},
                     {'name': 'label', 'id': 'label'},
                     {'name': 'value', 'id': 'value'},
                     ],
            #fixed_rows={'headers': True},
            page_size=5,
            filter_action='none',
            #row_selectable='multi',
            #selected_rows=[],
            style_cell=table_style_cell,
            css=table_css,
            style_table={'height': '25vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'variable'},
                 'width': '25%'},
                {'if': {'column_id': 'label'},
                 'width': '25%'},
                {'if': {'column_id': 'value'},
                 'width': '25%'},
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header=style_header_var,
            #tooltip_data=[
            #    {
            #        column: {'value': str(value), 'type': 'markdown'}
            #        for column, value in row.items()
            #    } for row in data
            #],
            tooltip_duration=None,
        )
        
        self.plots_table_df = pd.DataFrame(data=None, columns=['index','data_reference','data_label'])
        #self.plots_table_df.set_index('expid')

        self.plots_table = dash_table.DataTable(
            id='plots_table',
            data=self.plots_table_df.to_dict('records'),
            columns=[{'name': 'id', 'id': 'id'},
                     {'name': 'data_reference', 'id': 'data_reference'},
                     {'name': 'data_label', 'id': 'data_label'},
                     #{'name': 'spin_dependency', 'id': 'spin_dependency'},
                     #{'name': 'result_type', 'id': 'result_type'},
                     #{'name': 'year', 'id': 'year'},
                     ],
            #fixed_rows={'headers': True},
            page_size=4,
            style_cell=table_style_cell,
            css=table_css,
            #sort_action='native',
            #sort_mode='multi',
            #sort_as_null=['', 'No'],
            #sort_by=[{'column_id': 'expid', 'direction': 'desc'}],
            filter_action='none',
            row_deletable=True,
            #row_selectable='multi',
            #selected_rows=[],
            style_table={'height': '25vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'id'},
                 'width': '5%'},
                {'if': {'column_id': 'tablerowid'},
                 'width': '5%'},
                {'if': {'column_id': 'data_reference'},
                 'width': '20%'},
                {'if': {'column_id': 'data_label'},
                 'width': '35%'},
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header=style_header_var,
        )
