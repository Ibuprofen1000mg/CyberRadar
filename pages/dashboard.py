"""File for the implementation of the dashboard --> Frontend and data processing
__author__: Nic Holzapfel, Benjamin Götz, Jesse Kuhn
"""
from collections import Counter
# import threading --> for further development
import os
import pandas as pd
import plotly.graph_objs as go
import dash
import cve_ds
import Tweety
import Reddit
import Historic
import rating
import RSS
import WebCrawl

# Author: Jesse Kuhn
""" Registrating the page in the registry of the app; The page can be called and routing is enabled

Returns:
    _type_: _description_
"""
dash.register_page(__name__, path='/')

# Author: Jesse Kuhn
""" integrating a special style for css usage

Returns:
    _type_: _description_
"""
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

### GLOBALS ###
# Reddit
reddit_cve = []
reddit_cve_counter = []

# General CVE variables
filtered_score = []
filtered_severity = []
cve_descriptions = []
personal_rating = []
cve_rss_feed = RSS.parse_websites()
cve_web_feed = WebCrawl.parse_websites()
labels = ['MEDIUM', 'HIGH', 'N/A', 'CRITICAL']
values = [0, 0, 0, 0]
severity_map = {'MEDIUM': 0, 'HIGH': 1, 'N/A': 2, 'CRITICAL': 3}

# Current Security-Level
SUM_SCORE = 0
SUM_PERSONAL_SCORE = 0
RELEVANT_CVE = 0

# Author: Nic Holzapfel
#TWITTER DATA
try:
    last100Tweets = Tweety.get_cve_in_tweets(Tweety.get_tweets("#cve -from:RedPacketSec", 50))
    unfiltered_cve = list(Counter(last100Tweets).keys())
    unfiltered_cve_counter = list(Counter(last100Tweets).values())
except:
    unfiltered_cve = []
    unfiltered_cve_counter = []
    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'Textfiles\Twitter_data.txt')
        with open(file_name, "r", encoding="utf-8") as twitter_file:
            unfiltered_cve = (twitter_file.readline().split(", "))
            unfiltered_cve_counter = (twitter_file.readline().split(","))
    except:
        print("Error cannot read File or File empty in Twitter_data.txt")

# REDDIT DATA
def reddit_data():
    """Renders the Reddit data from the API. This part saves the reddit data into a textfile for faster loading of the Dashboard
    """
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, 'Textfiles\Reddit_data.txt')
    last_reddit_posts = Reddit.retrieve_reddit_cve_list()
    with open (file_name, "w+", encoding="utf-8") as reddit_file:
        try:
            reddit_file.write(str(list(Counter(last_reddit_posts).keys())))
            reddit_file.write("\n")
            reddit_file.write(str(list(Counter(last_reddit_posts).values())))
        except Exception as exc:
            print(exc)
            print("Error Cannot Read File or File empty (Reddit)")

#Reddit thread Daemon
# try:
#     print("No Exception")
#     #thread_reddit_fetch = threading.Thread(target=reddit_data())
#     #thread_reddit_fetch.daemon = True
#     #thread_reddit_fetch.start()
# except:
#     print("Reddit API Error!")

# Author: Nic Holzapfel, Benjamin Götz, Jesse Kuhn
""" Pulling data from the CVE database and configuring variables that can be used for the diagrams
"""
counter = len(unfiltered_cve)
for x in unfiltered_cve:
    print(counter)
    counter-=1
    cve_info = cve_ds.get_cve_info(x)
    score = cve_info[0]
    personal_score = rating.rate(cve_info, counter)
    personal_rating.append(personal_score)
    if score > 0:
        SUM_SCORE += score
        RELEVANT_CVE += 1
        SUM_PERSONAL_SCORE += personal_score
    filtered_score.append(cve_info[0])
    severity = cve_info[1]
    filtered_severity.append(cve_info[1])
    cve_descriptions.append(cve_info[2])
    values[severity_map.get(severity, 2)] += 1

def aktuelle_sicherheitslage(sum:float) -> str:
    """Calculates current security levels

    Args:
        sum (float): input of CVSS score from a CVE

    Returns:
        sec_lvl(str): Returns the current security level string
    """
    value = sum / RELEVANT_CVE
    sec_lvl = "LOW"

    if value < 2:
        sec_lvl = "LOW"
    elif value < 4:
        sec_lvl = "GUARDED"
    elif value < 6:
        sec_lvl = "ELEVATED"
    elif value < 8:
        sec_lvl = "HIGH"
    else:
        sec_lvl = "SEVERE"

    return sec_lvl

# Author: Benjamin Götz
"""
DATAFRAME
"""
df = pd.DataFrame({'CVE': [x for x in unfiltered_cve],
            'Score': [x for x in filtered_score],
            'Personal Rating': [x for x in personal_rating],
            'Severity': [x for x in filtered_severity],
            'Description': [x for x in cve_descriptions]},
            index=[*range(0, len(unfiltered_cve), 1)])

# Author: Jesse Kuhn
""" 
Configurations for the pie chart about severity distribution
"""
fig = go.Figure(data=[go.Pie(labels=labels, values=values)], layout={
    'title': 'Severity Distribution'
})

