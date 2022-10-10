from .show_user import ShowUser
from .drone_user.drone_user import DroneUser, PositionEventUser
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
    valid_drones_user = [
        DroneUser(
            position_events=[
                PositionEventUser(
                    frame=0, xyz=[index_x - nb_x + 1, index_y - nb_y + 1, 0]
                ),
                PositionEventUser(
                    frame=240, xyz=[index_x - nb_x + 1, index_y - nb_y + 1, 1]
                ),
                PositionEventUser(
                    frame=240 + show_duration_frame,
                    xyz=[index_x - nb_x + 1, index_y - nb_y + 1, 1],
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
