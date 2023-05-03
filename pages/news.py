'''MISSING!!!'''
import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        html.Iframe(
            #Important to remember min. CVE Score von 1 in der Website momentan
            src="https://www.cvedetails.com/widget.php?numrows=30&vendor_id=0&product_id=0&version_id=0& \
                hasexp=0&opec=1&opov=1&opcsrf=1&opfileinc=1&opgpriv=1&opsqli=1&opxss=1&opdirt=1&opmemc=1& \
                ophttprs=1&opbyp=1&opginf=1&opdos=1&orderby=1&cvssscoremin=1",
            width="100%",
            height="1000px")
    ),
])
