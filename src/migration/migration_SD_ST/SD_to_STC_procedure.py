from typing import List
from ...parameter.parameter import LandParameter, TakeoffParameter, FrameParameter
from ...show_dev.show_dev import DroneDev, ShowDev
from ...show_trajectory_collision.show_trajectory_collision import (
    ShowTrajectoryCollision,
    DroneTrajectoryCollision,
    TrajectoryCollisionInfo,
)
from .simulation.position_simulation import SimulationInfo
from .simulation.flight_simulation import flight_simulation


def get_trajectory_collision_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[TrajectoryCollisionInfo]:
    return [
        TrajectoryCollisionInfo(simulation_info.position, simulation_info.in_air)
        for simulation_info in simulation_infos
    ]


def SD_to_STC_procedure(
    show_dev: ShowDev,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> ShowTrajectoryCollision:
    return ShowTrajectoryCollision(
        [
            DroneTrajectoryCollision(
                drone_dev.drone_index,
                get_trajectory_collision_info_from_simulation_infos(
                    flight_simulation(
                        drone_dev,
                        show_dev.get_last_frame(land_parameter, frame_parameter),
                        frame_parameter,
                        takeoff_parameter,
                        land_parameter,
                    ),
                ),
            )
            for drone_dev in show_dev.drones_dev
        ]
    )
