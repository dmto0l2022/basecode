class CrudTables():
  

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
