from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .show_user import ColorEventUser, DroneUser, PositionEventUser, ShowUser


def get_valid_show_user(
    nb_x: int = 1,
    nb_y: int = 1,
    nb_drone_per_family: int = 1,
    step_takeoff: float = 0,
    angle_takeoff: int = 0,
    show_duration_absolute_time: float = 30.0,
) -> ShowUser:
    index_bias = 1.5
    valid_drones_user = [
        DroneUser(
            position_events=[
                PositionEventUser(
                    frame=0,
                    xyz=(
                        step_takeoff * (index_y - nb_y + index_bias),
                        step_takeoff * (index_x - nb_x + index_bias),
                        0.0,
                    ),
                ),
                PositionEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    ),
                    xyz=(
                        step_takeoff * (index_y - nb_y + index_bias),
                        step_takeoff * (index_x - nb_x + index_bias),
                        1.0,
                    ),
                ),
                PositionEventUser(
                    frame=FRAME_PARAMETER.from_second_to_frame(
                        TAKEOFF_PARAMETER.takeoff_duration_second
                    )
                    + FRAME_PARAMETER.from_second_to_frame(show_duration_absolute_time),
                    xyz=(
                        step_takeoff * (index_y - nb_y + index_bias),
                        step_takeoff * (index_x - nb_x + index_bias),
                        1.0,
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
        for index_x in range(nb_x)
        for index_y in range(nb_y)
        for _ in range(nb_drone_per_family)
    ]
    return ShowUser(drones_user=valid_drones_user)
