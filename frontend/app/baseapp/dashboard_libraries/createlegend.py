from plotly.subplots import make_subplots
import plotly.graph_objects as go

def CreateLegendFig(limits_in, limits_traces_df_in):
    
    #limit_id = [1]
    
    legend_plotseries = limits_traces_df_in[limits_traces_df_in['limit_id'].isin(limits_in)].copy()
    
    ##plotseries_default = CreatePlotSeries(limit_id)
    
    rows_list = list(range(1,6))
    cols_list = list(range(1,6))
    
    table_rows=12
    table_cols=5
    
    fig_legend_out = make_subplots(
    column_titles = ['limit_id','trace_id','trace_name','line', 'symbol'],
    rows=table_rows,
    cols=table_cols,
    horizontal_spacing = 0.00,
    vertical_spacing = 0.00,
    #subplot_titles=(titles)
    column_widths=[0.1,0.1,0.6,0.1, 0.1],)
    
    
    #fig_legend_out.update_xaxes(matches=None, showticklabels=True)
    #fig_legend_out.update_yaxes(matches=None, showticklabels=True)
    
    #fig_legend_out.update_layout(xaxis_range=[1,2])

    
    fig_legend_out.update_layout(
    #    autosize=False,
    #    width=800,
    #    height=200,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=20,
            pad=0
        ),
        paper_bgcolor="LightSteelBlue",
    )
    
    rowloop = 0

    for index, row in legend_plotseries.iterrows():
        #print(row['c1'], row['c2'])
        rowloop +=1
        for c in cols_list: #enumerate here to get access to i
            # STEP 2, notice position of arguments!
            table_column_names = ['limit_id','trace_id','trace_name','line','symbol']
            scatter_mode_list = ['text-number','text-number','text-text','lines','markers']
            current_column = table_column_names[c-1]
            current_mode = scatter_mode_list[c-1]
            if current_mode =='lines':
                fig_legend_out.add_trace(go.Scatter(x=[1,2],
                                         y=[1,1],
                                         mode=current_mode,
                                         #text=row[current_column],
                                         line=dict(width=4,dash=row['line'],color=row['line_color']),
                                        ),
                              row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                              col=c)
            if current_mode =='text-text':
                fig_legend_out.add_trace(go.Scatter(x=[1,2], 
                                         textposition='middle right',
                                         y=[1,1],
                                         mode='text',
                                         text=[row[current_column],'']
                                        ),
                              row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                              col=c)
            
            if current_mode =='text-number':
                fig_legend_out.add_trace(go.Scatter(x=[1], 
                                         textposition='middle right',
                                         y=[1],
                                         mode='text',
                                         text=row[current_column]
                                        ),
                              row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                              col=c)
            if current_mode =='markers':
                fig_legend_out.add_trace(go.Scatter(x=[1], 
                                        y=[1],
                                        mode=current_mode,
                                        #text=row[current_column],
                                        marker_symbol=row['symbol'],
                                        marker=dict(
                                        size=10,
                                        color=row['symbol_color'],#set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=False,
                                        )
                                        ),
                              row=rowloop, #index for the subplot, i+1 because plotly starts with 1
                              col=c)
                
            fig_legend_out.update_xaxes(showgrid=False)
            fig_legend_out.update_yaxes(showgrid=False)
            #legend
            fig_legend_out.update_layout(showlegend=False)
            #x axis
            fig_legend_out.update_xaxes(visible=False)
            #y axis    
            fig_legend_out.update_yaxes(visible=False)

    return fig_legend_out
