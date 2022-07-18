from ...procedure.import_procedure import apply_import_procedure
from ...procedure.import_report import ImportReport
from .json_convertion_test.dance_test_json import JSON_EXAMPLE


def test_apply_import_procedure():
    import_report = ImportReport()
    apply_import_procedure(JSON_EXAMPLE, import_report)
    assert import_report.show_check_report.drones_check_report[
        0
    ].events_format_check_report.position_events_check.takeoff_check_report.takeoff_duration_check_report.validation
