from datetime import datetime
import requests

data = dict(
    tower_id=0,
    raw_video_url="https://processed-videos-bucket.s3.eu-central-1.amazonaws.com/20220729_141520.mp4",
    processed_video_url="https://processed-videos-bucket.s3.eu-central-1.amazonaws.com/20220729_141520.mp4",
    timestamp=datetime.now().timestamp(),
    mean_size=0.5,
    nutrient_surplus=0.5,
    magnesium=0.5,
    phosphate=0.5,
    healthy=0.5,
    phosphorous=0.5,
    nitrates=0.5,
    potassium=0.5,
    nitrogen=0.5,
    calcium=0.5,
    sulfur=0.5,
    min_wl=0,
    max_wl=1,
    air_temp=0.5,
    hum=0.5,
    pres=0.5,
    water_temp=0.5,
    light1=0.5,
    light2=0.5,
    light3=0.5,
    light4=0.5,
    ph=0.5,
    ec=0.5,
    tds=0.5,
)

response = requests.post('http://localhost:8050/post_record', json=data)
print(response.status_code)