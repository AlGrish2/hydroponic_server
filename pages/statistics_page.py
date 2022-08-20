import dash
import dash_bootstrap_components as dbc
from dash import html


dash.register_page(__name__, path='/statistics')

def create_statistics_page():

    page = dbc.Container(
        [
            dash.dcc.Graph(id='graph'),
        ]
    )
    return page


layout = create_statistics_page()
