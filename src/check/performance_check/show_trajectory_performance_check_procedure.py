from ...migration.migration_SU_ST.SU_to_STP_procedure import SU_to_STP_procedure
from ...report import Displayer
from ...show_trajectory_performance.show_trajectory_performance import (
    DroneTrajectoryPerformance,
)
from ...show_user.show_user import ShowUser
from .performance_evaluation import performance_evaluation
from .show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
)


def apply_drone_trajectory_performance_check_procedure(
    drone_trajectory_performance: DroneTrajectoryPerformance,
    drone_trajectory_performance_check_report: Displayer,
) -> None:
    for (
        trajectory_performance_info
    ) in drone_trajectory_performance.trajectory_performance_infos:
        performance_evaluation(
            trajectory_performance_info.frame,
            trajectory_performance_info.position,
            trajectory_performance_info.velocity,
            trajectory_performance_info.acceleration,
            drone_trajectory_performance_check_report,
        )


# TO DO: place a test on it
def apply_show_trajectory_performance_check_procedure(
    show_user: ShowUser,
    show_trajectory_performance_check_report: ShowTrajectoryPerformanceCheckReport,
) -> None:
    show_trajectory_performance = SU_to_STP_procedure(show_user)
    for drone_trajectory_performance, drone_trajectory_performance_check_report in zip(
        show_trajectory_performance.drones_trajectory_performance,
        show_trajectory_performance_check_report.drones_trajectory_performance_check_report,
    ):
        apply_drone_trajectory_performance_check_procedure(
            drone_trajectory_performance, drone_trajectory_performance_check_report
        )
        drone_trajectory_performance_check_report.update_contenor_validation
    show_trajectory_performance_check_report.update_contenor_validation
