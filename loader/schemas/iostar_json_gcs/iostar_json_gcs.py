from typing import TYPE_CHECKING, List, Tuple

import numpy as np
from pydantic import BaseModel

from loader.parameters.frame_parameters import FRAME_PARAMETERS
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user.convex_hull import calculate_convex_hull

if TYPE_CHECKING:
    from loader.schemas.show_user import ShowUser


class Dance(BaseModel):
    dance: List[int]  # List of integer symbolising the list of octect


class Family(BaseModel):
    drones: List[Dance]  # List of the drone composing a family
    x: int  # X relative position (NED) of the family in centimeter
    y: int  # Y relative position (NED) of the family in centimeter
    z: int  # Z relative position (NED) of the family in centimeter

    @classmethod
    def from_drone_px4(
        cls,
        autopilot_format_family: List[DronePx4],
    ) -> "Family":
        return Family(
            drones=[
                Dance(dance=DronePx4.to_binary(drone_px4_family))
                for drone_px4_family in autopilot_format_family
            ],
            x=autopilot_format_family[0].position_events.specific_events[0].xyz[0],
            y=autopilot_format_family[0].position_events.specific_events[0].xyz[1],
            z=autopilot_format_family[0].position_events.specific_events[0].xyz[2],
        )


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
        int,
        int,
    ]  # Relative coordinate ( z_min and z_max in NED and centimeter) symbolising the range of the z-axis


class IostarJsonGcs(BaseModel):
    show: Show

    @property
    def nb_drones_per_family(self) -> int:
        return len(self.show.families[0].drones)

    @classmethod
    def from_show_user(cls, show_user: "ShowUser") -> "IostarJsonGcs":
        (nb_x, nb_y) = show_user.matrix.shape
        nb_drones_per_family = show_user.matrix.max()  # pyright: ignore[reportUnknownMemberType]
        step = JSON_BINARY_PARAMETERS.from_user_position_to_px4_position(show_user.step)
        angle_takeoff = -round(np.rad2deg(show_user.angle_takeoff))
        duration = from_user_duration_to_px4_duration(show_user.duration)
        hull = from_user_hull_to_px4_hull(show_user.convex_hull)
        altitude_range = from_user_altitude_range_to_px4_altitude_range(show_user.altitude_range)
        autopilot_format = DronePx4.from_show_user(show_user)
        return IostarJsonGcs(
            show=Show(
                families=[
                    Family.from_drone_px4(
                        autopilot_format[
                            nb_drones_per_family
                            * family_index : nb_drones_per_family
                            * family_index
                            + nb_drones_per_family
                        ],
                    )
                    for family_index in range(nb_x * nb_y)
                ],
                duration=duration,
                hull=hull,
                altitude_range=altitude_range,
                step=step,
                nb_x=nb_x,
                nb_y=nb_y,
                angle_takeoff=angle_takeoff,
            ),
        )


def from_user_altitude_range_to_px4_altitude_range(
    altitude_range: Tuple[float, float],
) -> Tuple[int, int]:
    user_minimal_coordinate, user_maximal_coordinate = (0.0, 0.0, altitude_range[0]), (
        0.0,
        0.0,
        altitude_range[1],
    )
    (
        px4_minimal_coordinate,
        px4_maximal_coordinate,
    ) = JSON_BINARY_PARAMETERS.from_user_xyz_to_px4_xyz(
        user_minimal_coordinate,
    ), JSON_BINARY_PARAMETERS.from_user_xyz_to_px4_xyz(
        user_maximal_coordinate,
    )
    return (px4_maximal_coordinate[2], px4_minimal_coordinate[2])


def from_user_duration_to_px4_duration(duration: float) -> int:
    return JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
        FRAME_PARAMETERS.from_second_to_frame(duration),
    )


def from_user_hull_to_px4_hull(
    user_hull: List[Tuple[float, float]],
) -> List[Tuple[int, int]]:
    user_coordinates = [(user_point[0], user_point[1], 0.0) for user_point in user_hull]
    px4_coordinates = [
        (JSON_BINARY_PARAMETERS.from_user_xyz_to_px4_xyz(user_coordinate))
        for user_coordinate in user_coordinates
    ]
    return [
        (x, y)
        for y, x in calculate_convex_hull(
            [(px4_coordinate[1], px4_coordinate[0]) for px4_coordinate in px4_coordinates],
        )
    ]
