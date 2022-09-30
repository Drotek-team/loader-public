import os

from ...parameter.parameter import Parameter
from .IJ_to_DP_procedure import (
    IJ_to_DP_procedure,
    get_nb_drone_per_family,
)
from .IJ_to_DP_report import IJ_to_DP_report
from .dance_test_json import JSON_EXAMPLE


def test_valid_json_extraction():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    json_extraction_report = IJ_to_DP_report(
        get_nb_drone_per_family(JSON_EXAMPLE["show"])
        * len(JSON_EXAMPLE["show"]["families"])
    )
    IJ_to_DP_procedure(
        JSON_EXAMPLE,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        json_extraction_report,
    )
    assert json_extraction_report.validation
