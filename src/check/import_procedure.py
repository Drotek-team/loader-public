from typing import Dict


from .show_check_report import ShowCheckReport
from ..show_user.show_user import ShowUser
from ..parameter.parameter import Parameter
from .import_report import ImportReport
from ..migration.migration_IJ_SP.IJ_to_SP_procedure import (
    IJ_to_SP_procedure,
)
from .show_check_procedure import apply_show_check_procedure
from ..migration.migration_IJ_SP.IJ_to_SP_report import IJ_to_SP_report
from ..iostar_json.iostar_json import IostarJson


def apply_import_procedure(
    iostar_json_dict: Dict,
    import_report: ImportReport,
    parameter: Parameter,
) -> ShowUser:
    iostar_json = IostarJson(**iostar_json_dict)

    import_report.json_extraction_report = IJ_to_SP_report(
        len(iostar_json.show.binary_dances)
    )
    show_px4 = IJ_to_SP_procedure(
        iostar_json,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        import_report.json_extraction_report,
    )
    import_report.show_check_report = ShowCheckReport(len(show_px4.drones))
    apply_show_check_procedure(
        show_px4,
        import_report.show_check_report,
        parameter,
    )
    import_report.update()
    # return ShowUser(**show_px4)