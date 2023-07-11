def create_layout():
    layout02 = html.Div([
    html.H3(‘App 1’),
    dcc.Dropdown(
        id=‘app-1-dropdown’,
        options=[
        {‘label’: ‘App 1 - {}’.format(i), ‘value’: i} for i in [
        ‘NYC’, ‘MTL’, ‘LA’
        ]
        ],
        value=session[‘app-1-display-val-session’]
        ),
    html.Div(id=‘app-1-display-value’)
    ])
    return layout02
