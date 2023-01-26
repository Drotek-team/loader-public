from ...report import Contenor
from ...show_env.show_user.show_user import ShowUser
from .migration.show_trajectory_performance import DroneTrajectoryPerformance
from .migration.su_to_stp import su_to_stp_procedure
from .performance_evaluation import performance_evaluation


def apply_drone_trajectory_performance_check_procedure(
    drone_trajectory_performance: DroneTrajectoryPerformance,
) -> Contenor:
    drone_trajectory_performance_check_report = Contenor(
        f"drone trajectory performance {drone_trajectory_performance.drone_index}"
    )
    for (
        trajectory_performance_info
    ) in drone_trajectory_performance.trajectory_performance_infos:
        drone_trajectory_performance_check_report.add_error_message(
            performance_evaluation(
                trajectory_performance_info.frame,
                trajectory_performance_info.performance,
            )
        )
    return drone_trajectory_performance_check_report


def apply_show_trajectory_performance_check_procedure(
    show_user: ShowUser,
) -> Contenor:
    show_trajectory_performance = su_to_stp_procedure(show_user)
    show_trajectory_performance_check_report = Contenor("Show trajectory performance")
    for (
        drone_trajectory_performance
    ) in show_trajectory_performance.drones_trajectory_performance:
        show_trajectory_performance_check_report.add_error_message(
            apply_drone_trajectory_performance_check_procedure(
                drone_trajectory_performance
            )
        )
    return show_trajectory_performance_check_report
