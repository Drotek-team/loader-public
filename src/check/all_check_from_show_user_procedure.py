from ..show_user.show_user import ShowUser
from .collision_check.show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .performance_check.show_trajectory_performance_check_procedure import (
    apply_show_trajectory_performance_check_procedure,
)
from .show_check_report import *
from .show_px4_check.show_px4_chek_procedure import apply_show_px4_check_procedure
from .show_user_check.show_user_check_procedure import apply_show_user_check_procedure


def apply_all_check_from_show_user_procedure(
    show_user: ShowUser,
    show_check_report: ShowCheckReport,
) -> None:
    apply_show_user_check_procedure(show_user, show_check_report.show_user_check_report)
    apply_show_px4_check_procedure(show_user, show_check_report.show_px4_check_report)
    apply_show_trajectory_performance_check_procedure(
        show_user,
        show_check_report.show_trajectory_performance_check_report,
    )
    apply_show_simulation_collision_check_procedure(
        show_user,
        show_check_report.show_simulation_collision_check_report,
    )
    show_check_report.update_contenor_validation
