from this import s
import pandas as pd
from datetime import datetime
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from pony.flask import Pony
from flask import request

from database import create_record, get_statistics, get_timestamps, get_tower_statistics, get_video_url, get_towers

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

@app.callback(Output("desc-info", "children"), Input("scene", "value"))
def update_statistics(i):
    i = float(i) if type(i) is str else i['value']
    statistics = get_statistics(datetime.fromtimestamp(i))
    return [
        html.P(f"Mean plant size: {round(statistics.mean_size, 3)}"),
        html.P(f"Nutrient surplus: {round(statistics.nutrient_surplus, 3)}"),
        html.P(f"Healthy: {round(statistics.healthy, 3)}"),
        html.P(f"Magnesium: {round(statistics.magnesium, 3)}"),
        html.P(f"Phosphate: {round(statistics.phosphate, 3)}"),
        html.P(f"Phosphorous: {round(statistics.phosphorous, 3)}"),
        html.P(f"Nitrates: {round(statistics.nitrates, 3)}"),
        html.P(f"Potassium: {round(statistics.potassium, 3)}"),
        html.P(f"Nitrogen: {round(statistics.nitrogen, 3)}"),
        html.P(f"Sulfur: {round(statistics.sulfur, 3)}"),
    ]

@app.callback(Output("sensor-info", "children"), Input("scene", "value"))
def update_sensor_info(i):
    i = float(i) if type(i) is str else i['value']
    statistics = get_statistics(datetime.fromtimestamp(i))
    return [
        html.P(f"min wl: {round(statistics.min_wl, 3)}"),
        html.P(f"max wl: {round(statistics.max_wl, 3)}"),
        html.P(f"air temp: {round(statistics.air_temp, 3)}"),
        html.P(f"hum: {round(statistics.hum, 3)}"),
        html.P(f"pres: {round(statistics.pres, 3)}"),
        html.P(f"water temp: {round(statistics.water_temp, 3)}"),
        html.P(f"light1: {round(statistics.light1, 3)}"),
        html.P(f"light2: {round(statistics.light2, 3)}"),
        html.P(f"light3: {round(statistics.light3, 3)}"),
        html.P(f"light4: {round(statistics.light4, 3)}"),
        html.P(f"ph: {round(statistics.ph, 3)}"),
        html.P(f"ec: {round(statistics.ec, 3)}"),
        html.P(f"tds: {round(statistics.tds, 3)}"),
    ]


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
    Output('mean_size_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.mean_size for stat in statistics],
        title='Mean size'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('defect_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)
    stats = []
    for stat in statistics:
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'nutrient_surplus', 
            'probability': stat.nutrient_surplus
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'magnesium', 
            'probability': stat.magnesium
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'phosphate', 
            'probability': stat.phosphate
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'healthy', 
            'probability': stat.healthy
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'phosphorous', 
            'probability': stat.phosphorous
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'nitrates', 
            'probability': stat.nitrates
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'potassium', 
            'probability': stat.potassium
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'nitrogen', 
            'probability': stat.nitrogen
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'calcium', 
            'probability': stat.calcium
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'defect': 'sulfur', 
            'probability': stat.sulfur
        })
    df = pd.DataFrame(stats)
    fig = px.line(
        df, 
        x='timestamp', 
        y='probability',
        color='defect',
        title='Defects'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('light_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)
    stats = []
    for stat in statistics:
        stats.append({
            'timestamp': stat.timestamp, 
            'num': 'light1', 
            'value': stat.light1
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'num': 'light2', 
            'value': stat.light2
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'num': 'light3', 
            'value': stat.light3
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'num': 'light4', 
            'value': stat.light4
        })
    df = pd.DataFrame(stats)
    fig = px.line(
        df, 
        x='timestamp', 
        y='value',
        color='num',
        title='Light'
    )
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('temp_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)
    stats = []
    for stat in statistics:
        stats.append({
            'timestamp': stat.timestamp, 
            'type': 'air', 
            'value': stat.air_temp
        })
        stats.append({
            'timestamp': stat.timestamp, 
            'type': 'water', 
            'value': stat.water_temp
        })
    df = pd.DataFrame(stats)
    fig = px.line(
        df, 
        x='timestamp', 
        y='value',
        color='type',
        title='Temperature'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('min_wl_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.min_wl for stat in statistics],
        title='min wl'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('max_wl_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.max_wl for stat in statistics],
        title='max wl'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('hum_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.hum for stat in statistics],
        title='hum'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('pres_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.pres for stat in statistics],
        title='pres'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('ph_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.ph for stat in statistics],
        title='ph'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('ec_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.ec for stat in statistics],
        title='ec'
    )
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('tds_graph', 'figure'),
    Input("tower_id", "value"))
def update_mean_size_figure(tower_id):
    tower_id = tower_id if type(tower_id) is str else tower_id['value']
    statistics = get_tower_statistics(tower_id)

    fig = px.line(
        x=[stat.timestamp for stat in statistics], 
        y=[stat.tds for stat in statistics],
        title='tds'
    )
    fig.update_layout(transition_duration=500)
    return fig


@server.route('/post_record', methods=['POST'])
def post_record():
    create_record(request.get_json(force=True))
    return 'ok'

if __name__ == "__main__":
    app.run_server(debug=True)
