from multiprocessing.sharedctypes import Value
from ....parameter.parameter import LandParameter, TakeoffParameter, FrameParameter
from .flight_simulation import (
    flight_simulation,
)
from .land_simulation import land_simulation
from .stand_by_simulation import (
    stand_by_simulation,
)
from ...migration_SP_SS.migration_DS_TS.takeoff_simulation import (
    takeoff_simulation,
)
from ....show_simulation.drone_simulation.drone_simulation import DroneSimulation
from ....show_simulation.trajectory_simulation import TrajectorySimulation


def DS_to_TS_procedure(
    drone_simulation: DroneSimulation,
    last_frame: int,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> TrajectorySimulation:
    trajectory_simulation = TrajectorySimulation([], [], [])
    if len(drone_simulation.position_events_simulation) == 1:
        trajectory_simulation.concatenate_trajectory(
            stand_by_simulation(
                frame_parameter.show_duration_min_frame,
                frame_parameter.show_duration_max_frame,
                drone_simulation.get_xyz_simulation_by_index(0),
                frame_parameter,
            )
        )
        return trajectory_simulation
    trajectory_simulation.concatenate_trajectory(
        stand_by_simulation(
            frame_parameter.show_duration_min_frame,
            drone_simulation.get_frame_by_index(0),
            drone_simulation.get_xyz_simulation_by_index(0),
            frame_parameter,
        )
    )
    trajectory_simulation.concatenate_trajectory(
        takeoff_simulation(
            drone_simulation.get_xyz_simulation_by_index(0),
            frame_parameter,
            takeoff_parameter,
        )
    )
    trajectory_simulation.concatenate_trajectory(
        flight_simulation(
            drone_simulation.flight_positions,
            frame_parameter,
        )
    )
    last_position = drone_simulation.get_xyz_simulation_by_index(-1)
    trajectory_simulation.concatenate_trajectory(
        land_simulation(
            last_position,
            frame_parameter,
            land_parameter,
        )
    )
    trajectory_simulation.concatenate_trajectory(
        stand_by_simulation(
            frame_begin=int(
                drone_simulation.get_frame_by_index(-1)
                + frame_parameter.json_fps
                * land_parameter.get_land_second_delta(last_position[2])
            ),
            frame_end=last_frame + frame_parameter.position_rate_frame,
            stand_by_position=(last_position[0], last_position[1], 0),
            frame_parameter=frame_parameter,
        )
    )
    return trajectory_simulation
