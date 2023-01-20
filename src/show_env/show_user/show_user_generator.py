import math
from dataclasses import dataclass
from typing import Tuple

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .show_user import ColorEventUser, DroneUser, PositionEventUser, ShowUser


@dataclass(frozen=True)
class GridConfiguration:
    nb_x: int = 1
    nb_y: int = 1
    nb_drone_per_family: int = 1
    step_takeoff: float = 1.5
    angle_takeoff: float = 0.0


@dataclass(frozen=True)
class ShowUserConfiguration(GridConfiguration):
    show_duration_absolute_time: float = 30.0
    takeoff_altitude: float = TAKEOFF_PARAMETER.takeoff_altitude_meter_min


def rotated_horizontal_coordinates(
    xyz: Tuple[float, float, float], angle_radian: float
) -> Tuple[float, float, float]:
    x_rotated = xyz[0] * math.cos(angle_radian) - xyz[1] * math.sin(angle_radian)
    y_rotated = xyz[0] * math.sin(angle_radian) + xyz[1] * math.cos(angle_radian)
    return (x_rotated, y_rotated, xyz[2])


def get_valid_show_user(show_user_configuration: ShowUserConfiguration) -> ShowUser:
    index_bias_x = (
        0.5 * (show_user_configuration.nb_x - 1) * show_user_configuration.step_takeoff
    )
    index_bias_y = (
        0.5 * (show_user_configuration.nb_y - 1) * show_user_configuration.step_takeoff
    )
    valid_drones_user = [
        DroneUser(
            position_events=[
                PositionEventUser(
                    frame=0,
                    xyz=rotated_horizontal_coordinates(
                        (
                            show_user_configuration.step_takeoff * index_x
                            - index_bias_x,
                            show_user_configuration.step_takeoff * index_y
                            - index_bias_y,
                            0.0,
                        ),
                        show_user_configuration.angle_takeoff,
                    ),
                ),
                PositionEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    ),
                    xyz=rotated_horizontal_coordinates(
                        (
                            show_user_configuration.step_takeoff * index_x
                            - index_bias_x,
                            show_user_configuration.step_takeoff * index_y
                            - index_bias_y,
                            show_user_configuration.takeoff_altitude,
                        ),
                        show_user_configuration.angle_takeoff,
                    ),
                ),
                PositionEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    )
                    + FRAME_PARAMETER.from_second_to_frame(
                        show_user_configuration.show_duration_absolute_time
                    ),
                    xyz=rotated_horizontal_coordinates(
                        (
                            show_user_configuration.step_takeoff * index_x
                            - index_bias_x,
                            show_user_configuration.step_takeoff * index_y
                            - index_bias_y,
                            show_user_configuration.takeoff_altitude,
                        ),
                        show_user_configuration.angle_takeoff,
                    ),
                ),
            ],
            color_events=[
                ColorEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    ),
                    rgbw=(1.0, 0.0, 0.0, 0.0),
                ),
                ColorEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    )
                    + 24,
                    rgbw=(0.0, 1.0, 0.0, 0.0),
                ),
                ColorEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    )
                    + 48,
                    rgbw=(0.0, 0.0, 1.0, 0.0),
                ),
            ],
            fire_events=[],
        )
        for index_y in range(show_user_configuration.nb_y)
        for index_x in range(show_user_configuration.nb_x)
        for _ in range(show_user_configuration.nb_drone_per_family)
    ]
    return ShowUser(drones_user=valid_drones_user)
