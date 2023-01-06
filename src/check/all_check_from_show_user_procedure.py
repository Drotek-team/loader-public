from ..migration.migration_SP_SU.SU_to_SP_procedure import SU_to_SP_procedure
from ..migration.migration_STC_SSC.STC_to_SSC_procedure import STC_to_SS_procedure
from ..migration.migration_SU_ST.SU_to_STC_procedure import SU_to_STC_procedure
from ..migration.migration_SU_ST.SU_to_STP_procedure import SU_to_STP_procedure
from ..show_user.show_user import ShowUser
from .collision_check.show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .performance_check.show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)
from .show_check_report import *
from .show_px4_check.show_px4_chek_procedure import apply_show_px4_check_procedure


def apply_all_check_from_show_user_procedure(
    show_user: ShowUser,
    show_check_report: ShowCheckReport,
) -> None:
    show_px4 = SU_to_SP_procedure(
        show_user,
    )
    apply_show_px4_check_procedure(show_px4, show_check_report.show_px4_check_report)

    show_trajectory_performance = SU_to_STP_procedure(show_user)
    apply_show_trajectory_performance_check_procedure(
        show_trajectory_performance,
        show_check_report.show_trajectory_performance_check_report,
    )

    show_trajectory_collision = SU_to_STC_procedure(
        show_user,
    )
    show_simulation = STC_to_SS_procedure(
        show_trajectory_collision,
    )
    apply_show_simulation_collision_check_procedure(
        show_simulation,
        show_check_report.show_simulation_collision_check_report,
    )
    show_check_report.update_contenor_validation
