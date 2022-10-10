from typing import List
from ...drones_px4.drones_px4 import DronesPx4
from ...show_simulation.drone_simulation import DroneSimulation, PositionEventSimulation
from ...drones_px4.drone_px4.events.position_events import PositionEvent
from ..migration_DP_DU.data_convertion_format import XyzConvertionStandard
from ...show_simulation.drone_simulation import DronesSimulation


def get_drone_simulation(
    drone_index: int,
    position_events: List[PositionEvent],
    xyz_convertion_standard: XyzConvertionStandard,
) -> DroneSimulation:
    return DroneSimulation(
        drone_index,
        [
            PositionEventSimulation(
                position_event.frame,
                xyz_convertion_standard.from_px4_xyz_to_user_xyz(position_event.xyz),
            )
            for position_event in position_events
        ],
    )


def DP_to_DS_procedure(drones_px4: DronesPx4) -> DronesSimulation:
    xyz_convertion_standard = XyzConvertionStandard()
    return DronesSimulation(
        [
            get_drone_simulation(
                drone_px4.index,
                drone_px4.position_events.events,
                xyz_convertion_standard,
            )
            for drone_px4 in drones_px4.drones
        ]
    )
