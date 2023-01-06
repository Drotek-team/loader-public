from ..migration.migration_SP_SU.SU_to_SP_procedure import SU_to_SP_procedure
from ..migration.migration_STC_SSC.STC_to_SSC_procedure import STC_to_SS_procedure
from ..migration.migration_SU_ST.SU_to_STC_procedure import SU_to_STC_procedure
from ..migration.migration_SU_ST.SU_to_STP_procedure import SU_to_STP_procedure
from ..show_user.show_user import ShowUser
from .show_check_report import *
from .show_px4_check.show_px4_chek_procedure import apply_show_px4_check_procedure
from .show_simulation_collision_check.show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .show_trajectory_performance_check.show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)


def apply_all_check_from_show_user_procedure(
    show_user: ShowUser,
) -> ShowCheckReport:
    show_px4 = SU_to_SP_procedure(
        show_user,
    )
    # PX4 part
    show_px4_check_report = ShowPx4CheckReport(show_px4.nb_drone)
    apply_show_px4_check_procedure(show_px4, show_px4_check_report)

    # Performance part
    show_trajectory_performance = SU_to_STP_procedure(show_user)
    show_trajectory_performance_check_report = ShowTrajectoryPerformanceCheckReport(
        show_trajectory_performance.nb_drones
    )
    apply_show_trajectory_performance_check_procedure(
        show_trajectory_performance,
        show_trajectory_performance_check_report,
    )

    # Collision part
    show_trajectory_collision = SU_to_STC_procedure(
        show_user,
    )
    show_simulation = STC_to_SS_procedure(
        show_trajectory_collision,
    )
    show_simulation_collision_check_report = ShowSimulationCollisionCheckReport(
        show_simulation.frames
    )
    apply_show_simulation_collision_check_procedure(
        show_simulation,
        show_simulation_collision_check_report,
    )
    show_check_report = ShowCheckReport(
        show_px4_check_report,
        show_trajectory_performance_check_report,
        show_simulation_collision_check_report,
    )

    show_check_report.update_contenor_validation
    return show_check_report
