from dash import html
import dash

dash.register_page(__name__, title='Cyber-Radar')

layout = dash.html.Div(
    style= {"text-align": "center"},
    children= [
        html.H1("Welcome to our Cyber-Radar !"),
        html.H3("If you want to have a look at current threats go to the Dashboard page. If you want to see news about the current CVEs go to the News page")
    ]
)
