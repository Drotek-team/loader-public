from typing import List

from ...show_dev.show_dev import ShowDev
from ...show_trajectory_collision.show_trajectory_collision import (
    DroneTrajectoryCollision,
    ShowTrajectoryCollision,
    TrajectoryCollisionInfo,
)
from .simulation.flight_simulation import flight_simulation
from .simulation.position_simulation import SimulationInfo


def get_trajectory_collision_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[TrajectoryCollisionInfo]:
    return [
        TrajectoryCollisionInfo(
            simulation_info.frame, simulation_info.position, simulation_info.in_air
        )
        for simulation_info in simulation_infos
    ]


def SD_to_STC_procedure(
    show_dev: ShowDev,
) -> ShowTrajectoryCollision:
    return ShowTrajectoryCollision(
        [
            DroneTrajectoryCollision(
                drone_dev.drone_index,
                get_trajectory_collision_info_from_simulation_infos(
                    flight_simulation(
                        drone_dev,
                        show_dev.get_last_frame,
                    )
                ),
            )
            for drone_dev in show_dev.drones_dev
        ]
    )
