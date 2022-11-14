from typing import List

from ....parameter.parameter import FrameParameter, LandParameter, TakeoffParameter
from ....show_dev.show_dev import DroneDev
from .in_air_flight_simulation import in_air_flight_simulation
from .land_simulation import land_simulation
from .position_simulation import SimulationInfo
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation

# TO DO: Hard to step unitarly, best way might be an input/ouput approch
# Do it, This border effect must be conventionnized


def flight_simulation(
    drone_dev: DroneDev,
    last_frame: int,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> List[SimulationInfo]:
    simulation_infos: List[SimulationInfo] = []
    if len(drone_dev.position_events_dev) == 1:
        simulation_infos += stand_by_simulation(
            frame_parameter.show_duration_min_frame,
            last_frame,
            drone_dev.get_xyz_simulation_by_index(0),
        )
        return simulation_infos
    simulation_infos += stand_by_simulation(
        frame_parameter.show_duration_min_frame,
        drone_dev.get_frame_by_index(0) + 1,
        drone_dev.get_xyz_simulation_by_index(0),
    )
    simulation_infos += takeoff_simulation(
        drone_dev.get_xyz_simulation_by_index(0),
        simulation_infos[-1].frame,
        frame_parameter,
        takeoff_parameter,
    )
    simulation_infos += in_air_flight_simulation(
        drone_dev.flight_positions,
    )
    last_position = drone_dev.get_xyz_simulation_by_index(-1)
    simulation_infos += land_simulation(
        last_position,
        simulation_infos[-1].frame,
        frame_parameter,
        land_parameter,
    )
    simulation_infos += stand_by_simulation(
        frame_begin=simulation_infos[-1].frame,
        frame_end=last_frame,
        stand_by_position=(last_position[0], last_position[1], 0),
    )
    return simulation_infos
