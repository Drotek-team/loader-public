from typing import Dict

from src.drones_px4.drones_px4 import DronesPx4

from .show_check_report import ShowCheckReport
from ..show_user.show_user import ShowUser
from ..parameter.parameter import Parameter
from .import_report import ImportReport
from .migration_IJ_DP.IJ_to_DP_procedure import (
    apply_json_extraction_procedure,
    get_nb_drone_per_family,
)
from .show_check_procedure import apply_show_check_procedure
from .migration_IJ_DP.IJ_to_DP_report import JsonExtractionReport


def apply_import_procedure(
    json_dict: Dict,
    import_report: ImportReport,
    parameter: Parameter,
) -> ShowUser:
    ### TO DO: Make a try into report for that
    import_report.json_extraction_report = JsonExtractionReport(
        get_nb_drone_per_family(json_dict["show"]) * len(json_dict["show"]["families"])
    )
    drones_px4, family_user = apply_json_extraction_procedure(
        json_dict,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        import_report.json_extraction_report,
    )
    import_report.show_check_report = ShowCheckReport(len(drones_px4.drones))
    apply_show_check_procedure(
        drones_px4,
        family_user,
        import_report.show_check_report,
        parameter,
    )
    import_report.update()
    return drones_px4, family_user
