from pydantic import BaseModel
from typing import List, Tuple
import json


class PositionEventUser(BaseModel):
    position_frame: int  # 4 frame per second
    absolute_frame: int  # 24 frame per second
    xyz: Tuple[float, float, float]  # ENU and meter


class ColorEventUser(BaseModel):
    color_frame: int  # 24 frame per second
    absolute_frame: int  # 24 frame per second
    rgbw: Tuple[float, float, float, float]  # between 0 and 1


class FireEventUser(BaseModel):
    fire_frame: int  # 24 frame per second
    absolute_frame: int  # 24 frame per second
    chanel: float  # Chanel of the drone
    duration: float  # Duration of the event


class DroneUser(BaseModel):
    position_events: List[PositionEventUser]
    color_events: List[ColorEventUser]
    fire_events: List[FireEventUser]


class ShowUser(BaseModel):
    drones_user: List[DroneUser]

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: ShowUser):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