# Author: Jesse Kuhn
""" 
The blueprint of the webpage, coded with python dash which enables html and css properties
"""
layout = dash.html.Div(
    children=[
        dash.html.Div(
            style={'display': 'flex', 'flexWrap': 'wrap', 'marginLeft': '20px',
                   'marginRight': '20px', 'max-width': '100%', 'padding': '0px'},
            children=[
                dash.html.Div(
                    className="card",
                    style= {'marginRight': '10px', 'flex': '1'},
                    children=dash.dcc.Graph(
                        id="numbers-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    'y': unfiltered_cve_counter,
                                    'x': unfiltered_cve,
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
                dash.html.Div(
                    className="card",
                    style= {'marginRight': '10px', 'flex': '1'},
                    children=
                    dash.dcc.Graph(
                        id='pie-chart',
                        figure=fig
                    ),
                ),
                dash.html.Div(
                    className="card",
                    style= {'flex': '1', 'display': 'flex',
                        'flex-direction': 'column', 'justify-content': 'center'},
                    children=[
                        dash.html.Center(
                            style={'height': '50%', 'align-items': 'center'},
                            children= [
                                dash.html.H2("General Securitylevel",
                                    style={'text-decoration': 'underline', 'height': '25%'}),
                                dash.html.P(
                                    aktuelle_sicherheitslage(SUM_SCORE),
                                    style={"color": "red", 'height': '25%'}
                                ),
                            ],
                        ),
                        dash.html.Center(
                            style={'height': '50%', 'align-items': 'center'},
                            children= [
                                    dash.html.H2("Personal Securitylevel",
                                        style={'text-decoration': 'underline', 'height': '25%'}),
                                    dash.html.P(
                                        aktuelle_sicherheitslage(SUM_PERSONAL_SCORE),
                                        style={"color": "red", 'height': '25%'}
                                    )
                            ]
                        )
                    ],
                ),
            ],
            className="wrapper",
        ),
        #REDDIT CVE
        #Author: Nic Holzapfel
        dash.html.Div(
            style={'width': '100%', 'margin': '0, 10, 0, 10'},
            id='reddit_page',
            children=[
                dash.html.Div(
                    className="card",
                    id="reddit_card",
                    style= {"marginLeft": "20px", "marginRight": "20px", 'flex': '1'},
                    children=[],
                ),
                    dash.dcc.Interval(id='reddit_timer', interval=60*1000, n_intervals=0),
            ]
        ),
        #RSS CVE
        #Author: Nic Holzapfel, Benjamin Götz
        dash.html.Div(
                style={'width': '100%', 'margin': '0, 10, 0, 10'},
                id='cve_rss',
                children=dash.dcc.Graph(
                    style={"marginLeft": "20px", "marginRight": "20px", 'flex': '1'},
                    className="card",
                    id="numbers-chart",
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                'y': list(Counter(cve_rss_feed).values()),
                                'x':  list(Counter(cve_rss_feed).keys()),
                                'type': 'bar'
                            },
                        ],
                        'layout': {
                            'title': {
                                'text': 'RSS CVE Data',
                                'x': 0.1,
                                'xanchor': 'down'
                            },
                            'colorway': ['#0CD33F']
                        }
                    },
                ),
        ),
        #WebsiteCrawl CVE
        #Author: Nic Holzapfel, Benjamin Götz
        dash.html.Div(
                style={'width': '100%', 'margin': '0, 10, 0, 10'},
                id='cve_website',
                children=dash.dcc.Graph(
                    style={"marginLeft": "20px", "marginRight": "20px", 'flex': '1'},
                    className="card",
                    id="numbers-chart",
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                'y': list(Counter(cve_web_feed).values()),
                                'x':  list(Counter(cve_web_feed).keys()),
                                'type': 'bar'
                            },
                        ],
                        'layout': {
                            'title': {
                                'text': 'WebsiteCrawl CVE Data',
                                'x': 0.1,
                                'xanchor': 'down'
                            },
                            'colorway': ['#DAF400']
                        }
                    },
                ),
        ),
        #HISTORIC CVE DATA
        #Author: Nic Holzapfel
        dash.html.Div(
            style={'width': '100%', 'margin': '0, 10, 0, 10'},
            id='cve_history',
            children=dash.dcc.Graph(
                style={"marginLeft": "20px", "marginRight": "20px", 'flex': '1'},
                className="card",
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
        ),
        #DATA TABLE
        # Author: Benjamin Götz
        dash.html.Div(
             style={'marginLeft': '20px', 'marginRight': '20px',},
            className="card",
            id='data_table',
            children=dash.dash_table.DataTable(
                style_table= {'width': '100%', 'margin': '0, 10, 0, 10',  'flex': '1',
                              'overflow-x': 'auto'},
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_cell={'textAlign': 'left', 'padding': '4px'}
            ),
        )
    ]
)

#Author: Nic Holapfel
@dash.callback(
    dash.Output(component_id="reddit_card", component_property="children"),
    dash.Input(component_id="reddit_timer", component_property="n_intervals"),
    dash.State(component_id="reddit_page", component_property="children")
)
def update_reddit_data(timer, div_children):
    """Updates Reddit Data as Thread Daemon

    Args:
        timer: Set timer interval to update the data from reddit
        div_children: input where to append a div-child to

    Returns:
        _type_: returns a full html div component with reddit data as a graph
    """
    reddit_cve = []
    reddit_cve_counter = []
    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'Textfiles\Reddit_data.txt')
        with open(file_name, "r") as reddit_file:
            reddit_cve = reddit_file.readline().replace("[","").replace("]","")
            reddit_cve_counter = reddit_file.readline().replace("[","").replace("]","")
    except:
        print("Error cannot read File or File empty in update_reddit_data")
    div_child = dash.dcc.Graph(
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
