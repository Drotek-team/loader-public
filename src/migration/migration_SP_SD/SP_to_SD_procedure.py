from typing import List

from ...parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ...show_dev.show_dev import DroneDev, PositionEventDev, ShowDev
from ...show_px4.drone_px4.events.position_events import PositionEvent
from ...show_px4.show_px4 import ShowPx4


def get_drone_dev(
    drone_index: int,
    position_events: List[PositionEvent],
) -> DroneDev:
    return DroneDev(
        drone_index,
        [
            PositionEventDev(
                position_event.frame,
                JSON_BINARY_PARAMETER.from_px4_xyz_to_user_xyz(position_event.xyz),
            )
            for position_event in position_events
        ],
    )


def SP_to_SD_procedure(show_px4: ShowPx4) -> ShowDev:
    return ShowDev(
        [
            get_drone_dev(
                drone_px4.index,
                drone_px4.position_events.events,
            )
            for drone_px4 in show_px4
        ]
    )
