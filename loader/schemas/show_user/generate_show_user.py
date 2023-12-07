import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Tuple

from loader.parameters import FRAME_PARAMETERS, TAKEOFF_PARAMETERS
from loader.parameters.json_binary_parameters import LandType
from loader.schemas.matrix import get_matrix

from .show_user import DroneUser, ShowUser

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


@dataclass()
class ShowUserConfiguration:
    matrix: "NDArray[np.intp]" = field(default_factory=get_matrix)
    step: float = 1.5
    angle_takeoff: float = 0.0
    show_duration_absolute_time: float = 30.0
    takeoff_altitude: float = TAKEOFF_PARAMETERS.takeoff_altitude_meter_min
    duration_before_takeoff: float = 0.0
    scale: int = 1
    land_type: LandType = LandType.Land

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

    @property
    def nb_x(self) -> int:
        return self.matrix.shape[1]

    @property
    def nb_y(self) -> int:
        return self.matrix.shape[0]


def rotated_horizontal_coordinates(
    xyz: Tuple[float, float, float],
    angle_radian: float,
) -> Tuple[float, float, float]:
    x_rotated = xyz[0] * math.cos(angle_radian) - xyz[1] * math.sin(angle_radian)
    y_rotated = xyz[0] * math.sin(angle_radian) + xyz[1] * math.cos(angle_radian)
    return (x_rotated, y_rotated, xyz[2])


def get_valid_position_events_user(
    index_x: int,
    index_y: int,
    show_user_configuration: ShowUserConfiguration,
    drone_user: DroneUser,
) -> None:
    nb_x = show_user_configuration.nb_x
    nb_y = show_user_configuration.nb_y
    step = show_user_configuration.step
    index_bias_x = 0.5 * (nb_x - 1) * step
    index_bias_y = 0.5 * (nb_y - 1) * step

    drone_user.add_position_event(
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
    )
    drone_user.add_position_event(
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
    )
    drone_user.add_position_event(
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
    )


def get_valid_color_events_user(
    show_user_configuration: ShowUserConfiguration,
    drone_user: DroneUser,
) -> None:
    drone_user.add_color_event(
        frame=FRAME_PARAMETERS.from_second_to_frame(
            show_user_configuration.duration_before_takeoff,
        ),
        rgbw=(1.0, 0.0, 0.0, 0.0),
    )
    drone_user.add_color_event(
        frame=FRAME_PARAMETERS.from_second_to_frame(
            show_user_configuration.duration_before_takeoff
            + TAKEOFF_PARAMETERS.takeoff_duration_second,
        ),
        rgbw=(0.0, 1.0, 0.0, 0.0),
    )
    drone_user.add_color_event(
        frame=FRAME_PARAMETERS.from_second_to_frame(
            show_user_configuration.duration_before_takeoff
            + TAKEOFF_PARAMETERS.takeoff_duration_second
            + show_user_configuration.show_duration_absolute_time,
        ),
        rgbw=(0.0, 0.0, 1.0, 0.0),
    )


def get_valid_fire_events(
    show_user_configuration: ShowUserConfiguration,
    drone_user: DroneUser,
) -> None:
    drone_user.add_fire_event(
        frame=FRAME_PARAMETERS.from_second_to_frame(
            show_user_configuration.duration_before_takeoff,
        ),
        channel=0,
        duration=0,
    )
    drone_user.add_fire_event(
        frame=FRAME_PARAMETERS.from_second_to_frame(
            show_user_configuration.duration_before_takeoff
            + TAKEOFF_PARAMETERS.takeoff_duration_second,
        ),
        channel=1,
        duration=0,
    )
    drone_user.add_fire_event(
        frame=FRAME_PARAMETERS.from_second_to_frame(
            show_user_configuration.duration_before_takeoff
            + TAKEOFF_PARAMETERS.takeoff_duration_second
            + show_user_configuration.show_duration_absolute_time,
        ),
        channel=0,
        duration=0,
    )


def get_valid_show_user(show_user_configuration: ShowUserConfiguration) -> ShowUser:
    matrix = show_user_configuration.matrix
    show_user = ShowUser.create(
        nb_drones=matrix.sum(),  # pyright: ignore[reportUnknownMemberType]
        angle_takeoff=show_user_configuration.angle_takeoff,
        step=show_user_configuration.step,
    )
    show_user.scale = show_user_configuration.scale
    show_user.land_type = show_user_configuration.land_type
    drone_index = 0
    for index_y, column in enumerate(show_user_configuration.matrix):
        for index_x, nb_drones_per_family in enumerate(column):
            for _ in range(nb_drones_per_family):
                drone_user = show_user[drone_index]
                get_valid_position_events_user(
                    index_x,
                    index_y,
                    show_user_configuration,
                    drone_user,
                )
                get_valid_color_events_user(show_user_configuration, drone_user)
                get_valid_fire_events(show_user_configuration, drone_user)
                drone_index += 1
    return show_user
