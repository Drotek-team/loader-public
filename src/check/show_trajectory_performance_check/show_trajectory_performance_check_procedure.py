from ...parameter.parameter import IostarParameter, TakeoffParameter
from .performance_evaluation import performance_evaluation
from .show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
    DroneTrajectoryPerformanceCheckReport,
)
from ...show_trajectory_performance.show_trajectory_performance import (
    ShowTrajectoryPerformance,
    DroneTrajectoryPerformance,
)


def apply_drone_trajectory_performance_check_procedure(
    drone_trajectory_performance: DroneTrajectoryPerformance,
    drone_trajectory_performance_check_report: DroneTrajectoryPerformanceCheckReport,
) -> None:
    for (
        trajectory_performance_info
    ) in drone_trajectory_performance.trajectory_performance_infos:
        performance_evaluation(
            trajectory_performance_info.position,
            trajectory_performance_info.velocity,
            trajectory_performance_info.acceleration,
            drone_trajectory_performance_check_report,
        )


def apply_show_trajectory_performance_check_procedure(
    show_trajectory_performance: ShowTrajectoryPerformance,
    show_trajectory_performance_check_report: ShowTrajectoryPerformanceCheckReport,
) -> None:
    for drone_trajectory_performance, drone_trajectory_performance_check_report in zip(
        show_trajectory_performance.drones_trajectory_performance,
        show_trajectory_performance_check_report.drones_trajectory_performance_check_report,
    ):
        apply_drone_trajectory_performance_check_procedure(
            drone_trajectory_performance, drone_trajectory_performance_check_report
        )
        drone_trajectory_performance_check_report.update()
    show_trajectory_performance_check_report.update()
