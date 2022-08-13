import os
from enum import Enum
import motor.motor_asyncio
from bson.objectid import ObjectId

mongo_host = os.environ["MONGO_HOST"]
MONGO_DETAILS = f"mongodb://admin:admin@{mongo_host}:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.data

recognitions_collection = database.get_collection("recognitions")
sensors_data_collection = database.get_collection("sensors")


async def put_recognitions_data(rec_data):
    await recognitions_collection.insert_one(rec_data)


async def put_sensors_data(sensors_data):
    await sensors_data_collection.insert_one(sensors_data)


if __name__ == "__main__":
    put_recognitions_data({"test": "data"})
    