"""MISSING!!!"""
from collections import Counter

#import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc, html, callback, Output, Input, State
import cve_ds
from Tweety import TwitterCVE
from Reddit import RedditCVE
import Historic
import threading
import os

dash.register_page(__name__, path='/')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
#Globals
reddit_cve = []
reddit_cve_counter = []
#TWITTER DATA
try:
    NewTwitter = TwitterCVE()
    last100Tweets = NewTwitter.get_cve_in_tweets(NewTwitter.get_tweets("#cve -from:RedPacketSec", 50))
    unfilterd_cve = list(Counter(last100Tweets).keys())
    unfilterd_cve_counter = list(Counter(last100Tweets).values())
except:
    unfilterd_cve = []
    unfilterd_cve_counter = []
    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'Twitter_data.txt')
        with open(file_name, "r") as twitter_file:
            unfilterd_cve = (twitter_file.readline().split(", "))
            unfilterd_cve_counter = (twitter_file.readline().split(","))
    except:
        print("Error cannot read File or File empty in Twitter_data.txt")

#REDDIT DATA
def reddit_data():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, 'Reddit_data.txt')
    NewReddit = RedditCVE()
    lastRedditPosts = NewReddit.retrieve_reddit_cve_list()
    with open (file_name, "w+") as reddit_file:
        try:
            reddit_file.write(str(list(Counter(lastRedditPosts).keys())))
            reddit_file.write("\n")
            reddit_file.write(str(list(Counter(lastRedditPosts).values())))
        except Exception as e:
            print(e)
            print("Error Cannot Read File or File empty (Reddit)")

        
#Reddit thread Daemon
thread_reddit_fetch = threading.Thread(target=reddit_data())
#thread_reddit_fetch.daemon = True
thread_reddit_fetch.start()

filtered_score = []
filtered_severity = []
labels = ['MEDIUM', 'HIGH', 'N/A', 'CRITICAL']
values = [0, 0, 0, 0]
severity_map = {'MEDIUM': 0, 'HIGH': 1, 'N/A': 2, 'CRITICAL': 3}

counter = len(unfilterd_cve)

for x in unfilterd_cve:
    print(counter)
    counter-=1
    if counter == 3:
        break
    cve_info = cve_ds.get_cve_info(x)
    score = cve_info[0]
    severity = cve_info[1]
    values[severity_map.get(severity, 2)] += 1

def aktuelle_sicherheitslage():
    """Wertet aktuelle Sicheheitslage aus"""
    meiste_werte = max(values)
    return labels[values.index(meiste_werte)]

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
                                    'text': 'Currently Trending CVEs on Twitter',
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
                 html.Div(
                    className="card",
                    style= {'marginRight': '10px', 'flex': '1'},
                    children=[
                        html.Center(
                            children=[
                                html.H2("Aktuelle Sicherheitslage"),
                                html.P(aktuelle_sicherheitslage())
                            ]
                        )
                    ],

                    
                ),
            ],
            className="wrapper",
        ),
        #REDDIT CVE
        html.Div(
            style={'width': '100%', 'margin': '0, 10, 0, 10'},
            id='reddit_page',
            className="card",
            children=[
                html.Div(
                    className="card",
                    id="reddit_card",
                    style= {"marginLeft": "20px", "marginRight": "20px", 'flex': '1'},
                    children=[],
                ),
                    dcc.Interval(id='reddit_timer', interval=60*1000, n_intervals=0),
            ]
        ),
        #HISTORIC CVE DATA
        html.Div(
            style={'width': '100%', 'margin': '0, 10, 0, 10'},
            id='cve_history',
            className="card",
            children=dcc.Graph(
                style={"marginLeft": "20px", "marginRight": "20px", 'flex': '1'},
                id="numbers-chart",
                config={"displayModeBar": False},
                figure={
                    "data": [
                        {
                            'y': Historic.data_array(),
                            'x': Historic.dates_array(),
                            'type': 'bar'
                        },
                    ],
                    'layout': {
                        'title': {
                            'text': 'Historic CVE Data',
                            'x': 0.1,
                            'xanchor': 'down'
                        },
                        'colorway': ['#0da784']
                    }
                },
            ),
        )
    ]
)

@callback(
    Output(component_id="reddit_card", component_property="children"),
    Input(component_id="reddit_timer", component_property="n_intervals"),
    State(component_id="reddit_page", component_property="children")
)
def update_reddit_data(timer, div_children):
    reddit_cve = []
    reddit_cve_counter = []
    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'Reddit_data.txt')
        with open(file_name, "r") as reddit_file:
                reddit_cve = reddit_file.readline()
                reddit_cve_counter = reddit_file.readline()
    except:
        print("Error cannot read File or File empty in update_reddit_data")
    div_child = dcc.Graph(
                        id="numbers-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    'y': reddit_cve_counter.split(),
                                    'x': reddit_cve.split(),
                                    'type': 'bar'
                                },
                            ],
                            'layout': {
                                'title': {
                                    'text': 'CVEs on Reddit',
                                    'x': 0.1,
                                    'xanchor': 'down'
                                },
                                'colorway': ['#E12D39']
                            }
                        },
                    )
    return div_child