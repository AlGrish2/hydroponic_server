from datetime import datetime

import dash
import dash_player
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/')


def create_main_page():

    options = []
    controls = [
        dbc.Select(
            id="scene",
            options=options,
            value={"label": datetime(year=1970, month=1, day=1).strftime("%Y/%m/%d, %H:%M:%S"), "value": 0}
        ),
    ]

    video = dbc.Card(
        [
            dbc.CardBody(
                dash_player.DashPlayer(
                    id="video", width="auto", height="768px", controls=True
                ), className = 'align-self-center'
            )
        ]
    )

    page = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            video,
                            html.Br(),
                            dbc.Card(dbc.Row([dbc.Col(c) for c in controls]), body=True),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.Col([
                                    html.H2("Video statistics", className="display-6"),
                                    html.Div(
                                        id='desc-info', 
                                        children=[
                                            html.P("Mean plant size: 50"),
                                            html.P("Healthy plants: 50%"),
                                            html.P("Defect 0: 50%"),
                                        ]
                                    )
                                ]), body=True 
                            )
                        ],
                        md=3,
                    )
                ]
            ),
        ],
        fluid=True,
    )

    return page 

layout = create_main_page()
