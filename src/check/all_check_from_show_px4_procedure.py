from ..show_px4.show_px4 import ShowPx4
from ..parameter.parameter import Parameter
from .show_simulation_check.simulation_check_procedure import (
    apply_simulation_check_procedure,
)
from .show_px4_check.show_px4_chek_procedure import apply_show_px4_check_procedure
from .show_check_report import ShowCheckReport
from ..migration.migration_STC_SSC.STC_to_SSC_procedure import ST_to_SS_procedure
from ..migration.migration_SP_SD.SP_to_SD_procedure import SP_to_SD_procedure
from .show_dev_check.show_dev_check_procedure import (
    apply_show_dev_procedure,
)


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

    show_trajectory = SD_to_ST_procedure(
        show_dev,
        parameter.frame_parameter,
        parameter.takeoff_parameter,
        parameter.land_parameter,
    )

    show_simulation = ST_to_SS_procedure(
        show_trajectory,
    )

    apply_simulation_check_procedure(
        show_simulation,
        show_check_report.simulation_check_report,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    show_check_report.update()
