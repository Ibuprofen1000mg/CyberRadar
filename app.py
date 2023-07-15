"""Main file to host the website\n
######################################################################\n
__author__ = "Benjamin G., Nic H., Jesse K."\n
__license__ = "GPL"\n
__version__ = "1.0.0"\n
__maintainer__ = "Benjamin G., Nic H., Jesse K."\n
__status__ = "Release/Production"\n
######################################################################\n
"""
from dash import Dash, html, dcc
import dash
#from dash.dependencies import Output, Input

""" Configuration for the page
__author__ = "Jesse Kuhn"
Returns:
    _type_: _description_
"""
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=False,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
    ]
)
app.title = 'Cyber-Radar'

""" The blueprint of the banner and the menu that is displayed on all pages
__author__ = "Jesse Kuhn"
Returns:
    _type_: _description_
"""
app.layout = html.Div([
	html.Div(
        children=[
            html.P(children="📡", className="header-emoji"),
            html.H1(
                children="Cyber-Radar", className="header-title"
            ),
            html.P(
                children="This dashboard displays information about CVEs aggregated from social media",
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
                        f"{dash.page_registry['pages.dashboard']['name']}",
                        href=dash.page_registry['pages.dashboard']["relative_path"],
                        style={'display': 'inline-block', 'width': '50%', 'text-align': 'center'},
                    ),
                    dcc.Link(
                        f"{dash.page_registry['pages.news']['name']}",
                        href=dash.page_registry['pages.news']["relative_path"],
                        style={'display': 'inline-block', 'width': '50%', 'text-align': 'center'},
                    )
                ]
            )
        ]
    ),
	dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=False)
