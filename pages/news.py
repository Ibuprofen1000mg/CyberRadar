'''MISSING!!!'''
import dash
<<<<<<< Updated upstream
from dash import html
=======
from dash import html, dcc, callback, Output, Input, State
from datetime import datetime
import requests
import json
>>>>>>> Stashed changes

dash.register_page(__name__)
#app.dash.register_page(__name__)

layout = html.Div(
    id='news_page',children=[
    html.Div(
<<<<<<< Updated upstream
        html.Iframe(
            #Important to remember min. CVE Score von 1 in der Website momentan
            src="https://www.cvedetails.com/widget.php?numrows=30&vendor_id=0&product_id=0&version_id=0& \
                hasexp=0&opec=1&opov=1&opcsrf=1&opfileinc=1&opgpriv=1&opsqli=1&opxss=1&opdirt=1&opmemc=1& \
                ophttprs=1&opbyp=1&opginf=1&opdos=1&orderby=1&cvssscoremin=1",
            width="100%",
            height="1000px")
    ),
])
=======
        id='last_cve',
        style={
            'textAlign': 'center'
        },
        children=[]
    ),
    # html.Div(
    #     html.Embed(
    #         id="cve-details",
    #         #Important to remember min. CVE Score von 1 in der Website momentan
    #         src="https://timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterdam",
    #         width="100%",
    #         height="1000px")
    # ),
    dcc.Interval(id='timer', interval=1*10000, n_intervals=0)
])


@callback(
    Output(component_id="last_cve", component_property="children"),
    Input(component_id="timer", component_property="n_intervals"),
)
def update_cve_details(timer):
    res = requests.get("http://www.cvedetails.com/json-feed.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=0&opov=0&opcsrf=0&opfileinc=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opginf=0&opdos=0&orderby=3&cvssscoremin=0")
    x = json.loads(res.content)
    return [(html.H4(x[i]['cve_id'] for i in range(10)))]
        #return f'http://www.cvedetails.com/widget.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=0&opov=0&opcsrf=0&opfileinc=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opginf=0&opdos=0&orderby=3&cvssscoremin=0'
>>>>>>> Stashed changes
