from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from models import RecognitionResultsSchema, SensorsSchema

from database import put_sensors_data, put_recognitions_data

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def healthcheck():
    return "I am alive!"


@app.post("/add_recognitions")
async def add_recognitions(recognitions: RecognitionResultsSchema):
    data = jsonable_encoder(recognitions)
    # await put_recognitions_data(data)
    return "Success"


@app.post("/add_sensors_data")
async def add_sensors_data(sensors_data: SensorsSchema):
    print(sensors_data)
    data = jsonable_encoder(sensors_data)
    await put_sensors_data(data)
    return "Success"
