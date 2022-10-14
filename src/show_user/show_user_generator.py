from .show_user import ShowUser
from .show_user import DroneUser, PositionEventUser
import json
from typing import Dict


def get_valid_show_user(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    step_takeoff: float,
    angle_takeoff: int,
    show_duration_frame: int,
) -> Dict:
    ### TO DO: a lot of arbitrary values here, take the value from "parameter.py"
    valid_drones_user = [
        DroneUser(
            position_events=[
                PositionEventUser(
                    position_frame=0,
                    absolute_frame=0,
                    xyz=[
                        step_takeoff * (index_x - nb_x + 1),
                        step_takeoff * (index_y - nb_y + 1),
                        0,
                    ],
                ),
                PositionEventUser(
                    position_frame=40,
                    absolute_frame=240,
                    xyz=[
                        step_takeoff * (index_x - nb_x + 1),
                        step_takeoff * (index_y - nb_y + 1),
                        1.0,
                    ],
                ),
                PositionEventUser(
                    position_frame=40 + show_duration_frame,
                    absolute_frame=240 + 4 * show_duration_frame,
                    xyz=[
                        step_takeoff * (index_x - nb_x + 1),
                        step_takeoff * (index_y - nb_y + 1),
                        1.0,
                    ],
                ),
            ],
            color_events=[],
            fire_events=[],
        )
        for index_x in range(nb_x)
        for index_y in range(nb_y)
        for _ in range(nb_drone_per_family)
    ]
    valid_show_user = ShowUser(drones_user=valid_drones_user)

    return dict(json.loads(valid_show_user.get_json()))
