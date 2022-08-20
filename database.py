from pony.orm import *
from datetime import datetime

db = Database()

class Record(db.Entity):
    tower_id = Required(int)
    video_url = Required(str)
    timestamp = Required(datetime)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def create_record(record):
    Record(tower_id=record['tower_id'], video_url=record['video_url'], timestamp=datetime.fromtimestamp(record['timestamp']))

@db_session
def get_towers():
    return select(rec.tower_id for rec in Record).distinct()[:]


@db_session
def get_timestamps(tower_id):
    return list(sorted(select(rec.timestamp for rec in Record if rec.tower_id == tower_id)[:], reverse=True))


@db_session
def get_video_url(timestamp):
    return select(rec.video_url for rec in Record if rec.timestamp == timestamp).first()
