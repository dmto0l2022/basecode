from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True, serve_locally = False, requests_pathname_prefix='/app/multipage/')

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
