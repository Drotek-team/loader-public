from math import degrees
from typing import List, Tuple

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ..iostar_json.show_configuration import ShowConfiguration
from ..iostar_json.show_configuration_gcs import ShowConfigurationGcs
from ..show_user.show_user import ShowUser
from .grid_math.grid import get_grid_from_show_user
from .grid_math.grid_angle_estimation import get_angle_takeoff_from_grid
from .grid_math.grid_nb_per_family_estimation import get_nb_drone_per_family_from_grid
from .grid_math.grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid
from .grid_math.grid_step_estimation import get_step_from_grid


def from_user_altitude_range_to_px4_altitude_range(
    altitude_range: Tuple[float, float]
) -> Tuple[int, int]:
    user_minimal_coordinate, user_maximal_coordinate = (0.0, 0.0, altitude_range[0]), (
        0.0,
        0.0,
        altitude_range[1],
    )
    (
        px4_minimal_coordinate,
        px4_maximal_coordinate,
    ) = JSON_BINARY_PARAMETER.from_user_xyz_to_px4_xyz(
        user_minimal_coordinate
    ), JSON_BINARY_PARAMETER.from_user_xyz_to_px4_xyz(
        user_maximal_coordinate
    )
    return (px4_minimal_coordinate[2], px4_maximal_coordinate[2])


def from_user_duration_to_px4_duration(duration: float) -> int:
    return JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
        FRAME_PARAMETER.from_second_to_frame(duration)
    )


def from_user_hull_to_px4_hull(
    user_hull: List[Tuple[float, float]]
) -> List[Tuple[int, int]]:
    user_coordinates = [(user_point[0], user_point[1], 0.0) for user_point in user_hull]
    px4_coordinates = [
        (JSON_BINARY_PARAMETER.from_user_xyz_to_px4_xyz(user_coordinate))
        for user_coordinate in user_coordinates
    ]
    return [
        (px4_coordinate[0], px4_coordinate[1]) for px4_coordinate in px4_coordinates
    ]


# TODO: test this
def sc_to_scg(show_configuration: ShowConfiguration) -> ShowConfigurationGcs:
    return ShowConfigurationGcs(
        nb_x=show_configuration.nb_x,
        nb_y=show_configuration.nb_y,
        nb_drone_per_family=show_configuration.nb_drone_per_family,
        step=JSON_BINARY_PARAMETER.from_user_position_to_px4_position(
            show_configuration.step
        ),
        angle_takeoff=int(degrees(show_configuration.angle_takeoff)),
        duration=from_user_duration_to_px4_duration(show_configuration.duration),
        hull=from_user_hull_to_px4_hull(show_configuration.hull),
        altitude_range=from_user_altitude_range_to_px4_altitude_range(
            show_configuration.altitude_range
        ),
    )


def su_to_sc_procedure(show_user: ShowUser) -> ShowConfiguration:
    grid = get_grid_from_show_user(show_user)
    nb_drone_per_family = get_nb_drone_per_family_from_grid(grid)
    step = get_step_from_grid(grid)
    angle_takeoff = get_angle_takeoff_from_grid(grid, nb_drone_per_family)
    nb_x, nb_y = get_nb_x_nb_y_from_grid(grid, nb_drone_per_family, angle_takeoff)
    return ShowConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=step,
        angle_takeoff=angle_takeoff,
        duration=show_user.duration,
        hull=show_user.convex_hull,
        altitude_range=show_user.altitude_range,
    )


def su_to_scg_procedure(show_user: ShowUser) -> ShowConfigurationGcs:
    return sc_to_scg(su_to_sc_procedure(show_user))
