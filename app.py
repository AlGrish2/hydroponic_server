from datetime import datetime
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from pony.flask import Pony
from flask import request

from database import create_record, get_timestamps, get_video_url, get_towers

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server
Pony(server)


def create_layout():
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
        color="#48a357",
        dark=True,
    )
    page = dbc.Container(
        [
            navbar,
            html.Br(),
            dash.page_container,
            html.Br(),
        ],
        fluid=True,
    )
    return page

app.layout = create_layout()

@app.callback(Output("video", "url"), Input("scene", "value"))
def update_scene(i):
    i = float(i) if type(i) is str else i['value']
    return get_video_url(datetime.fromtimestamp(i))

@app.callback(Output("scene", "value"), Input("scene", "options"))
def update_scene_value(i):
    return i[0]

@app.callback(Output("scene", "options"), Input("tower_id", "value"))
def update_tower(i):
    i = i if type(i) is str else i['value']
    i = int(i)
    options = [
        {"label": timestamp.strftime("%Y/%m/%d, %H:%M:%S"), "value": timestamp.timestamp()} 
        for timestamp in get_timestamps(i)
    ]
    return options

@app.callback(
    Output('graph', 'figure'),
    Input("tower_id", "value"))
def update_figure(tower_id):

    fig = px.line(x=['2022.08.1', '2022.08.2', '2022.08.3', '2022.08.4'], y=[0, 10, 20, 50])

    fig.update_layout(transition_duration=500)

    return fig


@server.route('/post_record', methods=['POST'])
def post_record():
    create_record(request.get_json(force=True))
    return 'ok'

if __name__ == "__main__":
    app.run_server(debug=True)
