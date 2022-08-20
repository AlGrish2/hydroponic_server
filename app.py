from datetime import datetime
import dash
import dash_player
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from pony.flask import Pony
from flask import request

from database import create_record, get_timestamps, get_towers, get_video_url

tower_ids = [{"label": f"Tower: {i}", "value": i} for i in get_towers()]
tower_select = dbc.Select(
    id="tower_id",
    options=tower_ids,
    value=tower_ids[0] if len(tower_ids) else {"label": f"Tower: None", "value": -1}
),

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Statistics", href="/statistics")),
        dbc.NavItem(tower_select),
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
Pony(server)

options = [
    {"label": i.strftime("%Y/%m/%d, %H:%M:%S"), "value": i.timestamp()} 
    for i in get_timestamps(tower_select[0].value['value'])
]
controls = [
    dbc.Select(
        id="scene",
        options=options,
        value=options[0] if len(options) else {"label": datetime(year=1970, month=1, day=1).strftime("%Y/%m/%d, %H:%M:%S"), "value": 0}
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
    i = float(i) if type(i) is str else i['value']
    return get_video_url(datetime.fromtimestamp(i))

@app.callback(Output("scene", "value"), [Input("scene", "options")])
def update_scene_value(i):
    return i[0]


@app.callback(Output("scene", "options"), [Input("tower_id", "value")])
def update_tower(i):
    i = i if type(i) is str else i['value']
    i = int(i)
    options = [
        {"label": timestamp.strftime("%Y/%m/%d, %H:%M:%S"), "value": timestamp.timestamp()} 
        for timestamp in get_timestamps(i)
    ]
    return options


@server.route('/post_record', methods=['POST'])
def post_record():
    create_record(request.get_json(force=True))
    return 'ok'

if __name__ == "__main__":
    app.run_server(debug=True)
