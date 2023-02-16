from typing import List

from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.show_env.show_user import DroneUser

from .in_dance_flight_simulation import in_dance_flight_simulation
from .land_simulation import land_simulation
from .position_simulation import SimulationInfo
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


def get_on_ground_flight_simulation(
    drone_user: DroneUser,
    last_frame: int,
) -> List[SimulationInfo]:
    simulation_infos: List[SimulationInfo] = []
    if last_frame == -1:
        last_frame = drone_user.position_events[0].frame
    simulation_infos += stand_by_simulation(
        FRAME_PARAMETER.from_second_to_frame(JSON_BINARY_PARAMETER.show_start_frame),
        last_frame + 1,
        drone_user.position_events[0].xyz,
    )
    return simulation_infos


def get_last_frame_stand_by(drone_user: DroneUser) -> int:
    return (
        drone_user.position_events[0].frame
        if drone_user.position_events[0].frame != 0
        else 0
    )


def get_in_air_flight_simulation(
    drone_user: DroneUser,
    last_frame: int,
) -> List[SimulationInfo]:
    simulation_infos: List[SimulationInfo] = []
    last_frame_stand_by = get_last_frame_stand_by(drone_user)
    if last_frame_stand_by != 0:
        simulation_infos += stand_by_simulation(
            FRAME_PARAMETER.from_second_to_frame(
                JSON_BINARY_PARAMETER.show_start_frame,
            ),
            drone_user.position_events[0].frame,
            drone_user.position_events[0].xyz,
        )
    simulation_infos += takeoff_simulation(
        drone_user.position_events[0].xyz,
        drone_user.position_events[1].xyz,
        last_frame_stand_by,
    )
    simulation_infos += in_dance_flight_simulation(
        drone_user.flight_positions,
    )
    last_position = drone_user.position_events[-1].xyz
    simulation_infos += land_simulation(
        last_position,
        simulation_infos[-1].frame + 1,
    )
    if last_frame == -1:
        last_frame = simulation_infos[-1].frame + 1
    simulation_infos += stand_by_simulation(
        frame_begin=simulation_infos[-1].frame + 1,
        frame_end=last_frame + 1,
        stand_by_position=(last_position[0], last_position[1], 0),
    )
    return simulation_infos


def get_flight_simulation(
    drone_user: DroneUser,
    last_frame: int = -1,
) -> List[SimulationInfo]:
    if len(drone_user.position_events) == 1:
        return get_on_ground_flight_simulation(drone_user, last_frame)
    return get_in_air_flight_simulation(drone_user, last_frame)
