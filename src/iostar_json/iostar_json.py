import json
from typing import List, Tuple
from pydantic import BaseModel


### TO DO: comment each attribute
class Dance(BaseModel):
    dance: List[int]


### TO DO: comment each attribute
class Family(BaseModel):
    drones: List[Dance]
    x: int
    y: int
    z: int


### TO DO: comment each attribute
class IostarJson(BaseModel):
    familes: List[Family]
    nb_x: int
    nb_y: int
    step: int
    angle_takeoff: int
    duration: int
    hull: List[Tuple[int, int]]
    altitude_range: Tuple[int, int]

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: IostarJson):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
