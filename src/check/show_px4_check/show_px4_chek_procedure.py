from ...show_env.migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from ...show_env.show_user.show_user import ShowUser
from .dance_size_check.dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)
from .show_px4_check_report import ShowPx4CheckReport


# TODO: I mean wtf there is not test for this ???
def apply_show_px4_check_procedure(
    show_user: ShowUser, show_px4_check_report: ShowPx4CheckReport
) -> None:
    show_px4 = su_to_sp_procedure(
        show_user,
    )
    for drone, drone_px4_check_report in zip(
        show_px4, show_px4_check_report.drones_px4_check_report
    ):
        apply_events_format_check_procedure(
            drone,
            drone_px4_check_report.events_format_check_report,
        )
        apply_dance_size_check_procedure(
            drone,
            drone_px4_check_report.dance_size_check_report,
        )
