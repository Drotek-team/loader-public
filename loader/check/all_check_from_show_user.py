from typing import Optional

from loader.report.report import BaseReport
from loader.show_env.show_user.show_user import ShowUser

from .collision_check.show_simulation_collision_check import (
    CollisionReport,
    get_collision_report,
)
from .performance_check.show_trajectory_performance_check import (
    PerformanceReport,
    get_performance_report,
)
from .show_px4_check.show_px4_check import ShowPx4Report, apply_show_px4_report
from .show_user_check.show_user_check import ShowUserReport, get_show_user_report


class GlobalReport(BaseReport):
    show_user: Optional[ShowUserReport] = None
    show_px4: Optional[ShowPx4Report] = None
    performance: Optional[PerformanceReport] = None
    collision: Optional[CollisionReport] = None


def get_global_report(
    show_user: ShowUser,
) -> GlobalReport:
    show_user_report = get_show_user_report(show_user)
    if show_user_report is not None:
        return GlobalReport(show_user=show_user_report)
    show_px4_report = apply_show_px4_report(show_user)
    if show_px4_report is not None:
        return GlobalReport(show_px4=show_px4_report)
    performance_report = get_performance_report(
        show_user,
    )
    collision_report = get_collision_report(
        show_user,
    )
    return GlobalReport(
        performance=performance_report,
        collision=collision_report,
    )
