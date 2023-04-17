from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.Div(
            children=[
                html.P(children="📡", className="header-emoji"),
                html.H1(
                    children="Cyber-Radar", className="header-title"
                ),
                html.P(
                    children="This dashboard displayes information about CVEs aggregated from social media",
                    className="header-description",
                ),
            ],
            className="header",
        ),

    html.Div(
        [
            html.Div(
                style={'flex-wrap': 'wrap', },
                children=[
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                    for page in dash.page_registry.values()
                ]
            )
            
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)