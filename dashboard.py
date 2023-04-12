'''File for creating the webpage of the Cyberradar'''
import dash
from dash import dcc
from dash import html
#import pandas as pd
from Tweety import TwitterCVE

# data = pd.read_csv("./avocado.csv")
# data = data.query("type == 'conventional' and region == 'Albany'")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)
NewTwitter = TwitterCVE()
retrieveLast100 = NewTwitter.get_tweets("#CVE", 100)
last100Tweets = NewTwitter.get_cve_in_tweets(retrieveLast100)
last100TweetsAmount = NewTwitter.sort_tweets_by_cve_frequency(last100Tweets)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__)
app.title = "Cyber-Dashboard"

app.layout = html.Div(
    children=[
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
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="numbers-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    'labels': last100Tweets,
                                    'values': last100TweetsAmount,
                                    'type': 'pie'
                                },
                            ],
                            'layout': {
                                'title': {
                                    'text': 'Currently open CVEs (not real data)',
                                    'x': 0.05,
                                    'xanchor': 'left'
                                },
                                'colorway': ['#E12D39']
                            }
                        },
                    ),
                    className="card",
                ),
                # html.Div(
                #     children=dcc.Graph(
                #         id="price-chart",
                #         config={"displayModeBar": False},
                #         figure={
                #             "data": [
                #                 {
                #                     "x": data["Date"],
                #                     "y": data["AveragePrice"],
                #                     "type": "lines",
                #                     "hovertemplate": "$%{y:.2f}"
                #                                      "<extra></extra>",
                #                 },
                #             ],
                #             "layout": {
                #                 "title": {
                #                     "text": "Average Price of Avocados",
                #                     "x": 0.05,
                #                     "xanchor": "left",
                #                 },
                #                 "xaxis": {"fixedrange": True},
                #                 "yaxis": {
                #                     "tickprefix": "$",
                #                     "fixedrange": True,
                #                 },
                #                 "colorway": ["#17B897"],
                #             },
                #         },
                #     ),
                #     className="card",
                # ),
                # html.Div(
                #     children=dcc.Graph(
                #         id="volume-chart",
                #         config={"displayModeBar": False},
                #         figure={
                #             "data": [
                #                 {
                #                     "x": data["Date"],
                #                     "y": data["Total Volume"],
                #                     "type": "lines",
                #                 },
                #             ],
                #             "layout": {
                #                 "title": {
                #                     "text": "Avocados Sold",
                #                     "x": 0.05,
                #                     "xanchor": "left",
                #                 },
                #                 "xaxis": {"fixedrange": True},
                #                 "yaxis": {"fixedrange": True},
                #                 "colorway": ["#E12D39"],
                #             },
                #         },
                #     ),
                #     className="card",
                # ),
            ],
            className="wrapper",
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)