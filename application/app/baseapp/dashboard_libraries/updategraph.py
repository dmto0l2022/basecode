#from all_data_tables import limits_metadata_df
#from all_data_tables import limits_data_df
#from all_data_tables import limits_traces_df
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from app.baseapp.dashboard_libraries import get_limit_data as gld


def UpdateGraph(dmtools_userid_in, plotseries_table_in):
    #result_ids = [1,262]
    print("plotseries_table_in >>>>>>>>>>>>", plotseries_table_in)
    plot_series_df = pd.DataFrame.from_dict(plotseries_table_in)
    
    result_ids_plot = plot_series_df['limit_id'].unique().tolist()
    
    limit_list_df, trace_list_df, limit_data_df, limit_list_dict = gld.GetListOfLimits(dmtools_userid_in, result_ids_plot)
    
    #plot_series_df = pd.DataFrame(plotseries_table_in)
    
    
    
    #plotseries_default, df_experiment_plot = CreatePlotSeries(result_ids_plot)
    #plotseries_default_plot = CreatePlotSeriesDefault(df_experiment_all_plot)

    # Create figure
    fig3 = go.Figure()

    for index, row in plot_series_df.iterrows():
        trace_data = limit_data_df[(limit_data_df['limit_id']==row['limit_id'])
                                        & (limit_data_df['trace_id']==row['trace_id'])]

        # print('trace_data>>>>', trace_data)
        
        trace2add = trace_data.sort_index()

        trace_name = str(row['trace_name'])
        
        fig3.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'],
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

        fig3.update(xaxis_type = 'log', yaxis_type = 'log')
        fig3.update(layout_showlegend=False)
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

    return fig3
#result_ids = [1,262]
#fig5 = UpdateGraph(plotseries_default)
#fig5.show()
