######################################################################
__author__ = "Benjamin G., Nic H., Jesse K."
__credits__ = ["Benjamin G., Nic H., Jesse K."]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Benjamin G., Nic H., Jesse K."
__status__ = "Release/Production"
######################################################################

from dash import Dash, html, dcc
import dash
#from dash.dependencies import Output, Input

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=False,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
    ]
)

app.title = 'Cyber-Radar'

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
                        f"{dash.page_registry['pages.dashboard']['name']}", href=dash.page_registry['pages.dashboard']["relative_path"],
                        style={'display': 'inline-block', 'width': '50%', 'text-align': 'center'},
                    ),
                    dcc.Link(
                        f"{dash.page_registry['pages.news']['name']}", href=dash.page_registry['pages.news']["relative_path"],
                        style={'display': 'inline-block', 'width': '50%', 'text-align': 'center'},
                    )
                    
                ]
            )
        ]
    ),
    # dash.html.Div(
    #     style= {"text-align": "center"},
    #     children= [
    #         html.H1("Welcome to our Cyber-Radar"),
    #         html.H2("If you want to have a look at current threats go to the Dashboard page. If you want to see news about the current CVEs go to the News page")
    #     ]
    # ),
	dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=False)
    #debug auf False damit es nur noch einmal lädt/hälfte der Zeit braucht zum bauen.
