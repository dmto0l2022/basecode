from dash import Dash, html, dcc
import dash

#app = Dash(__name__, use_pages=True,requests_pathname_prefix='/app/multipage/')
app = Dash(__name__, use_pages=True,requests_pathname_prefix='/')

server = app.server

app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

## locally
if __name__ == '__main__':
    app.run_server(debug=False)
