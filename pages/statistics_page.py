import dash
import dash_bootstrap_components as dbc
from dash import html


dash.register_page(__name__, path='/statistics')

def create_statistics_page():

    page = dbc.Container(
        [
            dash.dcc.Graph(id='mean_size_graph'),
            dash.dcc.Graph(id='defect_graph'),
            dash.dcc.Graph(id='light_graph'),
            dash.dcc.Graph(id='temp_graph'),
            dash.dcc.Graph(id='min_wl_graph'),
            dash.dcc.Graph(id='max_wl_graph'),
            dash.dcc.Graph(id='hum_graph'),
            dash.dcc.Graph(id='pres_graph'),
            dash.dcc.Graph(id='ph_graph'),
            dash.dcc.Graph(id='ec_graph'),
            dash.dcc.Graph(id='tds_graph'),
        ]
    )
    return page


layout = create_statistics_page()
