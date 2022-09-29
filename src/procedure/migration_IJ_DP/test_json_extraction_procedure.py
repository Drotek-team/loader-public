import os

from ...parameter.parameter import Parameter
from .IJ_to_DP_procedure import (
    apply_json_extraction_procedure,
    get_nb_drone_per_family,
)
from .IJ_to_DP_report import JsonExtractionReport
from .dance_test_json import JSON_EXAMPLE


def test_valid_json_extraction():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    json_extraction_report = JsonExtractionReport(
        get_nb_drone_per_family(JSON_EXAMPLE["show"])
        * len(JSON_EXAMPLE["show"]["families"])
    )
    apply_json_extraction_procedure(
        JSON_EXAMPLE,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        json_extraction_report,
    )
    assert json_extraction_report.validation
