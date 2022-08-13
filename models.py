from typing import List
from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class DeffectEnum(str, Enum):
    phosphor = "phosphor"
    magnesium = "magnesium"
    illness = "some illness"


class PlantDeffect(BaseModel):
    plant_id: int
    deffect: str

    class Config:
        schema_extra = {
            "example": {
                "plant_id": "1",
                "deffect": "some illness"
            }
        }

    
class RecognitionResultsSchema(BaseModel):
    filename: str
    deffects: List[PlantDeffect]

    class Config:
        schema_extra = {
            "example": {
                "filename": "video.mp4",
                "deffects": [
                    {"plant_id": "1", "deffect": "some_illness"},
                    {"plant_id": "2", "deffect": "phosphor"}
                    ]
            }
        }


class SensorsSchema(BaseModel):
    filename: str
    temp_celsius: float
    minerals: float
    check_time: datetime

    class Config:
        schema_extra = {
            "example": {
                "filename": "video.mp4",
                "temp_celsius": "21.0",
                "minerals": "0.9",
                "check_time": "2022-06-01T00:18:31+00:00"
            }
        }

