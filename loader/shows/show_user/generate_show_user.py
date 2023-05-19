import math
from dataclasses import dataclass
from typing import List, Tuple

from loader.parameters import FRAME_PARAMETERS, TAKEOFF_PARAMETERS
from loader.shows.grid_configuration.grid_configuration import GridConfiguration

from .show_user import (
    ColorEventUser,
    DroneUser,
    FireEventUser,
    PositionEventUser,
    ShowUser,
)


@dataclass()
class ShowUserConfiguration(GridConfiguration):
    show_duration_absolute_time: float = 30.0
    takeoff_altitude: float = TAKEOFF_PARAMETERS.takeoff_altitude_meter_min
    duration_before_takeoff: float = 0.0

    def __post_init__(self) -> None:
        if self.show_duration_absolute_time <= 0.0:
            msg = f"Show duration must be stricly positive, not {self.show_duration_absolute_time}"
            raise ValueError(msg)
        if (
            self.takeoff_altitude < TAKEOFF_PARAMETERS.takeoff_altitude_meter_min
            or self.takeoff_altitude > TAKEOFF_PARAMETERS.takeoff_altitude_meter_max
        ):
            msg = (
                f"Takeoff altitude must be between {TAKEOFF_PARAMETERS.takeoff_altitude_meter_min} "
                f"and {TAKEOFF_PARAMETERS.takeoff_altitude_meter_max}, not {self.takeoff_altitude}"
            )
            raise ValueError(msg)
        if self.duration_before_takeoff < 0.0:
            msg = f"Duration before takeoff must be positive, not {self.duration_before_takeoff}"
            raise ValueError(msg)


def rotated_horizontal_coordinates(
    xyz: Tuple[float, float, float],
    angle_radian: float,
) -> Tuple[float, float, float]:
    x_rotated = xyz[0] * math.cos(angle_radian) - xyz[1] * math.sin(angle_radian)
    y_rotated = xyz[0] * math.sin(angle_radian) + xyz[1] * math.cos(angle_radian)
    return (x_rotated, y_rotated, xyz[2])


def get_valid_position_events_user(
    index_x: int,
    index_bias_x: float,
    index_y: int,
    index_bias_y: float,
    show_user_configuration: ShowUserConfiguration,
) -> List[PositionEventUser]:
    return [
        PositionEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff,
            ),
            xyz=rotated_horizontal_coordinates(
                (
                    show_user_configuration.step * index_x - index_bias_x,
                    show_user_configuration.step * index_y - index_bias_y,
                    0.0,
                ),
                show_user_configuration.angle_takeoff,
            ),
        ),
        PositionEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff
                + TAKEOFF_PARAMETERS.takeoff_duration_second,
            ),
            xyz=rotated_horizontal_coordinates(
                (
                    show_user_configuration.step * index_x - index_bias_x,
                    show_user_configuration.step * index_y - index_bias_y,
                    show_user_configuration.takeoff_altitude,
                ),
                show_user_configuration.angle_takeoff,
            ),
        ),
        PositionEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff
                + TAKEOFF_PARAMETERS.takeoff_duration_second
                + show_user_configuration.show_duration_absolute_time,
            ),
            xyz=rotated_horizontal_coordinates(
                (
                    show_user_configuration.step * index_x - index_bias_x,
                    show_user_configuration.step * index_y - index_bias_y,
                    show_user_configuration.takeoff_altitude,
                ),
                show_user_configuration.angle_takeoff,
            ),
        ),
    ]


def get_valid_color_events_user(
    show_user_configuration: ShowUserConfiguration,
) -> List[ColorEventUser]:
    return [
        ColorEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff,
            ),
            rgbw=(1.0, 0.0, 0.0, 0.0),
        ),
        ColorEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff
                + TAKEOFF_PARAMETERS.takeoff_duration_second,
            ),
            rgbw=(0.0, 1.0, 0.0, 0.0),
        ),
        ColorEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff
                + TAKEOFF_PARAMETERS.takeoff_duration_second
                + show_user_configuration.show_duration_absolute_time,
            ),
            rgbw=(0.0, 0.0, 1.0, 0.0),
        ),
    ]


def get_valid_fire_events(
    show_user_configuration: ShowUserConfiguration,
) -> List[FireEventUser]:
    return [
        FireEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff,
            ),
            chanel=0,
            duration=0,
        ),
        FireEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff
                + TAKEOFF_PARAMETERS.takeoff_duration_second,
            ),
            chanel=1,
            duration=0,
        ),
        FireEventUser(
            frame=FRAME_PARAMETERS.from_second_to_frame(
                show_user_configuration.duration_before_takeoff
                + TAKEOFF_PARAMETERS.takeoff_duration_second
                + show_user_configuration.show_duration_absolute_time,
            ),
            chanel=0,
            duration=0,
        ),
    ]


def get_drone_user_index_from_family_indices(
    index_x: int,
    index_y: int,
    nb_x: int,
    family_index: int,
    nb_drone_per_family: int,
) -> int:
    return nb_drone_per_family * (index_y * nb_x + index_x) + family_index


def get_valid_show_user(grid_configuration: GridConfiguration) -> ShowUser:
    if not isinstance(grid_configuration, ShowUserConfiguration):
        show_user_configuration = ShowUserConfiguration(
            nb_x=grid_configuration.nb_x,
            nb_y=grid_configuration.nb_y,
            nb_drone_per_family=grid_configuration.nb_drone_per_family,
            step=grid_configuration.step,
            angle_takeoff=grid_configuration.angle_takeoff,
        )
    else:
        show_user_configuration = grid_configuration

    index_bias_x = 0.5 * (show_user_configuration.nb_x - 1) * show_user_configuration.step
    index_bias_y = 0.5 * (show_user_configuration.nb_y - 1) * show_user_configuration.step
    valid_drones_user = [
        DroneUser(
            index=get_drone_user_index_from_family_indices(
                index_x,
                index_y,
                show_user_configuration.nb_x,
                family_index,
                show_user_configuration.nb_drone_per_family,
            ),
            position_events=get_valid_position_events_user(
                index_x,
                index_bias_x,
                index_y,
                index_bias_y,
                show_user_configuration,
            ),
            color_events=get_valid_color_events_user(show_user_configuration),
            fire_events=get_valid_fire_events(show_user_configuration),
        )
        for index_y in range(show_user_configuration.nb_y)
        for index_x in range(show_user_configuration.nb_x)
        for family_index in range(show_user_configuration.nb_drone_per_family)
    ]
    return ShowUser(drones_user=valid_drones_user)
