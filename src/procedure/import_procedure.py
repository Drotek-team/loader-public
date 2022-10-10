from typing import Dict


from .show_check_report import ShowCheckReport
from ..show_user.show_user import ShowUser
from ..parameter.parameter import Parameter
from .import_report import ImportReport
from .migration_IJ_DP.IJ_to_DP_procedure import (
    IJ_to_DP_procedure,
    get_nb_drone_per_family,
)
from .show_check_procedure import apply_show_check_procedure
from .migration_IJ_DP.IJ_to_DP_report import IJ_to_DP_report
from ..iostar_json.iostar_json import IostarJson
from .migration_IJ_DP.migration_SC.IJ_to_SC_procedure import IJ_to_SC_procedure
from .show_configuration_check.show_configuration_check_procedure import (
    apply_show_configuration_check_procedure,
)
from .migration_DP_SS.DP_to_DS_procedure import DP_to_DS_procedure


def apply_import_procedure(
    iostar_json_dict: Dict,
    import_report: ImportReport,
    parameter: Parameter,
) -> ShowUser:
    iostar_json = IostarJson(**iostar_json_dict)

    import_report.json_extraction_report = IJ_to_DP_report(
        get_nb_drone_per_family(iostar_json.show)
    )
    drones_px4 = IJ_to_DP_procedure(
        iostar_json,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        import_report.json_extraction_report,
    )
    show_configuration = IJ_to_SC_procedure(iostar_json)
    import_report.show_check_report = ShowCheckReport(len(drones_px4.drones))

    apply_show_configuration_check_procedure(
        DP_to_DS_procedure(drones_px4),
        show_configuration,
        parameter.frame_parameter,
        parameter.iostar_json_configuration_parameter,
        import_report.show_check_report.show_configuration_check_report,
    )
    apply_show_check_procedure(
        drones_px4,
        import_report.show_check_report,
        parameter,
    )
    import_report.update()
    # return ShowUser(**drones_px4)
