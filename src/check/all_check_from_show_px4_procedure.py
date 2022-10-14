from ..show_px4.show_px4 import ShowPx4
from ..parameter.parameter import Parameter
from .show_simulation_check.show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)
from .show_px4_check.show_px4_chek_procedure import apply_show_px4_check_procedure
from .show_check_report import ShowCheckReport
from ..migration.migration_STC_SSC.STC_to_SSC_procedure import STC_to_SS_procedure
from ..migration.migration_SP_SD.SP_to_SD_procedure import SP_to_SD_procedure
from .show_dev_check.show_dev_check_procedure import (
    apply_show_dev_procedure,
)
from ..migration.migration_SD_ST.SD_to_STC_procedure import SD_to_STC_procedure
from ..migration.migration_SD_ST.SD_to_STP_procedure import SD_to_STP_procedure


def apply_all_check_from_show_px4_procedure(
    show_px4: ShowPx4,
    show_check_report: ShowCheckReport,
    parameter: Parameter,
) -> None:
    apply_show_px4_check_procedure(
        show_px4, show_check_report.show_px4_check_report, parameter
    )
    show_dev = SP_to_SD_procedure(show_px4)
    apply_show_dev_procedure(
        show_dev,
        show_check_report.show_dev_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )

    show_trajectory_performance = SD_to_STP_procedure(
        show_dev,
    )

    show_trajectory_collision = SD_to_STC_procedure(
        show_dev,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )

    show_simulation = STC_to_SS_procedure(
        show_trajectory_collision,
    )
    apply_show_simulation_collision_check_procedure(
        show_simulation,
        show_check_report.simulation_check_report,
        parameter.iostar_parameter,
    )
    show_check_report.update()
