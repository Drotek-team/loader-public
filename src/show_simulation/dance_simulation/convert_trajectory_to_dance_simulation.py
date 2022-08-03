from ...drones_manager.trajectory_simulation_manager.trajectory_simulation_manager import (
    TrajectorySimulation,
)
from ...parameter.parameter import LandParameter, TakeoffParameter, TimecodeParameter
from .dance_simulation import DanceSimulation
from .flight_simulation import flight_simulation
from .land_simulation import land_simulation
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


def convert_trajectory_to_dance_simulation(
    trajectory_simulation: TrajectorySimulation,
    last_second: float,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> DanceSimulation:
    dance_simulation = DanceSimulation()
    if len(trajectory_simulation.position_simulation_list) == 1:
        dance_simulation.update(
            stand_by_simulation(
                timecode_parameter.show_second_begin,
                trajectory_simulation.get_position_by_index(0),
                timecode_parameter,
            )
        )
        return dance_simulation
    dance_simulation.update(
        stand_by_simulation(
            timecode_parameter.show_second_begin,
            trajectory_simulation.get_second_by_index(0),
            trajectory_simulation.get_position_by_index(0),
            timecode_parameter,
        )
    )
    dance_simulation.update(
        takeoff_simulation(
            trajectory_simulation.get_position_by_index(0),
            timecode_parameter,
            takeoff_parameter,
        )
    )
    dance_simulation.update(
        flight_simulation(
            trajectory_simulation.flight_positions,
            timecode_parameter,
        )
    )
    ### TO DO: As the first position of the land is not a part of the dance, there is a corner case where you can teleport yourself at the last position of your dance
    ### Not critical because this teleportation last only 0.25 seconds so the drone can not do much during this period
    dance_simulation.update(
        land_simulation(
            trajectory_simulation.get_position_by_index(-1),
            timecode_parameter,
            land_parameter,
        )
    )
    last_position = trajectory_simulation.get_position_by_index(-1)

    dance_simulation.update(
        stand_by_simulation(
            trajectory_simulation.get_second_by_index(-1)
            + land_parameter.get_land_second_delta(last_position[2]),
            last_second + timecode_parameter.position_second_rate,
            (last_position[0], last_position[1], 0),
            timecode_parameter,
        )
    )
    return dance_simulation
