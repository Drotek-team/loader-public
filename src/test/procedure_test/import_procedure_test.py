import os

from ...parameter.parameter import Parameter
from ...procedure.import_procedure import apply_import_procedure
from ...procedure.import_report import ImportReport
from .json_convertion_test.dance_test_json import JSON_EXAMPLE


def test_apply_import_procedure():
    import_report = ImportReport()
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_import_procedure(JSON_EXAMPLE, import_report, parameter)
    assert import_report.show_check_report.validation
