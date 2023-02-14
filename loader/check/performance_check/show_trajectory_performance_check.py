import itertools
from typing import List, Optional

from loader.report import BaseReport
from loader.show_env.show_user import ShowUser

from .migration.show_trajectory_performance import (
    DroneTrajectoryPerformance,
    ShowTrajectoryPerformance,
)
from .migration.su_to_stp import su_to_stp
from .performance_evaluation import (
    PerformanceInfraction,
    get_performance_infractions_from_performance,
)


def get_performance_infractions_from_drone_performance(
    drone_trajectory_performance: DroneTrajectoryPerformance,
) -> List[PerformanceInfraction]:
    return list(
        itertools.chain.from_iterable(
            get_performance_infractions_from_performance(
                drone_trajectory_performance.index,
                trajectory_performance_info.frame,
                trajectory_performance_info.performance,
            )
            for (
                trajectory_performance_info
            ) in drone_trajectory_performance.trajectory_performance_infos
        ),
    )


def get_performance_infractions_from_show_trajectory(
    show_trajectory_performance: ShowTrajectoryPerformance,
) -> List[PerformanceInfraction]:
    return list(
        itertools.chain.from_iterable(
            get_performance_infractions_from_drone_performance(
                drone_trajectory_performance,
            )
            for (
                drone_trajectory_performance
            ) in show_trajectory_performance.drones_trajectory_performance
        ),
    )


class PerformanceReport(BaseReport):
    performance_infractions: List[PerformanceInfraction] = []


def get_performance_report(
    show_user: ShowUser,
) -> Optional[PerformanceReport]:
    performance_infracions = get_performance_infractions_from_show_trajectory(
        su_to_stp(show_user),
    )
    if performance_infracions:
        return PerformanceReport(performance_infractions=performance_infracions)
    return None
