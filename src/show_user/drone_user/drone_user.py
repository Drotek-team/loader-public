from lib2to3.pytree import Base
from pydantic import BaseModel
from typing import List


class PositionEvent(BaseModel):
    frame: int
    x: float
    y: float
    z: float


class ColorEvent(BaseModel):
    frame: int
    r: float
    g: float
    b: float
    w: float


class FireEvent(BaseModel):
    frame: int
    chanel: float
    duration: float


class DroneUser(BaseModel):
    position_events: List[PositionEvent]
    color_events: List[ColorEvent]
    fire_events: List[FireEvent]
