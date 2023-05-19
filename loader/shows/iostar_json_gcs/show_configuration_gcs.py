from math import degrees
from typing import List, Tuple

from pydantic import BaseModel

from loader.parameters.frame_parameters import FRAME_PARAMETERS
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.shows.iostar_json_gcs.show_configuration import ShowConfiguration
from loader.shows.show_user.convex_hull import calculate_convex_hull
from loader.shows.show_user.show_user import ShowUser


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


class ShowConfigurationGcs(BaseModel):
    nb_x: int  # Number of families on the x-axis during the takeoff
    nb_y: int  # Number of families on the y-axis during the takeoff
    nb_drone_per_family: int  # Number of drones in each families
    step: int  # Distance separating the families during the takeoff in centimeter
    angle_takeoff: int  # Angle of the takeoff grid in degree
    duration: int  # Duration of the show in microsecond
    hull: List[
        Tuple[int, int]
    ]  # List of the relative coordinate (XY in NED and centimeter) symbolysing a convex hull of a show
    altitude_range: Tuple[
        int,
        int,
    ]  # Relative coordinate ( z_min and z_max in NED and centimeter) symbolising the range of the z-axis

    @classmethod
    def from_show_configuration(
        cls,
        show_configuration: ShowConfiguration,
    ) -> "ShowConfigurationGcs":
        return cls(
            nb_x=show_configuration.nb_x,
            nb_y=show_configuration.nb_y,
            nb_drone_per_family=show_configuration.nb_drone_per_family,
            step=JSON_BINARY_PARAMETERS.from_user_position_to_px4_position(
                show_configuration.step,
            ),
            angle_takeoff=int(degrees(show_configuration.angle_takeoff)),
            duration=from_user_duration_to_px4_duration(show_configuration.duration),
            hull=from_user_hull_to_px4_hull(show_configuration.hull),
            altitude_range=from_user_altitude_range_to_px4_altitude_range(
                show_configuration.altitude_range,
            ),
        )

    @classmethod
    def from_show_user(cls, show_user: ShowUser) -> "ShowConfigurationGcs":
        return cls.from_show_configuration(ShowConfiguration.from_show_user(show_user))
