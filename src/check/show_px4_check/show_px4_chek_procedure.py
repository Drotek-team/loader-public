from ...show_px4.show_px4 import ShowPx4
from .dance_size_check.dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)
from .show_px4_check_report import ShowPx4CheckReport


def apply_show_px4_check_procedure(
    show_px4: ShowPx4, show_px4_check_report: ShowPx4CheckReport
) -> None:

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
        drone_px4_check_report.update()
    show_px4_check_report.update()
