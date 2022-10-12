from typing import List
from ...show_px4.show_px4 import ShowPx4
from ...show_dev.show_dev import (
    ShowDev,
    DroneDev,
    PositionEventDev,
)
from ...show_px4.drone_px4.events.position_events import PositionEvent
from ..migration_SP_SU.data_convertion_format import XyzConvertionStandard


def get_drone_dev(
    drone_index: int,
    position_events: List[PositionEvent],
    xyz_convertion_standard: XyzConvertionStandard,
) -> DroneDev:
    return DroneDev(
        drone_index,
        [
            PositionEventDev(
                position_event.frame,
                xyz_convertion_standard.from_px4_xyz_to_user_xyz(position_event.xyz),
            )
            for position_event in position_events
        ],
    )


def SP_to_SD_procedure(show_px4: ShowPx4) -> ShowDev:
    xyz_convertion_standard = XyzConvertionStandard()
    return ShowDev(
        [
            get_drone_dev(
                drone_px4.index,
                drone_px4.position_events.events,
                xyz_convertion_standard,
            )
            for drone_px4 in show_px4
        ]
    )
