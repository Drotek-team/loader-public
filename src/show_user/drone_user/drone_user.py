from pydantic import BaseModel
from typing import List, Tuple


class PositionEventUser(BaseModel):
    frame: int  # 24 frame per second
    xyz: Tuple[float, float, float]  # ENU and meter


class ColorEventUser(BaseModel):
    frame: int  # 24 frame per second
    rgbw: Tuple[float, float, float, float]  # between 0 and 1


class FireEventUser(BaseModel):
    frame: int  # 24 frame per second
    chanel: float  # Chanel of the drone
    duration: float  # Duration of the event


class DroneUser(BaseModel):
    position_events: List[PositionEventUser]
    color_events: List[ColorEventUser]
    fire_events: List[FireEventUser]
