import json
from typing import List, Tuple
from pydantic import BaseModel


class Dance(BaseModel):
    dance: List[int]  # List of integer symbolising the list of octect


class Family(BaseModel):
    drones: List[Dance]  # List of the drone composing a family
    x: int  # X relative position (NED) of the family in centimeter
    y: int  # Y relative position (NED) of the family in centimeter
    z: int  # Z relative position (NED) of the family in centimeter


class Show(BaseModel):
    families: List[Family]  # List of the families composing the show
    nb_x: int  # Number of families on the x-axis during the takeoff
    nb_y: int  # Number of families on the y-axis during the takeoff
    step: int  # Distance separating the families during the takeoff in centimeter
    angle_takeoff: int  # Angle of the takeoff grid
    duration: int  # Duration of the show in millisecond
    hull: List[
        Tuple[int, int]
    ]  # List of the relative coordinate (XY in NED and centimeter) symbolysing a convex hull of a show
    altitude_range: Tuple[
        int, int
    ]  # Relative coordinate ( z_min and z_max in NED and centimeter) symbolising the range of the z-axis


class IostarJson(BaseModel):
    show: Show

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: IostarJson):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
