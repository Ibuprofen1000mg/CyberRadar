"""MISSING!!!"""
from collections import Counter

#import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
import cve_ds
from Tweety import TwitterCVE

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

NewTwitter = TwitterCVE()#
last100Tweets = NewTwitter.get_cve_in_tweets(NewTwitter.get_tweets("#cve -from:RedPacketSec", 100))

unfilterd_cve = list(Counter(last100Tweets).keys())
unfilterd_cve_counter = list(Counter(last100Tweets).values())

filtered_score = []
filtered_severity = []
labels = ['MEDIUM', 'HIGH', 'N/A', 'CRITICAL']
values = [0, 0, 0, 0]
severity_map = {'MEDIUM': 0, 'HIGH': 1, 'N/A': 2, 'CRITICAL': 3}

for x in unfilterd_cve:
    cve_info = cve_ds.get_cve_info2(x)
    score = cve_info[0]
    severity = cve_info[1]
    values[severity_map.get(severity, 2)] += 1

# for x in unfilterd_cve:
#     cve_info = cve_ds.get_cve_info2(x)
#     try:
#         filtered_score.append(cve_info[1]['cvssV3_score'])
#         filtered_severity.append(cve_info[1]['severity'])
#         if cve_info[1]['severity']=='MEDIUM':
#             values[0] += 1
#         elif cve_info[1]['severity']=='HIGH':
#             values[1] += 1
#         elif cve_info[1]['severity']=='N/A':
#             values[2] += 1
#         elif cve_info[1]['severity']=='CRITICAL':
#             values[3] += 1
#         #print(x) --> Prints CVEs
#     except KeyError:
#         continue

fig = go.Figure(data=[go.Pie(labels=labels, values=values)], layout={
    'title': 'Severity Distribution'
})

dash.register_page(__name__)

layout = html.Div(
    children=[
        html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap',},
            children=[
                html.Div(
                    className="card",
                    style= {'marginRight': '10px', 'flex': '1'},
                    children=dcc.Graph(
                        id="numbers-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    'y': unfilterd_cve_counter,
                                    'x': unfilterd_cve,
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
                ),
                html.Div(
                    className="card",
                    style= {'marginRight': '10px', 'flex': '1'},
                    children=
                    dcc.Graph(
                        id='pie-chart',
                        figure=fig
                    ),
                ),
            ],
            className="wrapper",
        )
    ]
)
