from dash import Dash, html, dcc
import dash
#from dash.dependencies import Output, Input

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=False,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
    ]
)

# author: Jesse Kuhn
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
                style={'flex-wrap': 'wrap'},
                children=[
                    dcc.Link(
                        f"{page['name']}", href=page["relative_path"],
                        style={'display': 'inline-block', 'width': '50%', 'text-align': 'center'},
                    )
                    for page in dash.page_registry.values()
                ]
            )
        ]
    ),
	dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=False)
    #debug auf False damit es nur noch einmal lädt/hälfte der Zeit braucht zum bauen.
