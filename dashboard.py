import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
from collections import Counter
from Tweety import TwitterCVE

# data = pd.read_csv("./avocado.csv")
# data = data.query("type == 'conventional' and region == 'Albany'")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)

NewTwitter = TwitterCVE()
retrieveLast100 = NewTwitter.get_tweets("#cve -from:RedPacketSec", 100)
last100Tweets = NewTwitter.get_cve_in_tweets(retrieveLast100)

print(type(Counter(last100Tweets)))

data = {'Name': ['John', 'Amy', 'Peter', 'Jane'],
        'Age': [23, 45, 31, 28],
        'City': ['New York', 'London', 'Paris', 'Sydney']}
df = pd.DataFrame(data)

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
            html.Iframe(
                src="http://www.cvedetails.com/widget.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=1&opov=1&opcsrf=1&opfileinc=1&opgpriv=1&opsqli=1&opxss=1&opdirt=1&opmemc=1&ophttprs=1&opbyp=1&opginf=1&opdos=1&orderby=3&cvssscoremin=0",
                width="100%",
                height="300px")
        )
        ,
        html.Div(
            style={'display': 'flex', 'flex-wrap': 'wrap'},
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="numbers-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    'y': list(Counter(last100Tweets).values()),
                                    'x': list(Counter(last100Tweets).keys()),
                                    'type': 'bar'
                                },
                            ],
                            'layout': {
                                'title': {
                                    'text': 'Currently open CVEs (not real data)',
                                    'x': 0.1,
                                    'xanchor': 'down'
                                },
                                'colorway': ['#E12D39']
                            }
                        },
                    ),
                    className="card",
                    style={'flex': '1'}
                ),
                html.Div(
                    children=dcc.Graph(
                        id="numbers-chart_2test",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    'labels': 10,
                                    'values': 10,
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
                    style={'flex': '1'}
                ),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                     style_cell={'className': 'card'} #styling not working so far
                )
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
