
class StylingTable():
  
  def Create(self):
          self.TableFormat = dash_table.DataTable(
                  id=self.page_name + 'format_table_id',
                  columns=[
                      {'id': 'limit_id', 'name': 'limit_id'},
                      {'id': 'trace_id', 'name': 'trace_id'},
                      {'id': 'trace_name', 'name': 'trace_name'},
                      {'id': 'line_color', 'name': 'line_color', 'presentation': 'dropdown'},
                      {'id': 'line', 'name': 'line', 'presentation': 'dropdown'},
                      {'id': 'fill_color', 'name': 'fill_color', 'presentation': 'dropdown'},
                      {'id': 'symbol', 'name': 'symbol', 'presentation': 'dropdown'},
                      {'id': 'symbol_color', 'name': 'symbol_color', 'presentation': 'dropdown'},
                  ],
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
  
      
      def Update(self):
      
          #limits_traces_copy = limits_traces_in.copy()
          print("format table : trace_list_df.columns >> " , self.limit_data.trace_list_df.columns)
          print("format table : trace_list_df 5 >> " , self.limit_data.trace_list_df.head(5))
          palette_list = ['black','red','orange','yellow','limegreen', 'green', 'cyan','skyblue', 'blue', 'purple', 'magenta', 'pink']
          cycle_colors = itertools.cycle(palette_list)
          append_this = []
          #colored_limits = pd.DataFrame(data=None, columns=limits_traces_in.columns, index=limits_traces_in.index)
          colored_limits_list =[]
          for index, row in self.limit_data.trace_list_df.iterrows():
              #print(row['c1'], row['c2'])
              copy_row = row.copy()
              #color = next(cycle_colors)
              #copy_row['line_color'] = color
              #copy_row['symbol_color'] = color
              #copy_row['fill_color'] = color
              append_this = [copy_row['limit_id'], copy_row['data_label'],
                             copy_row['trace_id'],copy_row['trace_name'],
                             copy_row['line_color'],copy_row['symbol_color'],copy_row['fill_color'],
                             copy_row['line'],copy_row['symbol'],copy_row['id']]
              print(append_this)
              colored_limits_list.append(append_this)
      
          #Index(['id', 'limit_id', 'data_label', 'trace_id', 'trace_name', 'line_color',
          #   'symbol_color', 'fill_color', 'line', 'symbol'],
          
          print("append_this >>>>", append_this)
          print("self.limit_data.trace_list_df.columns >>>>>>", self.limit_data.trace_list_df.columns)
      
          colored_limits = pd.DataFrame(data=colored_limits_list, columns=self.limit_data.trace_list_df.columns)##, index=self.limit_data.trace_list_df.index)
          
        
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
          
          self.TableFormat = dash_table.DataTable(
                  id=self.page_name + 'format_table_id',
                  #row_deletable=True,
                  # Add this line
                  #fixed_rows={'headers': True},
                  #style_table=style_table,  # defaults to 500
                  #style_cell={'fontSize':10,'height':11} ,
                  style_cell=self.format_table_style_cell,
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
                  css=self.format_table_css,
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
