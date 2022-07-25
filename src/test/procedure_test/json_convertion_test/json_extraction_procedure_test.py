import os

from ....parameter.parameter import Parameter
from ....procedure.json_conversion.json_extraction_procedure import (
    apply_json_extraction_procedure,
)
from ....procedure.json_conversion.json_extraction_report import JsonExtractionReport
from .dance_test_json import JSON_EXAMPLE


def test_valid_json_extraction():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    json_extraction_report = JsonExtractionReport()
    apply_json_extraction_procedure(
        JSON_EXAMPLE, parameter.json_format_parameter, json_extraction_report
    )
    assert json_extraction_report.validation
