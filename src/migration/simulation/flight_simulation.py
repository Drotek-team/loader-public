from typing import List

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ...show_user.show_user import DroneUser
from .in_air_flight_simulation import in_air_flight_simulation
from .land_simulation import land_simulation
from .position_simulation import SimulationInfo
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


# TODO: this is the one that must be test like hell
def flight_simulation(
    drone_user: DroneUser,
    last_frame: int,
) -> List[SimulationInfo]:
    simulation_infos: List[SimulationInfo] = []
    if len(drone_user.position_events) == 1:
        simulation_infos += stand_by_simulation(
            FRAME_PARAMETER.from_absolute_time_to_position_frame(
                JSON_BINARY_PARAMETER.show_duration_min_second
            ),
            last_frame,
            drone_user.get_xyz_simulation_by_index(0),
        )
        return simulation_infos
    last_frame_stand_by = 0
    if drone_user.get_position_frame_by_index(0) != 0:
        simulation_infos += stand_by_simulation(
            FRAME_PARAMETER.from_absolute_time_to_position_frame(
                JSON_BINARY_PARAMETER.show_duration_min_second
            ),
            drone_user.get_position_frame_by_index(0) - 1,
            drone_user.get_xyz_simulation_by_index(0),
        )
        last_frame_stand_by = drone_user.get_position_frame_by_index(0)
    simulation_infos += takeoff_simulation(
        drone_user.get_xyz_simulation_by_index(0),
        last_frame_stand_by,
    )
    simulation_infos += in_air_flight_simulation(
        drone_user.flight_positions,
    )
    last_position = drone_user.get_xyz_simulation_by_index(-1)
    simulation_infos += land_simulation(
        last_position,
        simulation_infos[-1].frame + 1,
    )
    simulation_infos += stand_by_simulation(
        frame_begin=simulation_infos[-1].frame + 1,
        frame_end=last_frame + 1,
        stand_by_position=(last_position[0], last_position[1], 0),
    )
    return simulation_infos
