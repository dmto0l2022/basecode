import pandas as pd
from dash import dash_table

import os
from os import environ, path

class CrudTables():

    #import psycopg2
    #engine1 = create_engine(MARIADB_URI1)

    ##sqlquery = '''SELECT id, name FROM RubyDB.experiments;'''


    def __init__(self):
        self.limits_df = None
        self.limits_table_df = None
        self.limits_table = None
        self.populate_dataframes()


    def populate_dataframes(self):
        #do some parsing



        limits_sql = '''SELECT id, limit_id, spin_dependency, result_type, measurement_type, nomhash, x_units, y_units, x_rescale,
        y_rescale, default_color, default_style, data_label, file_name, data_comment,
        data_reference, created_at, updated_at, creator_id, experiment, rating, date_of_announcement,
        public, official, date_official, greatest_hit, date_of_run_start, date_of_run_end, `year`
        FROM data.limits_metadata;'''
        
        self.limits_df = pd.read_sql_query(limits_sql, self.engine)
        #self.limits_df['rowid'] = self.limits_df.index
        
        self.limits_table_df = self.limits_df[['id','limit_id','spin_dependency',
                                 'experiment','official','greatest_hit','data_label',
                                 'result_type','data_reference','year']].copy()


        ###########################################################################
        table_heights = 120
        
        style_header_var={ 'backgroundColor': 'black','color': 'white'}
                
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
            style_cell={'textAlign': 'left','padding': '0px','font_size': '12px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
            css=[{
                'selector': '.dash-spreadsheet td div',
                'rule': '''
                    line-height: 15px;
                    max-height: 45px; min-height:30px; height: 30px;
                    display: block;
                    overflow-y: hidden;
                '''
            }],
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
