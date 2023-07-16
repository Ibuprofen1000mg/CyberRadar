"""
File for the generation of the news CVE datasheet\n
__Author__: Nic Holzapfel\n
"""
import dash
from dash import html, dcc, callback, Output, Input, State, dash_table
from datetime import datetime
from collections import defaultdict
import requests
import pandas as pd
import json

dash.register_page(__name__)
layout = html.Div(
    id='news_page',
    children=[
    dcc.Interval(id='timer', interval=10*60*1000, n_intervals=0)
])


@callback(
    Output(component_id="news_page", component_property="children"),
    Input(component_id="timer", component_property="n_intervals"),
    State(component_id="news_page", component_property="children")
)
def update_cve_details(timer, div_children):
    """Fetches newest CVE numbers from cvedetails

    Args:
        timer (_type_): Timer Interval for updating the Website
        div_children (_type_): Dash-Datatype from which child the Table will be appended to

    Returns:
        _type_: Dash Datatype returns (children datatype) containing the newest cve table
    """
    res = requests.get("http://www.cvedetails.com/json-feed.php?numrows=30&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=0&opov=0&opcsrf=0&opfileinc=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opginf=0&opdos=0&orderby=3&cvssscoremin=0")
    df = json.loads(res.content)
    dd = defaultdict(list)
    for d in (df): 
        for key, value in d.items():
            dd[key].append(value)
    temp_dict = dict(dd)
    temp_dataframe = pd.DataFrame.from_dict(temp_dict)
    div_child = dash_table.DataTable(
            temp_dataframe.to_dict('records'),
            id="table",
            style_cell={'minWidth': 95, 'maxWidth': 500, 'width': 'auto', 'textAlign': 'center'},
            style_data={'whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
            style_table={'overflowX': 'auto'}
        ),

    return div_child    