from datetime import datetime
import requests

data = dict(
    tower_id=0,
    video_url="https://processed-videos-bucket.s3.eu-central-1.amazonaws.com/20220729_141520.mp4",
    timestamp=datetime.now().timestamp()
)

response = requests.post('http://localhost:8050/post_record', json=data)
print(response.status_code)