heighttesting = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.P("This is column 1"),
                    width=8,
                    style={"height": "100%","background-color": "red","padding":"0px", "margin":"0px"},
                ),
                dbc.Col(
                    html.P("This is column 2"),
                    width=4,
                    style={"height": "100%","background-color": "green","padding":"0px", "margin":"0px"},
                ),
            ],
            #className="h-25",
            style={"height": "50%"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.P("This is column 3"),
                    width=8,
                    style={"height": "100%","background-color": "blue", "padding":"0px", "margin":"0px"},
                ),
                dbc.Col(
                    html.P("This is column 4"),
                    width=4,
                    style={"height": "100%","background-color": "cyan","padding":"0px", "margin":"0px"},
                ),
            ],
            #className="h-25",
            style={"height": "50%"},
        ),
    ],
    style={"height": "50px"},
)

rightrow1 =          html.Div(
            [
                html.Div(
            [
                html.H3(children='Panel 1'),
                ##form,
            ],
            className="short-div", style={"height":"35vh","background-color":"green"}
        ), 
                 html.Div(
            [
                html.H3(children='Panel 2'),
            ],
            className="short-div", style={"height":"35vh","background-color":"yellow"}
        ), 
            ],
            className="col", style={"width": "30vw","padding":"0px",}
        )

rightrow2 = html.Div(
            [
                html.Div(
            [
                html.H3(children='Panel 3'),
            ],
            className="short-div", style={"height":"35vh","background-color":"red"}
        ), 
                 html.Div(
            [
                html.H3(children='Panel 4'),
            ],
            className="short-div", style={"height":"35vh","background-color":"blue"}
        ), 
            ],
            className="col", style={"width": "30vw", "padding":"0px"}
        )
