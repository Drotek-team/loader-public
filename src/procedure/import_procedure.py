from typing import Dict, Tuple

from .show_check.show_check_report import ShowCheckReport

from ..drones_px4.drones_px4 import DronesPx4
from ..family_user.family_user import FamilyUser
from ..parameter.parameter import Parameter
from .import_report import ImportReport
from .json_conversion.json_extraction_procedure import (
    apply_json_extraction_procedure,
    get_nb_drone_per_family,
)
from .show_check.show_check_procedure import apply_show_check_procedure
from .json_conversion.json_extraction_report import JsonExtractionReport


def apply_import_procedure(
    json_dict: Dict,
    import_report: ImportReport,
    parameter: Parameter,
) -> Tuple[DronesPx4, FamilyUser]:
    ### TO DO: Make a try into report for that
    import_report.json_extraction_report = JsonExtractionReport(
        get_nb_drone_per_family(json_dict["show"]) * len(json_dict["show"]["families"])
    )
    drones_user, family_user = apply_json_extraction_procedure(
        json_dict,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        import_report.json_extraction_report,
    )
    import_report.show_check_report = ShowCheckReport(len(drones_user.drones))
    apply_show_check_procedure(
        drones_user, family_user, import_report.show_check_report, parameter
    )
    import_report.update()
    return drones_user, family_user
