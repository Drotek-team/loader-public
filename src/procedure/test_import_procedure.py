import os

from dance_test_json import JSON_EXAMPLE

from ..parameter.parameter import Parameter
from .import_procedure import apply_import_procedure


def test_apply_import_procedure():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    show_user, import_report = apply_import_procedure(JSON_EXAMPLE, parameter)
    assert import_report.validation
