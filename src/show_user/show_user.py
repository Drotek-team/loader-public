import json
from typing import List, Tuple

from pydantic import BaseModel

from ..parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ..parameter.iostar_flight_parameter.iostar_land_parameter import LAND_PARAMETER


class PositionEventUser(BaseModel):
    frame: int  # 24 fps
    xyz: Tuple[float, float, float]  # ENU and meter

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETER.from_absolute_frame_to_absolute_time(self.frame)


class ColorEventUser(BaseModel):
    frame: int  # 24 fps
    rgbw: Tuple[float, float, float, float]  # between 0 and 1

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETER.from_absolute_frame_to_absolute_time(self.frame)


class FireEventUser(BaseModel):
    frame: int  # 24 fps
    chanel: float  # Chanel of the drone
    duration: float  # Duration of the event

    @property
    def absolute_time(self) -> float:
        return FRAME_PARAMETER.from_absolute_frame_to_absolute_time(self.frame)


class DroneUser(BaseModel):
    position_events: List[PositionEventUser]
    color_events: List[ColorEventUser]
    fire_events: List[FireEventUser]

    @property
    def nb_position_events(self) -> int:
        return len(self.position_events)

    @property
    def flight_positions(self) -> List[PositionEventUser]:
        return self.position_events[1:]

    @property
    def last_frame(self) -> int:
        return self.position_events[-1].frame

    @property
    def last_height(self) -> float:
        return self.position_events[-1].xyz[2]

    def get_position_frame_by_index(self, index: int) -> int:
        return self.position_events[index].frame

    def get_absolute_time_by_index(self, index: int) -> float:
        return self.position_events[index].absolute_time

    def get_xyz_simulation_by_index(self, index: int) -> Tuple[float, float, float]:
        return self.position_events[index].xyz


class ShowUser(BaseModel):
    drones_user: List[DroneUser]

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: ShowUser):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

    def __iter__(self):
        yield from self.drones_user

    def __getitem__(self, drone_user_index: int):
        return self.drones_user[drone_user_index]

    def __len__(self):
        return len(self.drones_user)

    @property
    def nb_drones(self) -> int:
        return len(self.drones_user)

    @property
    def get_last_frame(
        self,
    ) -> int:
        return max(
            [
                drone_user.last_frame
                + FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    LAND_PARAMETER.get_land_second_delta(drone_user.last_height)
                )
                for drone_user in self.drones_user
            ]
        )
