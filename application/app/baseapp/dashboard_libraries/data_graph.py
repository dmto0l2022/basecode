from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

from app.baseapp.dashboard_libraries import get_limit_data as gld

class DataGraph:
    def __init__(self,dmtools_userid_in,  listoflimits_in):
        self.dmtools_userid = dmtools_userid_in
        self.listoflimits = listoflimits_in
        self.limits_traces_df = pd.DataFrame()
        self.limits_data_df = pd.DataFrame()
        self.plot_series_df = pd.DataFrame()
        self.GraphFig = go.Figure()
        self.UpdateData()
        self.CreatGraph()
      
    def UpdateData(self):
        self.limits_list_df, self.limits_traces_df, self.limits_data_df, self.limit_list_dict = gld.GetListOfLimits(self.dmtools_userid, self.listoflimits)

    def CreateGraph(self):
      
        self.GraphFig = go.Figure()
        
        self.GraphFig.update_layout(autosize=True)
        
        for index, row in self.limits_list_df.iterrows():
          
            trace_data = self.limits_data_df[(self.limits_data_df['limit_id']==row['limit_id'])
                                          & (self.limits_data_df['trace_id']==row['trace_id'])]
            
            trace2add = trace_data
            
            #trace_name = str(row['id']) + str(row['series'])
            trace_name = str(row['trace_name'])
            
            x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
            y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
            
            self.GraphFig.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'], ## scaled needs to be updated
                              mode='lines+markers', # 'lines' or 'markers'
                              line=dict(width=4,dash=row['line'],color=row['line_color']),
                              #showscale=False,
                              fill='toself',
                              fillcolor = row['fill_color'],
                              text=row['trace_name'],
                              marker_symbol=row['symbol'],
                                  marker=dict(
                                  size=10,
                                  color=row['symbol_color'],#set color equal to a variable
                                  #colorscale='Viridis', # one of plotly colorscales
                                  showscale=False,
                              ),
                              legendgroup=str(row['limit_id']),  # this can be any string, not just "group"
                              legendgrouptitle_text=str(row['limit_id']),
                              name=str(row['trace_name'])
                                   ))
            
            self.GraphFig.update(layout_showlegend=False)
            
            self.GraphFig.update_xaxes(
              title_text=x_title_text,
              type="log"
              #type="linear"
            )
            self.GraphFig.update_yaxes(
              title_text=y_title_text,
              #type="log"
              type="linear"
            )
            #fig3.add_trace(go.Scatter(x=trace2add['x'], y=trace2add['scaled_y'],
            #                   mode='markers', # 'lines' or 'markers'
            #                    marker_symbol=row['symbol'],
            #                         marker=dict(
            #                        size=10,
            #                        color=row['color'],#set color equal to a variable
            #                        #colorscale='Viridis', # one of plotly colorscales
            #                        showscale=False,
            #                    ),
            #                    name=str(row['id'])))
  
  
    def UpdateGraph(plotseries_table_in):
        #result_ids = [1,262]
        print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
        self.plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
        
        #result_ids_plot = plot_series_df['limit_id'].unique().tolist()
        
        limit_list_df, trace_list_df, limit_data_df, limit_list_dict = gld.GetListOfLimits(self.dmtools_userid_in, self.listoflimits)
        
        #plot_series_df = pd.DataFrame(plotseries_table_in)
        
        x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
        y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
        
        #plotseries_default, df_experiment_plot = CreatePlotSeries(result_ids_plot)
        #plotseries_default_plot = CreatePlotSeriesDefault(df_experiment_all_plot)
        
        # Create figure
        self.GraphFig = go.Figure()
        self.GraphFig.update_xaxes(
              title_text=x_title_text,
              type="log"
              #type="linear"
          )
        
        self.GraphFig.update_yaxes(
              title_text=y_title_text,
              #type="log"
              type="linear"
          )

        for index, row in self.plot_series_df.iterrows():
            trace_data = self.limits_data_df[(self.limits_data_df['limit_id']==row['limit_id'])
                                          & (self.limits_data_df['trace_id']==row['trace_id'])]
            
            # print('trace_data>>>>', trace_data)
            
            trace2add = trace_data.sort_index()
            
            trace_name = str(row['trace_name'])
            
            self.GraphFig.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'],
                              mode='lines+markers', # 'lines' or 'markers'
                              line=dict(width=4,dash=row['line'],color=row['line_color']),
                              #showscale=False,
                              text=row['trace_name'],
                              fill='toself',
                              fillcolor = row['fill_color'],
                              marker_symbol=row['symbol'],
                                   marker=dict(
                                  size=10,
                                  color=row['symbol_color'],#set color equal to a variable
                                  #colorscale='Viridis', # one of plotly colorscales
                                  showscale=False,
                              ),
                              legendgroup=str(row['limit_id']),  # this can be any string, not just "group"
                              legendgrouptitle_text=str(row['limit_id']),
                              name=str(row['trace_name'])
                                   ))
            
            self.GraphFig.update(layout_showlegend=False)
            
#result_ids = [1,262]
#fig5 = UpdateGraph(plotseries_default)
#fig5.show()
