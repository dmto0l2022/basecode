from plotly.subplots import make_subplots
import plotly.graph_objects as go

def CreateGraph(limits_in,limits_traces_df_in,limits_data_df_in):
    
    
    #plot_series_df = pd.DataFrame.from_dict(plotseries_in[0])
    
    
    #result_ids_plot = plotseries_in['id'].unique().tolist()
    
    plotseries = limits_traces_df_in[limits_traces_df_in['limit_id'].isin(limits_in)].copy()
    #plotseries_default_plot = CreatePlotSeriesDefault(df_experiment_all_plot)

        # Create figure
    fig3 = go.Figure()
    
    fig3.update_layout(autosize=True)

    for index, row in plotseries.iterrows():
        
        trace_data = limits_data_df_in[(limits_data_df_in['limit_id']==row['limit_id'])
                                        & (limits_data_df_in['trace_id']==row['trace_id'])]

    
        trace2add = trace_data

        #trace_name = str(row['id']) + str(row['series'])
        trace_name = str(row['trace_name'])
        
        fig3.add_trace(go.Scatter(x=trace2add['masses'], y=trace2add['cross_sections'], ## scaled needs to be updated
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
