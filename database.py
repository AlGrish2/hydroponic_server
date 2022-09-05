from pony.orm import *
from datetime import datetime

db = Database()

class Record(db.Entity):
    tower_id = Required(int)
    raw_video_url = Required(str)
    processed_video_url = Required(str)
    timestamp = Required(datetime)
    mean_size = Required(float)
    nutrient_surplus = Required(float)
    magnesium = Required(float)
    phosphate = Required(float)
    healthy = Required(float)
    phosphorous = Required(float)
    nitrates = Required(float)
    potassium = Required(float)
    nitrogen = Required(float)
    calcium = Required(float)
    sulfur = Required(float)
    min_wl = Required(int)
    max_wl = Required(int)
    air_temp = Required(float)
    hum = Required(float)
    pres = Required(float)
    water_temp = Required(float)
    light1 = Required(float)
    light2 = Required(float)
    light3 = Required(float)
    light4 = Required(float)
    ph = Required(float)
    ec = Required(float)
    tds = Required(float)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def create_record(record):
    Record(
        tower_id=record['tower_id'], 
        raw_video_url=record['raw_video_url'], 
        processed_video_url=record['processed_video_url'], 
        timestamp=datetime.fromtimestamp(record['timestamp']),
        mean_size=record['mean_size'],
        nutrient_surplus=record['nutrient_surplus'],
        magnesium=record['magnesium'],
        phosphate=record['phosphate'],
        healthy=record['healthy'],
        phosphorous=record['phosphorous'],
        nitrates=record['nitrates'],
        potassium=record['potassium'],
        nitrogen=record['nitrogen'],
        calcium=record['calcium'],
        sulfur=record['sulfur'],
        min_wl=record['min_wl'],
        max_wl=record['max_wl'],
        air_temp=record['air_temp'],
        hum=record['hum'],
        pres=record['pres'],
        water_temp=record['water_temp'],
        light1=record['light1'],
        light2=record['light2'],
        light3=record['light3'],
        light4=record['light4'],
        ph=record['ph'],
        ec=record['ec'],
        tds=record['tds'],
    )

@db_session
def get_towers():
    return select(rec.tower_id for rec in Record).distinct()[:]


@db_session
def get_timestamps(tower_id):
    return list(sorted(select(rec.timestamp for rec in Record if rec.tower_id == tower_id)[:], reverse=True))


@db_session
def get_video_url(timestamp):
    return select(rec.processed_video_url for rec in Record if rec.timestamp == timestamp).first()

@db_session
def get_statistics(timestamp):
    return select(rec for rec in Record if rec.timestamp == timestamp).first()

@db_session
def get_tower_statistics(tower_id):
    return select(rec for rec in Record if rec.tower_id == tower_id)[:]
