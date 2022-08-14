import dash
import dash_player
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def Header(name, app):
    title = html.H2(name, style={"margin-top": 5})

    return dbc.Row([dbc.Col(title, md=8)])


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


# Start app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
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
                id="video", width="auto", height="480px", controls=True
            )
        )
    ]
)

graph_detection = dbc.Card(
    [
        dbc.CardBody(
            dcc.Graph(
                id="graph-detection",
                config={"modeBarButtonsToAdd": ["drawrect"]},
                style={"height": "calc(50vh - 100px)"},
            )
        )
    ]
)


app.layout = dbc.Container(
    [
        Header("Hydroponic", app),
        html.Hr(),
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
    return app.get_asset_url("https://www.youtube.com/watch?v=i7KXycA6VGo")


if __name__ == "__main__":
    app.run_server(debug=False)
