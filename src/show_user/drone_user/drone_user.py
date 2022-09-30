from pydantic import BaseModel
from typing import List, Tuple


class PositionEventUser(BaseModel):
    frame: int
    xyz: Tuple[float, float, float]


class ColorEventUser(BaseModel):
    frame: int
    rgbw: Tuple[float, float, float, float]


class FireEventUser(BaseModel):
    frame: int
    chanel: float
    duration: float


class DroneUser(BaseModel):
    position_events: List[PositionEventUser]
    color_events: List[ColorEventUser]
    fire_events: List[FireEventUser]
