import dash
import dash_player
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Statistics", href="/statistics")),

    ],
    brand="Hydroponic",
    brand_href="/",
    color="#008080",
    dark=True,
)


def add_editable_box(
    fig, x0, y0, x1, y1, name=None, color=None, opacity=1, group=None, text=None
):
    fig.add_shape(
        editable=True,
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        line_color=color,
        opacity=opacity,
        line_width=3,
        name=name,
    )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

controls = [
    dbc.Select(
        id="scene",
        options=[{"label": f"Scene #{i}", "value": i} for i in range(1, 4)],
        value=1,
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

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                dbc.Col(
                    [
                        video,
                        html.Br(),
                        dbc.Card(dbc.Row([dbc.Col(c) for c in controls]), body=True),
                    ],
                    md=7,
                ),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(Output("video", "url"), [Input("scene", "value")])
def update_scene(i):
    return "https://processed-videos-bucket.s3.eu-central-1.amazonaws.com/20220729_141520.mp4"


if __name__ == "__main__":
    app.run_server(debug=False)
