from dash import html

def GetStyleAndLegendColumn(styledatatable_in, legendgraph_in):
    
    styletable_div = html.Div(styledatatable_in,
                        className="TABLE_DIV NOPADDING")
    
    legendgraph_div = html.Div(legendgraph_in,
                        className="TABLE_DIV NOPADDING")

    style_col =  html.Div(children=[styletable_div],
                          className="col col-lg-12 TABLE_DIV NOPADDING")
    legend_col =  html.Div(children=[legendgraph_div],
                           className="col col-lg-12 TABLE_DIV NOPADDING")

    stylerow = html.Div([style_col],
                    className="row STYLE_ROW NOPADDING")
    legendrow = html.Div([legend_col,],
                    className="row LEGEND_ROW NOPADDING")

    styleandlegendcolumn_out = html.Div(
                [stylerow, legendrow],
                #[row1],
                #className="HALF_CONTENT_COLUMN",
                className="col col-lg-6 PAGE_GRAPH_COLUMN_CONTENT_RIGHT",
                #style={**CONTENT_ROW,**NOPADDING}
            )
    return  styleandlegendcolumn_out
